#!/usr/bin/env sh

set -x
nosetests --with-coverage --cover-package=pushnotify pushnotify/tests/tests.py
