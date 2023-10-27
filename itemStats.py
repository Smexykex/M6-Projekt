# Main file will import this to get buy/sell value, 
# info, interaction with specific item, stats for chosen item, etc.

# Structure:
# Use specific item function, eg function for cracking geode
# Dictionary of item statistics, 

def usePotion():
    #abstract from main file?
    return


def useUncrackedGeode():
    cprint("You hit the uncracked geode against a nearby bolder.", "misc")
    player["Inventory"].pop(inventoryIndex("Uncracked Geode"))
    roll = dice(100)
    if roll > 80:
        cprint("It opens up and reveals a shimmering purple interior", 'misc')
        player["Inventory"].append({thing["Amethyst Geode"]})
        cprint("You pick up an Amethyst Geode\n", tColor['addItem'])
    else:
        cprint("It opens up and reveals its interior glimmering with white quartz", 'misc')
        player["Inventory"].append({thing["Quartz Geode"]})
        cprint("You pick up a Quartz Geode\n", tColor['addItem'])
    return


# Using item as dict name might screw with stuff in main file
# Change how it works if you have a better idea
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
            "Attack Modifier":35,
            "Wisdom Modifier":0,
            "Defence Modifier":0,
            "Dexterity Modifier":-5,
            "Sell Price":200},
    
    "rare herb":{
        "Name":"Rare Herb", 
        "Sell Price":60},

    "uncracked geode":{
        "Name":"Uncracked Geode", 
        "Sell Price":5}, 
    
    "quartz qeode":{
        "Name":"Quartz Geode", 
        "Sell Price":25}, 
    
    "amethyst geode":{
        "Name":"Amethyst Geode", 
        "Sell Price":125}, 

}