import random
#manual delay can be added between print()s to help the player follow along
#call with sleep(), argument is ~seconds to wait
from time import sleep

def playerAction(validInputs, doWhat):
    while True:
        if doWhat == "buy":
            playerInput = input("What would you like to buy? ")
        elif doWhat == "sell":
            playerInput = input("What would you like to sell? ")
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
    while True:
        # Player attacks
        attack(player, monster)
        sleep(0.3)
        if monster["Health"] <= 0:
            player["Coins"] += monster["Coins"]
            print("Victory!\n")
            return "victory"
        
        # Monster attacks
        attack(monster, player)
        sleep(0.3)
        if player["Health"] <= 0:
            return "defeat"


def adventure():
    print("Adventure awaits!\n")
    
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

    validInputs = ["explore", "status", "inventory", "return", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            case "explore":
                # Pick a random monster from the monsterList and battles it
                # Stops the adventure if the player loses
                randomMonster = monsterList[random.randint(1, 3)]
                
                print(f'You encounter a {randomMonster["type"]}!\n')
                sleep(2)
                result = battle(randomMonster.copy())
                if result == "defeat":
                    print("Defeat! After managing to flee from combat, you return home\n")
                    return
                
            case "status":
                displayStats()
                
            case "inventory":
                displayInventory()
                
            case "return":
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