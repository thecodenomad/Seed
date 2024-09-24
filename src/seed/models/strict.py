"""Contains the Strict BaseModel used for validating and sanitizing."""

from pydantic import BaseModel


class StrictModel(BaseModel):
    """Provides a single variable to fascilitate validation and sanitation."""

    strict: bool = False
    # TODO: Move similar validations in here?
