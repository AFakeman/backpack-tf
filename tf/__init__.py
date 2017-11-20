from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import backpack

import os

app = Flask(__name__)
app.config.from_object(__name__ + ".default_config")

if 'INVENTORY_CONFIG' in os.environ:
    config = os.environ['INVENTORY_CONFIG']
    app.config.from_pyfile(config)
    print("Applied custom config")
else:
    print("No custom config found, APIs are not guranteed to work.")

db = SQLAlchemy(app)

Steam = backpack.Steam(api=app.config['STEAM_API_KEY'], 
                       host=app.config['WEBAPI_HOST'], 
                       port=app.config['WEBAPI_PORT'])

Backpack = backpack.Backpack(api=app.config['BACKPACK_API_KEY'], 
                             host=app.config['WEBAPI_HOST'], 
                             port=app.config['WEBAPI_PORT'])

from . import views
from . import models

# db.drop_all()
# db.create_all()


from . import database
# database.update_prices()
