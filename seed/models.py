from seed import common, errors
from pydantic import BaseModel
from typing import Dict, List, Set
from pydantic import BaseModel, field_validator, ValidationError

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
    next_fib: int = 1
    descriptions: List[str] = list()
    # TODO: Should Level Up be something done at the descriptor level?
    level_up: bool = False

    # A shared descriptor is something that multiple assets can have
    # For school should have grades, grades should have students, etc
    # A school can also have engineers, teachers, principles
    # This should be shared descriptor assets that can belong to an asset
    asset_links: Set[str] = set()

    @field_validator('descriptions')
    def validate_descriptions(cls, v):
        for item in v:
            if not common.is_fibonacci(common.get_num_words(item)):
                raise errors.FailedDescriptionLength("Description length does not equal a Fibonacci number")


    def add_description(self, description):
        if not self.descriptions:
            self.descriptions = []

        num_words = common.get_num_words(description)
        next_fib = common.get_next_fibonacci(self.next_fib)

        # KIS - The description length (number of words) should equal a Fibonacci number
        if not common.is_fibonacci(num_words):
            msg = f"Required Fibonacci length for the description"
            raise errors.FailedDescriptionLength(msg)

        self.descriptions.append(description.lower())
        self.level_up = False

        # If the number of descriptions equals the next_fib, then there is a level_up which bumps
        # the next_fib to the next Fibonacci number
        if self.next_fib == len(self.descriptions) or len(self.descriptions) < 3:
            # Add the description to the hash tag
            self.level_up = True
            self.next_fib = common.get_next_fibonacci(self.next_fib)

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
    next_fib: int = 1
    descriptors: Set[str] = set()

    # This is used to determine when the number of descriptions matches the
    # 'next_fib' number qualifying it for growth. All non-levelup assets
    # will be queried for prompting the user to add more information.
    # TODO: Is this a good name? for other calculations it might be,
    # LevelUp in this context means that the asset is 'complete' so it's a little
    # weird...
    level_up: bool = False

    # TODO: add/remove hashtags
    def add_descriptor(self, descriptor_name):
        """Add a descriptor to this asset.  When this occurs level up will always be False, unless the number of
        descriptors matches that of a fibonacci number (1,2,3,5,8). """
        self.descriptors.add(descriptor_name.lower())
        self.set_level()

    def remove_descriptor(self, descriptor_name):
        """Remove a descriptor from this asset. When this occurs level up will always be False, unless the number of
        descriptors matches that of a fibonacci number (1,2,3,5,8,etc). """
        # self.level_up = False
        self.descriptors.remove(descriptor_name.lower())
        self.set_level()

    def set_level(self):
        """Re-establish the next_fib value. If the number of descriptors matches a fibonacci number, then
        the next_fib is always the next literal fibonacci number."""
        num_descriptors = len(self.descriptors)
        self.next_fib = common.get_next_fibonacci(num_descriptors)

    # Only time this occurs is when a Fibonacci number in length occurs
    def is_uneven(self):
        if common.is_fibonacci(len(self.descriptors)):
            return False
        return True

    @property
    def hashtags(self):
        return self.descriptors


FIB_N_LEVEL = 1

# This should be exportable into something consumable by an AI model / Pytorch
class MainSeed(BaseModel):
    """The Global Seed to be fed into an AI Model."""

    global_descriptors: Dict[str, Descriptor] = {}
    global_desc_level_up: bool = False
    global_desc_next_fib: int = FIB_N_LEVEL

    global_assets: Dict[str, Asset] = {}
    global_assets_level_up: bool = False
    global_assets_next_fib: int = FIB_N_LEVEL

    def add_descriptor(self, asset_name, desc_name):
        self.global_assets[asset_name].add_descriptor(desc_name)
        self.global_descriptors[desc_name].link_asset(asset_name)

    def add_description_to_asset(self, asset_name, descriptor_name, description):

        # Validate Descriptors
        if not self.global_descriptors.get(descriptor_name):
            desc = Descriptor(name=descriptor_name)
            self.global_descriptors[descriptor_name] = desc

        # Validate Asset
        if not self.global_assets.get(asset_name):
            self.global_assets[asset_name] = Asset(name=asset_name, descriptors={descriptor_name})

        # Does this description already exist in the descriptor? If not, add
        desc = self.global_descriptors[descriptor_name]
        if description not in desc.descriptions:
            desc.add_description(description)
        else:
            print(f"Description: {description} has already been added to this descriptor: {descriptor_name}")

        self.set_descriptor_level()
        self.set_asset_level()

    def set_descriptor_level(self):
        # Calculate next fibs for descriptors
        num_descriptors = len(self.global_descriptors)
        self.global_desc_level_up = False
        if num_descriptors == self.global_desc_next_fib:
            # n for Fib(n)
            self.global_desc_next_fib = common.get_next_fibonacci(num_descriptors)
            self.global_desc_level_up = True

    def set_asset_level(self):
        # Calculate next fibs for descriptors
        num_assets = len(self.global_assets)
        self.global_assets_level_up = False
        if num_assets == self.global_assets_next_fib:
            # n for Fib(n)
            self.global_assets_next_fib = common.get_next_fibonacci(num_assets)
            self.global_assets_level_up = True

    # TODO: Make more performant, maybe a map of some sort with a lazy load?
    def asset_relations(self, sibling_name:str):
        """Determines if an asset relates to another asset via a shared descriptor.
        Args:
            sibling_asset: The asset looking for siblings
        """
        sibling_asset = self.global_assets.get(sibling_name)
        if not sibling_asset:
            raise errors.SeedException(f"Asset {sibling_name} doesn't exist.")

        relations = {}
        for asset_name, asset_obj in self.global_assets.items():
            # Skip the sibbling_asset that was passed in
            if asset_name == sibling_asset.name:
                continue

            # All descriptors for this asset, see if one of those is in the asset to find relations
            for descriptor_name in asset_obj.descriptors:
                if descriptor_name in sibling_asset.descriptors:
                    relations[descriptor_name] = asset_obj.name

        return relations

    def export_asset_descriptions(self, asset_name):
        asset_obj = self.global_assets[asset_name]

        all_descriptions = []
        for _desc in asset_obj.descriptors:
            desc = self.global_descriptors[_desc]
            all_descriptions.extend(desc.descriptions or [])

        print(f"All descriptions:\n{all_descriptions}")
        return all_descriptions
