"""The cognitive agents in the model"""
from datetime import timedelta
import random
from termcolor import colored
from model.library.enums import AgentType
from model.library.objects import Agenda, Context, SampleData

class Person:
    """Agent Parent Class"""
    agent_type = ""
    # TODO: begining they will be focused, not exausted yet, 4pm things go wrong and they are tired
    focus_meter = None
    # TODO: Add Attention
    attention = None

    def __init__(self, agent_type):
        self.agent_type = agent_type

class DataAnalyst(Person):
    """Retrives data from the instrument"""
    def __init__(self):
        super().__init__(AgentType.DA)

    def analyse_data(self, context:Context):
        """determine if the output of the instrument is good"""
        context.messages.concat("Check if data is good\n")

    def check_if_data_is_sufficient(self, context:Context):
        """Check if data is good"""
        # TODO: Ask Instrument scientist to see what is the real decision logic stopping criteria
        s_goal:SampleData = context.goal.samples[context.instrument_cxi.current_sample][0]
        # good_data_count:int = 0
        # for data in s_goal.data:
        #     if data.quality == 100:
        #         good_data_count += 1
        total_data_count:float = 0.0
        for data in s_goal.data:
            total_data_count += data.quality
        if total_data_count >= s_goal.datapoints_needed:
            context.file.write(f"{context.current_time} | DA: Data from run {context.instrument_cxi.run_number} is good\n")
            context.messages.concat(f"DA: Data from run {context.instrument_cxi.run_number} {colored('is good', 'green')}\n")
            context.agent_em.agenda.add_event(context.instrument_cxi.run_number, context.instrument_cxi.run_start_time, context.current_time)
            context.instrument_cxi.collecting_data = False


    def check_if_experiment_is_compleated(self, context:Context):
        """Check if experiment is compleated"""
        current_sample = None
        for index, sample_goal in enumerate(context.goal.samples):
            s_goal:SampleData = sample_goal[0]
            if len(s_goal.data) < s_goal.datapoints_needed:
                current_sample = index
                break
        if current_sample is None:
            context.goal.finished()

