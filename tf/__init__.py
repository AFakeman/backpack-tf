from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import backpack

from . import __file__ as kek

app = Flask(__name__)
app.config.from_object(__name__ + ".default_config")
db = SQLAlchemy(app)

Steam = backpack.Steam(api=app.config['STEAM_API_KEY'], host=app.config['WEBAPI_HOST'], port=app.config['WEBAPI_PORT'])
Backpack = backpack.Backpack(api=app.config['BACKPACK_API_KEY'], host=app.config['WEBAPI_HOST'], port=app.config['WEBAPI_PORT'])

from . import views
from . import models

#db.drop_all()
#db.create_all()


from . import database
#database.update_prices()