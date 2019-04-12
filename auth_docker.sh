#!/bin/bash

set -e
docker login -u _json_key -p "$GOOGLE_JSON_KEY" https://gcr.io