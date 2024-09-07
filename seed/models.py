from seed import common, errors
from pydantic import BaseModel
from typing import Dict, List, Set

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

# A descriptor is a a 'hashtag' used for searching related material.
# This type of object can be associated with a character or place.
class Descriptor(BaseModel):
    name: str
    next_fib: int = 0
    descriptions: List[str] = []
    # TODO: Should Level Up be something done at the descriptor level?
    # level_up: bool = False

    # A shared descriptor is something that multiple assets can have
    # For school should have grades, grades should have students, etc
    # A school can also have engineers, teachers, principles
    # This should be shared descriptor assets that can belong to an asset
    asset_links: Set[str] = set()

    def add_description(self, description):

        num_words = common.get_num_words(description)
        next_fib = common.get_next_fibonacci(self.next_fib)

        # This should satisfy entries with 1 word
        if len(self.descriptions) == 2:
            next_fib = 2

        # If the description length equals the next fibonacci sequence, add it
        # else fail. No level up here, descriptions must always be a fibonacci number
        # For descriptions, this is the way.
        if num_words != next_fib:
            print("In conditional num_words ! =next_fib")
            msg = f"Required {self.next_fib} length for the description"
            raise errors.FailedDescriptionLength(msg)

        # Add the description to the hash tag
        print("Adding description in descriptor")
        self.descriptions.append(description.lower())

        # Set the next description length
        self.next_fib = next_fib

    def is_dangling(self):
        """Determines if this descriptor doesn't belong to an asset"""
        return len(self.asset_links) == 0

    def is_multi_asset_linked(self):
        """Determines if this descriptor belongs to multiple assets"""
        return len(self.asset_links) > 1

    def link_asset(self, asset_name):
        self.asset_links.add(asset_name.lower())

    def remove_link(self, asset_name):
         self.asset_links = set([i for _,i in enumerate(self.asset_links) if i.lower() != asset_name.lower()])


# An Asset in the context of this application is a singular object or place
# that requires descriptions. Assets will contain descriptors as hashtags.
# Each descriptor will have descriptions added to it.
class Asset(BaseModel):
    name: str
    next_fib: int = 0
    descriptors: Dict[str, Descriptor] = {}

    # This is used to determine when the number of descriptions matches the
    # 'next_fib' number qualifying it for growth. All non-levelup assets
    # will be queried for prompting the user to add more information.
    # TODO: Is this a good name? for other calculations it might be,
    # LevelUp in this context means that the asset is 'complete' so it's a little
    # weird...
    level_up: bool = False

    # Lazy load
    shared_descriptors: List[str] = []

    # TODO: add/remove hashtags
    # TODO: add/remove descriptions from hashtags

    @property
    def hashtags(self):
        return list(self.descriptors.keys())

    def add_description(self, hashtag, description):

        # Check to see if the hashtag exists in the descriptors
        if self.descriptors.get(hashtag):
            self.descriptors[hashtag].add_description(description)
        else:
            # Create new descriptor
            descriptor = Descriptor(name=hashtag, next_fib=0)

            # Must still pass the validation
            descriptor.add_description(description)
            self.descriptors[hashtag] = descriptor

        # Level Up occurs only when the number of descriptors match the
        # next_fib value. The LevelUp attribute is used to quickly determine
        # which assets are considered incomplete to prioritize prompts to/from
        # the AI model.
        num_hashtags = len(self.descriptors)
        print(f"num_hastags: {num_hashtags}")
        if num_hashtags == self.next_fib:
            self.level_up = True
            self.next_fib = common.get_next_fibonacci(self.next_fib)
        else:
            self.level_up = False

    # TODO: Make more performant, maybe a map of some sort with a lazy load?
    def has_asset_relation(self):
        """ Determines if an asset relates to another asset via a shared descriptor """

        self.shared_descriptors = [name for name, o in self.descriptors.items() if o.is_multi_asset_linked()]
        return len(self.shared_descriptors) > 0
