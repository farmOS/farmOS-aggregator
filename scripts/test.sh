#! /usr/bin/env sh

# Exit in case of error
set -ex

DOMAIN=backend \
INSTALL_DEV=true \
AGGREGATOR_OAUTH_INSECURE_TRANSPORT=true \
docker-compose \
-f docker-compose.shared.yml \
-f docker-compose.dev.yml \
-f docker-compose.test.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -u www-data -T farmos_www drush site-install -y --db-url=pgsql://postgres:postgres@db/app --db-prefix=farm --account-pass=admin
docker-compose -f docker-stack.yml exec -u www-data -T farmos_www drush user-create tester --password test
docker-compose -f docker-stack.yml exec -u www-data -T farmos_www drush user-add-role farm_manager tester
docker-compose -f docker-stack.yml exec -T -e TEST_FARM_URL=http://farmos_www -e TEST_FARM_USERNAME=tester -e TEST_FARM_PASSWORD=test backend bash /app/tests-start.sh "$@"
docker-compose -f docker-stack.yml down -v --remove-orphans
