# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.8.0...HEAD

## [0.8.0][]

[0.8.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.7.0...0.8.0

### Changed

- don't set HTTP_PROXY/HTTPS_PROXY variables by default because they impact any
  call from the process, even those we don't want to go through the proxy.
  Instead, set LUEUR_PROXY_ADDRESS and let subsequent actions/probes decide
  what to do with it

## [0.7.0][]

[0.7.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.6.0...0.7.0

### Changed

-  wait until address is bound by proxy

## [0.6.0][]

[0.6.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.5.0...0.6.0

### Added

- bind to proxy any IPv4 interface if not specifically set by user

## [0.5.0][]

[0.5.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.4.0...0.5.0

### Added

- pass env variable proxy to demo when set

### Fixed

- wait until process is running to set proxy env variables

## [0.4.0][]

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.3.0...0.4.0

### Added

- add more logging

## [0.3.0][]

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.2.0...0.3.0

### Added

- proxy also sets `OHA_HTTP_PROXY` and `OHA_HTTPS_PROXY` to it can be picked by Reliably

## [0.2.0][]

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.6...0.2.0

### Added

- an action to run the demo server

## [0.1.6][]

[0.1.6]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.5...0.1.6

### Changed

- directly modify `os.environ` as the alternative didn't modify the underlying
  environment

## [0.1.5][]

[0.1.5]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.4...0.1.5

### Changed

- proxy never returns by default unless a duration is set

## [0.1.4][]

[0.1.4]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.3...0.1.4

### Changed

- Rename args into proxy_args and take a string

## [0.1.3][]

[0.1.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.2...0.1.3

### Fixed

- Capture errors when process is already gone

### Changed

- Remove higher level actions as it's just simpler to directly call the proxy
  with the lueur command line

## [0.1.2][]

[0.1.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.1...0.1.2

### Fixed

- Path to dist assets

## [0.1.1][]

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/compare/0.1.0...0.1.1

### Fixed

- Name of the upload action in release workflow

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-lueur/tree/0.1.0

### Added

- Initial release
