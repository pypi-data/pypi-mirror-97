# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2021-03-09

### Fixed

+ Pinning of the patch version number of the packages, i.e., the dependencies of miniff, has been removed. Not fixing the patch version number facilitates receiving bug fixes for individual packages by requirements.txt/env.yml and update the environment during the installation. The overall consistency is still maintained as the major and minor version numbers continue to remain fixed.

## [0.1.1] - 2021-02-23

### Fixed

+ Updated the installation section in the README to capture the single command installation via pip. Users who wish to install and use miniff can use `pip install miniff` instead of setting up a development environment explicitly.

## [0.1.0] - 2021-02-15

### Added

+ Initial development version

