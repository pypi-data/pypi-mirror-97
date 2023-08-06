# -*- coding: latin-1 -*-
defaultPlugins=[]

from .watershedithNewSeeds import watershedithNewSeeds
defaultPlugins.append(watershedithNewSeeds())

from .ExtremeWater import ExtremeWater
defaultPlugins.append(ExtremeWater())

from .createSeeds import createSeeds
defaultPlugins.append(createSeeds())