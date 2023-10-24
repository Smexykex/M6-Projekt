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
    "Potion":{
        "Name":"Potion", 
        "Usable":True, 
        "Cost":30, 
        "Sell Price":20},

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
        "Sell Price":150}, 
    
    "Rare Herb":{
        "Name":"Rare Herb", 
        "Sell Price":60},

    "Uncracked Geode":{
        "Name":"Uncracked Geode", 
        "Usable":True, 
        "Sell Price":5}, 
    
    "Quartz Geode":{
        "Name":"Quartz Geode", 
        "Sell Price":25}, 
    
    "Amethyst Geode":{
        "Name":"Amethyst Geode", 
        "Sell Price":125}, 

}