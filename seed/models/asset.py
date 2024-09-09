"""Contains a base Asset that is consumed by the MainSeed"""

from typing import Set

from pydantic import BaseModel

from seed import common


class Asset(BaseModel):
    """An Asset in the context of this application is a singular object or place
    that requires descriptions. Assets will contain descriptors as hashtags.
    Each descriptor will have descriptions added to it.
    """

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
        descriptors matches that of a fibonacci number (1,2,3,5,8)."""
        self.descriptors.add(descriptor_name.lower())
        self.set_level()

    def remove_descriptor(self, descriptor_name):
        """Remove a descriptor from this asset. When this occurs level up will always be False, unless the number of
        descriptors matches that of a fibonacci number (1,2,3,5,8,etc)."""
        # self.level_up = False
        self.descriptors.remove(descriptor_name.lower())
        self.set_level()

    def set_level(self):
        """Re-establish the next_fib value. If the number of descriptors matches a fibonacci number, then
        the next_fib is always the next literal fibonacci number."""
        num_descriptors = len(self.descriptors)

        # Level is basically the length of the descriptoers == a Fibonacci number
        self.level_up = common.is_fibonacci(num_descriptors)
        self.next_fib = common.get_next_fibonacci(num_descriptors)

    # Only time this occurs is when a Fibonacci number in length occurs
    def is_uneven(self):
        """Checks if the current number of descriptors is a Fibonacci number"""
        return not self.level_up

    @property
    def hashtags(self):
        """Helper representation of descriptors"""
        return self.descriptors
