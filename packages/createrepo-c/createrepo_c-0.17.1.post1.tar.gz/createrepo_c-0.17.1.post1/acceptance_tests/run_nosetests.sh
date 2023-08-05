#!/bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILDDIR="$( cd "$CURDIR/../build" && pwd )"

# All use cases
PATH="$BUILDDIR/src/:/home/tmlcoch/git/yum-metadata-diff/:$PATH" LD_LIBRARY_PATH=$BUILDDIR/src/ PYTHONPATH=$BUILDDIR/src/python/ nosetests -s -v ./tests/ --processes 4 --process-timeout=300

# Single module:
#PATH="$BUILDDIR/src/:/home/tmlcoch/git/repodiff/:$PATH" LD_LIBRARY_PATH=$BUILDDIR/src/ PYTHONPATH=$BUILDDIR/src/python/ nosetests -s -v --processes 4 --process-timeout=300 tests/test_sqliterepo.py

# Single test:
# PATH="$BUILDDIR/src/:/home/tmlcoch/git/repodiff/:$PATH" LD_LIBRARY_PATH=$BUILDDIR/src/ PYTHONPATH=$BUILDDIR/src/python/ nosetests -s -v --processes 4 --process-timeout=300 tests/test_createrepo.py:TestCaseCreaterepo_emptyrepo.test_01_createrepo
