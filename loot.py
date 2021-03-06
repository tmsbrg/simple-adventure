import random

from colors import colors
import exceptions

def applyStats(character, addStats, printIt=True,
               stats=None, keepNonNegative=False, deathMessage="died."):
    if stats == None:
        stats = self.stats
    if addStats:
        m = 1
    else:
        m = -1
    for key in stats:
        character.changeStat(key, stats[key] * m, printIt, keepNonNegative,
                             deathMessage)


class Equipment:
    def __init__(self, name="Unnamed", stats={}, slot="inventory"):
        self.name = name
        self.stats = stats
        self.slot = slot
        self.targetable = False

    def getEquippedOn(self, character, printIt=True):
        if printIt:
            print(character.name,"picks up the",self.name)
        applyStats(character, True, printIt, self.stats)

    def getDiscardedBy(self, character, printIt=True):
        if printIt:
            print(character.name,"discards the",self.name)
        applyStats(character, False, printIt, self.stats)


class Item():
    def __init__(self, name="Unnamed", useCommand="nothing", useObject=None,
                 targetable=False):

        self.name = name
        self.useCommand = useCommand
        self.useObject = useObject
        self.targetable = targetable

    def getUsedOn(self, character, world=None, other=None):
        if self.useCommand == "nothing":
            print("Nothing happens.")
        elif self.useCommand == "change_stats":
            applyStats(character, True, True, self.useObject, True)
        elif self.useCommand == "damage":
            self.doDamage(character)
        elif self.useCommand == "move_to":
            character.moveToRegion(self.useObject, world, other)
        elif self.useCommand == "custom":
            self.useObject(self, character)
        elif self.useCommand == "win":
            character.win()
        elif self.useCommand == "set_status":
            character.setStatus(self.useObject[0], self.useObject[1])
        elif self.useCommand == "remove_status":
            character.removeStatus(self.useObject[0])
        else:
            raise exception.UnknownItemCommand(self.name, self.useCommand)

    def doDamage(self, character):
        damage = self.getDamageObject(self.useObject)
        for stat in damage:
            print(character.name," lost ",
                  colors.DAMAGE, damage[stat], colors.ENDC,
                  " ", stat, sep="")
        applyStats(character, False, False, damage, True)

    def getDamageObject(self, useObject):
        r = {}
        for key in useObject:
            damageRange = useObject[key]
            r[key] = random.randint(damageRange[0], damageRange[1])
        return r
