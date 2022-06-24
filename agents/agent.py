"""The cognitive agents in the model"""
from datetime import timedelta
from termcolor import colored
from data import AgentType
from instrument import CXI

class Person:
    """Agent Parent Class"""
    agent_type = ""
    # begining they will be focused, not exausted yet, 4pm things go wrong and they are tired
    focus_meter = ""

    def __init__(self, agent_type):
        self.agent_type = agent_type

class DataAnalyst(Person):
    """Retrives data from the instrument"""
    def __init__(self):
        super().__init__(AgentType.DA)

    def analyse_data(self):
        """determine if the output of the instrument is good"""
        print("Check if data is good")

class Operator(Person):
    """Operator reponse delay combines noticing, attention shifting to button, decision delay,
    moving to the button, and pressing it (Possibly also need attention shift into the
    display, but we're leaving that out bcs it can be arbitrarily large)"""
    def __init__(self):
        super().__init__(AgentType.OP)

    def start_peak_chasing(self, instrument:CXI, current_time:timedelta, file):
        """Start Peak Chasing"""
        file.write("OP: Start Peak Chasing\n")
        print("OP: " + colored("Start Peak Chasing", "blue"))
        instrument.run_peak_chasing(current_time)

class ExperimentManager(Person):
    """High level GAP Goal Agenda Plan"""
    def __init__(self):
        super().__init__(AgentType.EM)

    def start_experiment(self, instrument:CXI, file):
        """determine if the output of the instrument is good"""
        file.write("EM: Start Experiment\n")
        print("EM: " + colored("Start Experiment", "green"))
        instrument.start()

    def tell_operator_start_data_collection(self, operator:Operator, instrument:CXI, current_time:timedelta, file):
        """Communicate with operator to start collecting data"""
        file.write("EM: Communicate with Operator\n")
        print("EM: " + colored("Communicate with Operator", "blue"))
        operator.start_peak_chasing(instrument, current_time, file)

class RemoteUser(Person):
    """A user who is not present on site"""
    # TODO: Who is communicating with the remote user from inside the hutch
    def __init__(self):
        super().__init__(AgentType.RU)

    def do_stuff(self):
        """determine if the output of the instrument is good"""
        pass

class ACROperator(Person):
    """An operator who is in the Accelerator Controll Room"""
    # TODO: who is the person talking to the ACR operator in the situation that the beam dissapears or has problems
    # TODO: or they want to change the photon energy level
    def __init__(self):
        super().__init__(AgentType.ACR)

    def do_stuff(self):
        """determine if the output of the instrument is good"""
        pass
