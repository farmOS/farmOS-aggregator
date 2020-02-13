FROM python:3.7

RUN pip install raven celery~=4.3 passlib[bcrypt] tenacity requests "fastapi==0.47.1" "pydantic==1.4" emails pyjwt email_validator jinja2 psycopg2-binary alembic SQLAlchemy "farmOS==0.1.5"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

ENV C_FORCE_ROOT=1

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
