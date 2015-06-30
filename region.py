import random
from copy import deepcopy

import exceptions
from character import Character

class Region:
    totalCharacterWeight = 0

    def __init__(self, name="Unnamed region",
                 charsAndWeights=[(Character(), 1)]):
        self.name = name
        self.setCharsAndWeights(charsAndWeights)

    def setCharsAndWeights(self, charsAndWeights):
        self.charsAndWeights = charsAndWeights
        self.totalCharacterWeight = 0
        for charAndWeight in charsAndWeights:
            self.totalCharacterWeight += charAndWeight[1]

    def getRandomChar(self):
        if self.totalCharacterWeight < 1:
            raise exceptions.NoCharactersInRegion(self.name)
        spawnValue = random.randint(1, self.totalCharacterWeight)
        for charAndWeight in self.charsAndWeights:
            spawnValue -= charAndWeight[1]
            if spawnValue <= 0:
                return deepcopy(charAndWeight[0])
