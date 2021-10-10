#!/usr/bin/env bash

# Run example: ./vn.sh g27-culrepo.sh
BACKLOG=$1

# Requires at least 4Gb assigned to docker container (default is 2Gb).
# Alternative is to install locally Visual Narrator
docker run -it --rm \
       -v "$PWD":/usr/src/app/output \
       acedesign/visualnarrator output/"${BACKLOG}" --json

mv System/reports/System_REPORT1.html "${BACKLOG}"_report.html
rm -rf System
