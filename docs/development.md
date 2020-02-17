# Development

- [Backend Development](#backend-development)
  - [FastAPI](#fastapi)
  - [Backend Structure](#backend-structure)
  - [General Workflow](#general-workflow)
  - [API Routes](#api-routes)
  - [Database Models](#database-models)
  - [Schemas](#schemas)
  - [Alembic Migrations](#alembic-migrations)
  - [Backend Tests](#backend-tests)
- [Frontend Development](#frontend-development)
  - [Configuration](#configuration)
  - [Views](#views)
  - [Actions](#actions)
  
Backend Requirements:
- Docker
- Docker Compose

Frontend Requirements:
- Node.js (with `npm`)

## Backend Development

- Start the stack with Docker Compose:
    
```shell script
docker-compose up -d
```

- Now you can open your browser and interact with these URLs:
  - Frontend, built with Docker, with routes handled based on the path: http://localhost
  - Backend, JSON based web API based on OpenAPI: http://localhost/api/
  - Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs
  - Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

- **Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```shell script
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```shell script
docker-compose logs backend
```

### FastAPI

The backend API is built with [FastAPI](https://fastapi.tiangolo.com)

farmOS Aggregator is roughly based on the [FastAPI Full Stack Template](https://github.com/tiangolo/full-stack-fastapi-postgresql)
 but has been modified for simpler deployment (with fewer feature dependencies) and complete configuration at runtime.

FastAPI allows us to quickly build a JSON API that conforms to OpenAPI standards. To begin, it is recommended that you
follow the [tutorial](https://fastapi.tiangolo.com/tutorial/).

FastAPI has many features, but not all are used in farmOS Aggregator. You can refer to the following docs for info on
core FastAPI features used by farmOS Aggregator:
- [Security](https://fastapi.tiangolo.com/tutorial/security/) for OAuth2 and custom `api_tokens`(JWT Tokens)
- [OAuth2 Scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/) 
- [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) for implementing a robust security mechanism
across all endpoints.
- [SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

### Backend Structure

farmOS-Aggregator follows the recommendations for defining the API in multiple files. Reference the 
[Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) documentation to better
understand the motivations for the structure of the backend.
 
### General Workflow

Open your editor at `./backend/app/` (instead of the project root: `./`), so that you see an `./app/` directory with 
your code inside. That way, your editor will be able to find all the imports, etc.

Modify or add SQLAlchemy models in `./backend/app/app/models/`, Pydantic schemas in `./backend/app/app/schemas/`, 
API endpoints in `./backend/app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/app/crud/`.

There is an `.env` file that has Docker Compose default values, and all default configuration values for the Aggregator.

### API Routes

Endpoints are defined in `./backend/app/app/api/api_v1/endpoints`, with `farm` specific endpoints defined in the
`./backend/app/app/api/api_v1/endpoints/farms` subdirectory.

Each file provides an `api_router` that is imported and included by FastAPI in the file
`./backend/app/app/api/api_v1/api.py`. OpenAPI `tags` and FastAPI `dependencies` are declared here when including
a router. This drastically cuts down on code repetition.

Utility methods for API routes are defined in `./backend/app/app/api/api_v1/utils` and provide methods for getting a DB
session, checking security permissions, and generating a farmOS.py client.

### Database Models

Database models are defined in `./backend/app/app/models`. Currently, 3 models are defined:
- `user.py` defines a table for Aggregator Users.
- `farm.py` defines a table for "Farm Profiles" that define a unique farmOS Server.
- `farm_token.py` defines a table for "Farm Tokens" to save OAuth Tokens used for authentication with a farmOS server.

### Schemas

`Pydantic` schemas are defined in `./backend/app/app/schemas`. These schemas are used in many places throughout the 
backend app:
- Automatic generation of JSON Schema models.
- Automatic validation of data received from API.
- Defines response types for data retrieved from the API.

### Alembic Migrations

As during local development your app directory is mounted as a volume inside the container (set in the file
`docker-compose.dev.volumes.yml`), you can also run the migrations with `alembic` commands inside the container and the
migration code will be in the app directory (instead of being only inside the container). So you can add it to the
git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you
 change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```bash
docker-compose exec backend bash
```

* If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`,
that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```bash
alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```bash
alembic upgrade head
```

### Backend tests

To test the backend run:

```bash
DOMAIN=backend sh ./scripts/test.sh
```

The file `./scripts/test.sh` has the commands to generate a testing `docker-stack.yml` file from the needed Docker 
Compose files, start the stack and test it.

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

If you need to install any additional package for the tests, add it to the file `./backend/app/tests.dockerfile`.

If your stack is already up and you just want to run the tests, you can use:

```bash
docker-compose exec backend-tests /tests-start.sh
```

That `/tests-start.sh` script inside the `backend-tests` container calls `pytest`. If you need to pass extra arguments
 to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker-compose exec backend-tests /tests-start.sh -x
```

## Frontend Development

The frontend is built using [Vue.js](https://vuejs.org/) and uses the [Vuetify](https://vuetifyjs.com/en/) material
design framework.

* Enter the `frontend` directory, install the NPM packages and start the live server using the `npm` scripts:

```bash
cd frontend
npm install
npm run serve
```

Then open your browser at http://localhost:8080

Notice that this live server is not running inside Docker, it is for local development, and that is the recommended
workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a
production-like environment. But compiling the image at every change will not be as productive as running the local
development server.

Check the file `package.json` to see other available options.

If you have Vue CLI installed, you can also run `vue ui` to control, configure, serve and analyse your application using
 a nice local web user interface.

### Configuration

Typically a Vue frontend is generated with `vue-cli` and is configured with environment variables prefixed with
`VUE_APP_`. These environment variables are then included in the build process and made available to the app during
runtime.

For farmOS Aggregator, however, we have designed the `frontend` image to be *configurable at runtime.* The advantage
here is that a pre-built image can be hosted on Docker Hub and be used by anyone. To make this possible, configuration
values are loaded into the global `window._env` variable by a static `env.js` file that is included in `index.html`.

The `./frontend/env-template.js` file is used to generate the static `env.js` that is loaded by the client.

For development, it is automatically generated when running `npm run serve` and loads configuration from the
default file `./frontend/.env`. Values in the file can modified or overwritten by exporting them to the shell
environment that runs the `npm run serve` command.

### Views

Views are broken into 2 main categories:
- Publicly accessible views at `./frontend/src/views/`
  - `login`, public `farm registration` and `farm authorization` views.
- Views requiring an Aggregator user at `./frontend/src/views/main`:
  - `Dashboard` at `./frontend/src/views/main/dashboard.vue`
  - `Profile` views (managing user profile, not necessarily an admin user) at `./frontend/src/views/main/profile/`
  - `Admin` views (creating users) at `./frontend/src/views/main/admin/`
  - `Farm` views (managing Farm Profiles) at `./frontend/src/views/main/farm/`

All views are defined and loaded by the `vue router` at `./frontend/src/router.ts`

### Actions

All API methods are defined in `./frontend/api.ts`.

These API methods are called by *actions* defined in directories under `./frontend/src/store/`
- `main` defines actions for logging in, logging out, managing user profiles, etc.
- `admin` defines actions for managing users
- `farm` defines actions for managing Farm Profiles

Some of these actions modify the `vuex` state, others are just used to make requests to the backend api.

