"""File for the data objects and classes used"""
from datetime import timedelta
from enum import Enum

# Enums
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

class InstrumentStatus(Enum):
    """Different States of the Instrument"""
    STOPPED = False
    RUNNING = True

# Classes
class Goal:
    """Defines what is supposed to be acomplished"""
    datapoints_needed_per_sample = 10000
    samples = []
    status = None

    def __init__(self, datapoints_needed_per_sample, number_of_samples):
        self.datapoints_needed_per_sample = datapoints_needed_per_sample
        self.samples = [0] * number_of_samples

    def finished(self):
        """Finished experiment"""
        self.status = "compleated"

    def __str__(self):
        return (f"Datapoints needed: {self.datapoints_needed_per_sample}, "+
                f"Samples: {self.samples}")

class Agenda:
    """High Level Schedule of events for acheiving the goal"""
    current_time = timedelta(0)
    experimental_time = timedelta(0)
    event_timeline = []

    def __init__(self, experimental_time):
        self.experimental_time = experimental_time

    def add_event(self, run_number:int, start_time:timedelta, end_time:timedelta):
        """Add event to agenda timeline"""
        self.event_timeline.append({"run_number":run_number,
                "start_time":start_time, "end_time":end_time})

    def __str__(self):
        return (f"Current Time: {self.current_time}, " +
                f"Experimental Time: {self.experimental_time}")

    def print_timeline(self):
        """print final timeline"""
        return_string = ""
        for event in self.event_timeline:
            return_string+=(f"Run: {event['run_number']},"+
                f" Start: {event['start_time']}, End: {event['end_time']}\n")
        return return_string
