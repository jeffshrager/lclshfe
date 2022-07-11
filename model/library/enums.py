"""Collection of enums"""
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
