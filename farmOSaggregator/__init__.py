# Import Flask.
from flask import Flask

# Import Flask Admin.
from flask_admin import Admin

# Create a Flask application.
app = Flask(__name__)

# Create a Flask Admin interface.
service_name = 'farmOS Aggregator'
admin = Admin(app, name=service_name, template_mode='bootstrap3', url='/')
