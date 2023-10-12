import random

def playerAction(validInputs):
    while True:
        playerInput = input("What would you like to do? ")
        # Return the input if it's valid
        if playerInput in validInputs:
            return playerInput
        
        print("Invalid input!")


def displayStats():
    for stat, value in player.items():
        if stat == "type":
            continue
        print('{:<10}'.format(stat), end=':')
        print('{:>10}'.format(value), end='')
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
            print("Victory!\n")
            return "victory"
        
        # Monster attacks
        attack(monster, player)
        if player["Health"] <= 0:
            return "defeat"
    
    
    
def adventure():
    monsterList = {
        1:{
            "type":"Wyvern",
            "Health":150,
            "Attack":35,
            "Defence":15,
            "Dexterity":50,
            },
        2:{
            "type":"Golem",
            "Health":300,
            "Attack":35,
            "Defence":40,
            "Dexterity":0,
            },
        3:{
            "type":"Dragon",
            "Health":250,
            "Attack":40,
            "Defence":30,
            "Dexterity":15,
            }
        }

    validInputs = ["explore", "status", "return", "help"]
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
                
            # Shows status of player
            case "status":
                print(f'\n{player}\n')
                
            case "return":
                print("You return home\n")
                return
            
            case "help":
                displayOptions(validInputs)
        
    
def game():
    print("Welcome to Replies and Ruins!")
    
    # Players stats
    global player
    player = {
        "type":"Player",
        "Max Health":150,
        "Health":150,
        "Attack":50,
        "Defence":25,
        "Dexterity":30,
        }
    
    validInputs = ["adventure", "status", "exit", "help"]
    while True:
        action = playerAction(validInputs)
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                print("\nAdventure awaits!\n")
                adventure()
                player["Health"] = player["Max Health"]
                
            # Shows status of player
            case "status":
                displayStats()
                
            case "exit":
                print("\nGoodbye!")
                return
            
            case "help":
                displayOptions(validInputs)
    