from pydantic import BaseModel
from typing import Dict, List

# A descriptor is a a 'hashtag' used for searching related material.
# This type of object can be associated with a character or place.
class Descriptor(BaseModel):
    name: str
    next_fib: int
    descriptions: list


# An Asset in the context of this application is a singular object or place
# that requires descriptions. Assets will contain descriptors as hashtags.
# Each descriptor will have descriptions added to it.
class Asset(BaseModel):
    name: str
    next_fib: int
    descriptors: Dict[str, Descriptor]
