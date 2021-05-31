# Deploying a farmOS Aggregator

The farmOS Aggregator is designed to have a robust configuration making it possible to use an Aggregator in many
different use cases without requiring custom modifications. To make deployment and updating of an Aggregator as easy as
possible, settings for both the `frontend` and `backend` images can be configured with environment variables at runtime.

There are two methods to deploy a farmOS Aggregator. It is recommended to use the configurable
[Docker Hub images](https://hub.docker.com/r/farmos/aggregator/tags), but the `backend` and `frontend` images can
also be built and deployed if customizations are required.

## Deploying from Docker Hub

*This is the recommended method for deploying an Aggregator.*

Deployment requires a few steps:

1. Configure Aggregator Settings
    - Configure environment variables to configure the Aggregator as desired. A `.env` template used for configuring the
    Aggregator environment variables is provided in the GitHub repo at [https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/.env-template](https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/.env-template)
    - Rename the file to `.env`. This will automatically be loaded by `docker-compose`.
    - Configure the domain:
      - Set the `DOMAIN` variable to the domain with Aggregator will be deployed to. (Without HTTP)
    - Configure db:
      - Generate a unique password for the database. Set the `POSTGRES_PASSWORD` variable to the output of the following:
        ```shell script
          openssl rand -hex 32
          # Outputs something like: 99d3b1f01aa639e4a76f4fc281fc834747a543720ba4c8a8648ba755aef9be7f
        ```
    - Configure backend:
      - Replace `https://localhost` with `https://DOMAIN` in the `BACKEND_CORS_ORIGINS` variable.
      - Generate a secret key for the backend FastAPI app. This is used when generating access tokens, etc.
      Set `SECRET_KEY` to the output of the following: (Don't share this with anyone!!!)
      ```shell script
          openssl rand -hex 32
          # Outputs something like: 99d3b1f01aa639e4a76f4fc281fc834747a543720ba4c8a8648ba755aef9be7f
        ````
      - Configure the admin super user for the Aggregator. Set the `FIRST_SUPERUSER` and `FIRST_SUPERUSER_PASSWORD`
      variables to desired values. This user is generated in the DB the first time the container is run. The password
      can be changed via the Admin GUI later.
      - Configure `SMTP_` variables to configure sending emails from the Aggregator.
    - Configure Aggregator Settings:
       - These settings are used to configure both the `backend` and `frontend` images at run-time. See 
        [configuring an aggregator](./configuration.md) for documentation on available configurations.
    
2. Setup the `docker-compose` file
    - Download the template docker-compose file provided in the GitHub 
repo at [https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/docker-compose.deploy-template.yml](https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/docker-compose.deploy-template.yml)
    - Rename the `docker-compose.deploy-template.yml` file to `docker-compose.yml`. 
    - Note that this template defaults to using the `backend` and `frontend` images which are aliases for the latest
     release from Docker Hub. The image tag can be modified to request a certain tagged release, if desired. See the 
     [Docker Hub repository](https://hub.docker.com/r/farmos/aggregator/tags) for available tags.
    - This template also provides a container for the `PostgresDB` and `NGINX` proxy. These are designed to work in
    production, but you could modify the `docker-compose` file to connect to a separately hosted DB, or use a different
    proxy.
    
3. Configure NGINX proxy.
    - Download the NGNIX configuration template from [https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/nginx.deploy.template](https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/nginx.deploy.template)
      - If you are just deploying the aggregator locally for testing, you may want to use the development NGINX config
      file from [https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/nginx.template](https://raw.githubusercontent.com/farmOS/farmOS-aggregator/master/nginx.template) This will not
      require setting up SSL certs, but _should not be used in deployment!!!_
    - Rename the file to `nginx.template` so it is correctly loaded in the proxy container.
    - Inside the template, replace `$DOMAIN` with the domain the Aggregator will be deployed to.

4. Setup SSL Certs
    - Generate a self-signed cert before starting the `nginx` proxy container. **_The container will not start if it
    fails to load a certificate._**
    ```shell script
        mkdir -p /etc/letsencrypt/live/$DOMAIN

        # Create temp self signed cert
        openssl req -x509 -nodes -newkey rsa:2048 -days 1\
            -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
            -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
            -subj /CN=$DOMAIN
    ```
    - Once self-signed certs are created, start the containers with
    ```shell script
      sudo docker-compose up -d
     ```
     - Generate LetsEncrypt certs with a temporary `certbot` container:
     ```shell script
        # Remove the temp cert directory
        rm -r /etc/letsencrypt/live

        # Get a new cert with certbot
        sudo docker run -it --rm --name certbot \
            -v "/etc/letsencrypt:/etc/letsencrypt" \
            -v "/var/log/letsencrypt:/var/log/letsencrypt" \
            -v "/var/www/letsencrypt:/var/www/letsencrypt" \
            certbot/certbot certonly \
            --email $EMAIL_ADDRESS \
            --agree-tos \
            --webroot \
            --webroot-path /var/www/letsencrypt \
            -d $DOMAIN 

        # Restart proxy container
        sudo docker-compose restart proxy
      ```
      - Create a CRON job to auto-update certs (replace `[proxy-container]` with
      the name of the Docker proxy container, eg: `aggregator_proxy_1`).
      ```shell script
      16 2 * * * sudo docker run --rm --name certbot -v '/etc/letsencrypt:/etc/letsencrypt' -v '/var/log/letsencrypt:/var/log/letsencrypt' -v '/var/www/letsencrypt:/var/www/letsencrypt' certbot/certbot renew && sudo docker exec [proxy-container] service nginx reload > /dev/null
      ```
 
 
## Deploying custom-built images

If the Aggregator `backend` or `frontend` must be customized, you can also build the images before deploying. This not
recommended as it requires building images on the production server which requires extra resources. Updating customized
images may also require extra work. If possible, consider contributing to the farmOS-Aggregator to make the desired
customizations another configuration option! No support or backwards compatibility can be provided to custom-images.

Steps:
 - Clone the farmOS Aggregator repo.
 - Make changes, and build images via:
 ```shell script
  # Build the backend and frontend images locally
  sudo TAG=prod FRONTEND_ENV=production bash ./scripts/build.sh 
 ```
 - This will create two tagged images available locally. To deploy, simply run the following from the root of the repo:
 ```shell script
    sudo TAG=prod bash ./scripts/deploy.sh
 ```
 - This will run `docker-compose up -d` with the correct docker-compose files to run the containers in production mode.
 - Follow the instructions above for generating a self signed certificate, and then proceed to creating LetsEncrypt
 certificates with `certbot`. _NOTE: The proxy container will not start in production mode if it cannot load
 certificates!_

# Maintaining Farm Profile Authorization

The OAuth2 protocol relies on the concept of using short-lived `access_tokens` for `Authentication` to protected
resources. These tokens get renewed with `refresh_tokens` that have a longer expiration time (currently 2 weeks in the 
farmOS server). Additionally, a new `refresh_token` is provided with each request for a new `access_token`. This means 
that requests must be made to the farmOS server every 2 weeks enable to maintain valid tokens. 

In the context of the farmOS Aggregator an expired `refresh_token` means the associated farm profile must be 
re-authorized before requests can be made to the farmOS server. Depending how an Aggregator is deployed, authorization 
would likely require interaction from the farmOS server admin. Fortunately, it is easy to configure a CRON job to "ping"
all active farmOS servers on a regular basis in order to keep tokens active.

The protected `/api/v1/utils/ping-farms/` endpoint is provided for this use case. Requests can be made by either an 
Aggregator user, or a pre-configured API key (The API key must have `all_farms` access. No special scope is required). 
This endpoint will respond with number of (active) farms successfully pinged:

```json
{
  "msg":"Pinged 3/4 active farms."
}
``` 

 * If successful, the `last_accessed` time on farm profiles should reflect the time a `ping-farms` request was made:
![CRON Last Accessed](../img/ui/cron_last_accessed.png)

 * If the `AGGREGATOR_ALERT_PING_FARMS_ERRORS` variable is `true`, then this endpoint will alert Aggregator administrators 
if any farmOS servers do not respond during this request.

## Configuring a CRON job
An example of a simple bash script:

```shell script
#!/bin/sh

# Save in file named ping-farms.sh or similar.

# Add pre-configured API key.
API_KEY="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE1ODU1ODYxMDkuMDQ2NTA2LCJmYXJtX2lkIjpbXSwiYWxsX2Zhcm1zIjp0cnVlLCJzY29wZXMiOlsiZmFybTpyZWFkIl19.TUDUhnwfhBufdQKH_lQWyf19qXA0CAoJTOitbK5kL44"

# POST to the /ping-farms/ endpoint. Trailing slash required.
curl -X POST "http://localhost/api/v1/utils/ping-farms/" -H "accept: application/json" -H "api-key: $API_KEY"
```

This script can then be run daily by adding the following CRON job to the CRON tab (Edit the existing CRON tab with 
`sudo crontab -e` and add the following line):
```
# Run the ping-farms.sh script daily at 12AM.
0 0 * * * bash /path/to/script/ping-farms.sh
```

