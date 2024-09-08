#
# Module to handle custom seed exceptions
#

class SeedException(Exception):
    """Base seed exception"""

class AssetNotFound(SeedException):
    """Occurs when an Asset doesn't exist in memory"""

class FailedDescriptionLength(SeedException):
    """Occurs when a description length doesn't meet the matched fibonacci sequence
    criteria"""

class LevelUpException(SeedException):
    """Occurs when hashtag number doesn't meet the minimum base requirement for an
    asset"""
