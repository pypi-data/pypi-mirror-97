# -*- coding: latin-1 -*-
from .MorphoPlugin import MorphoPlugin
__all__ = [
    'MorphoPlugin'
]


defaultPlugins=[]

from .creation import defaultPlugins as DP
defaultPlugins+=DP

from .deletion import defaultPlugins as DP
defaultPlugins+=DP

from .spliting import defaultPlugins as DP
defaultPlugins+=DP

from .temporal import defaultPlugins as DP
defaultPlugins+=DP
