"""
The cognitive agents in the model
"""

from enum import Enum
class AgentType(Enum):
    """Enum to mark the different agent roles"""
    DA = "Data Analyst"
    EM = "Experiment Manager"
    OP = "Operator"

class Person:
    """Agent Parent Class"""
    agent_type = ""

    def __init__(self, agent_type):
        self.agent_type = agent_type

class DataAnalyst(Person):
    """Retrives data from the instrument"""
    def __init__(self):
        super().__init__(AgentType.DA)

    def analyse_data(self):
        """determine if the output of the instrument is good"""
        print("Check if data is good")

class ExperimentManager(Person):
    """High level GAP Goal Agenda Plan"""
    def __init__(self):
        super().__init__(AgentType.EM)

    def plan(self):
        """Given current situation plan for goal"""
        print("Create a Plan")

class Operator(Person):
    """Operator reponse delay combines noticing, attention shifting to button, decision delay,
    moving to the button, and pressing it
    (Possibly also need attention shift into the display, but we're leaving that out bcs it can be arbitrarily large)"""
    noticing_delay = 1  # 100 ms
    decision_delay = 1  # 100 ms -- FFF incorporate differential switch time
    # attention shifting to button has to be computed from where we are and where the buttons are
    # current_eye_position = 0
    # left_button_position = -2 # we're actually not gonna use these but just use a fixed shift time
    # right_button_position = +2
    switch_button_delay_per_cm = 1  # ms
    button_press_delay = 1  # ms
    button_distance = 0  # cm
    which_button_were_on = "<<"  # or ">>"
    functional_acuity = 0.01

    def __init__(self, x, y):
        super().__init__(AgentType.OP)
        self.par_stream_pos = x
        self.par_beam_pos = y

    def which_way_do_we_need_to_shift(self):
        """Used in various places, returns "<<", ">>", "none" """
        delta = abs(self.par_beam_pos - self.par_stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif self.par_beam_pos > self.par_stream_pos:
            return "<<"
        else:
            return ">>"

    def operator_response_delay(self, instrument):
        """operator_response_delay() uses the current eye position and button distances to decide
        how many cycles it takes to hit the button, which is either short
        (you're there already), or long (you're not), the longer using the
        button distance to delay. It return an integer number of cycles to
        wait before the input arrives."""
        way = self.which_way_do_we_need_to_shift()
        if way == self.which_button_were_on:
            instrument.status["msg"] = instrument.status["msg"] + "[" + str(
                self.button_press_delay + self.decision_delay + self.noticing_delay) + "]"
            return self.button_press_delay + self.decision_delay + self.noticing_delay
        else:
            self.which_button_were_on = way
            instrument.status["msg"] = instrument.status["msg"] + "[" + str((self.button_distance * self.switch_button_delay_per_cm)
                                                + self.button_press_delay + self.decision_delay + self.noticing_delay) + "]"
            return (self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay \
                   + self.decision_delay + self.noticing_delay


    def manipulate_system(self):
        """using the goal from the em change the instrument"""
        print("Modify Instrument")
