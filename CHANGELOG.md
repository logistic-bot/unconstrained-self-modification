# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2-alpha] 2020-08-25

### Removed
 - Messages that were never shown: "DELETING SAVE", "IMPOSSIBLE", ...

### Fixed
 - Selected save would reset to the first when renaming.

### Changed
 - Colors when asking for confirmation are more readable.
 - Ignore pylint C0103: Variable name doesn't conform to snake_case naming style
   (invalid-name)
 - Ignore pylint W0707: Consider explicitly re-raising using the 'from' keyword

## [0.1.1-alpha]

### Changed
 - Documentation for ListRenderer
 - Reformatting for select_save.py

### Added
 - Changelog according to keepachangelog.com
 - Version number according to semver.org

## [0.1.0-alpha]

### Added
 - A whole lot of stuff
