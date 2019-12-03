FROM python:3.7

RUN pip install requests pytest tenacity passlib[bcrypt] celery~=4.3 "fastapi==0.30.0" psycopg2-binary SQLAlchemy "farmOS==0.1.4"

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
