# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Update to python 3.10 [#123](https://github.com/farmOS/farmOS-aggregator/issues/123)
- Update emails to ^0.6 [#123](https://github.com/farmOS/farmOS-aggregator/issues/123)

### Fixed
- Update poetry installer [#121](https://github.com/farmOS/farmOS-aggregator/issues/121)
- Only run codespell on backend.

## v2.0.0-beta.2 2022-03-04

### Added
- Add code linting

### Changed
- Use farmOS.py 1.0.0-beta.3
- Change relay endpoint to expect a single farm_url in the path

### Removed
- Remove api_v1 endpoints

## v2.0.0-beta.1 2021-03-21

First release with support for farmOS 2.0!

This introduces a second set of api endpoints at /api/v2/ for making requests to 2.x servers. Instead of separate endpoints for logs, assets, areas and terms, there is a singe /api/v2/resources/{entity_type}/{bundle} endpoint that requires the JSONAPI resource type be specified.

Requests can still be made to servers via the 1.x endpoints. The endpoint version must match the server version. **NOTE: This was removed in the next release 2.0.0-beta.2**

## v0.9.7 2020-08-12

### Changed
- Update farmOS.py to v0.2.0
- Manually trigger a refresh before tokens expire. [#91)(https://github.com/farmOS/farmOS-aggregator/issues/91)

## v0.9.6 2020-08-12

### Added
- Search by farm URL [#93)(https://github.com/farmOS/farmOS-aggregator/issues/93)

### Changed
- Run ping farms as background task [#87](https://github.com/farmOS/farmOS-aggregator/issues/87)
- Allow SQLAlchemy pool_size and max_overflow to be configurable [#89](https://github.com/farmOS/farmOS-aggregator/issues/89)
- Only return farm.info with requests to farms/{farm_id} [#90](https://github.com/farmOS/farmOS-aggregator/issues/90)
- Sort by URL ascending by default [#92)(https://github.com/farmOS/farmOS-aggregator/issues/92)
- Show "All" rows per page by default [#94)(https://github.com/farmOS/farmOS-aggregator/issues/94)

### Fixed
- Implement a lock to limit refresh token race condition #91

## v0.9.5 2020-04-23

### Added
- Add test coverage for endpoints with configurable public access [#68](https://github.com/farmOS/farmOS-aggregator/issues/68)

### Changed
- Simplify tests to run in the same backend container
- Refactor backend to use poetry for managing dependencies
- Update backend dependencies (FastAPI == v0.54.1)
- Refactor tests to use FastAPI TestClient
- Refactor endpoints to read settings with get_settings Dependency

### Fixed
- Fix deprecation warning for Pydantic skip_defaults

## v0.9.4 2020-04-20

### Added
- Display notes on farm edit screen.

### Changed
- Allow list of id query params for requests to DELETE farm records.

### Fixed
- Save empty fields when updating farm profiles. Fixes [#81](https://github.com/farmOS/farmOS-aggregator/issues/81)

## v0.9.3 2020-03-30

### Changed
- Reconnect to farmOS server and update farm.info after successful Authorization.
- Add https:// prefix to farm.url text fields.
- Improve Authorization error messages.
- Display success message after Authorization Flow.
- Display raw API Key within Admin UI.

### Fixed
- Build farm.url URLs to include a scheme before making requests.
- Ensure OAuth scope is always saved as a string.
- Fix error for GET requests to /api-keys/

## v0.9.2 2020-03-26

### Added
- Adds API Keys to provide scoped access to the Aggregator API.

### Changed
- Updates the farm.scope attribute to only be modified when authorizing with a farmOS server. (displays as readonly in the admin UI)
- Update the default oauth_client_id to match the development OAuth client provided by the farm_api_development module (Added in farmOS/farmOS#207)
- Update npm packages.

### Fixed
- Fix Authorize Now button in admin UI.

## v0.9.1 2020-03-10

### Added
- Adds ability to send authorization and registration emails #32
- Adds ability to send Administrators alerts via email #29
- Display success dialog after registering a new farm #72
- Adds stats to the admin Dashboard.
- Add documentation.

### Changed

- Simplify NGINX Configuration with template file.
- Simplify Admin menu items.

### Fixed
- Bug fixes in frontend UI regarding reloading and redirecting.

## v0.9.0 2020-02-14

### Added

- Add variables to docker-compose.test.yml to fix automatic tests.