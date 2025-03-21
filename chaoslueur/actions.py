# -*- coding: utf-8 -*-
import logging
import os
import shlex
import shutil
import subprocess  # nosec
import threading
import time
from typing import Tuple

import psutil
from chaoslib import decode_bytes
from chaoslib.exceptions import ActivityFailed

__all__ = ["run_proxy", "stop_proxy", "run_demo"]

logger = logging.getLogger("chaostoolkit")
lock = threading.Lock()

PROCS: dict[str, psutil.Process] = {}


def run_proxy(
    proxy_args: str,
    duration: float | None = None,
    set_http_proxy_variables: bool = False,
    verbose: bool = False,
) -> Tuple[int, str, str]:
    """
    Run the lueur proxy with the given command line arguments. Use the
    name argument to track the started process, this can be used to call
    `stop_proxy` from a rollback action.

    Set `set_http_proxy_variables` so the HTTP_PROXY and HTTPS_PROXY
    environment variables of the process point at the started proxy.

    By default, the proxy never ends (as duration is set to `None`). If you set
    a duration, the proxy will only run for the length of time.

    See https://lueur.dev/reference/cli-commands/#run for all proxy arguments.
    """
    lueur_path = shutil.which("lueur")
    if not lueur_path:
        raise ActivityFailed("lueur: not found")

    cmd = [lueur_path]
    if verbose:
        cmd.extend(["--log-stdout", "--log-level", "debug"])
    else:
        cmd.extend(["--log-stdout"])
    cmd.extend(["run", "--no-ui"])
    cmd.extend(shlex.split(proxy_args))

    env = {}  # type: dict[str, str]
    stdout = stderr = b""
    try:
        logger.debug(f"Running lueur proxy: '{shlex.join(cmd)}'")
        p = psutil.Popen(  # nosec
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )

        while not p.is_running():
            time.sleep(0.1)

        logger.debug(f"lueur proxy is now running with PID {p.pid}")

        with lock:
            PROCS["proxy"] = p

        if set_http_proxy_variables:
            logger.debug("lueur guessing proxy listening address")
            bound_proxy_addr = ""
            for c in p.net_connections("tcp4"):
                if c.status == "LISTEN":
                    addr = c.laddr
                    bound_proxy_addr = f"http://{addr[0]}:{addr[1]}"
                    break

            if bound_proxy_addr:
                logger.debug(f"lueur proxy env variables to {bound_proxy_addr}")
                os.environ["HTTP_PROXY"] = bound_proxy_addr
                os.environ["HTTPS_PROXY"] = bound_proxy_addr
                os.environ["OHA_HTTP_PROXY"] = bound_proxy_addr
                os.environ["OHA_HTTPS_PROXY"] = bound_proxy_addr

        stdout, stderr = p.communicate(timeout=duration)
    except KeyboardInterrupt:
        logger.debug(
            "Caught SIGINT signal while running load test. Ignoring it."
        )
    except subprocess.TimeoutExpired:
        pass
    finally:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
        finally:
            with lock:
                PROCS.pop("proxy", None)

            return (p.returncode, decode_bytes(stdout), decode_bytes(stderr))


def stop_proxy(unset_http_proxy_variables: bool = False) -> None:
    """
    Terminate the lueur proxy
    """
    with lock:
        p = PROCS.pop("proxy", None)
        if p is not None:
            try:
                p.terminate()
            except psutil.Error:
                pass

    if unset_http_proxy_variables:
        logger.debug("Unset lueur proxy env variables")
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        os.environ.pop("OHA_HTTP_PROXY", None)
        os.environ.pop("OHA_HTTPS_PROXY", None)


def run_demo(
    duration: float | None = None, port: int = 7070
) -> Tuple[int, str, str]:
    """
    Run the lueur demo web application.
    """
    lueur_path = shutil.which("lueur")
    if not lueur_path:
        raise ActivityFailed("lueur: not found")

    cmd = [lueur_path]
    cmd.extend(["demo", "run", "0.0.0.0", str(port)])

    env = {}  # type: dict[str, str]
    stdout = stderr = b""
    try:
        logger.debug(f"Running lueur demo: '{shlex.join(cmd)}'")
        p = psutil.Popen(  # nosec
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )

        stdout, stderr = p.communicate(timeout=duration)
    except KeyboardInterrupt:
        logger.debug(
            "Caught SIGINT signal while running load test. Ignoring it."
        )
    except subprocess.TimeoutExpired:
        pass
    finally:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
        finally:
            return (p.returncode, decode_bytes(stdout), decode_bytes(stderr))
