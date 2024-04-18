import random
import json
# Add manual delay with sleep(), argument is ~seconds to wait
from time import sleep

from termcolor import colored, cprint
# colorama might be needed to make terminal color work on Windows, 
# termcolor is the actual code
import colorama
colorama.init()

# Local files
import defaultStats
import itemStats

# Initialise color theme
tColor = defaultStats.default_color_theme

global monsterList
monsterList = defaultStats.default_monsterList


# Returns a number between 1 and a given number
def dice(upperNumber):
    return random.randint(1, upperNumber)


# Returns the players action (a string) if the action is in the given list of valid actions
def playerAction(validInputs, doWhat):
    while True:
        match doWhat:
            case "buy":
                playerInput = input("What would you like to buy? ")
            case "sell":
                playerInput = input("What would you like to sell? ")
            case "where":
                playerInput = input("Where would you like to go? ")
            case "attribute":
                playerInput = input("What attribute would you like to increase? ")
            case _: # misc
                playerInput = input("What would you like to do? ")
        print()
        
        # Return the input in lower case if it's valid
        for validInput in validInputs:
            returnInput = playerInput.lower()
            if returnInput == validInput.lower():
                return returnInput
        
        cprint("Invalid input! Try again\n", tColor['fail'])


# Displays the players stats
def displayStats():
    for stat, value in player.items():
        # We don't display some player data
        if stat in ["type", "Inventory", "Equipment", "Coins", "Heal Buff"]:
            continue
        
        print('{:<11}'.format(stat), end=':')
        print('{:>6}'.format(value), end='')
        print()
    print()


# Displays the players inventory
def displayInventory():
    print('Coins:' + '{:^20}'.format(player["Coins"]))
    
    for count, item in enumerate(player["Inventory"]):
        print('{:^5}'.format(count+1), end=':')
        print('{:^20}'.format(item["Name"]), end='')
        print()
    print()


# Displays the players equipment
def displayEquipment():
    for equipmentType, equipment in player["Equipment"].items():
        if equipment != None:
            print('{:^7}'.format(equipmentType), end=':')
            print('{:^20}'.format(equipment["Name"]), end='')
            print()
    print()
    

# Displays the players current valid inputs
def displayOptions(validInputs):
    for string in validInputs:
        cprint(string.lower(), tColor['choices'], end='  ')
    print("\n")


# An attack against an opponent
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
        print(f'{attacker["type"]} deals {damageTaken} damage to {reciver["type"]}\n')
        
    else:
        print(f'{attacker["type"]} missed {reciver["type"]}!\n')
        

# The players turn in a battle
def playerTurn(monster, canRun = True):
    validInputs = ["attack", "fire ball", "frost blast", "regenerate", "use potion", "inventory", "status"]
    if canRun:
        validInputs += ["run"]
    
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
                if itemStats.castFireBall(player, monster) == True:
                    return
            
                cprint("You don't have enough mana!\n", tColor['fail'])
                
            case "frost blast":
                if itemStats.castFrostBlast(player, monster) == True:
                    return
                
                cprint("You don't have enough mana!\n", tColor['fail'])
                
            case "regenerate":
                if itemStats.castRegenerate(player) == True:
                    return
                
                cprint("You don't have enough mana!\n", tColor['fail'])

            case "use potion":
                if itemStats.usePotion(player) == True:
                    return
            
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


# What happens when the player gains experience
def gainXp(exp):
    player["Experience"] += exp
    
    # If the player levels up
    if player["Experience"] >= player["Next level"]:
        print("Level up!\n")
        player["Experience"] -= player["Next level"]
        player["Max Health"] += 10
        player["Level"] += 1
        # The next level requires 10% more experience then the last
        player["Next level"] = round(player["Next level"] * 1.1)
        
        # Selection of which attributes to increase
        statPoints = 5
        validInputs = ["1", "2", "3", "4"]
        attributes = ["Attack", "Wisdom", "Defence", "Dexterity"]
        while statPoints > 0:
            cprint("<Attributes you can increase>\n", tColor['listSomething'])
            for count, stat in enumerate(player.keys()):
                if stat in attributes:
                    print('{:<13}'.format(f'{count-10}) {stat}'), end=':')
                    print('{:>6}'.format(player[stat]), end='')
                    print()
            print()
            
            action = playerAction(validInputs, "attribute")
            player[attributes[int(action) - 1]] += 1
            statPoints -= 1


