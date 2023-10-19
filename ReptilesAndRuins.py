"""
READ THIS TO GET LIBRARIES WORKING:
Using Thonny:
    open Tools -> Manage packages
    then search and install: 
        termcolor
        colorama

for Linux (hopfully similar with Windows), USING A DIFFERENT CODE EDITOR, NOT THONNY:
    go to project directory in terminal in code editor, and type:
        pip install -r requirements.txt
    if not using a virtual environment and on Windows, do this:
        py -m pip install -r requirements.txt
    You may need to install pip first.

To check colored text is working, uncomment the color test after import lines below.
If attribute 'bold' breaks program in Windows, just remove it from battle()

To note: extra print()s exists here and there, as I couln't figure out how to fit \n 
with color code in line above, without coloring both lines
Remember this when adding cprints with background colors and using \n.
Library still adds color to the line in empty lines

If you want to add more, check
https://pypi.org/project/termcolor/
"""
import random
# Add manual delay with sleep(), argument is ~seconds to wait
from time import sleep

from termcolor import colored, cprint
# colorama might be needed to make terminal color work on Windows, 
# termcolor is the actual code
import colorama
colorama.init()

# Colored text will only work with cprint(), 
# and you cannot do input(cprint("test", "red")) since cprint() always returns none.

# COLOR TEST
# cprint("test1234", "red")
# cprint("testbold", "green", attrs=["bold"])

# PUT THIS IN EXTERNAL FILE AND IMPORT
tColor = {
    'listSomething': 'cyan',
    'dialogue': 'magenta',
    'newEnemy': 'light_red',
    'victory': 'light_green',
    'fail': 'red',
    'addItem': 'yellow',
    'misc': 'light_blue'

}

def dice(upperNumber):
    return random.randint(1, upperNumber)


def playerAction(validInputs, doWhat):
    while True:
        match doWhat:
            case "buy":
                playerInput = input("What would you like to buy? ")
            case "sell":
                playerInput = input("What would you like to sell? ")
            case "where":
                playerInput = input("Where would you like to go? ")
            case _: # misc
                playerInput = input("What would you like to do? ")
        
        print()
        # Return the input if it's valid
        if playerInput in validInputs:
            return playerInput
        
        cprint("Invalid input! write 'help' for help\n", tColor['fail'])


def displayStats():
    for stat, value in player.items():
        if stat in ["type", "Inventory", "Coins"]:
            continue
        
        print('{:<10}'.format(stat), end=':')
        print('{:>10}'.format(value), end='')
        print()
    print()


def displayInventory():
    print('Coins:' + '{:^10}'.format(player["Coins"]))
    
    for count, item in enumerate(player["Inventory"]):
        print('{:^5}'.format(count+1), end=':')
        print('{:^15}'.format(item["Name"]), end='')
        print()
    print()


def inventoryIndex(checkItem):
    for count, item in enumerate(player["Inventory"]):
        if item["Name"] == checkItem:
            return count
    

def displayOptions(validInputs):
    for string in validInputs[0:-1]:
        print(string, end='  ')
    print("\n")


def equipItem():
    validInputs = []
    equipment_list = []
    for count, item in enumerate(player["Inventory"]):
        if item["Equipable"]:
            equipment_list.append(item)
            validInputs.append(item["Name"])
    validInputs += ["exit", "help"] 
                
    if len(equipment_list) == 0:
        print("You don't have anything to equip!")
        return
                
    while True:
        action = playerAction(validInputs, "misc")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            for count, item in enumerate(player["Inventory"]):
                if action == item["Name"]:
                    player["Attack"] += item["Attack Modifier"]
                    player["Defence"] += item["Defence Modifier"]
                    player["Inventory"].pop(count)
                    return
            
    
    
def attack(attacker, reciver):
    # Every point of dex increaces your dodge chance by 1%, starting at 0%
    hit = random.randint(1, 100) > reciver["Dexterity"]
    if hit:
        # Every point in defence reduces damage taken by 1
        damage = attacker["Attack"] - reciver["Defence"]
        reciver["Health"] -= damage
        print(f'{attacker["type"]} deals {damage} damage to {reciver["type"]}!\n')
        
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!\n')
        

