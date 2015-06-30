import exceptions
from region import Region

class World:
    def __init__(self, name="Unknown world", currentRegion="",
                 regions=[Region()]):
        self.name = name
        self.setRegions(regions)
        self.setCurrentRegion(currentRegion)

    def setRegions(self, regions):
        self.regions = {}
        for region in regions:
            self.regions[region.name] = region

    def setCurrentRegion(self, regionName):
        if regionName in self.regions:
            self.currentRegion = self.regions[regionName]
        else:
            raise exceptions.UnknownRegionForWorld(self.name, regionName)
