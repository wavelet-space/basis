# basis

[![main](https://github.com/wavelet-space/basis/actions/workflows/main.yml/badge.svg)](https://github.com/wavelet-space/basis/actions/workflows/main.yml)
[![docs](https://github.com/wavelet-space/basis/actions/workflows/docs.yml/badge.svg)](https://github.com/wavelet-space/basis/actions/workflows/docs.yml)

**Useful things shared across Python based projects.**

This serves as a focal point for other packages. Apparently some modules could exist as stand-alone packages, but for simplicity, we distribute them as a unified package. The reason is that this package, or modules, is constantly being added and modified, and managing one package is much easier than several packages at once. Our goal is to contain classes and functions for both normal programming and more specialized code, e.g., for optimization and numerical programming. It fulfills a similar role as, e.g., <https://github.com/facebook/folly> or <https://github.com/bloomberg/bde>, but for Python instead of C++. 

## Description

### Motivation

The goal of this project is to centralize code that reappears over projects, and/or we want to point out and document some patterns and solutions to the problems.

### Features

- datetime, periods, and calendar
  - https://www.geonames.org/export/
- patterns (domain driven design, gang-of-four)
  - repository pattern
  - specification pattern
- transaction
  - file system
- numbers
  - natural

## Installation

Please install the latest version from main branch on GitHub [^1] with following command.

```shell
python -m pip install git+https://github.com/wavelet-space/basis.git
```

