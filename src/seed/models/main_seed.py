"""The purpose of this module is to create an entrypoint for data collected for
assets and descriptors. These may included shared descriptors, which link the
assets together."""

from typing import Dict

from pydantic import model_validator

from seed import common, errors
from seed.models import Asset, Descriptor
from seed.models.strict import StrictModel

FIB_N_LEVEL = 1


# This should be exportable into something consumable by an AI model / Pytorch
class MainSeed(StrictModel):
    """The Global Seed to be fed into an AI Model."""

    global_descriptors: Dict[str, Descriptor] = {}
    global_desc_level_up: bool = False
    global_desc_next_fib: int = FIB_N_LEVEL

    global_assets: Dict[str, Asset] = {}
    global_assets_level_up: bool = False
    global_assets_next_fib: int = FIB_N_LEVEL

    # Fix calculations if strict == False, else fail on invalid formatting
    strict: bool = False

    @model_validator(mode="after")
    def verify_and_sanitize(self):
        """Model Validation method, this will recalculate next_fib and level_up if they appear
        to be invalid.
        """
        # Sanitize next_fib if strict = False, fail if mismatch or invalid number
        try:
            if self.global_desc_next_fib != common.get_next_fibonacci(self.num_descriptors):
                msg = f"Invalid global_desc_next_fib: {self.global_desc_next_fib} for {self.num_descriptors} descriptors"
                raise errors.SeedValidationException(msg)

            if self.global_assets_next_fib != common.get_next_fibonacci(self.num_assets):
                msg = f"Invalid global_assets_next_fib: {self.global_assets_next_fib} for {self.num_assets} assets"
                raise errors.SeedValidationException(msg)

        except errors.SeedValidationException:
            if self.strict:
                raise
            self.global_desc_next_fib = common.get_next_fibonacci(self.num_descriptors)
            self.global_assets_next_fib = common.get_next_fibonacci(self.num_assets)

        # Sanitize level_up if strict = False, fail if invalid
        try:
            if self.global_desc_level_up != (common.is_fibonacci(self.num_descriptors)):
                msg = f"Invalid global_desc_level_up: {self.global_desc_level_up} for len(descriptors): {self.num_descriptors}"
                raise errors.SeedValidationException(msg)

            if self.global_assets_level_up != (common.is_fibonacci(self.num_assets)):
                msg = f"Invalid global_assets_level_up: {self.global_assets_level_up} for len(assets): {self.num_assets}"
                raise errors.SeedValidationException(msg)

        except errors.SeedValidationException:
            if self.strict:
                raise
            self.global_desc_level_up = common.is_fibonacci(self.num_descriptors)
            self.global_assets_level_up = common.is_fibonacci(self.num_assets)

        return self

    @property
    def num_descriptors(self):
        """Retrieve the number of descriptors currently in memory"""
        return len(self.global_descriptors)

    @property
    def num_assets(self):
        """Retrieve the number of assets currently in memory"""
        return len(self.global_assets)

    def link_descriptor(self, asset_name, descriptor_name):
        """Link a descriptor to an asset"""
        self.global_assets[asset_name].add_descriptor(descriptor_name)
        self.global_descriptors[descriptor_name].link_asset(asset_name)

    def add_description(self, descriptor_name, description):
        """Adds a description to a descriptor."""
        # Attempt adding the description
        self._ensure_descriptor(descriptor_name=descriptor_name)

        # Sanitize
        description = description.lower()

        # Make sure the description doesn't already exist
        # TODO: For anything more than 21 words, should there be a threshold? We don't
        # want multiple sentences that are the same. Does that even matter for AI Input? Likely not
        desc = self.global_descriptors[descriptor_name]
        if description not in desc.descriptions:
            self.global_descriptors[descriptor_name].add_description(description)
        else:
            # TODO: Should be using a logger
            print(f"Description: {description} has already been added to this descriptor: {descriptor_name}")

    def _ensure_asset(self, asset_name):
        """Helper method to make sure an asset name exists."""
        if not self.global_assets.get(asset_name):
            asset = Asset(name=asset_name)
            self.global_assets[asset_name] = asset
        self._set_global_asset_level()

    def _ensure_descriptor(self, descriptor_name):
        """Helper method to make sure a desriptor name exists."""
        if not self.global_descriptors.get(descriptor_name):
            desc = Descriptor(name=descriptor_name)
            self.global_descriptors[descriptor_name] = desc
        self._set_global_descriptor_level()

    def add_description_to_asset(self, asset_name, descriptor_name, description):
        """Adds a description to an asset."""

        # Sanitize
        asset_name = asset_name.lower()
        descriptor_name = descriptor_name.lower()

        # Create the asset and descriptor objects as necessary
        self._ensure_descriptor(descriptor_name)
        self._ensure_asset(asset_name)

        # Add the description to the descriptor and link descriptor to the asset
        # NOTE: Asset descriptors is a set.
        self.add_description(descriptor_name, description)
        self.link_descriptor(asset_name, descriptor_name)

    def _set_global_descriptor_level(self):
        """Level the global descriptors by checking to see if the list is a Fibonacci number in length"""
        # Calculate next fibs for descriptors
        num_descriptors = len(self.global_descriptors)
        self.global_desc_next_fib = common.get_next_fibonacci(num_descriptors)
        self.global_desc_level_up = common.is_fibonacci(num_descriptors)

    def _set_global_asset_level(self):
        """Level the global assets by checking to see if the list is a Fibonacci number in length"""
        # Calculate next fibs for descriptors
        num_assets = len(self.global_assets)
        self.global_assets_next_fib = common.get_next_fibonacci(num_assets)
        self.global_assets_level_up = common.is_fibonacci(num_assets)

    def asset_relations(self, sibling_name: str):
        """Determines if an asset relates to another asset via a shared descriptor.
        Args:
            sibling_asset: The asset looking for siblings
        """
        sibling_asset = self.global_assets.get(sibling_name)
        if not sibling_asset:
            raise errors.AssetNotFound(f"Asset {sibling_name} doesn't exist.")

        relations = {}
        for asset_name, asset_obj in self.global_assets.items():
            # Skip the sibbling_asset that was passed in
            if asset_name == sibling_asset.name:
                continue

            # All descriptors for this asset, see if one of those is in the asset to find relations
            for descriptor_name in asset_obj.descriptors:
                if descriptor_name in sibling_asset.descriptors:
                    relations[descriptor_name] = asset_obj.name
                else:
                    print(f"Descriptor name not found: {descriptor_name}")

        return relations

    def export_asset_descriptions(self, asset_name):
        """Export all descriptions for a given asset in a single list."""
        asset_obj = self.global_assets[asset_name]

        all_descriptions = []
        for desc_name in asset_obj.descriptors:
            desc = self.global_descriptors[desc_name]
            all_descriptions.extend(desc.descriptions or [])

        return all_descriptions
