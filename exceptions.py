class SadvException(Exception):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

class ItemNotInInventory(SadvException):
    def __init__(self, item):
        super(ItemNotInInventory, self).__init__(
            'Attempted to use item not in inventory: "'+item+'"'
        )

class UnknownItemCommand(SadvException):
    def __init__(self, item, command):
        super(UnknownItemCommand, self).__init__(
            'Unknown item command "'+command+'" for "'+item+'"'
        )

class NoCharactersInRegion(SadvException):
    def __init__(self, region):
        super(NoCharactersInRegion, self).__init__(
            'No characters in region: "'+region+'"'
        )

class UnknownRegionForWorld(SadvException):
    def __init__(self, world, region):
        super(UnknownRegionForWorld, self).__init__(
            'Cannot find region with name "'+region+'"'+' in world "'+world+'"'
        )

class MovingWithoutWorld(SadvException):
    def __init__(self, character, region):
        super(MovingWithoutWorld, self).__init__(
            'Attempted to move character "'+character+'" to region "'+region+
            '" without telling on what world it is'
        )
