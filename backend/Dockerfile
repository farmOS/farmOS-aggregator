FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --default-timeout=100 passlib[bcrypt] tenacity requests emails "fastapi==0.47.1" "pydantic==1.4" uvicorn gunicorn pyjwt python-multipart email_validator jinja2 psycopg2-binary alembic SQLAlchemy "farmOS==0.1.6b3"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80
