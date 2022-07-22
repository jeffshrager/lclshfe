"""Collection of enums"""
from datetime import timedelta
from enum import Enum

class AgentType(Enum):
    """Enum to mark the different agent roles"""
    DA = "Data Analyst"
    EM = "Experiment Manager"
    OP = "Operator"
    RU = "Remote User"
    ACR = "ACR Operator"

class InstrumentType(Enum):
    """Enum to mark the different hutches"""
    CXI = "CXI"

class InstrumentRunState(Enum):
    """Different States of the Instrument"""
    STOPPED = False
    RUNNING = True

class ExperimentState(Enum):
    """Different States of the Instrument"""
    STOPED = False
    STARTED = True

class SampleType(Enum):
    """Different States of the Instrument"""
    WATER_JET = {'setup_time':timedelta(seconds=30)}
    TAPE = {'setup_time':timedelta(seconds=40)}
    OTHER = {'setup_time':timedelta(seconds=60)}

class SampleImportance(Enum):
    """Each sample has a different level of importance"""
    IMPORTANT = 2
    UNIMPORTANT = 1
    # MOST_IMPORTANT = 5
    # IMPORTANT = 4
    # LESS_IMPORTANT = 3
    # EXPERIMENTAL = 2
    # OTHER = 1
