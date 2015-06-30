import random

from colors import colors
import exceptions

class Loot:
    def __init__(self, name="Unnamed", stats={}, slot="inventory"):
        self.name = name
        self.stats = stats
        self.slot = slot
        self.useCommand = ""
        self.useObject = None
        self.targetable = False

    def getEquippedOn(self, character, printIt=True):
        if printIt:
            print(character.name,"picks up the",self.name)
        self.applyStats(character, True, printIt)

    def getDiscardedBy(self, character, printIt=True):
        if printIt:
            print(character.name,"discards the",self.name)
        self.applyStats(character, False, printIt)

    def applyStats(self, character, addStats, printIt=True,
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

    def isTargetable(self):
        return self.targetable

    def canBeUsed(self):
        return self.useCommand != ""

    def getUsedOn(self, character, world=None, other=None):
        if self.canBeUsed():
            if self.useCommand == "nothing":
                print("Nothing happens.")
            elif self.useCommand == "change_stats":
                self.applyStats(character, True, True, self.useObject, True)
            elif self.useCommand == "damage":
                self.doDamage(character)
            elif self.useCommand == "move_to":
                character.moveToRegion(self.useObject, world, other)
            elif self.useCommand == "custom":
                self.useObject(self, character)
            elif self.useCommand == "win":
                character.win()
            else:
                raise exception.UnknownItemCommand(self.name, self.useCommand)
        else:
            raise exceptions.ItemUnusable(self.name)

    def doDamage(self, character):
        damage = self.getDamageObject(self.useObject)
        for stat in damage:
            print(character.name," lost ",
                  colors.DAMAGE, damage[stat], colors.ENDC,
                  " ", stat, sep="")
        self.applyStats(character, False, False, damage, True)

    def getDamageObject(self, useObject):
        r = {}
        for key in useObject:
            damageRange = useObject[key]
            r[key] = random.randint(damageRange[0], damageRange[1])
        return r

# simple constructor for usable loot
class Item(Loot):
    def __init__(self, name="Unnamed", useCommand="nothing", useObject=None,
                 targetable=False):

        super(Item, self).__init__(name)
        self.useCommand = useCommand
        self.useObject = useObject
        self.targetable = targetable
