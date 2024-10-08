"""Contains a base Descriptor that is consumed by the MainSeed"""

from typing import List, Set

from pydantic import field_validator, model_validator, Field

from seed import common, errors
from seed.models.strict import StrictModel


class Descriptor(StrictModel):
    """A descriptor is a a 'hashtag' used for searching related material.
    This type of object can be associated with a character or place.
    """

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

    # pylint: disable=E0213
    @field_validator("descriptions")
    def validate_descriptions(cls, v):
        """Each description must be a Fibonacci number in length."""
        for item in v:
            if not common.is_fibonacci(common.get_num_words(item)):
                raise errors.FailedDescriptionLength("Description length does not equal a Fibonacci number")
        return v

    # pylint: enable=E0213

    @model_validator(mode="after")
    def validate_and_sanitize(self):
        """Sanitize the descriptor next_fib and level_up."""

        # Sanitize next_fib if strict = False, fail if mismatch or invalid number
        try:
            if self.next_fib != common.get_next_fibonacci(self.num_descriptions):
                msg = f"Invalid next_fib: {self.next_fib} for {self.num_descriptions} descriptions"
                raise errors.SeedValidationException(msg)
        except errors.SeedValidationException:
            if self.strict:
                raise
            self.next_fib = common.get_next_fibonacci(self.num_descriptions)

        # Sanitize level_up if strict = False, fail if invalid
        try:
            if self.level_up != (common.is_fibonacci(self.num_descriptions)):
                msg = f"Invalid level_up: {self.level_up} for len(descriptions: {self.num_descriptions}"
                raise errors.SeedValidationException(msg)
        except errors.SeedValidationException:
            if self.strict:
                raise
            self.level_up = common.is_fibonacci(self.num_descriptions)

        # Sanitize name and descriptors
        # TODO: Can this be done at attribute level?
        self.name = self.name.lower()
        self.descriptions = [i.lower() for i in self.descriptions]

        return self

    @property
    def num_descriptions(self):
        """The number of descriptions in memory."""
        return len(self.descriptions)

    def add_description(self, description):
        """Add a description to the descriptor."""

        # KIS - The description length (number of words) should equal a Fibonacci number
        #
        # Why a Fibonacci length check?
        #
        # Easily to calculate, easy to teach, symbolic since it felt Natural
        # (Living organism grow with the golden ratio).
        #
        # It takes thought to produce a sentence with a Fibonacci word-length.
        # The constraints are high enough that rewording is required multiple times as
        # things get more complex. Its like texts in the late 90s... and you only have 100/month!
        num_words = common.get_num_words(description)
        if not common.is_fibonacci(num_words):
            msg = "Required Fibonacci length for the description"
            raise errors.FailedDescriptionLength(msg)

        self.descriptions.append(description.lower())  # pylint: disable=E1101
        self.set_level()

    def remove_description(self, description):
        """Remove a description from the descriptor"""
        self.descriptions.remove(description.lower())  # pylint: disable=E1101
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
        self.asset_links = {i for _, i in enumerate(self.asset_links) if i.lower() != asset_name.lower()}

    def is_uneven(self):
        """Uneven is determined based on the number of descriptions matching a Fibonacci number."""
        return not self.level_up
