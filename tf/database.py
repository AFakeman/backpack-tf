from . import db, Backpack, Steam
from .models import Item, Item_name, Effect, Kill_eater
import time


def add_item_to_session(price_data, name, quality, 
                        trade, craft, priceindex):
    is_craft = craft == "Craftable"
    is_trade = trade == "Tradable"
    currency = price_data['currency']
    price = price_data['value']
    if not price:
        price = 0
    price_high = price_data.get('value_high', price)
    new_item = Item(
        defindex=int(defindex), 
        quality=int(quality), 
        craftable=bool(is_craft),
        tradeable=bool(is_trade), 
        item_metadata=str(priceindex), 
        currency=str(currency),
        price=float(price), 
        price_high=float(price_high), 
        name=str(name)
    )
    new_item = db.session.merge(new_item)

def update_prices():
    prices = Backpack.get_prices()['response']
    for name, item1 in prices['items'].items():
        defindices = item1['defindex']
        for quality, item2 in item1['prices'].items():
            for trade, item3 in item2.items():
                for craft, item4 in item3.items():
                    if (isinstance(item4, dict)):
                        for priceindex, price_data in item4.items():
                            for defindex in defindices:
                                add_item_to_session(price_data, name, quality, 
                                                    trade, craft, priceindex)
                    else:
                        for price_data in item4:
                            for defindex in defindices:
                                add_item_to_session(price_data, name, quality, 
                                                    trade, craft, 0)
    db.session.commit()



def update_names():
    schema = Steam.get_schema()
    name_limit = Item_name.name.property.columns[0].type.length
    url_limit = Item_name.url.property.columns[0].type.length
    for item in schema["result"]["items"]:
        name = item["item_name"]
        url = item["image_url_large"]
        if name:
            name = name[:name_limit]
        if url:
            url = url[:name_limit]
        new_item = Item_name(defindex=item["defindex"], name=name, url=url)
        db.session.add(new_item)
    db.session.commit()


def update_effects():
    schema = Steam.get_schema()
    for effect in schema["result"]["attribute_controlled_attached_particles"]:
        new_effect = Effect(id=effect["id"], name=effect["name"])
        db.session.add(new_effect)
    db.session.commit()


def update_kill_eaters():
    schema = Steam.get_schema()
    for kill_eater in schema["result"]["kill_eater_score_types"]:
        new_eater = Kill_eater(
            type=kill_eater["type"], name=kill_eater["type_name"])
        db.session.add(new_eater)
    db.session.commit()


def get_name(defindex):
    item = Item_name.query.filter_by(defindex=int(defindex)).first()
    if not item:
        return "MISSINGNO"
    else:
        return item.name


def get_name_img(defindex):
    item = Item_name.query.filter_by(defindex=int(defindex)).first()
    if not item:
        return "MISSINGNO", ""
    else:
        return item.name, item.url


def get_effect_name(id):
    effect = Effect.query.filter_by(id=int(id)).first()
    if not effect:
        return str(id)
    else:
        return effect.name


def get_eater(type):
    eater = Kill_eater.query.filter_by(type=int(type)).first()
    if not eater:
        return str(id)
    else:
        return eater.name


def get_price(defindex, name=None, quality=6, craftable=True, tradable=True, 
                                                                    metadata=0):
    if name:
        item = Item.query.filter_by(
            defindex=int(defindex), 
            name=str(name), 
            quality=int(quality),
            craftable=bool(craftable), 
            tradeable=bool(tradable), 
            item_metadata=str(metadata)
        ).first()
    else:
        item = Item.query.filter_by(
            defindex=int(defindex), 
            quality=int(quality),
            craftable=bool(craftable), 
            tradeable=bool(tradable), 
            item_metadata=str(metadata)
        ).first()

    if item:
        return item.price, item.currency
    else:
        return None, None
