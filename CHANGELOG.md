# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2020-05-19
### Changed
- Instead of having a *14-level* (pattern, buy price, Monday AM, ..., Saturday PM) dictionary which ended up difficult to read and impossible to load, the value of the 2nd level key, buy price, is now a list containing lists of tuples, with each tuple reprseenting minimum and maximum, and each list of tuples representing a possible sequence.
- In [patterns.py](patterns.py):
    - Renamed `Pattern.possible` to `Pattern.patterns`, because the variable represents not just possible patterns but rather all patterns.
    - Renamed `POSSIBLE_PATTERNS`, a type definition, to `PATTERNS`, for reasons similar to above.
    - `PATTERNS` was changed to `List[List[Tuple[int, int]]]` to match the new YAML structure
    - Moved `MIN` and `MAX` to [turnips.py](turnips.py). It was unused here.
- In [turnips.py](turnips.py):
    - Renamed `Mapper.possible_patterns` to `Mapper.pattern_seqs`, for reasons similar to `Pattern.patterns` above; `pattern_seqs` contains sequences for all patterns (0 through 3).

## [1.0.0] - 2020-05-04
### Changed
- Instead of 2nd level keys being a string in the pattern of `min_phase_1-max_phase_1:min_phase_2-max_phase_2:...`, each entry is now a 12-level dictionary (excluding pattern and buy price) corresponding to the 12 phases.

### Fixed
- Pattern 0 should now be fixed, with each entry having 12 phases.
- Patterns 1 and 3 had a similar problem; each entry had an extra 5 phases.

## [0.0.1] - 2020-05-03
### Added
- Initial version, taken from turnip-bot
