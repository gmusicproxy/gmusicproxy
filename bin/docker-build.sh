#!/usr/bin/env bash

if ! $(which jq &> /dev/null && which docker &> /dev/null) ; then
  echo "build script requires jq and docker" ;
  exit 1
fi

# Run from project base directory

TAG_VERSION=$(jq -r '.version' < version.json)
IMG_NAME="gmusicproxy/gmusicproxy"

if docker build -t ${IMG_NAME}:${TAG_VERSION} . && \
   docker build -t ${IMG_NAME}:${TAG_VERSION}-alpine -f Dockerfile-alpine . ; then
   echo "##########################################"
   echo "Successfully built images. To push to hub:"
   echo "docker push ${IMG_NAME}:${TAG_VERSION}"
   echo "docker push ${IMG_NAME}:${TAG_VERSION}-alpine"
else
   echo "Build Failed"
fi