# Starts battle against a monster
# Returns "defeat" if the player lost the battle and "ran away" if they ran from the battle
def battle(monster, canRun = True):
    tempMonster = dict(monster) # Copy of monster
    cprint(f"You encounter a {tempMonster['type']}!",tColor['newEnemy'], 'on_black', attrs=['bold'])
    print() # Needs this instead of backslash n to cut background color off
    sleep(2)
    
    while True:
        print("-"*30)
        print(f'Player -- Health: [{player["Health"]}/{player["Max Health"]}] Mana: [{player["Mana"]}/{player["Max Mana"]}]')
        print(f'Monster -- Health: [{tempMonster["Health"]}/{tempMonster["Max Health"]}]\n')
        # Player's turn
        turn = playerTurn(tempMonster, canRun)
        sleep(0.3)
        
        # The battle is won if the monster has less than 0 health 
        if tempMonster["Health"] <= 0:
            cprint("Victory!", tColor['victory'])
            cprint(f"{tempMonster['Coins']} coins have been acquired\n", tColor['addItem'])
            
            player["Coins"] += tempMonster["Coins"]
            sleep(0.3)
            # 20% chance of getting a drop from the monster
            chanceForDrop = dice(100)
            if chanceForDrop <= tempMonster["Drop Rate"]:
                print(f'{tempMonster["type"]} dropped {tempMonster["Drop"]["Name"]}\n')
                player["Inventory"].append(tempMonster["Drop"])
                
            sleep(0.3)
            
            # Gain experience
            gainXp(tempMonster["Experience gain"])
            return "victory"
        
        elif turn == "ran away":
            return "ran away"

        
        # Monster attacks
        attack(tempMonster, player)
        sleep(0.3)
        
        # The battle is lost if the player has less than 0 health
        if player["Health"] <= 0:
            cprint("Defeat! You lost 50 coins\n", tColor['fail'])
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


# Boss battle
def bossBattle():
    result = battle(dict(monsterList[5]), False) # Can't run from the battle
    if result == "defeat":
        return "defeat"
    
    sleep(0.3)
    validInputs = ["demon sword", "demon shield", "demon armour"]
    
    cprint("The demon's head pulsates with magic. You get the feeling you can change it's shape to suit your needs\n", tColor['lore'])
    cprint("<Equipment you can make>\n", tColor['listSomething'])
    for equipment in validInputs:
        print('{:<13}'.format(f'{itemStats.thing[equipment]["Name"]}'), end=' ')
    print("\n")
    
    displayOptions(validInputs)
    action = playerAction(validInputs, "misc")
    # Removes the demon head from the players inventory and adds the crafted equipment
    print(f'You created {itemStats.thing[action]["Name"]}\n')
    player["Inventory"].pop(itemStats.inventoryIndex(player, "Demon Head"))
    player["Inventory"].append(itemStats.thing[action])

    
# When the player finds a herb
def foundHerb():
    sleep(1)
    cprint("You stumble upon a rare herb\n", tColor['misc'])
    validInputs = ["harvest", "return"]
    displayOptions(validInputs)
    action = playerAction(validInputs, "misc")
    match action:
        case "harvest":
            chanceForHarvest = dice(100)
            if chanceForHarvest > 20:
                player["Inventory"].append(itemStats.thing["rare herb"])
                cprint("Harvest successful!", tColor['victory'])
                cprint( "Rare Herb added to inventory\n", tColor['addItem'])
            else:
                cprint("Harvest unsuccessful, the herb was damaged beyond usability\n", tColor['fail'])
    return


# When the player finds a geode
def foundGeode(number):
    sleep(1)
    if number == 0:
        cprint("As you are walking, you hit your foot on an unusually light-weight rock.", tColor['misc'])
    else:
        cprint("Distracted by the geode you just found, you hit your other foot on another one..", tColor['misc'])
    validInputs = ["take", "return"]
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        match action:
            case "take":
                player["Inventory"].append(itemStats.thing["uncracked geode"])
                cprint("You pick up an uncracked geode\n", tColor['addItem'])
                break

            case "return":
                return False
    return True


# Enter highlands
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


# Enter mines
def newMines():
    noEvent = True
    chanceForEncounter = dice(100)
    if chanceForEncounter > 20:
        noEvent = False
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
            noEvent = False
            pickedUp = foundGeode(chanceForGeode)
            if pickedUp is False:
                break
    
    if noEvent is True:
        cprint("The journey through the abandoned mines is uneventful...", tColor['misc'])
    sleep(1)
    cprint("You return back to the crossroads\n", tColor['misc'])


