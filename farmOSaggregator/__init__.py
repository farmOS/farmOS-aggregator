# Import Flask.
from flask import Flask

# Import Flask Admin.
from flask_admin import Admin

# Import SQLAlchemy.
from flask_sqlalchemy import SQLAlchemy

# Import BasicAuth.
from flask_basicauth import BasicAuth

# Import models.
import farmOSaggregator.models as models

# Import views.
import farmOSaggregator.views as views

# Import default settings.
import farmOSaggregator.default_settings

# Create a Flask application.
app = Flask(__name__, instance_relative_config=True)

# Load configuration from defaults first, then override with a settings.py file
# inside the instance path.
app.config.from_object('farmOSaggregator.default_settings')
app.config.from_pyfile('settings.py', silent=True)

# Create a database session.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.instance_path + '/' + app.config['DATABASE_FILENAME']
db = SQLAlchemy(app)

# Create the database tables, if necessary.
models.Base.metadata.create_all(db.engine)

# Configure HTTP Basic Authentication for the entire application.
basic_auth = BasicAuth(app)

# Create a Flask Admin interface.
service_name = 'farmOS Aggregator'
index_name = 'Farms'
index_view = views.FarmView(models.Farm, db.session, name=index_name, endpoint='admin')
admin = Admin(app, name=service_name, template_mode='bootstrap3', url='/', index_view=index_view)
