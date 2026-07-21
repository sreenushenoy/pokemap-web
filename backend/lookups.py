"""Name lookup tables for items, Pokemon, and reward type metadata."""

ITEM_NAMES = {
    "1": "Poke Ball", "2": "Great Ball", "3": "Ultra Ball",
    "301": "Lucky Egg", "401": "Ordinary Incense", "501": "Lure Module",
    "701": "Razz Berry", "705": "Nanab Berry", "706": "Pinap Berry",
    "708": "Golden Razz Berry", "709": "Silver Pinap Berry",
    "1301": "Premium Raid Pass", "1404": "Star Piece",
    "1101": "Sun Stone", "1102": "King Rock", "1103": "Metal Coat",
    "1104": "Dragon Scale", "1105": "Up-Grade", "1106": "Sinnoh Stone",
    "1107": "Unova Stone",
}

POKEMON_NAMES = {
    "1": "Bulbasaur", "2": "Ivysaur", "3": "Venusaur",
    "4": "Charmander", "5": "Charmeleon", "6": "Charizard",
    "7": "Squirtle", "8": "Wartortle", "9": "Blastoise",
    "15": "Beedrill", "16": "Pidgey", "18": "Pidgeot",
    "19": "Rattata", "25": "Pikachu", "26": "Raichu",
    "27": "Sandshrew", "35": "Clefairy", "36": "Clefable",
    "37": "Vulpix", "38": "Ninetales", "39": "Jigglypuff",
    "46": "Paras", "50": "Diglett", "52": "Meowth",
    "54": "Psyduck", "56": "Mankey", "58": "Growlithe",
    "59": "Arcanine", "60": "Poliwag", "61": "Poliwhirl",
    "66": "Machop", "67": "Machoke", "74": "Geodude",
    "77": "Ponyta", "79": "Slowpoke", "84": "Doduo",
    "93": "Haunter", "95": "Onix", "103": "Exeggutor",
    "104": "Cubone", "105": "Marowak", "109": "Koffing",
    "111": "Rhyhorn", "113": "Chansey", "117": "Seadra",
    "119": "Seaking", "121": "Starmie", "123": "Scyther",
    "125": "Electabuzz", "126": "Magmar", "127": "Pinsir",
    "129": "Magikarp", "131": "Lapras", "133": "Eevee",
    "134": "Vaporeon", "135": "Jolteon", "136": "Flareon",
    "138": "Omanyte", "140": "Kabuto", "142": "Aerodactyl",
    "143": "Snorlax", "147": "Dratini", "148": "Dragonair",
    "152": "Chikorita", "155": "Cyndaquil", "158": "Totodile",
    "164": "Noctowl", "172": "Pichu", "173": "Cleffa",
    "175": "Togepi", "176": "Togetic", "183": "Marill",
    "185": "Sudowoodo", "191": "Sunkern", "196": "Espeon",
    "197": "Umbreon", "198": "Murkrow", "202": "Wobbuffet",
    "206": "Dunsparce", "207": "Gligar", "209": "Snubbull",
    "215": "Sneasel", "216": "Teddiursa", "219": "Magcargo",
    "221": "Piloswine", "223": "Remoraid", "226": "Mantine",
    "228": "Houndour", "246": "Larvitar", "247": "Pupitar",
    "252": "Treecko", "255": "Torchic", "258": "Mudkip",
    "263": "Zigzagoon", "271": "Lombre", "274": "Nuzleaf",
    "278": "Wingull", "280": "Ralts", "290": "Nincada",
    "296": "Makuhita", "303": "Mawile", "304": "Aron",
    "320": "Wailmer", "326": "Grumpig", "327": "Spinda",
    "328": "Trapinch", "333": "Swablu", "343": "Baltoy",
    "345": "Lileep", "347": "Anorith", "349": "Feebas",
    "356": "Dusclops", "361": "Snorunt", "364": "Sealeo",
    "366": "Clamperl", "371": "Bagon", "374": "Beldum",
    "375": "Metang", "387": "Turtwig", "390": "Chimchar",
    "393": "Piplup", "397": "Staravia", "399": "Bidoof",
    "403": "Shinx", "404": "Luxio", "415": "Combee",
    "427": "Buneary", "431": "Glameow", "434": "Stunky",
    "443": "Gible", "444": "Gabite", "449": "Hippopotas",
    "453": "Croagunk", "459": "Snover", "495": "Snivy",
    "498": "Tepig", "501": "Oshawott", "507": "Herdier",
    "510": "Liepard", "524": "Roggenrola", "531": "Audino",
    "544": "Whirlipede", "546": "Cottonee", "554": "Darumaka",
    "562": "Yamask", "564": "Tirtouga", "566": "Archen",
    "568": "Trubbish", "580": "Ducklett", "582": "Vanillite",
    "587": "Emolga", "588": "Karrablast", "597": "Ferroseed",
    "603": "Eelektrik", "605": "Elgyem", "608": "Lampent",
    "610": "Axew", "613": "Cubchoo", "616": "Shelmet",
    "618": "Stunfisk", "650": "Chespin", "653": "Fennekin",
    "656": "Froakie", "659": "Bunnelby", "660": "Diggersby",
    "662": "Fletchinder", "667": "Litleo", "688": "Binacle",
    "692": "Clauncher", "696": "Tyrunt", "698": "Amaura",
    "702": "Dedenne", "704": "Goomy", "722": "Rowlet",
    "725": "Litten", "728": "Popplio", "732": "Trumbeak",
    "742": "Cutiefly", "747": "Mareanie", "751": "Dewpider",
    "759": "Stufful", "767": "Wimpod", "810": "Grookey",
    "813": "Scorbunny", "816": "Sobble", "819": "Skwovet",
    "827": "Nickit", "831": "Wooloo", "906": "Sprigatito",
    "909": "Fuecoco", "912": "Quaxly", "915": "Pawmi",
    "917": "Tarountula", "919": "Nymble", "921": "Lokix",
    "928": "Finizen", "932": "Wiglett",
}

