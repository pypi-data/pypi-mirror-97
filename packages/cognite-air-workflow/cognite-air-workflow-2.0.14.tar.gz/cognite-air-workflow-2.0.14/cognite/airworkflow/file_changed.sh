#!/usr/bin/env bash

SOURCE=${SOURCE:-.}

cd ${GITHUB_WORKSPACE}/${SOURCE}

PATHS_TO_SEARCH="$*"

# 2. Make sure the paths to search are not empty
if [ -z "$PATHS_TO_SEARCH" ]; then
    echo "Please provide the paths to search for"
    exit 1
fi

# 4. Get the latest commit in the searched paths
LATEST_COMMIT_IN_PATH=$(git log -1 --format=format:%H --full-diff $PATHS_TO_SEARCH)

if [ $LATEST_COMMIT != $LATEST_COMMIT_IN_PATH ]; then
    echo "False"
    exit 0
fi

echo "True"
exit 0