#!/bin/bash

# enable job control
set -m

while getopts b: option; do
case "${option}"
in
    b) BRANCH=${OPTARG}; # git branch name
esac; done

WORKSPACE=$HOME
PROJECT_NAME="AutomazioneTende"
PROJECT_REPO="https://github.com/ara-astronomia/${PROJECT_NAME}"

cd $WORKSPACE
ZIP_FILE="${PROJECT_REPO}/archive/refs/heads/${BRANCH}.zip"
ZIP_FILE=`echo $ZIP_FILE | sed 's/#/\%23/g;'`
wget $ZIP_FILE
unzip "${BRANCH}.zip"
rm "${BRANCH}.zip"
BRANCH=`echo $BRANCH | sed 's/#/-/g;'`
for x in "*${BRANCH}"; do
    cd $x
done 

pipenv update
pipenv shell
