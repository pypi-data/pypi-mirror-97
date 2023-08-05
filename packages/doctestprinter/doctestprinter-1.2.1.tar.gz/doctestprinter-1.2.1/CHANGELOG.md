# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 1.2.1 [2021-03-03]
### Fixed
- Error occurring if object within series doesn't support default format specification
  e.g. if pathlib.PurePath was used within a Series. Series with objects are converted
  to string using str() before formatting with the defined format specifier.

### Added
- Read-the-docs badge to README.md

## 1.2.0 [2021-02-24]
### Fixed
- *doctest_print* is now removing trailing tabs and whitespaces.
- left occurrences of function *remove_trailing_whitespaces*

### Removed
- remove_trailing_* functions were removed.


## 1.1.0 [2021-02-20]
### Added
- strip_trailing_* as replacements for remove_trailing_*

### Deprecated
- remove_trailing_* will be removed in the next release.

### Changed
- Changed old plain text LICENCE file to markdown formatted file.
- Made changes to setup.cfg

## 1.0.0 [2021-02-06]
### Changed
- Reordered code within code maintanance.
- Added additional docstrings.
- keywords within setup.cfg

## 0.8rc2 [2021-02-03]
### Fixed
- Fixed wrong package description.

## 0.8rc1 [2021-02-02]
### Added
- Function *print_pandas* for a static user defined printing of *pandas.Series* and
  *pandas.DataFrames*. The function was written to handle failing pytest in combination
  with doctests, where the formatting within pytest changes.
- Function *remove_trailing_tabs* and *remove_trailing_whitespaces_and_tabs*
- Function *prepare_pandas* which makes the string representation.
- Function *set_in_quotes* to be used with *doctest_iter_print*
- Additional tests besides doctests.
- Requirements.txt

## 0.7b0 [2021-01-20]
### Added
- Function *prepare_print* returning the string representation before the print.

## 0.6b7 [2021-01-20]
### Fixed
- Wrong sting replacement using bumpversion.
- Missing dependencies in tox.

## 0.6b1
### Added
- Testing via travis-ci and tox
- Code coverage via coveralls.io

### Changed
- Layout of setup.py to setup.cfg
- Added badges to readme.

## 0.6b0 [2020-12-28]
### Added
- Helper method *round_collections* for rounding items using the 
  *edit_item* argument or *doctest_iter_print*.

## 0.5b2 [2020-12-18]
### Fixed
- Text was not printed correctly if it span over 2 lines.

## 0.5b1 [2020-12-01]
### Fixed
- Text was not printed correctly, if it was within a single line smaller than 
  *max_line_width*.

## 0.5b0 [2020-11-27]
### Added
- Argument 'item_edit' allows a preliminary editing of each first level item
  before printing.

## 0.4a0.post1 [2020-11-21]
### Added
- Argument `indent` supports indentation in `doctest_print`
- Function `doctest_iter_print` iterates through the first level of an Iterable or
  Mapping.

## 0.3a0 [unreleased]
### Changed
- Renamed `doctest_print` to `doctest_print_list`
- Changed behavior of former `doctest_print` to an overall printing method.
- Added optional argument 'max_line_width' to `doctest_print`.

## 0.0b2 [unreleased]
### Added
- method *remove_trailing_whitespaces* removes trailing whitespaces from a
  multiline text.
- method *repr_posix_path* and *strip_base_path*

## 0.0a1 [unreleased]
- initialized *doctestprinter*