MEGA_POKEMON_NAMES = {
    "3": "Venusaur", "6": "Charizard", "9": "Blastoise",
    "15": "Beedrill", "18": "Pidgeot", "65": "Alakazam",
    "80": "Slowbro", "94": "Gengar", "115": "Kangaskhan",
    "127": "Pinsir", "130": "Gyarados", "142": "Aerodactyl",
    "181": "Ampharos", "208": "Steelix", "212": "Scizor",
    "214": "Heracross", "229": "Houndoom", "248": "Tyranitar",
    "254": "Sceptile", "257": "Blaziken", "260": "Swampert",
    "282": "Gardevoir", "302": "Sableye", "303": "Mawile",
    "306": "Aggron", "308": "Medicham", "310": "Manectric",
    "319": "Sharpedo", "323": "Camerupt", "334": "Altaria",
    "354": "Banette", "359": "Absol", "362": "Glalie",
    "373": "Salamence", "376": "Metagross", "380": "Latias",
    "381": "Latios", "384": "Rayquaza", "428": "Lopunny",
    "445": "Garchomp", "448": "Lucario", "460": "Abomasnow",
    "531": "Audino", "719": "Diancie",
}

TYPE_META = {
    "t2":  {"group": "items",       "label": "Items",              "icon": "gift",     "type_num": 2,  "id_field": True,  "lookup": "item"},
    "t3":  {"group": "stardust",    "label": "Stardust",           "icon": "star",     "type_num": 3,  "id_field": False, "lookup": None},
    "t7":  {"group": "encounters",  "label": "Pokemon Encounters", "icon": "pokeball", "type_num": 7,  "id_field": True,  "lookup": "pokemon"},
    "t8":  {"group": "coins",       "label": "PokeCoins",          "icon": "coins",    "type_num": 8,  "id_field": False, "lookup": None},
    "t12": {"group": "mega",        "label": "Mega Energy",        "icon": "mega",     "type_num": 12, "id_field": True,  "lookup": "mega"},
}


def filter_code(type_num: int, id_field: bool, val: str) -> str:
    base_val = val.split("-")[0]
    if id_field:
        return f"{type_num},1,{base_val}"
    return f"{type_num},{base_val},0"


def filter_label(meta: dict, val: str) -> str:
    base_val = val.split("-")[0]
    suffix = f" ({val.split('-')[1]})" if "-" in val else ""
    lookup = meta["lookup"]
    t = meta["type_num"]
    if lookup == "item":
        return ITEM_NAMES.get(base_val, f"Item #{base_val}")
    if lookup == "pokemon":
        return POKEMON_NAMES.get(base_val, f"Pokemon #{base_val}") + suffix
    if lookup == "mega":
        name = MEGA_POKEMON_NAMES.get(base_val) or POKEMON_NAMES.get(base_val, f"Pokemon #{base_val}")
        return f"{name} Mega Energy"
    if t == 3:
        return f"{int(base_val):,} Stardust"
    if t == 8:
        return f"{base_val} PokeCoins"
    return val


def normalize_filters(raw: dict) -> list:
    DISPLAY_ORDER = ["coins", "stardust", "items", "encounters", "mega"]
    groups: dict = {}
    for t_key, values in raw.items():
        if t_key not in TYPE_META or not values:
            continue
        meta = TYPE_META[t_key]
        gid = meta["group"]
        options = []
        for val in values:
            code = filter_code(meta["type_num"], meta["id_field"], str(val))
            label = filter_label(meta, str(val))
            options.append({"code": code, "label": label})
        if not meta["id_field"]:
            options.sort(key=lambda o: int(o["code"].split(",")[1]))
        else:
            options.sort(key=lambda o: o["label"])
        groups[gid] = {
            "group": gid,
            "label": meta["label"],
            "icon": meta["icon"],
            "options": options,
        }
    return [groups[g] for g in DISPLAY_ORDER if g in groups]
