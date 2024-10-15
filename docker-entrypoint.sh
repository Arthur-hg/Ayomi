#!/bin/bash

set -o errexit
set -o pipefail

CMD="$*"


# /src-volume should only exist during local server development
if [ -d /src-volume ]; then
    if echo $CMD | grep pytest > /dev/null; then
        echo "Test Mode Detected."
        # Delete local cache files to not conflict with docker tests running locally
        find /src-volume -name \*.pyc -delete
    else
        GUNICORN_NUM_WORKERS=${GUNICORN_NUM_WORKERS:-1}
        CMD="${CMD} --workers $GUNICORN_NUM_WORKERS --reload"
    fi

    cd /src-volume
else
    cd /src-dist
fi

echo "BOOTING with command: ${CMD}"
exec $CMD
