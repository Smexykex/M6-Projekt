import random
# Add manual delay with sleep(), argument is ~seconds to wait
from time import sleep

from termcolor import colored, cprint
# colorama might be needed to make terminal color work on Windows, 
# termcolor is the actual code
import colorama
colorama.init()

# Local files
import defaultStats

# Initialise color theme
tColor = defaultStats.default_color_theme

# Could be initialised locally if you want to pass
#  the dictionary between all of the relevant functions
global monsterList
monsterList = defaultStats.default_monsterList


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
        print('{:^20}'.format(count+1), end=':')
        print('{:^20}'.format(item["Name"]), end='')
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
    
    for equipment in equipment_list:
        print('{:^20}'.format(equipment["Name"]), end=" ")
    print("\n")
    
    if len(equipment_list) == 0:
        cprint("You don't have anything to equip!\n", tColor['fail'])
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
    # Every point of dexterity increaces your dodge chance by 1%, starting at 0%
    hit = dice(100) > reciver["Dexterity"]
    if hit:
        # Attackers damage is between attack/2 and attack (attack/2 is rounded down)
        damage = random.randint(round(attacker["Attack"] / 2), attacker["Attack"])
        # Every point in defence reduces damage taken by 1 
        damageTaken = damage - reciver["Defence"]
        if damageTaken < 0:
            damageTaken = 0
        reciver["Health"] -= damageTaken
        print(f'{attacker["type"]} deals {damageTaken} damage to {reciver["type"]}!\n')
        
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!\n')
    
    
def hasMana(manaCost):
    if player["Mana"] >= manaCost:
        player["Mana"] -= manaCost
        if player["Mana"] < 0:
            player["Mana"] = 0
        return True
    
    cprint("You don't have enough mana!\n", tColor['fail'])
    
    
def playerTurn(monster):
    validInputs = ["attack", "fire ball", "frost blast", "regenerate", "use potion", "inventory", "status", "run", "help"]
    while True:
        if healBuff > 0:
            player["Health"] += 10
            print(f'Player is healed by regenerate')
            healBuff -= 1
            
        action = playerAction(validInputs, "misc")
        match action:
            case "attack":
                attack(player, monster)
                return
            
            case "fire ball":
                if hasMana(45):
                    damage = 15 + player["Wisdom"]
                    monster["Health"] -= damage
                    print(f'Player casts fire ball on {monster["type"]} and deals {damage} damage\n')
                    return
            
            case "frost blast":
                if hasMana(35):
                    damage = 10 + round(player["Wisdom"]/2)
                    monster["Health"] -= damage
                    monster["Dexterity"] -= 5
                    print(f'Player casts frost blast on {monster["type"]} and deals {damage} damage')
                    print(f'{monster["type"]} now has {monster["Dexterity"]} dexterity\n')
                    return
            
            case "regenerate":
                if hasMana(80):
                    healBuff = 4
                    print("Player casts regenerate\n")
                    return

            case "use potion":
                if inventoryIndex("Potion") != None:
                    print("You use a potion\n")
                    player["Health"] += 50
                    if player["Health"] > player["Max Health"]:
                        player["Health"] = player["Max Health"]
                        
                    player["Inventory"].pop(inventoryIndex("Potion"))
                    return
                
                else:
                    cprint("You don't have any potions!\n", tColor['fail'])
                    
            
                print("You use a potion\n")
                player["Health"] += 50
                if player["Health"] > player["Max Health"]:
                    player["Health"] = player["Max Health"]
                                    
                player["Inventory"].pop(inventoryIndex("Potion"))
                return
            
            case "run":
                if dice(100) < player["Dexterity"]:
                    cprint("You successfully run away\n", 'yellow')
                    return "ran away"
                
                cprint("You failed to run away!\n", tColor['fail'])
                return
                
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
    
    healBuff = 0
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
        attack(tempMonster, player)
        sleep(0.3)
        if player["Health"] <= 0:
            cprint("Defeat! After managing to flee from combat, you return home\n", tColor['fail'])
            return "defeat"
        
        if player["Mana"] >= 90:
            player["Mana"] = 100
        
        else:
            manaRegen = 7 + round(player["Wisdom"] / 10)
            player["Mana"] += manaRegen


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
                    player["Inventory"].append({"Name":"Rare Herb", "Sell Price":50})
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
                player["Inventory"].append({"Name":"Uncracked Geode", "Sell Price":50})
                cprint("You pick up an uncracked geode\n", tColor['addItem'])
                break

            case "return":
                #cprint("You return back to the crossroads\n", tColor['misc'])
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
        if result == "defeat":
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
        if result == "defeat":
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
                cprint("You return home\n", tColor['misc'])
                return
            
            case "help":
                displayOptions(validInputs)


