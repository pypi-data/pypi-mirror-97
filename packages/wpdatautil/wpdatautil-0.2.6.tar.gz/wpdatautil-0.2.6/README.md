# wp-dataops-pyutil
This provides **`wpdatautil`**, a Python 3.8 package with specific reusable utility functions for data processing.

A limited version of this readme which is published to PyPI is [available separately](README_PyPI.md).

[![cicd badge](https://github.com/wqpredtech/wp-dataops-pyutil/workflows/cicd/badge.svg?branch=master)](https://github.com/wqpredtech/wp-dataops-pyutil/actions?query=workflow%3Acicd+branch%3Amaster)

| [GitHub Releases/Changelog](https://github.com/wqpredtech/wp-dataops-pyutil/releases) | [PyPI release](https://pypi.org/project/wpdatautil/) |
|-|-|

## Installation
`pip install -U wpdatautil` will install the package but intentionally not any third-party requirements.
Given that the third-party package requirements can be numerous, and not all of them are relevant to most users, they can be installed as needed by a user.

## Usage
The implemented utilities are broadly organized by their primary third-party or builtin package requirement.
For example, `.pandas` contains utilities which primarily require the `pandas` package.
Similarly, `.boto3.s3path` contains utilities which require both the `boto3` and `s3path` packages.

## Development
### Setup
To set up the project locally:
1. Install Python 3.8
1. Clone the repo and setup a corresponding new IDE project. Use the IDE to create a virtual environment for this repo and project.
1. Configure the IDE to use a max line length of 180. This is also defined in various static analyzer configuration files in the project.
It facilitates the use of descriptive variable names while ensuring that lines still display fully.
1. Run `make setup`, and ensure an exitcode of 0.
### Contribute
To contribute to this repository:
1. Develop the changes in a feature branch with 100% line test coverage.
1. Run `make prep`. Ensure the build is passing.
1. Create a pull request into `master` and assign it to a [codeowner](.github/CODEOWNERS).
### Publish
To publish the package to PyPI:
1. Ensure the commits which are to be released are merged into `master`, and the build is passing.
1. Create and publish a [release on GitHub](https://github.com/wqpredtech/wp-dataops-pyutil/releases) with a [semver](https://semver.org/) tag, e.g. "v0.1.2", including a changelog since the last release.
This triggers the [release workflow](https://github.com/wqpredtech/wp-dataops-pyutil/actions?query=workflow%3Acicd+event%3Arelease) which publishes the release to PyPI.
If there is a noticeable delay in triggering the workflow, check [GitHub Status](https://www.githubstatus.com/).
1. Confirm that the published version is [listed on PyPI](https://pypi.org/project/wpdatautil/#history).
