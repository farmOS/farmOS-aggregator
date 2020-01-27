#! /usr/bin/env bash

# Exit in case of error
set -e

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose \
    -f docker-compose.test.yml \
    -f docker-compose.shared.yml \
    -f docker-compose.dev.yml \
    config > docker-stack.yml


docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T backend-tests /tests-start.sh
