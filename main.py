#!/usr/bin/python3
import random
import readline

from colors import colors
import settings

player = None
world = settings.world
currentEnemy = None

def getInput(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("exit")
        exit(0)

def main():
    global currentEnemy
    setPlayer(settings.player)

    print("\nSimple adventure v0.02\n")
    player.name = getInput("What is thy name? ")
    print(colors.IMPORTANTTEXT,
          "\n", player.name,", praise the scholars, you're here!\n",
          colors.ENDC,
          "\n"
          "The Holy Artifact of our temple has been stolen and taken to a\n"
          "place far into the wilderness. It is what protected us from dark\n"
          "forces outside of our town. If we can't get it back, we'll all be\n"
          "doomed!\n"
          "\n"
          "Travel to the wilderness, and try to get it back! But...\n"
          "Don't get killed along the way!\n", sep="")

    getInput("(Press enter to continue) ")

    print("\nYou enter ",colors.REGIONTEXT, world.currentRegion.name,
          colors.ENDC, sep="")
    print("\nType 'h' and enter for help")

    while True:
        currentEnemy = world.currentRegion.getRandomChar()
        print("\nAn evil",currentEnemy.name,"has appeared!")
        while True:
            player.reduceStatuses()
            currentEnemy.reduceStatuses()
            if player.getStat("health") < 10:
                color = colors.CRITICAL
            elif player.getStat("health") < 30:
                color = colors.HURT
            else:
                color = colors.HEALTHY
            print("Your health:",color,player.getStat("health"),colors.ENDC)
            inp = getInput("> ")
            if (inp == '' or inp[0] == 'a'):
                player.attack(currentEnemy)
                if advanceTurn():
                    break
            else:
                if interpretInput(inp) and advanceTurn():
                    break

# makes the enemy attack and checks for enemy and player death, returns true
# if enemy is dead, false otherwise
def advanceTurn():
    if currentEnemy.dead:
        getLoot(currentEnemy)
        return True
    elif currentEnemy.movedAway:
        return True
    currentEnemy.attack(player)
    checkDeath()
    return False


def getLoot(enemy):
    loot = enemy.dropLoot(settings.lootAmount)
    if len(loot) > 0:
        print("\nLoot(select one):")
        item = printAndSelect(loot, "take none",
                              "Type the number of the loot you want to get,"
                              " and then enter")
        if item != None:
            player.pickupItem(item)
    else:
        print("\n",enemy.name," has no loot.", sep="")
        printAndSelect([], "continue",
                       "Type 0 and enter to fight the next enemy.")

def setPlayer(new_player):
    global player
    if player != None:
        player.isPlayer = False
    player = new_player
    player.isPlayer = True


def selectAndUseItem():
    items = player.getUsableItems()
    if len(items) > 0:
        print("\nUsable items(Type number to use)")
        while True: # allow us to go back to item selection
            item = printAndSelect(items, "do nothing", 
                                  "Type the number of the item you want to use,"
                                  "and then enter",
                                  ['u'])
            if item != None:
                if item.isTargetable():
                    target = selectTarget()
                    if target == None:
                        continue # back to the item selection
                    elif target is player:
                        other = currentEnemy
                    else:
                        other = player
                else:
                    target = player
                    other = currentEnemy
                print("Using",item.name)
                player.useItem(item, target, world, other)
                checkDeath()
                return True
            else:
                break # no item selected, go back to previous menu

    else:
        print("\nNo usable items in inventory")
    return False


def selectTarget():
    return printAndSelect([currentEnemy, player], "go back",
                          "Type the number of the target you want to use the"
                          " item on, and then enter",
                         ['u'])

def printAndSelect(objects, defaultMessage, helpMessage, ignoreCommands=[]):
    printObjects(objects)
    print("(0) ("+defaultMessage+")", sep='')
    return getObject(objects, helpMessage, ignoreCommands)


def checkDeath():
    if player.dead:
        print(player.endStats())
        exit(0)


def printObjects(objects):
    for i in range(len(objects)):
        print("(",str(i+1),") ",objects[i].name, sep="")


def getObject(objects, helpMessage, ignoreCommands=[]):
        got_object = False
        while not got_object:
                inp = getInput("> ")
                if inp.isdigit():
                    inp = int(inp)
                    if (inp < 0 or inp > len(objects)):
                        print("No object at index",inp)
                    else:
                        got_object = True
                        if inp != 0:
                            return objects[inp-1]
                        return None
                elif inp == '' or inp[0] == 'h':
                    print(helpMessage)
                else:
                    cmd_ignore = False
                    for cmd in ignoreCommands:
                        if inp.startswith(cmd):
                            print("Cannot do that here")
                            cmd_ignore = True
                    if not cmd_ignore:
                        interpretInput(inp)


# interprets input not handled elsewhere, returns true if input causes the
# player to use up a turn, otherwise false
def interpretInput(inp):
    if inp[0] == 'h':
        print("Controls:\n"
             "    '' or 'a' - attack\n"
             "          'i' - inventory\n"
             "          's' - your stats\n"
             "          'u' - use an item\n"
             "          'h' - this help screen\n"
             "\n"
             "Press enter after entering a command.\n")
    elif inp[0] == 'i':
        inv = player.getInventory()
        if len(inv) > 0:
            for key in inv:
                print(key,": ",inv[key].name, sep='')
        else:
            print("\nNo items in inventory")
    elif inp[0] == 's':
        player.printStats()
    elif inp[0] == 'u':
        return selectAndUseItem()
    elif inp == '' or inp[0] == 'a':
        print("Cannot attack here")
    elif inp == "exit":
        exit(0)
    else:
        print("Don't understand command",inp)
    return False

if __name__ == '__main__':
    main()

