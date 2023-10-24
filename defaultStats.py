# Main file will import this file for getting stats for a new save, 
# fighting monsters, choosing color theme.

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
    'info': 'light_cyan',
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
    'info': 'white',
    'lore': 'light_grey'
}


home_shop = {
    "Potion":{
        "Name":"Potion", 
        "Cost":30, "Sell Price":20}, 
    "Iron Sword":{
        "Name":"Iron Sword", 
        "Equipable":True, 
        "Attack Modifier":15, 
        "Defence Modifier":0, 
        "Cost":150, 
        "Sell Price":75}, 
    "Iron Shield":{
        "Name":"Iron Shield", 
        "Equipable":True, 
        "Attack Modifier":0, 
        "Defence Modifier":5, 
        "Cost":200, 
        "Sell Price":100}, 
    "Iron Armour":{
        "Name":"Iron Armour", 
        "Equipable":True, 
        "Attack Modifier":0, 
        "Defence Modifier":10, 
        "Cost":300, 
        "Sell Price":150}
    }


default_human = {
        "type":"Player",
        "Inventory":[],
        "Coins":200,
        "Max Health":150,
        "Health":150,
        "Max Mana":100,
        "Mana":100,
        "Attack":50,
        "Wisdom":20,
        "Defence":25,
        "Dexterity":30,
        "Heal Buff":0
        }


default_monsterList = {
    1:{
        "type":"Wyvern",
        "Health":150,
        "Attack":35,
        "Defence":15,
        "Dexterity":50,
        "Coins":50
        },
    2:{
        "type":"Golem",
        "Health":300,
        "Attack":35,
        "Defence":40,
        "Dexterity":0,
        "Coins":75
        },
    3:{
        "type":"Dragon",
        "Health":250,
        "Attack":40,
        "Defence":30,
        "Dexterity":15,
        "Coins":100
        },
    4:{
        "type":"Troll",
        "Health":90,
        "Attack":40,
        "Defence":25,
        "Dexterity":20,
        "Coins":25
        }
}