from seed import common, errors
from pydantic import BaseModel, field_validator, ValidationError, Field
from pydantic.dataclasses import dataclass
from typing import Dict, List, Set, Optional

# A descriptor is a a 'hashtag' used for searching related material.
# This type of object can be associated with a character or place.
class Descriptor(BaseModel):
    name: str
    next_fib: int = 1
    descriptions: List[str] = Field(default_factory=list)
    # TODO: Should Level Up be something done at the descriptor level?
    level_up: bool = False

    # A shared descriptor is something that multiple assets can have
    # For school should have grades, grades should have students, etc
    # A school can also have engineers, teachers, principles
    # This should be shared descriptor assets that can belong to an asset
    asset_links: Set[str] = Field(default_factory=set)

    @field_validator('descriptions')
    def validate_descriptions(cls, v):
        for item in v:
            if not common.is_fibonacci(common.get_num_words(item)):
                raise errors.FailedDescriptionLength("Description length does not equal a Fibonacci number")
        return v

    def add_description(self, description):
        """Add a description to the descriptor."""

        # KIS - The description length (number of words) should equal a Fibonacci number
        num_words = common.get_num_words(description)
        if not common.is_fibonacci(num_words):
            msg = f"Required Fibonacci length for the description"
            raise errors.FailedDescriptionLength(msg)

        self.descriptions.append(description.lower())
        self.set_level()

    def remove_description(self, description):
        """Remove a description from the descriptor"""
        self.descriptions.remove(description.lower())
        self.set_level()

    def set_level(self):
        """Re-establish the next_fib value. If the number of descriptors matches a fibonacci number, then
        the next_fib is always the next literal fibonacci number."""
        num_descriptions = len(self.descriptions)

        # Level is basically the length of the descriptoers == a Fibonacci number
        self.level_up = common.is_fibonacci(num_descriptions)
        self.next_fib = common.get_next_fibonacci(num_descriptions)

    def is_dangling(self):
        """Determines if this descriptor doesn't belong to an asset"""
        return len(self.asset_links) == 0

    def is_multi_asset_linked(self):
        """Determines if this descriptor belongs to multiple assets"""
        return len(self.asset_links) > 1

    def link_asset(self, asset_name):
        """Link an asset to this descriptor"""
        self.asset_links.add(asset_name.lower())

    def remove_link(self, asset_name):
        """Remove an asset link to this descriptor."""
        self.asset_links = set([i for _,i in enumerate(self.asset_links) if i.lower() != asset_name.lower()])

    def is_uneven(self):
        """Uneven is determined based on the number of descriptions matching a Fibonacci number."""
        return not self.level_up
