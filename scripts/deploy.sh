#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN} \
TAG=${TAG} \
docker-compose \
-f docker-compose.shared.yml \
-f docker-compose.deploy.yml \
-f docker-compose.deploy.images.yml \
up -d

