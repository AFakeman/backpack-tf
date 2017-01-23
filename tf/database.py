from . import db, Backpack, Steam
from .models import Item, Item_name, Effect

def update_prices():
    names = {}
    prices = Backpack.get_prices()['response']
    for name, item1 in prices['items'].items():
        defindices = item1['defindex']
        for quality, item3 in item1['prices'].items():
            for trade, item4 in item3.items():
                for craft, item5 in item4.items():
                    if (isinstance(item5, dict)):
                        for priceindex, item6 in item5.items():
                            for defindex in defindices:
                                names[defindex] = name
                                is_craft = True if craft == "Craftable" else False
                                is_trade = True if trade == "Tradable" else False
                                currency = item6['currency']
                                price = item6['value']
                                price_high = price if not 'value_high' in item6.keys() else item6['value_high']
                                new_item = Item(defindex=defindex, quality=quality, craftable=is_craft,
                                                tradeable=is_trade, item_metadata=priceindex, currency=currency,
                                                price=price, price_high=price, name=name)
                                db.session.add(new_item)
                                db.session.commit()
                    else:
                        for item6 in item5:
                            priceindex = 0
                            for defindex in defindices:
                                names[defindex] = name
                                is_craft = True if craft == "Craftable" else False
                                is_trade = True if trade == "Tradable" else False
                                currency = item6['currency']
                                price = item6['value']
                                price_high = price if not 'value_high' in item6.keys() else item6['value_high']
                                new_item = Item(defindex=defindex, quality=quality, craftable=is_craft,
                                                tradeable=is_trade, item_metadata=priceindex, currency=currency,
                                                price=price, price_high=price, name=name)
                                db.session.add(new_item)
    db.session.commit()

def update_names():
    schema = Steam.get_schema()
    for item in schema["result"]["items"]:
        new_item = Item_name(defindex=item["defindex"], name=item["item_name"], url=item["image_url_large"])
        db.session.add(new_item)
    db.session.commit()

def update_effects():
    schema = Steam.get_schema()
    for effect in schema["result"]["attribute_controlled_attached_particles"]:
        new_effect = Effect(id=effect["id"], name=effect["name"])
        db.session.add(new_effect)
    db.session.commit()

def get_name(defindex):
    item = Item_name.query.filter_by(defindex=defindex).first()
    if not item:
        return "MISSINGNO"
    else:
        return item.name

def get_name_img(defindex):
    item = Item_name.query.filter_by(defindex=defindex).first()
    if not item:
        return "MISSINGNO", ""
    else:
        return item.name, item.url

def get_effect_name(id):
    effect = Effect.query.filter_by(id=id).first()
    if not effect:
        return str(id)
    else:
        return effect.name

def get_price(defindex, name=None, quality=6, craftable=True, tradable=True, metadata=0):
    if name:
        item = Item.query.filter_by(defindex=defindex, name=name, quality=quality,
                             craftable=craftable, tradeable=tradable, item_metadata=metadata).first()
    else:
        item = Item.query.filter_by(defindex=defindex, quality=quality,
                                    craftable=craftable, tradeable=tradable, item_metadata=metadata).first()
    if item:
        return item.price, item.currency
    else:
        return None, None