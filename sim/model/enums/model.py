"""These are the enums for the model

This contains enums for the model so that is is
easier to change values.
"""
from datetime import timedelta
from enum import Enum

class AgentType(Enum):
    """The type of the agents

    Determine what the agent is.

    Attributes:
        enum: The enum for the agent type.
    """
    DA = "Data Analyst"
    EM = "Experiment Manager"
    OP = "Operator"
    RU = "Remote User"
    ACR = "ACR Operator"

class InstrumentType(Enum):
    """The type of the insturment

    Future right now this is just for CXI but
    when instruments are added this will be used.

    Attributes:
        enum: The enum for the agent type.
    """
    CXI = "CXI"

class InstrumentRunState(Enum):
    """The state of the instrument

    Determine if the instrument is running or not.

    Attributes:
        enum: The enum for the agent type.
    """
    STOPPED = False
    RUNNING = True

class ExperimentState(Enum):
    """The state of the experiment

    If the experiment is running or not.

    Attributes:
        enum: The enum for the agent type.
    """
    STOPED = False
    STARTED = True

class ExperimentManagerAlgorithm(Enum):
    """Future, the algorithm to use for the experiment manager

    Future, the algorithm to use for the experiment manager

    Attributes:
        enum: The enum for the agent type.
    """
    THIS = 1
    THAT = 2

class SampleType(Enum):
    """The type of the sample

    This determines how long it takes to setup
    the sample as well as other sample paramters.

    Attributes:
        enum: The enum for the agent type.
    """
    INSTANT = {'setup_time':timedelta(seconds=10)}
    WATER_JET = {'setup_time':timedelta(seconds=30)}
    TAPE = {'setup_time':timedelta(seconds=40)}
    OTHER = {'setup_time':timedelta(seconds=60)}

class SampleImportance(Enum):
    """The importance of the sample

    Used to determine the importance of the sample.
    This will interact with the other parameters to
    maximize data for the samples. This also includes
    the color to display the sample in the output.

    Attributes:
        enum: The enum for the agent type.
    """
    IMPORTANT = {'importance':2, 'color':'cyan'}
    UNIMPORTANT = {'importance':1, 'color':'magenta'}
    # MOST_IMPORTANT = 5s
    # IMPORTANT = 4
    # LESS_IMPORTANT = 3
    # EXPERIMENTAL = 2
    # OTHER = 1
