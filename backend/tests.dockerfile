FROM python:3.7

RUN pip install requests pytest tenacity passlib[bcrypt] "fastapi==0.47.1" "pydantic==1.4" email_validator pyjwt psycopg2-binary SQLAlchemy "farmOS==0.1.6b3"

# Load farm registration configuration.
ARG OPEN_FARM_REGISTRATION
ARG INVITE_FARM_REGISTRATION
ENV AGGREGATOR_OPEN_FARM_REGISTRATION=${OPEN_FARM_REGISTRATION}
ENV AGGREGATOR_INVITE_FARM_REGISTRATION=${INVITE_FARM_REGISTRATION}

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

COPY ./app /app

ENV PYTHONPATH=/app

COPY ./app/tests-start.sh /tests-start.sh
COPY ./app/single-test-start.sh /single-test-start.sh

RUN chmod +x /tests-start.sh /single-test-start.sh

# This will make the container wait, doing nothing, but alive
CMD ["bash", "-c", "while true; do sleep 1; done"]

# Afterwards you can exec a command /tests-start.sh in the live container, like:
# docker exec -it backend-tests /tests-start.sh
