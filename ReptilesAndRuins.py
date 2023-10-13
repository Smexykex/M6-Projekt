import random

def playerAction(validInputs):
    while True:
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
    for count, item in enumerate(player["Inventory"]):
        print('{:^5}'.format(count+1), end=':')
        print('{:^10}'.format(item), end='')
        print()
    print('Coins:' + '{:^10}'.format(player["Coins"]))
    print()
    
def displayOptions(validInputs):
    print()
    for string in validInputs[0:-1]:
        print('{:^10}'.format(string), end='')
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
        if monster["Health"] <= 0:
            player["Coins"] += monster["Coins"]
            print("Victory!\n")
            return "victory"
        
        # Monster attacks
        attack(monster, player)
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
        action = playerAction(validInputs)
        match action:
            case "explore":
                # Pick a random monster from the monsterList and battles it
                # Stops the adventure if the player loses
                randomMonster = monsterList[random.randint(1, 3)]
                
                print(f'You encounter a {randomMonster["type"]}!\n')
                result = battle(randomMonster.copy())
                if result == "defeat":
                    print("Defeat! You return home\n")
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


def enterShop():
    print("Welcome to my shop!")
    
    validInputs = ["buy", "sell", "status", "inventory", "exit", "help"]
    while True:
        action = playerAction(validInputs)
        match action:
            case "buy":
                # Opens i list of items you can buy
                
            case "sell":
                # Opens i list of items you can sell
                
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
                
            case "exit":
                print("Goodbye!")
                return
            
            case "help":
                displayOptions(validInputs)
    

def game():
    print("Welcome to Replies and Ruins!")
    
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
        action = playerAction(validInputs)
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                adventure()
                player["Health"] = player["Max Health"]
            
            case "shop"
                enterShop()
                
            # Shows status of player
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
                
            case "exit":
                print("Goodbye!")
                return
            
            case "help":
                displayOptions(validInputs)
    