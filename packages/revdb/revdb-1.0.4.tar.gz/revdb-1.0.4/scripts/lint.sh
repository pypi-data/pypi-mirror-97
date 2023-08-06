#!/usr/bin/env bash

set -e
set -x

mypy revdb
flake8 revdb tests
black revdb tests --check
isort revdb tests --check-only
