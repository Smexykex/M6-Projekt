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
    'choices': 'light_grey',
    'lore': 'light_grey'
}


home_shop = {
    thing["potion"]["Name"].lower():thing["potion"],
    thing["iron sword"]["Name"].lower():thing["iron sword"],
    thing["iron shield"]["Name"].lower():thing["iron shield"],
    thing["iron armour"]["Name"].lower():thing["iron armour"],
}


default_human = {
    "type":"Player",
    "Inventory":[],
    "Equipment":{
        "Sword":thing["bronze sword"],
        "Shield":None,
        "Armour":None},
    "Coins":200,
    "Level":1,
    "Experience":0,
    "Next level":100,
    "Max Health":150,
    "Max Mana":100,
    "Health":150,
    "Mana":100,
    "Attack":40,
    "Wisdom":20,
    "Defence":10,
    "Dexterity":30,
    "Heal Buff":0
}


default_monsterList = {
    1:{
        "type":"Wyvern",
        "Health":150,
        "Attack":30,
        "Defence":15,
        "Dexterity":50,
        "Coins":50,
        "Experience gain":35,
        "Drop":thing["wyvernscale armour"]
        },
    2:{
        "type":"Golem",
        "Health":250,
        "Attack":30,
        "Defence":30,
        "Dexterity":0,
        "Coins":75,
        "Experience gain":75,
        "Drop":thing["golem core"]
        },
    3:{
        "type":"Dragon",
        "Health":250,
        "Attack":40,
        "Defence":20,
        "Dexterity":15,
        "Coins":100,
        "Experience gain":80,
        "Drop":thing["dragon tooth"]
        },
    4:{
        "type":"Troll",
        "Health":90,
        "Attack":40,
        "Defence":25,
        "Dexterity":20,
        "Coins":25,
        "Experience gain":25,
        "Drop":thing["troll club"]
        }
}