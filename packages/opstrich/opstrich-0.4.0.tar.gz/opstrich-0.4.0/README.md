# Opstrich
#### DevOps tooling, various scripts, etc.

![CI](https://github.com/RevolutionTech/opstrich/actions/workflows/ci.yml/badge.svg)

## Installation

First install the `opstrich` package:

    pip install opstrich

To use the provided [invoke](http://www.pyinvoke.org/) tasks, you will also need to add these to a collection in your project:

    # tasks.py

    from invoke import Collection
    from opstrich.invoke import check, openssl, package

    namespace = Collection(check, openssl, package)

## Usage

Once the invoke tasks have been added, you can view help information on them via `inv -l` and `inv --help`.
