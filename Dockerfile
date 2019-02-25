# Inherit from the official Python 3 image.
FROM python:3

# Expose port 80.
EXPOSE 80

# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

# Install uwsgi with pip.
RUN pip install --no-cache-dir uwsgi

# Copy setup.py and README.md into /usr/src/app.
# Install application dependencies with pip.
# Build the farmOSaggregator package.
# We do these first to reduce image build time during development.
COPY setup.py README.md ./
RUN pip install -e .
RUN python setup.py install

# Copy the app.
COPY . ./

# Run the application with uwsgi on port 80.
CMD [ "uwsgi", "--shared-socket", "[::]:80", \
               "--http", "=0", \
               "--protocol", "uwsgi", \
               "--wsgi", "farmOSaggregator:app", \
               "--master", "--enable-threads" ]