# Opens a uncracked geode from the players inventory
def useUncrackedGeode(player):
    player["Inventory"].remove(itemStats.thing["uncracked geode"])
    cprint("You hit the uncracked geode against a nearby boulder.", tColor["misc"])
    sleep(0.5)
    roll = dice(100)
    if roll > 80:
        player["Inventory"].append(itemStats.thing["amethyst geode"])
        cprint("It opens up and reveals a shimmering purple interior", tColor['misc'])
        cprint("You pick up an Amethyst Geode\n", tColor['addItem'])
    else:
        player["Inventory"].append(itemStats.thing["quartz geode"])
        cprint("It opens up and reveals its interior glimmering with white quartz", tColor['misc'])
        cprint("You pick up a Quartz Geode\n", tColor['addItem'])
    return


# Restores the player's health and mana
def restoreStats():
    player["Health"] = player["Max Health"]
    player["Mana"] = player["Max Mana"]
    

# Starts an adventure
def adventure():
    cprint("Adventure awaits!", tColor['misc'])
    cprint("You find yourself at a crossroad\n", tColor['misc'])
    validInputs = ["wilds", "highlands", "mines", "boss", "status", "inventory",
    "equipment", "equip", "unequip", "home"]
    
    while True:
        if "crack geode" not in validInputs:
            if itemStats.thing["uncracked geode"] in player["Inventory"]:
                validInputs.insert(0, "crack geode")
        displayOptions(validInputs)
        action = playerAction(validInputs, "where")
        match action:
            case "crack geode":
                useUncrackedGeode(player)
                if itemStats.thing["uncracked geode"] not in player["Inventory"]:
                    validInputs.remove("crack geode")

            case "wilds":
                # Pick a random monster from the monsterList and battles it
                # Stops the adventure if the player loses
                randomMonster = monsterList[random.randint(1, 3)]
                result = battle(randomMonster.copy())
                restoreStats()
                if result == "defeat":
                    return
            
            case "highlands":
                result = newHighlands()
                restoreStats()
                if result == "defeat":
                    return
            
            case "mines":
                result = newMines()
                restoreStats()
                if result == "defeat":
                    return
            
            case "boss":
                bossBattle()
                return
            
            case "status":
                displayStats()
                
            case "inventory":
                displayInventory()
            
            case "equipment":
                displayEquipment()
            
            case "equip":
                equip()
            
            case "unequip":
                unequip()
                
            case "home":
                cprint("You return home\n", tColor['misc'])
                return


# Updates the stats of the player when they remove equipment
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
            try:
                player["Equipment"][equipmentType]
                
            # If the player haven't that type of equipment already equiped
            except:
                print(f'You equiped {equipment}\n')
                player["Equipment"][equipmentType] = item
                updateStats(equipmentType)
                player["Inventory"].pop(count)
                return
            
            # If the player have that type of equipment already equiped
            else:
                print(f'You replaced {player["Equipment"][equipmentType]["Name"]} with {item["Name"]}\n')
                player["Inventory"].append(player["Equipment"][equipmentType])
                updateStats(equipmentType, -1)
                            
                player["Equipment"][equipmentType] = item
                updateStats(equipmentType)
                player["Inventory"].pop(count)
                return


# Equip/Swap equipment
def equip():
    validInputs = []
    equipmentCount = 0
    
    for item in player["Inventory"]:
        if item["Equipable"]:
            print('{:<20}'.format(item["Name"]), end=" ")
            equipmentCount += 1
            validInputs.append(item["Name"])
    validInputs += ["exit"]
    
    if equipmentCount == 0:
        cprint("You don't have anything to equip!\n", tColor['fail'])
        return
    
    print("\n")
    
    displayOptions(validInputs)
    action = playerAction(validInputs, "misc")
    match action:
        case "exit":
            return
        
        case _:
            equipItem(action)
            return


# Remove equipment
def unequip():
    validInputs = []
    wornEquipmentCount = 0
    
    for equipmentType, equipment in player["Equipment"].items():
        print('{:<20}'.format(equipmentType), end=" ")
        wornEquipmentCount += 1
        validInputs.append(equipmentType)
    validInputs += ["exit"]
    
    if wornEquipmentCount == 0:
        cprint("You don't have anything to unequip!\n", tColor['fail'])
        return
    
    print("\n")
                
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        if action == "exit":
            return
        
        else:
            action = action.capitalize()
            print(f'You unequiped {player["Equipment"][action]["Name"]}\n')
            player["Inventory"].append(player["Equipment"][action])
            updateStats(action, -1)
            player["Equipment"].pop(action)
            return


