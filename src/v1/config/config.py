from enum import Enum

entry_split = "|"
property_split = "-"

PRE_DEFINED = {}
PRE_DEFINED[45868] = {
    "id": 45868,
    "locale_default": "us",
    "locale_name": {
        "us": "Signature Classic Box",
    },
    "grade": 4,
    "category_primary": "Pearl Items",
    "category_secondary": "Class-based Apparel (Set)",
}
PRE_DEFINED[601251] = {
    "id": 601251,
    "locale_default": "us",
    "locale_name": {
        "us": "Value Pack (30 Days)",
    },
    "grade": 3,
    "category_primary": "Pearl Items",
    "category_secondary": "Functional",
}

LOCALES = [
    "na",
    "eu",
    "sea",
    "mena",
    "kr",
    "ru",
    "jp",
    "th",
    "tw",
    "sa",
    "gl",
]

MARKET_URLS = {
    "regions": {
        "na": "na-trade.naeu.playblackdesert.com",
        "eu": "eu-trade.naeu.playblackdesert.com",
        "sea": "trade.sea.playblackdesert.com",
        "mena": "trade.tr.playblackdesert.com",
        "kr": "trade.kr.playblackdesert.com",
        "ru": "trade.ru.playblackdesert.com",
        "jp": "trade.jp.playblackdesert.com",
        "th": "trade.th.playblackdesert.com",
        "tw": "trade.tw.playblackdesert.com",
        "sa": "trade.sa.playblackdesert.com",
        "gl": "trade.global-lab.playblackdesert.com",
    }
}

class MarketEndpoint(Enum):
    GET_WORLD_MARKET_LIST = "GetWorldMarketList"
    GET_WORLD_MARKET_SUB_LIST = "GetWorldMarketSubList"
    GET_WORLD_MARKET_SEARCH_LIST = "GetWorldMarketSearchList"
    GET_BIDDING_INFO_LIST = "GetBiddingInfoList"
    GET_MARKET_PRICE_INFO = "GetMarketPriceInfo"


market_url_structure = {
    region: {endpoint.name: f"https://{url}/Trademarket/{endpoint.value}"
             for endpoint in MarketEndpoint}
    for region, url in MARKET_URLS["regions"].items()
}



