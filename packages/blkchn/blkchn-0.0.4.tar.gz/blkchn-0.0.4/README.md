# Blkchn [![Build Status](http://178.62.80.42:8081/buildStatus/icon?job=blkchn%2Fdevelop&build=2)](http://178.62.80.42:8081/job/blkchn/job/develop/2/)

A Python implementation of a Blockchain data structure.

# Features

  * Easily integrate into existing code a Blockchain design pattern
  * 100% coverage and extensively tested
  * Tested with Python 3.8
  * Plenty of examples to get you going!

# Installation

You can install the latest version using Pip:

`pip install blkchn`

# Contributing

Pull requests are always welcome to help maintain and improve the codebase.
Please work on your own branch and then raise a PR when ready.

## Release Instructions

If Jenkins fails, for whatever reason, follow these instructions to release a new version:

First, create the source distribution (ensure you've version bumped `setup.py`):

`python setup.py sdist`

Then upload the new version to PyPi:

`twine upload dist/*`

# License

This project is licensed under the MIT License - see the LICENSE.md file for details