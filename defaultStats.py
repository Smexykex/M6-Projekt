# Main file will import this file for getting stats for a new save, 
# fighting monsters, choosing color theme.

# Dictionary med all data for items
from itemStats import thing

# Structure:
# Themes
# Shop items
# default player stats
# default monster stats

default_color_theme = {
    'listSomething': 'cyan',
    'dialogue': 'magenta',
    'newEnemy': 'light_red',
    'victory': 'light_green',
    'fail': 'red',
    'addItem': 'yellow',
    'misc': 'light_blue',
    'choices': 'light_magenta',
    'lore': 'light_magenta'
}

alt1_color_theme = {
    'listSomething': 'white',
    'dialogue': 'light_cyan',
    'newEnemy': 'light_red',
    'victory': 'yellow',
    'fail': 'red',
    'addItem': 'light_blue',
    'misc': 'light_green',
    'choices': 'light_blue',
    'lore': 'light_grey'
}


home_shop = {
    thing["potion"]["Name"].lower():thing["potion"],
    thing["iron sword"]["Name"].lower():thing["iron sword"],
    thing["iron shield"]["Name"].lower():thing["iron shield"],
    thing["iron armour"]["Name"].lower():thing["iron armour"],
}


default_player = {
    "type":"Player",
    "Inventory":[],
    "Equipment":{
        "Sword":thing["bronze sword"],
    },
    "Coins":120,
    "Level":1,
    "Experience":0,
    "Next level":100,
    "Max Health":150,
    "Max Mana":100,
    "Health":150,
    "Mana":100,
    "Attack":40,
    "Wisdom":20,
    "Defence":20,
    "Dexterity":20,
    "Heal Buff":0
}


default_monsterList = {
    1:{
        "type":"Wyvern",
        "Max Health":150,
        "Health":150,
        "Attack":35,
        "Defence":15,
        "Dexterity":50,
        "Coins":50,
        "Experience gain":50,
        "Drop Rate":25,
        "Drop":thing["wyvernscale armour"]
        },
    2:{
        "type":"Golem",
        "Max Health":250,
        "Health":250,
        "Attack":30,
        "Defence":25,
        "Dexterity":0,
        "Coins":75,
        "Experience gain":75,
        "Drop Rate":25,
        "Drop":thing["golem core"]
        },
    3:{
        "type":"Dragon",
        "Max Health":250,
        "Health":250,
        "Attack":40,
        "Defence":20,
        "Dexterity":15,
        "Coins":100,
        "Experience gain":100,
        "Drop Rate":25,
        "Drop":thing["dragon tooth"]
        },
    4:{
        "type":"Troll",
        "Max Health":120,
        "Health":120,
        "Attack":40,
        "Defence":25,
        "Dexterity":20,
        "Coins":25,
        "Experience gain":25,
        "Drop Rate":25,
        "Drop":thing["troll club"]
        },
    5:{
        "type":"Demon",
        "Max Health":500,
        "Health":500,
        "Attack":60,
        "Defence":45,
        "Dexterity":30,
        "Coins":500,
        "Experience gain":400,
        "Drop Rate":100,
        "Drop":thing["demon head"]
        }
}