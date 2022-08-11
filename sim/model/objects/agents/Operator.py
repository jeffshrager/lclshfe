"""The operator agent class

The operator is responsible for the overall control of the experiment.
This includes peak chasing the beam and controlling the instrument to make sure
that the data is being maximized and that the beam is not lost.

  Typical usage example:

  OP = Operator()
  DA.start_peak_chasing(context)
"""
import sim.model.enums as enums
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.objects.agents.base as base

class Operator(base.Person):
    """The operator extends the base class Person

    The operator is responsible for the overall control of the experiment.
    This includes peak chasing the beam and controlling the instrument to make sure
    that the data is being maximized and that the beam is not lost.
    Operator reponse delay combines noticing, attention shifting to button, decision delay,
    moving to the button, and pressing it (Possibly also need attention shift into the
    display, but we're leaving that out bcs it can be arbitrarily large)
    attention shifting to button has to be computed from where we are and where the buttons are

    Attributes:
        Base.Person: The name of the operator
    """
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
        """Stop Collecting Data

        Changes the state of the instrument from collecting data to not collecting data.

        Args:
            context: The context of the experiment.
        """
        context.printer("OP: [blue]Stop Collecting Data[/blue]", "OP: Stop Collecting Data")
        context.instrument.collecting_data = False

    def start_peak_chasing(self, context:objects.Context) -> bool:
        """Starts peak chasing of the beam and stream

        Runs peak chasing of the beam and stream on the instrument.
        This is by calling run_peak_chasing.

        Args:
            context: The context of the experiment.

        Returns:
            True: communication sucessful and instrument started
            False: Instrumnent not started
        """
        if context.instrument.run_peak_chasing(context):
            context.printer("OP: [green]Start Peak Chasing[/green]", "OP: Start Peak Chasing")
            return True
        else:
            context.messages.concat("OP: [blue]Instrument transition[/blue]\n")
            return False

    def track_stream_position(self, context:objects.Context):
        """Moving the beam to the stream position

        Determines where the steam is and moves the beam to that position.

        Args:
            context: The context of the experiment.
        """
        if self.allow_response_cycle == 99999999999:
            self.allow_response_cycle = context.instrument.stream_status.cycle + self.operator_response_delay(context)
        if context.instrument.stream_status.cycle >= self.allow_response_cycle:
            context.instrument.beam_status.beam_pos = round(self.tracker_tool(context), 4)
        if abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos) < self.functional_acuity:
            self.allow_response_cycle = 99999999999

    def tracker_tool(self, context:objects.Context):
        """Tracks which way the beam needs to be shifted to get to the stream position

        This should use a model of visual UI-mediated visual acuity,
        rather than just exact operators.

        Args:
            context: The context of the experiment.
        """
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
        """Used in various places

        Determines which way the beam needs to be shifted to get to the stream position.

        Args:
            context: The context of the experiment.

        Returns:
             returns '<<', '>>', 'none'
        """
        delta = abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif context.instrument.beam_status.beam_pos > context.instrument.stream_status.stream_pos:
            return "<<"
        else:
            return ">>"

    def operator_response_delay(self, context:objects.Context):
        """Determines the operator response delay

        operator_response_delay() uses the current eye position and button distances to decide
        how many cycles it takes to hit the button, which is either short
        (you're there already), or long (you're not), the longer using the
        button distance to delay. It return an integer number of cycles to
        wait before the input arrives.

        Args:
            context: The context of the experiment.
        """
        way = self.which_way_do_we_need_to_shift(context)
        if way == self.which_button_were_on:
            # context.messages.concat(f"button_press_delay + decision_delay + noticing_delay: [{str(self.button_press_delay + self.decision_delay + self.noticing_delay)}]\n")
            return self.button_press_delay + self.decision_delay + self.noticing_delay
        else:
            self.which_button_were_on = way
            # context.messages.concat(f"button_press_delay + decision_delay + noticing_delay: [{str((self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay)}]\n")
            return (self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay
