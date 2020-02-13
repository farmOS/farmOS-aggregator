# Deploying a farmOS Aggregator

The farmOS Aggregator is designed to have a robust configuration making it possible to use an Aggregator in many
different use cases without requiring custom modifications. To make deployment and updating of an Aggregator as easy as
possible, settings for both the `frontend` and `backend` images can be configured with environment variables at runtime.

There are two methods to deploy a farmOS Aggregator. It is recommended to use the configurable Docker Hub images, but
the `backend` and `frontend` images can also be built and deployed if customizations are required.

## Deploying from Docker Hub

*This is the recommended method for deploying an Aggregator.*

Deployment requires a few steps:
 - Configure environment variables to configure the Aggregator as desired. A`.env` template used for configuring the
 Aggregator environment variables is provided in the GitHub repo at [https://github.com/farmOS/farmOS-aggregator/blob/master/.env-template]()
 - Download the template docker-compose file provided in the GitHub 
repo at [https://github.com/farmOS/farmOS-aggregator/blob/master/docker-compose.deploy-template.yml]()
   - Note that this template defaults to using the `latest` tagged images of both the `backend` and `frontend` from 
   Docker Hub. The image tag can be modified to request a certain tagged releast, if desired. Set the Docker Hub
   repository for available tags.
   - This template also provides a container for the `PostgresDB` and `NGINX` proxy. These are designed to work in
   production, but you could modify the `docker-compose` file to connect to a separately hosted DB, or use a different
   proxy.
 - Rename the `docker-compose.deploy-template.yml` file to `docker-compose.yml`. 
 - Generate a self-signed cert before starting the `nginx` proxy container. The container will not start if it fails to
 load a certificate.
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
  - TODO: Document creating a CRON job to auto-update certs.
 
 
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