# Buy wares from shop
def buyWares(wares):
    validInputs = []
    for item in wares.keys():
        validInputs.append(item)
    validInputs += ["exit"]
    
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
        
        else:
            if wares[action]["Cost"] <= player["Coins"]:
                cprint(f'You bought {wares[action]["Name"]}\n', tColor['addItem'])
                player["Inventory"].append(wares[action])
                player["Coins"] -= wares[action]["Cost"]
            
            else:
                cprint("You don't have enough money!\n", tColor['fail'])


# Sell wares in shop
def sellWares():
    validInputs = []
    for item in player["Inventory"]:
        validInputs.append(item["Name"])
    validInputs += ["exit"]
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
        
        for count, item in enumerate(player["Inventory"]):
            if action == item["Name"].lower():
                print(f'You sold {item["Name"]} for {item["Sell Price"]} coins\n')
                player["Coins"] += item["Sell Price"]
                player["Inventory"].pop(count)
                validInputs.remove(item["Name"])
                break
    #import sell value 


# Enters shop
def enterShop(wares):
    # Weird symbols makes text cursive
    cprint("\x1B[3m Welcome to my shop! \x1B[0m \n", tColor['dialogue'])
    
    validInputs = ["buy", "sell", "status", "inventory", "equipment", "equip", "unequip", "exit"]
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
            
            case "equipment":
                displayEquipment()
            
            case "equip":
                equip()
            
            case "unequip":
                unequip()
                
            case "exit":
                cprint("\x1B[3m Come again! \x1B[0m \n", tColor['dialogue'])
                return


# Starts the game
def game():    
    cprint("---Game initialised---\n", 'light_green', attrs=["bold"])
    
    validInputs = ["adventure", "shop", "status", "inventory", "equipment",
    "equip", "unequip", "main menu", "exit"]
    while True:
        displayOptions(validInputs)
        action = playerAction(validInputs, "misc")
        match action:
            # Starts an adventure. Restores the players health when they return
            case "adventure":
                adventure()
            
            case "shop":
                wares = defaultStats.home_shop
                enterShop(wares)
                
            case "status":
                displayStats()
            
            case "inventory":
                displayInventory()
            
            case "equipment":
                displayEquipment()
            
            case "equip":
                equip()
            
            case "unequip":
                unequip()
            
            case "main menu":
                # Save player
                savedPlayer = json.dumps(player, indent=4)
                with open("player_stats.json", "w") as statsFile:
                    statsFile.write(savedPlayer)
                
                cprint("Exited to main menu", 'green')
                return False
            
            case "exit":
                # Save player
                savedPlayer = json.dumps(player, indent=4)
                with open("player_stats.json", "w") as statsFile:
                    statsFile.write(savedPlayer)
                
                cprint("Exited game", 'green')
                return True


# Changes color theme
def changeTheme():
    global tColor
    validInputs = ["default", "alternate", "back"]
    cprint("Available themes: ", tColor['misc'])
    displayOptions(validInputs)

    menuChoice = playerAction(validInputs, tColor['misc'])
    match menuChoice:
        case "default":
            tColor = defaultStats.default_color_theme
            cprint("Color theme set to default\n", tColor['misc'])

        case "alternate":
            tColor = defaultStats.alt1_color_theme
            cprint("Color theme set to alternate\n", tColor['misc'])
        
    sleep(0.5)
    cprint("Returned to main menu", tColor['misc'])
    return


def main():
    cprint("\nWelcome to Replies and Ruins!\n", 'light_green')
    sleep(0.5)
    print("You are in the main menu")
    validInputs = ["new game", "resume game", "change theme", "exit"]
    fullExit = False
    global player
    while True:
        displayOptions(validInputs)
        menuChoice = playerAction(validInputs, 'misc')
        match menuChoice:
            case "new game":
                player = defaultStats.default_player
                fullExit = game()
            
            case "resume game":
                with open('player_stats.json', 'r') as statsFile:
                    player = json.load(statsFile)
                
                fullExit = game()
                
            case "change theme":
                changeTheme()
            
            case "exit":
                cprint("Exited game", 'green')
                return
            
        if fullExit is True:
            break


if __name__ == "__main__":
    main()