MARKET_CATEGORIES = {
    "1":
        (
            "Main Weapon",
            {
                "1":"Longsword",
                "2":"Longbow",
                "3":"Amulet",
                "4":"Axe",
                "5":"Shortsword",
                "6":"Blade",
                "7":"Staff",
                "8":"Kriegsmesser",
                "9":"Gauntlet",
                "10":"Crescent Pendulum",
                "11":"Crossbow",
                "12":"Florang",
                "13":"Battle Axe",
                "14":"Shamshir",
                "15":"Morning Star",
                "16":"Kyve",
                "17":"Serenaca",
            },
        ),
    "5":
        (
            "Sub Weapon",
            {
                "1":"Shield",
                "2":"Dagger",
                "3":"Talisman",
                "4":"Ornamental Knot",
                "5":"Trinket",
                "6":"Horn Bow",
                "7":"Kunai",
                "8":"Shuriken",
                "9":"Vambrace",
                "10":"Noble Sword",
                "11":"Ra'ghon",
                "12":"Vitclari",
                "13":"Haladie",
                "14":"Quoratum",
                "15":"Mareca",
            },
        ),
    "10":
        (
            "Awakening Weapon",
            {
                "1":"Great Sword",
                "2":"Scythe",
                "3":"Iron Buster",
                "4":"Kamasylven Sword",
                "5":"Celestial Bo Staff",
                "6":"Lancia",
                "7":"Crescent Blade",
                "8":"Kerispear",
                "9":"Sura Katana",
                "10":"Sah Chakram",
                "11":"Aad Sphera",
                "12":"Godr Sphera",
                "13":"Vediant",
                "14":"Gardbrace",
                "15":"Cestus",
                "16":"Crimson Glaives",
                "17":"Greatbow",
                "19":"Jordun",
                "20":"Dual Glaives",
                "21":"Sting",
                "22":"Kibelius",
                "23":"Patraca",
            },
        ),
    "15":
        (
            "Armor",
            {
                "1":"Helmet",
                "2":"Armor",
                "3":"Gloves",
                "4":"Shoes",
                "5":"Functional Clothes",
                "6":"Crafted Clothes",
            },
        ),
    "20":
        (
            "Accessory",
            {
                "1":"Ring",
                "2":"Necklace",
                "3":"Earring",
                "4":"Belt",
            },
        ),
    "25":
        (
            "Material",
            {
                "1":"Ore/Gem",
                "2":"Plants",
                "3":"Seed/Fruit",
                "4":"Leather",
                "5":"Blood",
                "6":"Meat",
                "7":"Seafood",
                "8":"Misc.",
            },
        ),
    "30":
        (
            "Enhancement/Upgrade",
            {
                "1":"Black Stone",
                "2":"Upgrade"
            },
        ),
    "35":
        (
            "Consumables",
            {
                "1":"Offensive Elixir",
                "2":"Defensive Elixir",
                "3":"Functional Elixir",
                "4":"Food",
                "5":"Potion",
                "6":"Siege Items",
                "7":"Item Parts",
                "8":"Other Consumables",
            },
        ),
    "40":
        (
            "Life Tools",
            {
                "1":"Lumbering Axe",
                "2":"Fluid Collector",
                "3":"Butcher Knife",
                "4":"Pickaxe",
                "5":"Hoe",
                "6":"Tanning Knife",
                "7":"Fishing Tools",
                "8":"Matchlock",
                "9":"Alchemy/Cooking",
                "10":"Other Tools",
            },
        ),
    "45":
        (
            "Alchemy Stone",
            {
                "1":"Destruction",
                "2":"Protection",
                "3":"Life",
                "4":"Spirit Stone",
            },
        ),
    "50":
        (
            "Magic Crystal",
            {
                "1":"Main Weapon",
                "2":"Sub-weapon",
                "3":"Helmet",
                "4":"Armor",
                "5":"Gloves",
                "6":"Shoes",
                "7":"Versatile",
                "8":"Awakening Weapon",
            },
        ),
    "55":
        (
            "Pearl Items",
            {
                "1":"Male Apparel (Set)",
                "2":"Female Apparels (Set)",
                "3":"Male Apparel (Individual)",
                "4":"Female Apparel (Individual)",
                "5":"Class-based Apparel (Set)",
                "6":"Functional",
                "7":"Mount",
                "8":"Pet",
            },
        ),
    "60":
        (
            "Dye",
            {
                "1":"Basic",
                "2":"Olvia",
                "3":"Velia",
                "4":"Heidelian",
                "5":"Keplan",
                "6":"Calpheon",
                "7":"Mediah",
                "8":"Valencia",
            },
        ),
    "65":
        (
            "Mount",
            {
                "1":"Registration",
                "2":"Feed",
                "3":"Champron",
                "4":"Barding",
                "5":"Saddle",
                "6":"Stirrups",
                "7":"Horseshoe",
                "9":"[Elephant] Stirrups",
                "10":"[Elephant] Armor",
                "11":"[Elephant] Mask",
                "12":"[Elephant] Saddle",
                "13":"Courser Training",
            },
        ),
    "70":
        (
            "Ship",
            {
                "1":"Registration",
                "2":"Cargo",
                "3":"Prow",
                "4":"Decoration",
                "5":"Totem",
                "6":"Prow Statue",
                "7":"Plating",
                "8":"Cannon",
                "9":"Sail",
            },
        ),
    "75":
        (
            "Wagon",
            {
                "1":"Registration",
                "2":"Wheel",
                "3":"Cover",
                "4":"Flag",
                "5":"Emblem",
                "6":"Lamp",
            },
        ),
    "80":
        (
            "Furniture",
            {
                "1":"Bed",
                "2":"Bedside Table/Table",
                "3":"Wardrobe/Bookshelf",
                "4":"Sofa/Chair",
                "5":"Chandelier",
                "6":"Floor/Carpet",
                "7":"Wall/Curtain",
                "8":"Decoration",
                "9":"Others",
            },
        ),
}
