import random
#manual delay can be added between print()s to help the player follow along
#call with sleep(), argument is ~seconds to wait
from time import sleep

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
            case _: #misc
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
        print('{:^10}'.format(item), end='')
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


def foundHerb():
    sleep(1)
    print("You stumble upon a rare herb\n")
    validInputs = ["harvest", "return", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "harvest":
                chanceForHarvest = dice(100)
                if chanceForHarvest > 20:
                    player["Inventory"].append("Rare Herb")
                    print("Harvest successful, added Herb to inventory\n")
                else:
                    print("Harvest unsuccessful, the herb was damaged beyond usability\n")
                break

            case "return":
                break
            
            case "help":
                displayOptions(validInputs)


def foundGeode(number):
    sleep(1)
    if number == 0:
        print("As you are walking, you hit your foot on an unusually light-weight rock.")
    else:
        print("Distracted by the geode you just found, you hit you other foot on another one..")
    validInputs = ["take", "return", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "take":
                player["Inventory"].append("Uncracked Geode")
                print("You pick up an uncracked geode\n")
                break
            case "return":
                print("You return back to the crossroads\n")
                return 
            case "help":
                displayOptions(validInputs)


def newHighlands():
    chanceForEncounter = dice(100)
    chanceForHerb = dice(100)
    #fail on both event rolls
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
        foundHerb()
    sleep(1)
    print("You return back to the crossroads\n")


def newMines():
    chanceForEncounter = dice(100)
    if chanceForEncounter > 20:
        #start encounter with golem or troll
        whichMonster = random.choice([2, 4])
        result = battle(monsterList[whichMonster])
        if result == "defeat":
            return result
        
    #maybe needs changing, to be able to do if != any of event rolls, 
    # return with special print message
    for chanceForGeode in range(2):
        roll = dice(100)
        if roll > 70:
            foundGeode(chanceForGeode)
    sleep(1)
    print("You return back to the crossroads\n")


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
    for item in wares:
        validInputs.append(item)
    validInputs += ["exit", "help"]
    
    print(f"You have {player['Coins']} coins.")
    print("<Items in stock> ")
    for item in wares:
        print('{:<15}'.format(f"{item}) {wares[item][0]}"), end=':')
        print('{:>10}'.format(wares[item][1]), end='')
        print()
    print()
    
    while True:
        action = playerAction(validInputs, "buy")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            if wares[action][1] <= player["Coins"]:
                print(f'You bought {wares[action][0]}\n')
                player["Inventory"].append(wares[action][0])
                player["Coins"] -= wares[action][1]
            
            else:
                print("You don't have enough money!\n")


#def sellWares(inventory):
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

            #case "sell":
                #sellWares(inventory)
                
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
        "Inventory":["Potion"],
        "Coins":100,
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
                    "1":("Potion", 30), 
                    "2":("Iron Sword", 150), 
                    "3":("Iron Shield", 200), 
                    "4":("Iron Armour", 300)}
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