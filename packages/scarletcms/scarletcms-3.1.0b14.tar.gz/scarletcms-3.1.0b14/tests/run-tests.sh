#!/bin/bash

set +e
TESTDIR="$(dirname $0)"
COVERAGE=$(which coverage)
SETTINGS=""
TEST_RUNNER="pytest"

if [ -z $TEST_RUNNER ]; then
    echo "django-admin command not found"
    exit 1
fi

set -e

usage()
{
    echo "run-tests.sh [-s or --settings or --settings=] [test-to-run]"
    exit $1
}

if [ $COVERAGE ]; then
    TEST_RUNNER="$COVERAGE run -a --source=$TESTDIR/../scarlet -m $TEST_RUNNER"
fi

pytest_args=$@
if [ -z $pytest_args ]; then
  $TEST_RUNNER $TESTDIR
else
  $TEST_RUNNER $pytest_args

fi

if [ $COVERAGE ]; then
    $COVERAGE report -m
fi
