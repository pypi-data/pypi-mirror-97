# -*- coding: latin-1 -*-
defaultPlugins=[]

from .watershedithNewSeeds import WatershedithNewSeeds
defaultPlugins.append(WatershedithNewSeeds())

from .ExtremeWater import ExtremeWater
defaultPlugins.append(ExtremeWater())

from .createSeeds import CreateSeeds
defaultPlugins.append(CreateSeeds())