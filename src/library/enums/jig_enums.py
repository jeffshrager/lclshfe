"""These are the enums for the configuration of the Jig.

This contains enums for the config dictonary so that is is
easier to change values.
"""
from enum import Enum

class SaveType(Enum):
    """The save type for the Jig.

    Detailed will print all of the information about each data point.
    This will produce a huge output and will have every thing that
    the jig does.
    The collapsed will only print a summary of the data in a much smaller
    file but is fine for graphing.

    Attributes:
        enum: The enum for the save type.
    """
    DETAILED = "DETAILED"
    COLLAPSED = "COLLAPSED"
