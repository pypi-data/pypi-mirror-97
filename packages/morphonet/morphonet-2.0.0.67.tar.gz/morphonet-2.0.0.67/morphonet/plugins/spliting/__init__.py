# -*- coding: latin-1 -*-
defaultPlugins=[]

from .splitInTwoDistancePeak import SplitInTwoDistancePeak
defaultPlugins.append(SplitInTwoDistancePeak())

from .splitOnAxis import SplitOnAxis
defaultPlugins.append(SplitOnAxis())

from .splitOnRaw import SplitOnRaw
defaultPlugins.append(SplitOnRaw())