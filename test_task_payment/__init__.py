import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .helpers import Piastrix
from .settings import Config, LOG_FORMAT


logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
piastrix = Piastrix(
    shop_id=app.config['PIASTRIX_SHOP_ID'],
    secret_key=app.config['PIASTRIX_SECRET_KEY'],
    base_url=app.config['PIASTRIX_BASE_URL'],
)


from .urls import *
