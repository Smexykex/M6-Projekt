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
from itemStats import useUncrackedGeode

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
        
        # Return the input in lower case if it's valid
        for validInput in validInputs:
            returnInput = playerInput.lower()
            if returnInput == validInput.lower():
                return returnInput
        
        cprint("Invalid input! write 'help' for help\n", tColor['fail'])


def displayStats():
    for stat, value in player.items():
        # We don't display some player data
        if stat in ["type", "Inventory", "Equipment", "Coins", "Heal Buff"]:
            continue
        
        print('{:<11}'.format(stat), end=':')
        print('{:>6}'.format(value), end='')
        print()
    print()


def displayInventory():
    print('Coins:' + '{:^20}'.format(player["Coins"]))
    
    for count, item in enumerate(player["Inventory"]):
        print('{:^5}'.format(count+1), end=':')
        print('{:^20}'.format(item["Name"]), end='')
        print()
    print()


def displayEquipment():
    for equipmentType, equipment in player["Equipment"].items():
        if equipment != None:
            print('{:^7}'.format(equipmentType), end=':')
            print('{:^20}'.format(equipment["Name"]), end='')
            print()
    print()


# Returns the index of a item in the inventory. Retruns None otherwise
def inventoryIndex(checkItem):
    for count, item in enumerate(player["Inventory"]):
        if item["Name"] == checkItem:
            return count
    

def displayOptions(validInputs):
    for string in validInputs[0:-1]:
        print(string.lower(), end='  ')
    print("\n")


def updateStats(equipmentType, sign = 1):
    player["Attack"] += player["Equipment"][equipmentType]["Attack Modifier"] * sign
    player["Wisdom"] += player["Equipment"][equipmentType]["Wisdom Modifier"] * sign
    player["Defence"] += player["Equipment"][equipmentType]["Defence Modifier"] * sign
    player["Dexterity"] += player["Equipment"][equipmentType]["Dexterity Modifier"] * sign
    

# Equips an equipment from the inventory. Puts equiped equipment in the inventory
def equipItem(equipment):
    for count, item in enumerate(player["Inventory"]):
        if equipment == item["Name"].lower():
            equipmentType = item["Type"] # Type of equipment the player is equiping
            # If the player haven't that type of equipment already equiped
            if player["Equipment"][equipmentType] == None:
                print(f'You equiped {equipment}\n')
                player["Equipment"][equipmentType] = item
                updateStats(equipmentType)
                player["Inventory"].pop(count)
                return
            
            # If the player have that type of equipment already equiped
            print(f'You replaced {player["Equipment"][equipmentType]["Name"]} with {item["Name"]}\n')
            player["Inventory"].append(player["Equipment"][equipmentType])
            updateStats(equipmentType, -1)
                        
            player["Equipment"][equipmentType] = item
            updateStats(equipmentType)
            player["Inventory"].pop(count)
            return

    
def equip():
    validInputs = []
    equipmentCount = 0
    
    for item in player["Inventory"]:
        if item["Equipable"]:
            print('{:<20}'.format(item["Name"]), end=" ")
            equipmentCount += 1
            validInputs.append(item["Name"])
    validInputs += ["exit", "help"]
    
    if equipmentCount == 0:
        cprint("You don't have anything to equip!\n", tColor['fail'])
        return
    
    print("\n")
                
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        match action:
            case "exit":
                return
            
            case "help":
                displayOptions(validInputs)
            
            case _:
                equipItem(action)
                return

    
def unequip():
    validInputs = []
    wornEquipmentCount = 0
    
    for equipmentType, equipment in player["Equipment"].items():
        if equipment != None:
            print('{:<20}'.format(equipmentType), end=" ")
            wornEquipmentCount += 1
            validInputs.append(equipmentType)
    validInputs += ["exit", "help"]
    
    if wornEquipmentCount == 0:
        cprint("You don't have anything to unequip!\n", tColor['fail'])
        return
    
    print("\n")
                
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            action = action.capitalize()
            print(f'You unequiped {player["Equipment"][action]["Name"]}\n')
            player["Inventory"].append(player["Equipment"][action])
            updateStats(action, -1)
            player["Equipment"][action] = None
            return
    
