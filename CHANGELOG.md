# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
 - Documentation for user_interface.py and TreeListRenderer
 - Documentation for select_save.py

### Fixed
 - Linting in user_interface.py

### Changed
 - Ignore pylint C0103: Variable name doesn't conform to snake_case naming style
   (invalid-name)
 - Refactoring of select_save.py
   - action_list, save_list and treelist are now members of SelectSave
   - Delete action now uses get_confirmation to confirm
   - Moved show_info() function outside of the start() method
   - Renamed show_info() method to show_properties()

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
