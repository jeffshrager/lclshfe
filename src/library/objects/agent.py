"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from functools import reduce
from datetime import timedelta
from termcolor import colored
from scipy.stats import linregress
from src.library.enums.jig_enums import SaveType
from src.library.enums.model_enums import AgentType
from src.library.functions.func import clamp, cognative_temperature_curve
from src.library.objects.objs import Context, SampleData
from src.settings.config import Config

class Person:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    agent_type = ""
    # TODO: Add system stability affect attention level
    # If the system is unstable attention should increase, if system is stable attention
    # will decrease, We know what the status of the system is use this to callibrate
    # the system, begining they will be focused, not exausted yet, 4pm things go
    # wrong and they are tired

    # TODO: Analygous attentional properties will attach to data analyst
    # Hot vs cold cognition, hot rappid makes more mistakes, cold slower more accurate
    # Eventually check when worrying check all the time, when not check once in a while
    # TODO: Attention/ exaustion/ focus controlls for ever person
    # TODO _: Add Attention
    # TODO: begining they will be focused, not exausted yet, 4pm things go wrong and they are tired
    cognative_temperature:float = None
    cogtemp_curve:float = None
    # 1.0 / 0.002 = 8.3, total level of energy / minutes = 8.3 total hours of energy
    energy_degradation:float = 0.002
    attention_meter:float = None
    previous_check:timedelta = None
    noticing_delay:float = 1.0  # 100 ms
    decision_delay:float = 1.0  # 100 ms -- FFF incorporate differential switch time
    functional_acuity:float = 0.01

    def __init__(self, agent_type):
        self.agent_type = agent_type
        self.cognative_temperature = 1.0
        self.cogtemp_curve = 0.0
        self.attention_meter = 1.0
        self.previous_check = timedelta(0)

    def get_energy(self):
        """get the level of energy"""
        return self.cognative_temperature

    def get_attention(self):
        """get the level of attention"""
        return self.cogtemp_curve

    def update(self, context:Context):
        """Calculate agents attention and focus each cycle

        Goes through each sample and determines if they all were compleated.
        If they were, the ROI would be 100%, if not the roi percent
        is calculated.

        Args:
            ami: an AMI object which contains all the data and the state
            that the sample is in.

        Returns:
            A string that is the ROI of the experiment. In percent.
        """
        # TODO _: energy degredation on a curve
        # TODO: coupled also on a curve
        if context['cognative_degredation']:
            delta:timedelta = context.current_time - self.previous_check
            if delta >= timedelta(minutes=1):
                self.cogtemp_curve = clamp(self.cogtemp_curve + self.energy_degradation, 0.0, 1.0)
                self.cognative_temperature = clamp(cognative_temperature_curve(self.cogtemp_curve), 0.01, 1.0)
                self.previous_check = context.current_time
            self.noticing_delay = 1 + (1 - self.cognative_temperature)
            self.decision_delay = 1 + (1 - self.cognative_temperature)

class DataAnalyst(Person):
    """The Data Analyst will be able to predict the error of the current sample

    Longer class information...
    Longer class information...

    Attributes:
        Person: A boolean indicating if we like SPAM or not.
    """
    # """Retrives data from the instrument"""
    projected_intercept:float = None
    target_error:float = None
    predictions:list = []

    def __init__(self, config:Config):
        super().__init__(AgentType.DA)
        self.last_sample_with_enough_data = None
        self.target_error = config['data_analysis']['target_error']

    def check_if_enough_data_to_analyse(self, context:Context) -> bool:
        """Check if there is enough data to start analysing, right now this is a constant"""
        # III: Reconnect prediction to operation
        current_sample = context.ami.samples[context.instrument.current_sample]
        if current_sample.count > 100:
            if self.projected_intercept is None or self.projected_intercept <= current_sample.count:
                last_count_array = current_sample.count_array[-10000:]
                last_err_array = current_sample.err_array[-10000:]
                regression = linregress(last_count_array[::100], last_err_array[::100])
                self.projected_intercept = (self.target_error - regression.intercept) / regression.slope
                context.ami.samples[context.instrument.current_sample].projected_intercept = self.projected_intercept
                if self.projected_intercept <= current_sample.count:
                    context.printer(f"DA: Data from run {context.instrument.run_number} {colored('has enough data to analyse', 'green')}", f"DA: Data from run {context.instrument.run_number} has enough data to analyse")
            return True
        return False

    def check_if_data_is_sufficient(self, context:Context) -> bool:
        """If there is enough data True, else False to ask to keep running"""
        # TODO: Ask Instrument scientist to see what is the real decision logic stopping criteria
        current_sample = context.ami.samples[context.instrument.current_sample]
        # TODO: DA does not have access to preformance quality
        #  Determine that the mean is settling
        if current_sample.err <= self.target_error:
            context.printer(f"DA: Data from run {context.instrument.run_number} {colored('is good', 'green')}", f"DA: Data from run {context.instrument.run_number} is good")
            context.agenda.add_event(context.instrument.run_number, context.instrument.run_start_time, context.current_time, current_sample, False)
            current_sample.compleated = True
            self.projected_intercept = None
            return True
        context.printer(f"DA: {colored('More data needed from run', 'yellow')} {context.instrument.run_number}", f"DA: More data needed from run {context.instrument.run_number}")
        return False

    def check_if_experiment_is_compleated(self, context:Context):
        """Check if experiment is compleated"""
        current_sample = None
        for index, sample_goal in enumerate(context.ami.samples):
            if not sample_goal.compleated:
                current_sample = index
                break
        if current_sample is None:
            context.agenda.finished()

