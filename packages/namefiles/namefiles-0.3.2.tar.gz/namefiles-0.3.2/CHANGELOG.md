# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - 2021-03-05
### Added
- A lot more tests and docstrings.
- functions *get_filename_convention* and *get_filename_validator* to encapsulate
  the standard file naming convention.
- Most of the documentation.

## [0.2.0] - unreleased
### Changed
- opened the context length from 3-4 to 3-12

## [0.1.0] - unreleased
### Changed
- renamed *ANameGiver.as_path* to *ANameGiver.to_path* and adding the option to
  define a root path for the file.
- *ANameGiver.disassemble* now always defines a *root_path*. It is either the supplied
  filepath's root path or the current working directory.

## [0.0.2] - unreleased
### Changed
- *disassemble_filename* replaces *disassemble_name* for better context.

### Fixed
- Bug in *disassemble_filename* if no filename validator is supplied. 

## [0.0.1] - unreleased
Start of namefiles.