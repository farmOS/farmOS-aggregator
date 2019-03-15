# Import Flask.
from flask import Flask

# Import Flask Admin.
from flask_admin import Admin

# Import SQLAlchemy.
from flask_sqlalchemy import SQLAlchemy

# Import BasicAuth.
from flask_basicauth import BasicAuth

# Import models.
from farmOSaggregator.models import db

# Import views.
import farmOSaggregator.views as views

# Import default settings.
import farmOSaggregator.default_settings

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-basicauth, etc.) in
# the global scope, but without instance specific argumentss passed in.
# These instances are not attached to the application at this point.
basic_auth = BasicAuth()

# Application Factory Function http://flask.pocoo.org/docs/1.0/patterns/appfactories/
def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from defaults first, then override with a settings.py file
    # inside the instance path.
    app.config.from_object('farmOSaggregator.default_settings')
    app.config.from_pyfile(config_filename, silent=True)

    # Create a database session.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.instance_path + '/' + app.config['DATABASE_FILENAME']
    db.init_app(app)

    # Configure HTTP Basic Authentication for the entire application.
    basic_auth.init_app(app)

    with app.app_context():

        db.create_all()

        return app


# Create a Flask Admin interface.
service_name = 'farmOS Aggregator'
index_name = 'Farms'
index_view = views.FarmView(models.Farm, db.session, name=index_name, endpoint='admin')
admin = Admin(app, name=service_name, template_mode='bootstrap3', url='/', index_view=index_view)
