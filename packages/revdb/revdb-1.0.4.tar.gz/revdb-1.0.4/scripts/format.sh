#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place revdb tests --exclude=__init__.py
black revdb tests
isort revdb tests
