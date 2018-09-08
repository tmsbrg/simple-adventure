import random
import sys
from copy import copy

from colors import colors
import exceptions

class Character:
    dead = False
    movedAway = False
    isPlayer = False

    def __init__(self, name="Unnamed", stats={}, loot=[]):
        self.name = name
        self.loot = loot
        self.stats = stats
        self.setStatsDefaults()
        self.kills = {}
        self.equipment = {}
        self.status = {}

    def setStatsDefaults(self):
        self.setDefaultStat("health", 50)
        self.setDefaultStat("defence", 0)
        self.setDefaultStat("minimum attack", 1)
        self.setDefaultStat("maximum attack", 10)

    def setDefaultStat(self, stat, value):
        if stat not in self.stats:
            self.stats[stat] = value

    def changeStat(self, stat, value, printIt=True, keepNonNegative=False,
                   deathMessage="died mysteriously."):
        self.stats[stat] += value
        if keepNonNegative and self.stats[stat] < 0:
            self.stats[stat] = 0
        if printIt:
            print(self.name,"'s ",stat," is now ",self.stats[stat], sep="")
        # special case: make sure maximum attack >= minimum attack
        if (stat == "maximum attack" and 
            self.stats[stat] < self.stats["minimum attack"]):
            self.stats["minimum attack"] = self.stats[stat]
        elif (stat == "minimum attack" and
              self.stats[stat] > self.stats["maximum attack"]):
            self.stats["maximum attack"] = self.stats[stat]
        # special case: check death if we lost health
        elif stat == "health":
            self.checkDeath(self.name+" "+deathMessage, printIt)

    def setStatus(self, status, turns):
        if status not in self.status or self.status[status] < turns:
            print(self.name," is ",status,"!", sep="")
            self.status[status] = turns

    def removeStatus(self, status):
        if status in self.status:
            print(self.name,"is no longer",status)
            del self.status[status]

    def reduceStatuses(self):
        removestatus = []
        for status in self.status:
            self.status[status] -= 1
            if self.status[status] <= 0:
                removestatus.append(status)
        for status in removestatus:
            self.removeStatus(status)

    def attack(self, target=None):
        if "stunned" in self.status:
            print(self.name,"cannot attack!")
            return
        amount = random.randint(self.stats["minimum attack"],
                                self.stats["maximum attack"])
        target.damage(amount, self)
        if target.dead:
            if target.name in self.kills:
                self.kills[target.name] += 1
            else:
                self.kills[target.name] = 1

    def damage(self, amount, attacker=None, printIt=True):
        amount -= random.randint(0, self.stats["defence"])
        if amount < 0:
            amount = 0
        self.stats["health"] -= amount
        if printIt:
            print(self.getHurtMessage(amount))
        self.checkDeath(self.getDeathMessage(attacker), printIt)

    def checkDeath(self, deathMessage, printIt=True):
        if not self.dead and self.stats["health"] <= 0:
            self.die(deathMessage)

    def die(self, deathmessage, printIt=True):
        self.dead = True
        if printIt:
            print(deathmessage)

    def getHurtMessage(self, amount=0):
        return (self.name+" got hit for "+colors.DAMAGE+
                str(amount)+colors.ENDC+" damage.")

    def getDeathMessage(self, attacker=None):
        if attacker == None:
            return self.name+" died."
        elif attacker is self:
            return self.name+" killed himself."
        else:
            return self.name+" was vanquished by "+attacker.name+"."

    def dropLoot(self, amount):
        r = []
        unusedLoot = copy(self.loot)
        for i in range(amount):
            if len(unusedLoot) > 0:
                itemi = random.randint(0, len(unusedLoot)-1)
                r.append(unusedLoot[itemi])
                del unusedLoot[itemi]
            else:
                break
        return r

    def moveToRegion(self, regionName, world, other=None):
        if world == None:
            raise exceptions.MovingWithoutWorld(self.name, regionName)
        if regionName != world.currentRegion.name:
            if self.isPlayer:
                world.setCurrentRegion(regionName)
                print("Moved to ",colors.REGIONTEXT,regionName,colors.ENDC,
                      sep="")
                if other != None:
                    other.moveAway()
            elif not self.dead:
                self.moveAway("fled away")
        else:
            print("Already in that region!")

    def moveAway(self, message=None):
        if message != None:
            print(self.name,message)
        self.movedAway = True
    
    def pickupItem(self, item, printIt = True):
        if item.slot in self.equipment:
            self.equipment[item.slot].getDiscardedBy(self, printIt)
        self.equipment[item.slot] = item
        item.getEquippedOn(self, printIt)

    def useItem(self, item, target=None, world=None, other=None):
        if target == None:
            target = self
        if item in self.equipment.values():
            item.getUsedOn(target, world, other)
            item.getDiscardedBy(self, False)
            del self.equipment[item.slot]
            self.checkDeath(self.getDeathMessage(self))
        else:
            raise exceptions.ItemNotInInventory(item.name)

    def getStat(self, stat):
        return self.stats[stat]

    def getUsableItems(self):
        r = []
        for item in self.equipment.values():
            if item.canBeUsed():
                r.append(item)
        return r

    def getInventory(self):
        return self.equipment

    def printStats(self):
        for stat in self.stats:
            print(stat,": ",self.stats[stat], sep="")

    def win(self):
        if self.isPlayer:
            print(colors.IMPORTANTTEXT,"\nYou have won!\n",colors.ENDC,
                  "\n"
                  "You have found the Holy Artifact that was stolen from your\n"
                  "people. You restore it to the temple and protection of the\n"
                  "town returns. Your quest is successful.\n", sep="")
            print(self.endStats())
            sys.exit(0)
        else:
            print(self.name,"has won.")

    def endStats(self):
        text = "kills:\n"
        total = 0
        for name in self.kills:
            text += (name + " - " +
                     colors.KILLTEXT+str(self.kills[name])+colors.ENDC + "\n")
            total += self.kills[name]
        text += "Total - "+colors.KILLTEXT+str(total)+colors.ENDC
        return text
