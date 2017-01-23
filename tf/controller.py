from . import database
from . import Steam

killstreak = {
    1: "Killstreak",
    2: "Specialized Killstreak",
    3: "Professional Killstreak"
}

paints = {
    0x2f4f4f: "A Color Similar to Slate",
    0x7d4071: "A Deep Commitment to Purple",
    0x141414: "A Distinctive Lack of Hue",
    0xbcddb3: "A Mann's Mint",
    0x2d2d24: "After Eight",
    0x7e7e7e: "Aged Moustache Grey",
    0xe6e6e6: "An Extraordinary Abundance of Tinge",
    0xe7b53b: "Australium Gold",
    0xd8eed8: "Color No. 216-190-216",
    0xe9967a: "Dark Salmon Injustice",
    0x808000: "Drably Olive",
    0x729e42: "Indubitably Green",
    0xcf7336: "Mann Co. Orange",
    0xa57545: "Muskelmannbraun",
    0x51384a: "Noble Hatter's Violet",
    0xc5af91: "Peculiarly Drab Tincture",
    0xff69b4: "Pink as Hell",
    0x694d3a: "Radigan Conagher Brown",
    0x32cd32: "The Bitter Taste of Defeat and Lime",
    0xf0e68c: "The Color of a Gentlemann^s Business Pants",
    0x7c6c57: "Ye Olde Rustic Colour",
    0x424f3b: "Zepheniah's Greed",
    0x654740: "An Air of Debonair",
    0x3b1f23: "Balaclavas Are Forever",
    0xc36c2D: "Cream Spirit",
    0x483838: "Operator's Overalls",
    0xb8383b: "Team Spirit",
    0x803020: "The Value of Teamwork",
    0xa89a8c: "Waterlogged Lab Coat",
}

qcolor={
    0:"B2B2B2",
    1:"4D7455",
    2:"8D834B",
    3:"476291",
    5:"8650AC",
    6:"FFD700",
    7:"70B04A",
    8:"A50F79",
    9:"70B04A",
    11:"CF6A32",
    13:"38F3AB",
    14:"AA0000",
}

def get_items(id):
    return process_inventory(Steam.fetch_items(id)["result"]["items"])

def process_inventory(inventory):
    processed = []
    for item in inventory:
        unit = {}
        unit['quality'] = item['quality']
        unit['quantity'] = item['quantity']
        unit['level'] = item['level']
        unit['defindex'] = item['defindex']
        unit['color'] = qcolor[unit['quality']]
        unit['name'], unit['url'] = database.get_name_img(unit['defindex'])

        if not "flag_cannot_trade" in item.keys():
            unit['tradable'] = True
        else:
            unit['tradable'] = not item['flag_cannot_trade']

        if not "flag_cannot_craft" in item.keys():
            unit['craftable'] = True
        else:
            unit['craftable'] = not item['flag_cannot_craft']

        if not "custom_name" in item.keys():
            unit['custom_name'] = None
        else:
            unit['custom_name'] = item['custom_name']

        if not "custom_desc" in item.keys():
            unit['custom_desc'] = None
        else:
            unit['custom_desc'] = item['custom_desc']

        target_defindex = None
        target_name = None
        australium = False
        kstreak = None
        paint = None
        kills = None
        fabricates = None
        crate = None
        effect = 0
        meta = 0

        if 'attributes' in item.keys():
            for attr in item['attributes']:
                attr_def = attr["defindex"]
                if attr_def == 2012: #what should the tool be applied to
                    target_defindex = attr["float_value"]
                    target_name = database.get_name(target_defindex)
                elif attr_def == 2027:
                    australium = True
                elif attr_def == 134:
                    effect = attr["float_value"]
                elif attr_def == 187:
                    crate = attr["float_value"]
                elif attr_def == 2025:
                    kstreak = attr["float_value"]
                elif attr_def == 142:
                    paint = attr["float_value"]
                elif attr_def == 214:
                    kills = attr["value"]
                elif (attr_def == 2005 or attr_def == 2006) and attr["is_output"]:
                    for sub_attr in attr['attributes']:
                        if sub_attr["defindex"] == 2012:
                            fabricates = database.get_name(sub_attr["float_value"])

        if crate:
            unit['crate'] = crate
            meta = crate
            print("Crate id {0}, number {1}".format(unit['defindex'], meta))

        if effect:
            unit['effect'] = database.get_effect_name(effect)
            meta = effect

        if target_name and unit['name'] == "Strangifier":
            meta = target_defindex

        if target_name:
            unit['target_name'] = target_name

        if paint:
            if paint in paints:
                unit['painted'] = paints[paint]
            else:
                unit['painted'] = "Unknown paint: {0}".format(hex(paint))

        if kills:
            unit['strange'] = kills

        if australium:
            unit['name'] = "Australium {0}".format(unit['name'])

        unit["price"], unit["currency"] = database.get_price(defindex = unit["defindex"], name = unit["name"], quality=unit["quality"],
                                   craftable = unit["craftable"], tradable = unit["tradable"], metadata=meta)

        if kstreak:
            unit['name'] = "{0} {1}".format(killstreak[kstreak], unit['name'])

        if fabricates:
            unit['fabricate'] = fabricates

        processed.append(unit)

    return processed