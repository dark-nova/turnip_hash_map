# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2020-05-04
### Changed
- Instead of 2nd level keys being a string in the pattern of `min_phase_1-max_phase_1:min_phase_2-max_phase_2:...`, each entry is now a 12-level dictionary (excluding pattern and buy price) corresponding to the 12 phases.

### Fixed
- Pattern 0 should now be fixed, with each entry having 12 phases.
- Patterns 1 and 3 had a similar problem; each entry had an extra 5 phases.

## [0.0.1] - 2020-05-03
### Added
- Initial version, taken from turnip-bot
