# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [0.1.6] - 2021-03-05

### Added

* A new action allows to create an asset registered in the Kitsu database, and configure its files.

## [0.1.5] - 2021-03-04

### Fixed

* Add missed Blender operator call in scene building action for layout scene setup.

## [0.1.4] - 2021-03-04

### Changed

* Users can build a layout scene with missing dependencies. In this case, and for now, a warning message reminds that the scene will have to be manually updated later.

## [0.1.3] - 2021-03-01

### Added

* A new action in layout department for building Blender scenes, based on Kitsu information.

### Changed

* A new Blender template file with no collection, no object, and the right start frame (101), FPS (24), resolution (2048x854), color space and transparent background (/film) at render.

### Fixed

* Project object is systematically touched when accessed from a home page widget to ensure user environment update.

## [0.1.1] - 2021-02-15

### Changed

Ai file format have been move in main libreflow package.

### Fixed

Deprecated references to flag enabling file system operations have been removed.

## [0.1.0] - 2021-02-08

### Added

- Added a films map at project's root to allow project flow and test flow on a test movie
- Added the right asset library description with a asset family 
- Added many basic departements for the library and the shots
- Added a Custom Home for this project, so far it's the same as libreflow.examples.majorque's but will be tuned soon.
- Added a custom GUI, allowing to call the new custom Home
- Added a custom Style, allowing us to fix issues with released style, and make tweaks for this project.
- AI and WAV file formats made available for the production
- Custom TrackedFolder injection to handle the new lib filenames righ

### Changed

- The home page has been changed
- Minimum libreflow requiered version is now 1.2.0

## [0.0.4] - 2021-02-05

### Fixed

Rename source folder in accordance to PyPI package name

## [0.0.3] - 2021-02-05

Configuration for auto deployment

## [0.0.1] - 2021-02-04

Initial public commit and PyPI setup. This version is an early version of libreflow.the_siren. It defines a flow derived from Libre Flow's baseflow, and designed to support the workflow and dataflow involved in an animation feature film project.

### Fixed

libreflow.the_siren is now ready for use as a pip package