class Operator(Person):
    """Operator reponse delay combines noticing, attention shifting to button, decision delay,
    moving to the button, and pressing it (Possibly also need attention shift into the
    display, but we're leaving that out bcs it can be arbitrarily large)"""
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

    def __init__(self):
        super().__init__(AgentType.OP)

    def start_peak_chasing(self, context:Context) -> bool:
        """True: communication sucessful and instrument started, False: Instrumnent not started"""
        if context.instrument_cxi.run_peak_chasing(context):
            context.file.write(f"{context.current_time} | OP: Start Peak Chasing\n")
            context.messages.concat(f"OP: {colored('Start Peak Chasing', 'green')}\n")
            return True
        else:
            context.messages.concat(f"OP: {colored('Instrument transition', 'blue')}\n")
            return False

    def track_stream_position(self, context:Context):
        "Move beam"
        context.instrument_cxi.beam_status.beam_pos = round(self.tracker_tool(context), 4)

    def tracker_tool(self, context:Context):
        """FFF This should use a model of visual UI-mediated visual acuity,
        rather than just exact operators."""
        which_way = self.which_way_do_we_need_to_shift(context.instrument_cxi.stream_status.stream_pos, context.instrument_cxi.beam_status.beam_pos)
        if which_way == "none":
            context.instrument_cxi.instrument_status.msg = context.instrument_cxi.instrument_status.msg + "(FA)"
            return context.instrument_cxi.beam_status.beam_pos
        elif which_way == "<<":
            context.file.write(f"{context.current_time} | OP: Move Beam <<\n")
            context.messages.concat(f"OP: {colored('Move Beam <<', 'blue')}\n")
            context.instrument_cxi.instrument_status.msg = context.instrument_cxi.instrument_status.msg + "<<"
            return context.instrument_cxi.beam_status.beam_pos - context.instrument_cxi.beam_status.beam_shift_amount
        else:
            context.file.write(f"{context.current_time} | OP: Move Beam >>\n")
            context.messages.concat(f"OP: {colored('Move Beam >>', 'blue')}\n")
            context.instrument_cxi.instrument_status.msg = context.instrument_cxi.instrument_status.msg + ">>"
            return context.instrument_cxi.beam_status.beam_pos + context.instrument_cxi.beam_status.beam_shift_amount

    def which_way_do_we_need_to_shift(self, par_stream_pos, par_beam_pos):
        """Used in various places, returns '<<', '>>', 'none'"""
        delta = abs(par_beam_pos - par_stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif par_beam_pos > par_stream_pos:
            return "<<"
        else:
            return ">>"

class ExperimentManager(Person):
    """High level GAP Goal Agenda Plan"""
    agenda:Agenda = None
    
    previous_transition_check:timedelta = None
    transition_time:timedelta = timedelta(minutes=1)
    current_transition_time:timedelta = None

    current_sample_switch_time:timedelta = None
    previous_switch_check:timedelta = timedelta(0)
    previous_sample:SampleData = None

    def __init__(self, experiment_time:timedelta):
        super().__init__(AgentType.EM)
        self.agenda = Agenda(experiment_time)

    def start_experiment(self, context:Context):
        """determine if the output of the instrument is good"""
        context.file.write(f"{context.current_time} | EM: Start Experiment\n")
        context.messages.concat(f"EM: {colored('Start Experiment', 'green')}\n")
        context.instrument_cxi.start()

    def check_if_next_run_can_be_started(self, context:Context) -> bool:
        """Check to see if the sample needs to be changed if so wait
        TODO: Ask person to change sample"""
        # TODO: Simplify
        if context.instrument_cxi.current_sample is None:
            next_sample:SampleData = context.goal.samples[0][0]
        elif context.instrument_cxi.current_sample is not None:
            next_sample:SampleData = context.goal.samples[context.instrument_cxi.current_sample+1][0]
        if self.previous_sample is not None:
            if self.previous_sample.type == next_sample.type:
                if self.current_transition_time is None:
                    self.current_transition_time = timedelta(minutes=random.uniform(0.2, 2.0))
                if self.current_transition_time > timedelta(0):
                    if self.previous_transition_check is None:
                        self.previous_transition_check = context.current_time
                    else:
                        context.file.write(f"{context.current_time} | Instrument transition: {self.current_transition_time}\n")
                        context.messages.concat(f"Instrument transition: {colored(f'{self.current_transition_time}', 'blue')}\n")
                        self.current_transition_time -= context.current_time - self.previous_transition_check
                        self.previous_transition_check = context.current_time
                        return False
                else:
                    self.previous_transition_check = None
                    self.current_transition_time = None
                    return True
                return False
            self.previous_switch_check = context.current_time
            self.previous_sample = None
        if self.current_sample_switch_time is None:
            self.current_sample_switch_time = next_sample.setup_time
        self.current_sample_switch_time -= context.current_time - self.previous_switch_check
        self.previous_switch_check = context.current_time
        context.messages.concat(f"Sample: {0 if context.instrument_cxi.current_sample is None else context.instrument_cxi.current_sample + 1}, Setting up: {colored(f'{self.current_sample_switch_time}', 'blue')}\n")
        if self.current_sample_switch_time == timedelta(0):
            self.current_sample_switch_time = None
            self.previous_sample = next_sample
            return True
        else:
            return False

    def tell_operator_start_data_collection(self, context:Context):
        """Communicate with operator to start collecting data"""
        if context.agent_op.start_peak_chasing(context):
            context.file.write(f"{context.current_time} | EM: Communicate with Operator\n")
            context.messages.concat(f"EM: {colored('Communicate with Operator', 'green')}\n")
        else:
            context.messages.concat(f"EM: {colored('Instrument cannot start', 'blue')}\n")

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