class Operator(Person):
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

    def __init__(self, config:Config):
        super().__init__(AgentType.OP)
        self.switch_button_delay_per_cm = config['operator']['switch_button_delay_per_cm']
        self.button_press_delay = config['operator']['button_press_delay']
        self.button_distance = config['operator']['button_distance']
        self.functional_acuity = config['operator']['functional_acuity']
        self.noticing_delay = config['operator']['noticing_delay']
        self.decision_delay = config['operator']['decision_delay']

    def stop_collecting_data(self, context:Context):
        """Stop Collecting Data"""
        context.printer(f"OP: {colored('Stop Collecting Data', 'blue')}", "OP: Stop Collecting Data")
        context.instrument.collecting_data = False

    def start_peak_chasing(self, context:Context) -> bool:
        """True: communication sucessful and instrument started, False: Instrumnent not started"""
        if context.instrument.run_peak_chasing(context):
            context.printer(f"OP: {colored('Start Peak Chasing', 'green')}", "OP: Start Peak Chasing")
            return True
        else:
            context.messages.concat(f"OP: {colored('Instrument transition', 'blue')}\n")
            return False

    def track_stream_position(self, context:Context):
        "Move beam"
        if self.allow_response_cycle == 99999999999:
            self.allow_response_cycle = context.instrument.stream_status.cycle + self.operator_response_delay(context)
        if context.instrument.stream_status.cycle >= self.allow_response_cycle:
            context.instrument.beam_status.beam_pos = round(self.tracker_tool(context), 4)
        if abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos) < self.functional_acuity:
            self.allow_response_cycle = 99999999999

    def tracker_tool(self, context:Context):
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
            context.printer(f"OP: {colored('Move Beam <<', 'blue')}", "OP: Move Beam <<")
            context.instrument.instrument_status.msg = context.instrument.instrument_status.msg + "<<"
            return context.instrument.beam_status.beam_pos - context.instrument.beam_status.beam_shift_amount
        else:
            context.printer(f"OP: {colored('Move Beam >>', 'blue')}", "OP: Move Beam >>")
            context.instrument.instrument_status.msg = context.instrument.instrument_status.msg + ">>"
            return context.instrument.beam_status.beam_pos + context.instrument.beam_status.beam_shift_amount

    def which_way_do_we_need_to_shift(self, context:Context):
        """Used in various places, returns '<<', '>>', 'none'"""
        delta = abs(context.instrument.beam_status.beam_pos - context.instrument.stream_status.stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif context.instrument.beam_status.beam_pos > context.instrument.stream_status.stream_pos:
            return "<<"
        else:
            return ">>"

    def operator_response_delay(self, context:Context):
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

class ExperimentManager(Person):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # """High level GAP Goal Agenda Plan"""
    previous_transition_check:timedelta = None
    transition_time:timedelta = None
    current_transition_time:timedelta = None
    max_transition_time:timedelta = None

    current_sample_switch_time:timedelta = None
    previous_switch_check:timedelta = timedelta(0)
    previous_sample:SampleData = None

    # current_data_check_time:timedelta = None
    previous_data_check:timedelta = None
    data_check_wait:timedelta = timedelta(minutes=1)

    def __init__(self, config:Config):
        super().__init__(AgentType.EM)
        self.max_transition_time = config['instrument']['sample_transition_time']


    def start_experiment(self, context:Context):
        """Start Experiment and load samples"""
        context.agenda.start_experiment()
        context.printer(f"EM: {colored('Load Samples', 'green')}", 'EM: Load Samples')
        context.ami.load_samples(context)
        context.printer('EM: sort samples by PQ in decending order',
         'EM: sort samples by PQ in decending order')
        context.ami.sort_samples()

    def start_instrument(self, context:Context):
        """determine if the output of the instrument is good"""
        context.printer(f"EM: {colored('Start Instrument', 'green')}", 'EM: Start Instrument')
        context.instrument.start()

    def sample_change_logic(self, context:Context):
        """Sample change logic"""
        num_samples_done = len(context.agenda.event_timeline)
        if num_samples_done >= 2:
            this_run_pq = context.agenda.event_timeline[num_samples_done-1].sample.preformance_quality
            this_run_length = context.agenda.event_timeline[num_samples_done-1].duration
            last_run_pq = context.agenda.event_timeline[num_samples_done-2].sample.preformance_quality
            last_run_length = context.agenda.event_timeline[num_samples_done-2].duration
            pq_delta:float = round(last_run_pq - this_run_pq,5)
            run_length_delta:timedelta = timedelta(seconds=abs(last_run_length.total_seconds() - this_run_length.total_seconds()))
            estimated_delta_seconds_per_pq:float = round(abs(run_length_delta.total_seconds()/pq_delta))
            estimated_run_length_map = [timedelta(seconds=(sample.duration.total_seconds() + round(((s*pq_delta) * estimated_delta_seconds_per_pq)))) for s, sample in enumerate(context.ami.samples) if sample.compleated is False]
            estimated_total_time_for_remaining_samples:timedelta = reduce(lambda a, b: a + b, estimated_run_length_map)
            time_remaining:timedelta = context.agenda.experimental_time - context.current_time
            projected_seconds_overtime:float = time_remaining.total_seconds() - estimated_total_time_for_remaining_samples.total_seconds()
            if projected_seconds_overtime < 0:
                if context.agent_da.target_error == context['data_analysis']['target_error'] * 10:
                    pass
                else:
                    context.agent_da.target_error+=context['data_analysis']['target_error']
            elif projected_seconds_overtime > 500:
                if context.agent_da.target_error == context['data_analysis']['target_error']:
                    pass
                else:
                    context.agent_da.target_error-=context['data_analysis']['target_error']

    def check_if_next_run_can_be_started(self, context:Context) -> bool:
        """Check to see if the sample needs to be changed if so wait"""
        next_sample:SampleData
        # TODO: Ask person to change sample
        if context.instrument.current_sample is not None:
            if len(context.ami.samples) == (context.instrument.current_sample + 1):
                return False
            next_sample = context.ami.samples[context.instrument.current_sample+1]
        else:
            next_sample = context.ami.samples[0]
        if self.previous_sample is not None:
            if self.current_transition_time is None:
                self.current_transition_time = self.max_transition_time
                # self.current_transition_time = timedelta(minutes=random.uniform(0.2, 2.0))
                if context['settings']['save_type'][0] == SaveType.DETAILED:
                    context.file_write(f"Instrument transition: {self.current_transition_time}")
            if self.current_transition_time > timedelta(0):
                if self.previous_transition_check is None:
                    self.previous_transition_check = context.current_time
                else:
                    context.messages.concat(f"Instrument transition: {colored(f'{self.current_transition_time}', 'blue')}\n")
                    self.current_transition_time -= context.current_time - self.previous_transition_check
                    self.previous_transition_check = context.current_time
                    return False
            else:
                self.previous_transition_check = None
                self.current_transition_time = None
                self.sample_change_logic(context)
                return True
            return False
        if self.current_sample_switch_time is None:
            self.current_sample_switch_time = next_sample.setup_time
        self.current_sample_switch_time -= context.current_time - self.previous_switch_check
        self.previous_switch_check = context.current_time
        if self.current_sample_switch_time <= timedelta(0):
            self.current_sample_switch_time = None
            self.previous_sample = next_sample
            self.sample_change_logic(context)
            return True
        else:
            context.messages.concat(f"Sample: {0 if context.instrument.current_sample is None else context.instrument.current_sample + 1}, Setting up: {colored(f'{self.current_sample_switch_time}', 'blue')}\n")
            return False

    def tell_operator_start_data_collection(self, context:Context):
        """Communicate with operator to start collecting data"""
        if context.agent_op.start_peak_chasing(context):
            context.printer(f"EM: {colored('Communicate with Operator', 'green')}", 'EM: Communicate with Operator')
        else:
            context.messages.concat(f"EM: {colored('Instrument cannot start', 'blue')}")

    def check_if_data_is_sufficient(self, context:Context):
        """Communiate with the data analyst to see if the run has enough
        data or if the run needs to continue, if so tell the operator to continue
        the run for longer"""
        # TODO _: Check if run should be stopped as something is wrong with Standard deviation
        if context.agent_da.check_if_enough_data_to_analyse(context):
        # and 0 == random.randint(0, 30):
            # TODO: Timer
            # if self.previous_data_check is None:
            #     self.previous_data_check = context.current_time
            # elif self.previous_data_check + self.data_check_wait <= context.current_time:
            #     self.previous_data_check = context.current_time
            # else:
            #     return False
            context.printer(f"EM: {colored('Ask DA if data is sufficient', 'green')}", "EM: Ask DA if data is sufficient")
            if context.agent_da.check_if_data_is_sufficient(context):
                context.printer(f"EM: {colored('Tell operator to stop collecting data', 'blue')}", "EM: Tell operator to stop collecting data")
                context.agent_op.stop_collecting_data(context)
            # TODO _: Does operator keep going until told to stop or do they need to be told to keep going

class RemoteUser(Person):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # FFF: Who is communicating with the remote user from inside the hutch
    def __init__(self):
        super().__init__(AgentType.RU)

class ACROperator(Person):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # FFF: who is the person talking to the ACR operator in
    # the situation that the beam dissapears or has problems
    # FFF: or they want to change the photon energy level
    def __init__(self):
        super().__init__(AgentType.ACR)
