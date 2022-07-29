"""These are the enums for the model

This contains enums for the model so that is is
easier to change values.
"""
from datetime import timedelta
from enum import Enum

class AgentType(Enum):
    """Summary of class here.

    Longer class information...
    Enum to mark the different agent roles

    Attributes:
        enum: The enum for the agent type.
    """
    DA = "Data Analyst"
    EM = "Experiment Manager"
    OP = "Operator"
    RU = "Remote User"
    ACR = "ACR Operator"

class InstrumentType(Enum):
    """Summary of class here.

    Longer class information...
    Enum to mark the different hutches

    Attributes:
        enum: The enum for the instrument type.
    """
    CXI = "CXI"

class InstrumentRunState(Enum):
    """Summary of class here.

    Longer class information...
    Different States of the Instrument

    Attributes:
       enum: The enum for the instrument run state.
    """
    STOPPED = False
    RUNNING = True

class ExperimentState(Enum):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        enum: The enum for the experiment state.
    """
    STOPED = False
    STARTED = True

class SampleType(Enum):
    """Summary of class here.

    Different States of the Instrument

    Attributes:
        enum: The enum for the sample type.
    """
    INSTANT = {'setup_time':timedelta(seconds=10)}
    WATER_JET = {'setup_time':timedelta(seconds=30)}
    TAPE = {'setup_time':timedelta(seconds=40)}
    OTHER = {'setup_time':timedelta(seconds=60)}

class SampleImportance(Enum):
    """Summary of class here.

    Each sample has a different level of importance

    Attributes:
        enum: The enum for the sample importance.
    """
    IMPORTANT = 2
    UNIMPORTANT = 1
    # MOST_IMPORTANT = 5
    # IMPORTANT = 4
    # LESS_IMPORTANT = 3
    # EXPERIMENTAL = 2
    # OTHER = 1
