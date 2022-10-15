import os

SECRET_KEY = os.urandom(32)
# Random characters - protects against modifying cookies, cross-site request,
# forgery attacks when using forms

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:1@localhost:5432/fyyur"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# saves memory, see below:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
