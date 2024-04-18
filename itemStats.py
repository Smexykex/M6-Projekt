# Main file will import this to get buy/sell value, 
# info, interaction with specific item, stats for chosen item, etc.

# Structure:
# Use specific item function
# Dictionary of item statistics,

# Checks if the player can cast a spell.
# If they can, return True and subtract the mana cost from the players mana
def hasMana(player, manaCost):
    if player["Mana"] < manaCost:
        return False
    
    player["Mana"] -= manaCost
    return True
    

def castFireBall(player, monster):
    if not hasMana(player, 45):
        return False
    
    damage = 15 + player["Wisdom"]
    monster["Health"] -= damage
    print(f'Player casts fire ball on {monster["type"]} and deals {damage} damage\n')
    return True


def castFrostBlast(player, monster):
    if not hasMana(player, 30):
        return False
    
    damage = 10 + player["Wisdom"] // 2
    monster["Health"] -= damage
    monster["Dexterity"] -= 5
    print(f'Player casts frost blast on {monster["type"]} and deals {damage} damage')
    print(f'{monster["type"]} now has {monster["Dexterity"]} dexterity\n')
    return True


def castRegenerate(player):
    if not hasMana(player, 80):
        return False
    
    player["Heal Buff"] = 3 + player["Wisdom"] // 15
    print("Player casts regenerate\n")
    return True


# Returns the index of a item in the inventory. Retruns None otherwise
def inventoryIndex(player, checkItem):
    for count, item in enumerate(player["Inventory"]):
        if item["Name"] == checkItem:
            return count


def usePotion(player):
    index = inventoryIndex(player, "Potion")
    if index == None:
        return False
    
    print("You use a potion\n")
    player["Inventory"].pop(index)
    player["Health"] += 50
    if player["Health"] > player["Max Health"]:
        player["Health"] = player["Max Health"]
    return True


# Using item as dict name might screw with stuff in main file
thing = {
    "potion":{
        "Name":"Potion", 
        "Cost":30, 
        "Sell Price":20},
    
    "bronze sword":{
        "Name":"Bronze Sword",
        "Type":"Sword",
        "Equipable":True, 
        "Attack Modifier":20,
        "Wisdom Modifier":0,
        "Defence Modifier":0,
        "Dexterity Modifier":0,
        "Sell Price":30},

    "iron sword":{
        "Name":"Iron Sword",
        "Type":"Sword",
        "Equipable":True, 
        "Attack Modifier":30,
        "Wisdom Modifier":0,
        "Defence Modifier":0,
        "Dexterity Modifier":0,
        "Cost":150, 
        "Sell Price":75}, 

    "iron shield":{
        "Name":"Iron Shield",
        "Type":"Shield",
        "Equipable":True, 
        "Attack Modifier":0,
        "Wisdom Modifier":0,
        "Defence Modifier":5,
        "Dexterity Modifier":0,
        "Cost":200, 
        "Sell Price":100}, 

    "iron armour":{
        "Name":"Iron Armour",
        "Type":"Armour",
        "Equipable":True, 
        "Attack Modifier":0,
        "Wisdom Modifier":0,
        "Defence Modifier":10,
        "Dexterity Modifier":0,
        "Cost":300, 
        "Sell Price":150},
    
    "wyvernscale armour":{
            "Name":"Wyvernscale Armour",
            "Type":"Armour",
            "Equipable":True, 
            "Attack Modifier":0,
            "Wisdom Modifier":0,
            "Defence Modifier":10,
            "Dexterity Modifier":5,
            "Sell Price":250},
    
    "golem core":{
            "Name":"Golem Core",
            "Type":"Shield",
            "Equipable":True, 
            "Attack Modifier":0,
            "Wisdom Modifier":5,
            "Defence Modifier":7,
            "Dexterity Modifier":0,
            "Sell Price":300},
    
    "dragon tooth":{
            "Name":"Dragon Tooth",
            "Type":"Sword",
            "Equipable":True, 
            "Attack Modifier":35,
            "Wisdom Modifier":5,
            "Defence Modifier":0,
            "Dexterity Modifier":0,
            "Sell Price":300},
    
    "troll club":{
            "Name":"Troll Club",
            "Type":"Sword",
            "Equipable":True, 
            "Attack Modifier":30,
            "Wisdom Modifier":0,
            "Defence Modifier":0,
            "Dexterity Modifier":-5,
            "Sell Price":100},
    
    "demon armour":{
            "Name":"Demon Armour",
            "Type":"Armour",
            "Equipable":True, 
            "Attack Modifier":0,
            "Wisdom Modifier":10,
            "Defence Modifier":15,
            "Dexterity Modifier":10,
            "Sell Price":500},
    
    "demon sword":{
            "Name":"Demon Sword",
            "Type":"Sword",
            "Equipable":True, 
            "Attack Modifier":45,
            "Wisdom Modifier":10,
            "Defence Modifier":0,
            "Dexterity Modifier":5,
            "Sell Price":500},
    
    "demon shield":{
            "Name":"Demon Shield",
            "Type":"Shield",
            "Equipable":True, 
            "Attack Modifier":5,
            "Wisdom Modifier":10,
            "Defence Modifier":20,
            "Dexterity Modifier":0,
            "Sell Price":500},
    
    "rare herb":{
        "Name":"Rare Herb", 
        "Sell Price":60},

    "uncracked geode":{
        "Name":"Uncracked Geode", 
        "Sell Price":5}, 
    
    "quartz geode":{
        "Name":"Quartz Geode", 
        "Sell Price":25}, 
    
    "amethyst geode":{
        "Name":"Amethyst Geode", 
        "Sell Price":125},
    
    "demon head":{
        "Name":"Demon Head", 
        "Sell Price":1}

}