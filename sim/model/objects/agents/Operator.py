"""The agents represented in the model

In the model, there are three primary agents responsible for the operation of the
instrument. The Operator is directly in controll of the beamline of the instrument.
The Data Analyst observes the AMI and determines when the data is good enough to
stop the run as well as gives updates to the Experiment Manager when there is a problem.
The Experiment Manager is responsible for the overall control of the experiment and
communicates with both the Operator and the Data Analyst to understand the state of 
the Experiment as well as make changes at a high level to improve the quality and
efficiency of the experiment.

  Typical usage example:

  DA = DataAnalyst()
  DA.check_if_enough_data_to_analyse(context)

  bar = foo.FunctionBar()
"""
import sim.model.enums as enums
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.objects.agents.Base as Base

class Operator(Base.Person):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # """Operator reponse delay combines noticing, attention shifting to button, decision delay,
    # moving to the button, and pressing it (Possibly also need attention shift into the
    # display, but we're leaving that out bcs it can be arbitrarily large)"""
    # attention shifting to button has to be computed from where we are and where the buttons are
    # current_eye_position = 0
    # left_button_position = -2 # we're actually not gonna use these but just use a fixed shift time
    # right_button_position = +2
    switch_button_delay_per_cm = None  # ms
    button_press_delay = None  # ms
    button_distance = None  # cm
    which_button_were_on = "<<"  # or ">>"
    running_peak_chasing = False
    allow_response_cycle = 99999999999

    def __init__(self, config:settings.Config):
        super().__init__(enums.AgentType.OP)
        self.switch_button_delay_per_cm = config['operator']['switch_button_delay_per_cm']
        self.button_press_delay = config['operator']['button_press_delay']
        self.button_distance = config['operator']['button_distance']
        self.functional_acuity = config['operator']['functional_acuity']
        self.noticing_delay = config['operator']['noticing_delay']
        self.decision_delay = config['operator']['decision_delay']

    def stop_collecting_data(self, context:objects.Context):
        """Stop Collecting Data"""
        context.printer("OP: [blue]Stop Collecting Data[/blue]", "OP: Stop Collecting Data")
        context.instrument.collecting_data = False

    def start_peak_chasing(self, context:objects.Context) -> bool:
        """True: communication sucessful and instrument started, False: Instrumnent not started"""
        if context.instrument.run_peak_chasing(context):
            context.printer("OP: [green]Start Peak Chasing[/green]", "OP: Start Peak Chasing")
            return True
        else:
            context.messages.concat("OP: [blue]Instrument transition[/blue]\n")
            return False

    def track_stream_position(self, context:objects.Context):
        "Move beam"
        if self.allow_response_cycle == 99999999999:
            self.allow_response_cycle = context.instrument.stream_status.cycle + self.operator_response_delay(context)
        if context.instrument.stream_status.cycle >= self.allow_response_cycle:
            context.instrument.beam_status.beam_pos = round(self.tracker_tool(context), 4)
        if abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos) < self.functional_acuity:
            self.allow_response_cycle = 99999999999

    def tracker_tool(self, context:objects.Context):
        """FFF This should use a model of visual UI-mediated visual acuity,
        rather than just exact operators."""
        which_way = self.which_way_do_we_need_to_shift(context)
        if which_way == "none":
            context.instrument.instrument_status.msg = context.instrument.instrument_status.msg + "(FA)"
            delta = abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos)
            context.instrument.stream_status.stream_pos = 0.0 + delta
            context.instrument.beam_status.beam_pos = 0.0
            return context.instrument.beam_status.beam_pos
        elif which_way == "<<":
            context.printer("OP: [blue]Move Beam <<[/blue]", "OP: Move Beam <<")
            context.instrument.instrument_status.msg = context.instrument.instrument_status.msg + "<<"
            return context.instrument.beam_status.beam_pos - context.instrument.beam_status.beam_shift_amount
        else:
            context.printer("OP: [blue]Move Beam >>[/blue]", "OP: Move Beam >>")
            context.instrument.instrument_status.msg = context.instrument.instrument_status.msg + ">>"
            return context.instrument.beam_status.beam_pos + context.instrument.beam_status.beam_shift_amount

    def which_way_do_we_need_to_shift(self, context:objects.Context):
        """Used in various places, returns '<<', '>>', 'none'"""
        delta = abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif context.instrument.beam_status.beam_pos > context.instrument.stream_status.stream_pos:
            return "<<"
        else:
            return ">>"

    def operator_response_delay(self, context:objects.Context):
        # FFF Deconvolve this
        """operator_response_delay() uses the current eye position and button distances to decide
        how many cycles it takes to hit the button, which is either short
        (you're there already), or long (you're not), the longer using the
        button distance to delay. It return an integer number of cycles to
        wait before the input arrives."""
        way = self.which_way_do_we_need_to_shift(context)
        if way == self.which_button_were_on:
            # context.messages.concat(f"button_press_delay + decision_delay + noticing_delay: [{str(self.button_press_delay + self.decision_delay + self.noticing_delay)}]\n")
            return self.button_press_delay + self.decision_delay + self.noticing_delay
        else:
            self.which_button_were_on = way
            # context.messages.concat(f"button_press_delay + decision_delay + noticing_delay: [{str((self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay)}]\n")
            return (self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay
