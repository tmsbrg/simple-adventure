from character import *
from loot import *
from region import *
from world import *

# DOCUMENTATION:
# (see also the settings as they are below, you can start by editing those and
#  seeing what happens)

# EQUIPMENT CONSTRUCTOR:
#   var_name = Equipment("name", {"stat1": n, "stat2": n2, ...},
#                   "slot")
#
#       where: "stat1", "stat2", ... are valid stat names* to increase with this
#                   item
#           ,  n, n2, ... are numbers telling to game how much to increase their
#                   associated stat
#           ,  "slot" is the equipment slot it uses. You can easily add slots
#                   by just making an object that uses a previously unused slot.
#                   beware: this means spelling errors aren't caught by this
#                   system: "weapon" and "waepon" are both different valid slots
#
#       * see "VALID STAT NAMES"

# ITEM CONSTRUCTOR:
#   var_name = Item("name", "command", command_obj, targetable)
#
#       where: "command" is one of the valid commands*
#           ,  command_obj is an object of the type needed for that command
#                  (see list of valid commands*)
#           ,  targetable is either True or False, and determines whether you
#                  can use this item on enemies
#
#       * see "VALID COMMANDS"

# CHARACTER CONSTRUCTOR:
#       Character("name", {"stat1": n, "stat2": n2, ...},
#                 [var_loot1, var_loot2, ...])
#
#       where: "stat1", "stat2", ... are valid stat names* that indicate this
#                   character's stats, if a stat is not given it will use the
#                   default*
#           ,   n, n2, ... are numbers indicating the value of their associated
#                   stat
#           ,   var_loot1, var_loot2, ... are var_names of loot or items this
#                   character can drop
#
#       * see "VALID STAT NAMES"

# VALID STAT NAMES:
#   This is a list of stats currently in use
#       - "health", a character dies if it reaches 0, default: 50
#       - "minimum attack", the minimum damage the character does when he 
#                           attacks, default: 1
#       - "maximum attack", the maximum damage the character does when he
#                           attacks, default: 10
#       - "defence", whenever a character is attacked, a random number is
#                    generated between 0 and this value, which is substracted
#                    from the amount of damage done, default: 0

# VALID COMMANDS:
#   This is a list of commands currently in use, and the command_obj they use
#       - "nothing", does nothing on use except saying that nothing happened,
#                    ignores command_obj
#       - "change_stats", takes set of stats like in the Equipment constructor as
#                         command_obj and adds them to the character it is
#                         used on
#       - "damage", takes a set of stats like in the Equipment constructor, except
#                   it takes 2 values for each stat, the minimum damage done
#                   and the maximum damage done. e.g.:
#                   e.g. {"health":[2,4], "defence":[1,3]} deals between 2 and 4
#                   health damage(inclusive) and between 1 and 3 defence damage
#                   on use
#                    3 damage to the "defence" stat of the target
#       - "custom", (advanced) calls a custom function that takes the item and
#                   the target character as arguments, and does something with
#                   them(see the randomize_name function for example, used in
#                   the name scrolls)


# custom item functions
def randomize_name(self, character):
    def toStr(l):
        r = ""
        for item in l:
            r += item
        return r
    name_as_list = list(character.name)
    random.shuffle(name_as_list)
    character.name = toStr(name_as_list).capitalize()
    if character.isPlayer:
        print("You feel like something about you has changed, "
              "but you don't know what.")

# weapons
beginners_knife = Equipment("beginner's knife", {"maximum attack": 10}, "weapon")
rusty_axe = Equipment("rusty axe", {"maximum attack":14}, "weapon")
orcish_blade = Equipment("orcish blade", {"maximum attack":18}, "weapon")
scythe = Equipment("Scythe", {"maximum attack":22}, "weapon")
greatsword = Equipment("greatsword", {"maximum attack":26}, "weapon")

# armor
wizard_cloak = Equipment("wizard's cloak", {"defence":2}, "armor")
knight_armor = Equipment("knight's armor", {"defence":6}, "armor")

# shields
shield = Equipment("shield", {"defence":2}, "shield")

# helmets
leather_helm = Equipment("leather helm", {"defence": 2}, "helmet")
iron_helm = Equipment("iron helm", {"defence":4}, "helmet")

# buffs
wolf_pelt = Item("wolf pelt", "change_stats", {"defence":1})
orc_tooth = Item("orc tooth", "change_stats", {"maximum attack":1})

# healing items
wolf_meat = Item("wolf meat", "change_stats", {"health":7})
bread = Item("bread", "change_stats", {"health":12})
red_potion = Item("red potion", "change_stats", {"health":30})

# scrolls
name_scroll = Item("name scroll", "custom", randomize_name, True)
weakness_scroll = Item("scroll of weakness", "damage",
                       {"maximum attack":[1, 10]}, True)
fire_scroll = Item("fire scroll", "damage", {"health":[15, 25]}, True)

# maps
greenfields_map = Item("map to the Green Fields", "move_to", "the Green Fields")
orclands_map = Item("map to the Orclands", "move_to", "the Orclands")
dark_map = Item("map to the Darkness", "move_to", "the Darkness")

# misc
spider_silk = Item("spider silk", "set_status", ("stunned", 3), True)
holy_artifact = Item("Holy Artifact", "win")
bomb = Item("bomb", "damage", {"health":[20, 60]}, True)


# enemies
bandit = Character("Bandit", {"health":30}, 
                   [rusty_axe, leather_helm, bread, shield, orclands_map])
orc = Character("Orc", {"health":50},
                [orcish_blade, shield, red_potion, iron_helm, orc_tooth,
                 orclands_map, greenfields_map])
wolf = Character("Wolf", {"health":15, "maximum attack": 8},
                 [wolf_meat, wolf_pelt])
giant = Character("Giant", {"health":80, "maximum attack": 20}, 
                  [greatsword, knight_armor, holy_artifact, bomb])
rat = Character("Rat", {"health":5, "maximum attack": 5})
giant_spider = Character("Giant Spider", {"health":10, "maximum attack": 6}, 
                         [spider_silk])
wizard = Character("Wizard", {"health":40, "maximum attack": 15},
                   [name_scroll, fire_scroll, wizard_cloak, dark_map])
reaper = Character("Reaper", {"health":30, "minimum attack": 10,
                              "maximum attack" : 30},
                   [bomb, weakness_scroll, red_potion, scythe])

# regions
greenfields = Region("the Green Fields",
                     [(rat, 2), (wolf, 3),
                      (bandit, 4), (giant_spider, 2), (orc, 1)]
                    )

orclands = Region("the Orclands",
                  [(orc, 4), (rat, 1), (wolf, 1), (wizard, 2)]
                 )

darkness = Region("the Darkness",
                  [(giant, 2), (wizard, 2), (orc, 1), (reaper, 1)]
                 )

# world
world = World("Earth", "the Green Fields", [greenfields, orclands, darkness])

player = Character("Player", {"health": 60, "maximum attack": 6})
player.pickupLoot(beginners_knife, False)

lootAmount = 2
