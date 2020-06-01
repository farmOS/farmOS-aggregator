# Configuration

The `backend` and `frontend` images can be configured at runtime with environment variables. This makes it possible to
generate pre-built images on [Docker Hub](https://hub.docker.com/r/farmos/aggregator) that the community can use.
It makes [deployment](./deployment.md) of a farmOS Aggregator instance much easier.

The `backend` image simply reads in environment variables. The `frontend` image generates a static file with these
environment variables that is used to load a configuration at run-time (read more on this [here](./development.md))

## Configuration options for farmOS Aggregator

### General Config

- `AGGREGATOR_NAME`: The name of the farmOS Aggregator. This is displayed in the Admin UI, Farm Registration UI and 
in emails sent from the Aggregator.
- `AGGREGATOR_OPEN_FARM_REGISTRATION`: This allows public access to POST to the `/api/api_v1/farms` endpoint to create
 Farm Profiles. This also enables the public `/register-farm` view in the frontend UI.
- `AGGREGATOR_INVITE_FARM_REGISTRATION`: This allows requests authenticated with an `api_token` to POST to
`/api/api_v1/farms` and create Farm Profiles. This also enables the `/register-farm` view in the frontend UI to accept
an `api_token`.
- `FARM_ACTIVE_AFTER_REGISTRATION`: Defines if newly-registered farm profiles are `active` by default. Disabling this
requires an Aggregator Administration to "activate" farm profiles before their data is made available by the aggregator.
- `AGGREGATOR_OAUTH_INSECURE_TRANSPORT`: Allows requests to be made to farmOS servers that do support `https`. This is
disabled by default and should only be used during development.
- `AGGREGATOR_OAUTH_CLIENT_ID`: The machine-name of the OAuth Client to use on farmOS servers.
- `AGGREGATOR_OAUTH_CLIENT_SECRET`: (Optional) A secret for the OAuth Client.
- `AGGREGATOR_OAUTH_CLIENT_SCOPES`: A JSON List of OAuth Scopes in the following format:
    ```json
    [
      {
        "name":"machine_name",
        "label":"Scope Label",
        "description":"Description of access the scope authorizes."
      },
      {...}
    ]
    ``` 
  This online [formatter](https://www.freeformatter.com/json-formatter.html) can be used to format the JSON object
  down to one line. Set the `Indentation Level` to `Compact (1 line)` and copy into a `.env` file.
  
  These OAuth Scopes are used in the UI form for authorizing farm profiles. It is important they have clear descriptions
  so users know what level of access & permissions they are authorizing with an Aggregator.
- `AGGREGATOR_OAUTH_CLIENT_DEFAULT_SCOPES`: A JSON List of recommended OAuth Scopes:
    ```json
    ["farm_info", "farm_metrics"]
    ``` 
  
  In the UI form, these scopes will appear automatically checked as a way of defining "recommended" OAuth scopes to the
  user. The descriptions should define why these are recommended scopes.
- `AGGREGATOR_OAUTH_CLIENT_REQUIRED_SCOPES`: A JSON List of required OAuth scopes:
    ```json
    ["farm_info"]
    ``` 
  
  In some cases it may be acceptable for an Aggregator to *require* one or many OAuth scopes for farms to register.
  These scopes will appear in the UI form as `disabled` so the user cannot modify their selection value. Note that for 
  an OAuth scope to appear `disabled` *and* `checked`, the oauth scope must also be listed in the
  `AGGREGATOR_OAUTH_DEFAULT_SCOPE` list.


### DB Config
The FastAPI app uses SQLAlchemy to interface with the Postgres DB. Connections to the DB are held in a connection pool 
to maintain long-running connections in memory for efficient re-use. The size of the pool is configurable with the 
`pool_size` and `max_overflow` parameters passed to `sqlalchemy.create_engine()`. Before setting these values, the 
total number of active DB connections should be taken into account. The Postgres default is 100.

[SQLAlchemy Documentation on Pooling](https://docs.sqlalchemy.org/en/13/core/pooling.html)

- `SQLALCHEMY_POOL_SIZE`: (`int`) Number of persistent connections to DB. Defaults to 10.

> The size of the pool to be maintained, defaults to (10). This is the largest number of connections that will be kept persistently in the pool. Note that the pool begins with 
> no connections; once this number of connections is requested, that number of connections will remain. `pool_size` can 
> be set to 0 to indicate no size limit.

- `SQLALCHEMY_MAX_OVERFLOW`: (`int`) Maximum number of connections to open with the DB. Defaults to 15.

> The maximum overflow size of the pool. When the number of checked-out connections reaches the size set in pool_size, 
> additional connections will be returned up to this limit. When those additional connections are returned to the pool, 
> they are disconnected and discarded. It follows then that the total number of simultaneous connections the pool will 
> allow is pool_size + max_overflow, and the total number of “sleeping” connections the pool will allow is pool_size. 
> `max_overflow` can be set to -1 to indicate no overflow limit; no limit will be placed on the total number of 
> concurrent connections. 
  
Example configuration:
```shell script
# General Aggregator Configuration
AGGREGATOR_NAME=farmOS-aggregator
FARM_ACTIVE_AFTER_REGISTRATION=true
AGGREGATOR_OAUTH_INSECURE_TRANSPORT=false
AGGREGATOR_OPEN_FARM_REGISTRATION=true
AGGREGATOR_INVITE_FARM_REGISTRATION=true
AGGREGATOR_OAUTH_CLIENT_ID=farmos_api_client
AGGREGATOR_OAUTH_CLIENT_SECRET=
AGGREGATOR_OAUTH_SCOPES=[{"name":"farm_info","label":"farmOS Info","description":"Allow access to basic farm info."},{"name":"farm_metrics","label":"farmOS Metrics","description":"Allow access to basic farm metrics."}]
AGGREGATOR_OAUTH_DEFAULT_SCOPES=[]
AGGREGATOR_OAUTH_REQUIRED_SCOPES=[]
```

### Alerts

If a valid SMTP email configuration is provided, additional admin-alert emails can be configured. These alert emails are
sent to all Aggregator users that are a `superuser`. Thus if multiple should receive alert emails, simply add them as
`superusers` to the aggregator.

- `AGGREGATOR_ALERT_NEW_FARMS`: Send an email to admin users when a new farm is registered.
(Useful for notification of Public Registration)
- `AGGREGATOR_ALERT_ALL_ERRORS`: Send an email to admin users whenever a farmOS server fails to respond. (Useful for 
instant notification of problems)
- `AGGREGATOR_ALERT_PING_FARMS_ERROS`: Send a summary email to admin users if any farms don't respond in the CRON
ping-all-farms method.

Example configuration:
```shell script
# Configure Email alerts to admins
AGGREGATOR_ALERT_NEW_FARMS=true
AGGREGATOR_ALERT_ALL_ERRORS=true
AGGREGATOR_ALERT_PING_FARMS_ERRORS=true
```