def attack(attacker, reciver):
    # Every point of dexterity increaces your dodge chance by 1%, starting at 0%
    hit = dice(100) > reciver["Dexterity"]
    if hit:
        # The attackers damage is between attack/2 and attack (attack/2 is rounded down)
        damage = random.randint(attacker["Attack"] // 2, attacker["Attack"])
        # Every point in defence reduces damage taken by 1 
        damageTaken = damage - reciver["Defence"]
        if damageTaken < 0:
            damageTaken = 0
        reciver["Health"] -= damageTaken
        print(f'{attacker["type"]} deals {damageTaken} damage to {reciver["type"]}!\n')
        
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!\n')
    

# Checks if the player can cast a spell.
# If they can, return True and subtract the mana cost from the players mana
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
        # Heal the player if they have casted regenerate
        if player["Heal Buff"] > 0:
            player["Health"] += 10
            print("Player is healed by regenerate\n")
            player["Heal Buff"] -= 1
            
        displayOptions(validInputs)
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
                if hasMana(30):
                    damage = 10 + player["Wisdom"] // 2
                    monster["Health"] -= damage
                    monster["Dexterity"] -= 5
                    print(f'Player casts frost blast on {monster["type"]} and deals {damage} damage')
                    print(f'{monster["type"]} now has {monster["Dexterity"]} dexterity\n')
                    return
            
            case "regenerate":
                if hasMana(80):
                    player["Heal Buff"] = 3 + player["Wisdom"] // 15
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


def gainXp(exp):
    player["Experience"] += exp
    if player["Experience"] >= player["Next level"]:
        print("Level up!\n")
        player["Experience"] -= player["Next level"]
        player["Level"] += 1
        player["Next level"] = round(player["Next level"] * 1.1)
        player["Max Health"] += 10
        
        statPoints = 5
        validInputs = ["Attack", "Wisdom", "Defence", "Dexterity"]
        print("---Select which stats you would like to increase---\n")
        while statPoints > 0:
            for stat, value in player.items():
                if stat in validInputs:
                    print('{:<10}'.format(stat), end=':')
                    print('{:>10}'.format(value), end='')
                    print()
            print()
            
            action = playerAction(validInputs, "misc")
            player[action.capitalize()] += 1
            statPoints -= 1


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
            cprint("Victory!", tColor['victory'])
            cprint(f"{tempMonster['Coins']} coins have been acquired!\n", tColor['addItem'])
            
            player["Coins"] += tempMonster["Coins"]
            sleep(0.3)
            chanceForDrop = dice(100)
            if chanceForDrop <= 100:
                print(f'{tempMonster["type"]} dropped {tempMonster["Drop"]["Name"]}\n')
                player["Inventory"].append(tempMonster["Drop"])
            
            sleep(0.3)
            gainXp(tempMonster["Experience gain"])
            return
        
        elif turn == "ran away":
            return "ran away"

        
        # Monster attacks
        attack(tempMonster, player)
        sleep(0.3)
        if player["Health"] <= 0:
            cprint("Defeat! You lost 50 coins!\n", tColor['fail'])
            player["Coins"] -= 50
            if player["Coins"] < 0:
                player["Coins"] = 0
                
            print("After managing to flee from combat, you return home\n")
            return "defeat"
        
        # The player gains 5 mana every turn plus 1 extra per 5 wisdom
        manaRegen = 5 + player["Wisdom"] // 5
        player["Mana"] += manaRegen
        if player["Mana"] > player["Max Mana"]:
            player["Mana"] = player["Max Mana"]


def foundHerb():
    sleep(1)
    cprint("You stumble upon a rare herb\n", tColor['misc'])
    validInputs = ["harvest", "return", "help"]
    while True:
        displayOptions(validInputs)
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
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        match action:
            case "take":
                player["Inventory"].append({"Name":"Uncracked Geode", "Sell Price":50})
                cprint("You pick up an uncracked geode\n", tColor['addItem'])
                break

            case "return":
                return False

            case "help":
                displayOptions(validInputs)
    return True


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
            pickedUp = foundGeode(chanceForGeode)
            if pickedUp is False:
                break
    sleep(1)
    cprint("You return back to the crossroads\n", tColor['misc'])


def adventure():
    cprint("Adventure awaits!", tColor['misc'])
    cprint("You find yourself at a crossroad\n", tColor['misc'])
    validInputs = ["wilds", "highlands", "mines", "status", "inventory", "home", "help"]
    if "Uncracked Geode" in player["Inventory"]:
        validInputs.insert(0, "crack geode")
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "where")
        match action:
            case "crack geode":
                useUncrackedGeode()
                if "Uncracked Geode" not in player["Inventory"]:
                    validInputs.remove("crack geode")

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
        
        displayOptions(validInputs)
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
        
        displayOptions(validInputs)
        action = playerAction(validInputs, "sell")
        if action == "exit":
            return
        
        elif action == "help":
            displayOptions(validInputs)
        
        else:
            for count, item in enumerate(player["Inventory"]):
                if action == item["Name"].lower():
                    print(f'You sold {item["Name"]} for {item["Sell Price"]} coins\n')
                    player["Coins"] += item["Sell Price"]
                    player["Inventory"].pop(count)
                    break
    #import sell value 


def enterShop(wares):
    cprint("Welcome to my shop!\n", tColor['dialogue'])
    
    validInputs = ["buy", "sell", "status", "inventory", "exit", "help"]
    while True:
        displayOptions(validInputs)
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
     "equip", "unequip", "main menu", "exit", "help"]
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                adventure()
                player["Health"] = player["Max Health"]
                player["Mana"] = player["Max Mana"]
            
            case "shop":
                wares = defaultStats.home_shop
                enterShop(wares)
                
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
            
            case "equip":
                equip()
            
            case "unequip":
                unequip()
            
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
        displayOptions(validInputs)
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