def buyWares(wares):
    validInputs = []
    for item in wares.keys():
        validInputs.append(item)
    validInputs += ["exit", "help"]
    
    while True:
        cprint(f"You have {player['Coins']} coins.", tColor['listSomething'])
        cprint("<Items in stock> ", tColor['listSomething'])
        for item in wares.values():
            print('{:<15}'.format(item["Name"]), end=':')
            print('{:>10}'.format(item["Cost"]), end='')
            print()
        print()
        
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
    
    while True:
        cprint(f"You have {player['Coins']} coins.", tColor['listSomething'])
        cprint("<Items in inventory> ", tColor['listSomething'])
        for item in player["Inventory"]:
            print('{:<15}'.format(item["Name"]), end=':')
            print('{:>10}'.format(item["Sell Price"]), end='')
            print()
        print()
        
        action = playerAction(validInputs, "sell")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            for count, item in enumerate(player["Inventory"]):
                if action == item["Name"]:
                    print(f'You sold {item["Name"]} for {item["Sell Price"]} coins\n')
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
    # Initiate Player stats
    global player
    player = defaultStats.default_human
    cprint("---Game initialised---\n", 'light_green', attrs=["bold"])
    
    validInputs = ["adventure", "shop", "status", "inventory",
     "equip", "main menu", "exit", "help"]
    while True:
        action = playerAction(validInputs, "misc")
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                adventure()
                player["Health"] = player["Max Health"]
            
            case "shop":
                wares = defaultStats.home_shop
                enterShop(wares)
                
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
            
            case "equip":
                equipItem()
            
            case "main menu":
                cprint("Exited to main menu", 'green')
                return False
            
            case "exit":
                cprint("Exited game", 'green')
                return True
            
            case "help":
                displayOptions(validInputs)


def changeTheme():
    global tColor
    validInputs = ["default", "alternate", "back", "help"]
    cprint("Available themes: ", tColor['misc'])
    displayOptions(validInputs)
    while True:
        menuChoice = playerAction(validInputs, tColor['misc'])
        match menuChoice:
            case "default":
                tColor = defaultStats.default_color_theme
                cprint("Color theme set to default", tColor['misc'])
                sleep(1)
                cprint("Returned to main menu", tColor['misc'])
                return

            case "alternate":
                tColor = defaultStats.alt1_color_theme
                cprint("Color theme set to alternate", tColor['misc'])
                sleep(1)
                cprint("Returned to main menu", tColor['misc'])
                return
            
            case "back":
                cprint("Returned to main menu", tColor['misc'])
                return

            case "help":
                displayOptions(validInputs)

 
def main():
    cprint("\nWelcome to Replies and Ruins!\n", 'light_green')
    print("You are in the main menu")
    print("type 'help' for a list of avalible commands!\n")
    validInputs = ["start", "change theme", "exit", "help"]
    fullExit = False
    while True:
        menuChoice = playerAction(validInputs, 'misc')
        match menuChoice:
            case "start":
                fullExit = game()
            
            case "change theme":
                changeTheme()
            
            case "exit":
                cprint("Exited game", 'green')
                return
            
            case "help":
                displayOptions(validInputs)
            
        if fullExit is True:
            break


if __name__ == "__main__":
    main()