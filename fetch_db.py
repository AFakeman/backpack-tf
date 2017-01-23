import tf.database as database
from tf import db

db.drop_all()
db.create_all()

database.update_prices()
database.update_effects()
database.update_names()