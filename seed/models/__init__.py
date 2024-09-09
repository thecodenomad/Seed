# TODO: Abstract away the calculation aspect so others can modify
# the mechanism with how a particular asset is LeveledUp. The initial idea
# of this project was to use an organic growth model. Since fibonacci is
# the cornerstone of organic growth, it was natural, hehe, to use this as
# the base calculation. Another calculation could involve something like
# a mandelbrot set. Anything more advanced will need this type of abstraction.
#    - Abstract out calculation for the asset
#    - Abstract out calculation for a descriptor
#    - Rename all functions corresponding to the calculator
#
# KIS - Assets are related to assets only through descriptors. For instance,
#       a brother relates to a sister through a shared sibling descriptor.
#
#         - All (natural) siblings share the same parents.
#         - All cities share the same state.
#
# Assets sphere of influence is determined by their shared descriptors. Think
# neurons. Assets start firing together to form a memory. Memories are collections
# of assets firing.

from .asset import Asset
from .descriptor import Descriptor
from .main_seed import MainSeed