def playerTurn(monster):
    validInputs = ["attack", "use potion", "inventory", "status", "run", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "attack":
                attack(player, monster)
                return

            case "use potion":
                if inventoryIndex("Potion") == None:
                    cprint("You don't have any potions!\n", tColor['fail'])
                    return
            
                print("You use a potion\n")
                player["Health"] += 50
                if player["Health"] > player["Max Health"]:
                    player["Health"] = player["Max Health"]
                                    
                player["Inventory"].pop(inventoryIndex("Potion"))
                return
            
            case "run":
                if dice(100) > player["Dexteriry"]:
                    cprint("You successfully run away", 'yellow')
                    return "ran away"
                
                cprint("You falied to run away!", tColor['fail'])
                
            case "inventory":
                displayInventory()
                    
            case "status":
                displayStats()
                    
                    
            case "help":
                displayOptions(validInputs)
    
    
# Returns "defeat" if the player lost the battle and "ran away" if they ran form the battle
def battle(monster):
    tempMonster = dict(monster)
    cprint(f"You encounter a {tempMonster['type']}!",tColor['newEnemy'], 'on_black', attrs=['bold'])
    print() #needs this instead of backslash n to cut background color off
    sleep(2)
    
    while True:
        # Player's turn
        turn = playerTurn(tempMonster)
        sleep(0.3)
        
        if tempMonster["Health"] <= 0:
            player["Coins"] += tempMonster["Coins"]
            cprint("Victory!", tColor['victory'])
            cprint(f"{tempMonster['Coins']} coins have been acquired!\n", tColor['addItem'])
            return
        
        elif turn == "ran away":
            return "ran away"

        
        # Monster attacks
        attack(monster, player)
        sleep(0.3)
        if player["Health"] <= 0:
            cprint("Defeat! After managing to flee from combat, you return home\n", tColor['fail'])
            return "defeat"


def foundHerb():
    sleep(1)
    cprint("You stumble upon a rare herb\n", tColor['misc'])
    validInputs = ["harvest", "return", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "harvest":
                chanceForHarvest = dice(100)
                if chanceForHarvest > 20:
                    player["Inventory"].append("Rare Herb")
                    cprint("Harvest successful!", tColor['victory'])
                    cprint( "Rare Herb added to inventory\n", tColor['addItem'])
                else:
                    cprint("Harvest unsuccessful, the herb was damaged beyond usability\n", tColor['fail'])
                break

            case "return":
                break
            
            case "help":
                displayOptions(validInputs)


def foundGeode(number):
    sleep(1)
    if number == 0:
        cprint("As you are walking, you hit your foot on an unusually light-weight rock.", tColor['misc'])
    else:
        cprint("Distracted by the geode you just found, you hit your other foot on another one..", tColor['misc'])
    validInputs = ["take", "return", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "take":
                player["Inventory"].append("Uncracked Geode")
                cprint("You pick up an uncracked geode\n", tColor['addItem'])
                break
            case "return":
                cprint("You return back to the crossroads\n", tColor['misc'])
                return 
            case "help":
                displayOptions(validInputs)


def newHighlands():
    chanceForEncounter = dice(100)
    chanceForHerb = dice(100)
    # Fail on both event rolls
    if not (chanceForEncounter > 30 or chanceForHerb > 50):
        sleep(1)
        cprint("After a long and uneventful trek, you haven't come across anything of value.", tColor['misc'])
        cprint("You decide to return back to the crossroads.\n", tColor['misc'])
        return

    if chanceForEncounter > 30:
        # Start encounter with wyvern
        result = battle(monsterList[1])
        if result in ["defeat", "ran away"]:
            return result

    if chanceForHerb > 50:
        foundHerb()
    sleep(1)
    cprint("You return back to the crossroads\n", tColor['misc'])


def newMines():
    chanceForEncounter = dice(100)
    if chanceForEncounter > 20:
        # Start encounter with golem or troll
        whichMonster = random.choice([2, 4])
        result = battle(monsterList[whichMonster])
        if result in ["defeat", "ran away"]:
            return result
        
    #maybe needs changing, to be able to do if != any of event rolls, 
    # return with special print message
    for chanceForGeode in range(2):
        roll = dice(100)
        if roll > 70:
            foundGeode(chanceForGeode)
    sleep(1)
    cprint("You return back to the crossroads\n", tColor['misc'])


def adventure():
    cprint("Adventure awaits!", tColor['misc'])
    cprint("You find yourself at a crossroad\n", tColor['misc'])
    #WOULD WANT TO PUT THIS IN A SEPARATE FILE LATER
    global monsterList
    monsterList = {
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

    validInputs = ["wilds", "highlands", "mines", "status", "inventory", "home", "help"]
    while True:
        action = playerAction(validInputs, "where")
        match action:
            case "wilds":
                # Pick a random monster from the monsterList and battles it
                # Stops the adventure if the player loses
                randomMonster = monsterList[random.randint(1, 3)]
                result = battle(randomMonster.copy())
                if result in ["defeat", "ran away"]:
                    return
            
            case "highlands":
                result = newHighlands()
                if result in ["defeat", "ran away"]:
                    return
            
            case "mines":
                result = newMines()
                if result in ["defeat", "ran away"]:
                    return
            
            case "status":
                displayStats()
                
            case "inventory":
                displayInventory()
                
            case "home":
                cprint("You return home\n", tColor['misc'])
                return
            
            case "help":
                displayOptions(validInputs)


def buyWares(wares):
    validInputs = []
    for item in wares.keys():
        validInputs.append(item)
    validInputs += ["exit", "help"]
    
    cprint(f"You have {player['Coins']} coins.", tColor['listSomething'])
    cprint("<Items in stock> ", tColor['misc'])
    for item in wares.values():
        print('{:<15}'.format(item["Name"]), end=':')
        print('{:>10}'.format(item["Cost"]), end='')
        print()
    print()
    
    while True:
        action = playerAction(validInputs, "buy")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            if wares[action]["Cost"] <= player["Coins"]:
                cprint(f'You bought {wares[action]["Name"]}\n', tColor['addItem'])
                player["Inventory"].append(wares[action])
                player["Coins"] -= wares[action]["Cost"]
            
            else:
                cprint("You don't have enough money!\n", tColor['fail'])


def sellWares():
    validInputs = []
    for item in player["Inventory"]:
        validInputs.append(item["Name"])
    validInputs += ["exit", "help"]
    
    print(f"You have {player['Coins']} coins.")
    print("<Items in inventory> ")
    for item in player["Inventory"]:
        print('{:<15}'.format(item["Name"]), end=':')
        print('{:>10}'.format(item["Sell Price"]), end='')
        print()
    print()
    
    while True:
        action = playerAction(validInputs, "sell")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            for count, item in enumerate(player["Inventory"]):
                if action == item["Name"]:
                    print(f'You sold {item["Name"]}\n')
                    player["Coins"] += item["Sell Price"]
                    player["Inventory"].pop(count)
                    break
    #make a check at some point to see if the chosen item/which items are sellableitems 
    #import sell value 


def enterShop(wares):
    cprint("Welcome to my shop!\n", tColor['dialogue'])
    
    validInputs = ["buy", "sell", "status", "inventory", "exit", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "buy":
                buyWares(wares)

            case "sell":
                sellWares()
                
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
                
            case "exit":
                cprint("Come again!\n", tColor['dialogue'])
                return
            
            case "help":
                displayOptions(validInputs)
    

def game():
    cprint("\nWelcome to Replies and Ruins!\n", 'light_green')
    print("type 'help' for a list of avalible commands!\n")
    
    # Players stats
    global player
    player = {
        "type":"Player",
        "Inventory":[],
        "Coins":200,
        "Max Health":150,
        "Health":150,
        "Attack":50,
        "Defence":25,
        "Dexterity":30
        }
    
    validInputs = ["adventure", "shop", "status", "inventory", "equip", "exit", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                adventure()
                player["Health"] = player["Max Health"]
            
            case "shop":
                wares = {
                    "Potion":{"Name":"Potion", "Cost":30, "Sell Price":20}, 
                    "Iron Sword":{"Name":"Iron Sword", "Equipable":True, "Attack Modifier":15, "Defence Modifier":0, "Cost":150, "Sell Price":75}, 
                    "Iron Shield":{"Name":"Iron Shield", "Equipable":True, "Attack Modifier":0, "Defence Modifier":5, "Cost":200, "Sell Price":100}, 
                    "Iron Armour":{"Name":"Iron Armour", "Equipable":True, "Attack Modifier":0, "Defence Modifier":10, "Cost":300, "Sell Price":150}
                    }
                enterShop(wares)
                
            # Shows status of player
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
            
            case "equip":
                equipItem()
                
            case "exit":
                cprint("Exited game", 'green')
                return
            
            case "help":
                displayOptions(validInputs)


game()