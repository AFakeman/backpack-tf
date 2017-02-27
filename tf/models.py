from . import db

class Item(db.Model):
    __tablename__ = "prices"
    defindex = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.Integer, primary_key=True)
    craftable = db.Column(db.Boolean, primary_key=True)
    tradeable = db.Column(db.Boolean, primary_key=True)
    item_metadata = db.Column(db.String(70), primary_key=True)
    name = db.Column(db.String(70), primary_key=True)
    currency = db.Column(db.String(70))
    price = db.Column(db.Float)
    price_high = db.Column(db.Float)

class Item_name(db.Model):
    __tablename__ = "item_names"
    defindex = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(210))

class Effect(db.Model):
    __tablename__ = "effects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

class Kill_eater(db.Model):
    __tablename__ = "kill_eaters"
    type = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))