from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from . import backpack
Steam = backpack.Steam(app.config['STEAM_API_KEY'])
Backpack = backpack.Backpack(app.config['BACKPACK_API_KEY'], local=True)

from . import views
from . import models

#db.drop_all()
#db.create_all()


from . import database
#database.update_prices()