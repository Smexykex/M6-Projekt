import random

def playerAction(validInputs):
    while True:
        playerInput = input("What would you like to do? ")
        if playerInput in validInputs:
            break
        
        print("Invalid input!")
    
    return playerInput

def attack(attacker, reciver):
    # Every point of dex increaces your dodge chance by 1%, starting at 0%
    hit = random.randint(1, 100) >= reciver["dexterity"]
    if hit:
        # Every point in defence reduces damage taken by 1
        damage = attacker["attack"] - reciver["defence"]
        reciver["hp"] -= damage
        
        print(f'{attacker["type"]} deals {damage} damage to {reciver["type"]}!')
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!')


def adventure():
    monster = {
        "type":"Dragon",
        "hp":150,
        "attack":45,
        "defence":30,
        "dexterity":10,
        }

    player = {
        "type":"Player",
        "hp":100,
        "attack":50,
        "defence":15,
        "dexterity":50,
        }
    
    # Battle starts!
    while True:
        # Player attacks
        attack(player, monster)
        if monster["hp"] <= 0:
            print("Victory!")
            break
        
        # Monster attacks
        attack(monster, player)
        if player["hp"] <= 0:
            print("Defeat!")
            break
    return
        
    
def game():
    print("Welcome to Replies and Ruins!")
    
    validInputs = ["adventure", "exit", "help"]
    while True:
        action = playerAction(validInputs)
        match action:
            case "adventure":
                adventure()
                
            case "exit":
                return
            
            case "help":
                print(validInputs)
    
    
    