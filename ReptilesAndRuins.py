import random
#manual delay can be added between print()s to help the player follow along
#call with sleep(), argument is ~seconds to wait
from time import sleep

def roll100():
    return random.randint(1, 100)


def playerAction(validInputs, doWhat):
    while True:
        if doWhat == "buy":
            playerInput = input("What would you like to buy? ")
        elif doWhat == "sell":
            playerInput = input("What would you like to sell? ")
        elif doWhat == "where":
            playerInput = input("Where would you like to go? ")
        else: #misc
            playerInput = input("What would you like to do? ")
        
        print()
        # Return the input if it's valid
        if playerInput in validInputs:
            return playerInput
        
        print("Invalid input!\n")


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



def displayOptions(validInputs):
    for string in validInputs[0:-1]:
        print(string, end='  ')
    print("\n")
    

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


# Returns "victory" if the playter won and "defeat" if they lost
def battle(monster):
    tempMonster = dict(monster)
    print(f'You encounter a {tempMonster["type"]}!\n')
    sleep(2)
    while True:
        # Player attacks
        attack(player, tempMonster)
        sleep(0.3)
        if tempMonster["Health"] <= 0:
            player["Coins"] += tempMonster["Coins"]
            print("Victory!")
            print(f"{tempMonster['Coins']} coins have been acquired!\n")
            return "victory"
        
        # Monster attacks
        attack(monster, player)
        sleep(0.3)
        if player["Health"] <= 0:
            print("Defeat! After managing to flee from combat, you return home\n")
            return "defeat"


def newHighlands():
    chanceForEncounter = roll100()
    chanceForHerb = roll100()
    if not (chanceForEncounter > 30 or chanceForHerb > 50):
        sleep(1)
        print("After a long and uneventful trek, you haven't come across anything of value.")
        print("You decide to return back to the crossroads.\n")
        return

    if chanceForEncounter > 30:
        #start encounter with wyvern
        result = battle(monsterList[1])
        if result == "defeat":
            return result

    if chanceForHerb > 50:
        validInputs = ["harvest", "return", "help"]
        sleep(1)
        print("You stumble upon a rare herb\n")
        while True:
            action = playerAction(validInputs, "misc")
            match action:
                case "harvest":
                    chanceForHarvest = roll100()
                    if chanceForHarvest > 20:
                        player["Inventory"].append("Rare Herb")
                        print("Harvest sucessful, added Herb to inventory\n")
                    else:
                        print("Harvest unsuccessful, the herb was damaged beyond usability\n")
                    break

                case "return":
                    break
                
                case "help":
                    displayOptions(validInputs)
    sleep(1)
    print("You return back to the crossroads\n")
    return 


#def newMines():
    #TBD


def adventure():
    print("Adventure awaits!")
    print("You find yourself at a crossroad\n")
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
            }
        }

    validInputs = ["wilds", "highlands", "status", "inventory", "home", "help"]
    while True:
        action = playerAction(validInputs, "where")
        match action:
            case "wilds":
                # Pick a random monster from the monsterList and battles it
                # Stops the adventure if the player loses
                randomMonster = monsterList[random.randint(1, 3)]
                result = battle(randomMonster.copy())
                if result == "defeat":
                    return
            
            case "highlands":
                result = newHighlands()
                if result == "defeat":
                    return
            
            case "mines":
                result = newMines()
                if result == "defeat":
                    return
            
            case "status":
                displayStats()
                
            case "inventory":
                displayInventory()
                
            case "home":
                print("You return home\n")
                return
            
            case "help":
                displayOptions(validInputs)


def buyWares(wares):
    validInputs = []
    for item in wares.keys():
        validInputs.append(item)
    validInputs += ["exit", "help"]
    
    print(f"You have {player['Coins']} coins.")
    print("<Items in stock> ")
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
                print(f'You bought {wares[action]["Name"]}\n')
                player["Inventory"].append(wares[action])
                player["Coins"] -= wares[action]["Cost"]
            
            else:
                print("You don't have enough money!\n")


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
    #make a check at some point to see if the chosen item/which items are sellableitems 
    #import sell value 


def enterShop(wares):
    print("Welcome to my shop!\n")
    
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
                print("Come again!\n")
                return
            
            case "help":
                displayOptions(validInputs)
    

def game():
    print("Welcome to Replies and Ruins!\n")
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
    
    validInputs = ["adventure", "shop", "status", "inventory", "exit", "help"]
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
                    "Iron Sword":{"Name":"Iron Sword", "Cost":150, "Sell Price":75}, 
                    "Iron Shield":{"Name":"Iron Shield", "Cost":200, "Sell Price":100}, 
                    "Iron Armour":{"Name":"Iron Armour", "Cost":300, "Sell Price":150}
                    }
                enterShop(wares)
                
            # Shows status of player
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
                
            case "exit":
                print("Exited game")
                return
            
            case "help":
                displayOptions(validInputs)


game()