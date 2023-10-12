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
    hit = random.randint(1, 100) > reciver["dexterity"]
    if hit:
        # Every point in defence reduces damage taken by 1
        damage = attacker["attack"] - reciver["defence"]
        reciver["health"] -= damage
        print(f'{attacker["type"]} deals {damage} damage to {reciver["type"]}!\n')
        
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!\n')


# Returns "victory" if the playter won and "defeat" if they lost
def battle(monster):
    while True:
        # Player attacks
        attack(player, monster)
        if monster["health"] <= 0:
            print("Victory!\n")
            return "victory"
        
        # Monster attacks
        attack(monster, player)
        if player["health"] <= 0:
            return "defeat"
    
    
    
def adventure():
    monsterList = {
        1:{
            "type":"Wyvern",
            "health":150,
            "attack":35,
            "defence":15,
            "dexterity":50,
            },
        2:{
            "type":"Golem",
            "health":300,
            "attack":35,
            "defence":40,
            "dexterity":0,
            },
        3:{
            "type":"Dragon",
            "health":250,
            "attack":40,
            "defence":30,
            "dexterity":15,
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
        "maxHealth":150,
        "health":150,
        "attack":50,
        "defence":25,
        "dexterity":30,
        }
    
    validInputs = ["adventure", "status", "exit", "help"]
    while True:
        action = playerAction(validInputs)
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                print("\nAdventure awaits!\n")
                adventure()
                player["health"] = player["maxHealth"]
                
            # Shows status of player
            case "status":
                print(f'{player}\n')
                
            case "exit":
                print("\nGoodbye!")
                return
            
            case "help":
                displayOptions(validInputs)
    