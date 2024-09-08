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
