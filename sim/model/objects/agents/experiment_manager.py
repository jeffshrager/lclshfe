"""The experiment manager agent

The experiment manager agent is responsible for managing the experiment.
This is the main agent that ensures that the experiment is running and
that the data is being collected. The experiment manager is also responsible
for changing the error and ensuring that the data is being collected
within the given timeframe.

  Typical usage example:

  EM = ExperimentManager()
  EM.check_if_enough_data_to_analyse(context)

  bar = foo.FunctionBar()
"""
from functools import reduce
from datetime import timedelta
import sim.model.enums as enums
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.objects.agents.Base as base

class ExperimentManager(base.Person):
    """Experiment Manager Logic

    The experiment manager agent is responsible for managing the experiment.
    This is the main agent that ensures that the experiment is running and
    that the data is being collected. The experiment manager is also responsible
    for changing the error and ensuring that the data is being collected
    within the given timeframe.
    """
    # """High level GAP Goal Agenda Plan"""
    previous_transition_check:timedelta = None
    transition_time:timedelta = None
    current_transition_time:timedelta = None
    max_transition_time:timedelta = None

    current_sample_switch_time:timedelta = None
    previous_switch_check:timedelta = timedelta(0)
    previous_sample:objects.SampleData = None

    # current_data_check_time:timedelta = None
    previous_data_check:timedelta = None
    data_check_wait:timedelta = timedelta(minutes=1)

    amount_of_time_to_save:timedelta = timedelta(seconds=30)
    # new_error_value:float = None

    def __init__(self, config:settings.Config):
        super().__init__(enums.AgentType.EM)
        self.max_transition_time = config['instrument']['sample_transition_time']


    def start_experiment(self, context:objects.Context):
        """Start Experiment and load samples"""
        context.agenda.start_experiment()
        context.printer("EM: [green]Load Samples[/green]", 'EM: Load Samples')
        context.ami.load_samples(context)
        if context['experiment_manager']['experimental_time_to_prediction']:
            context.config.default_dictionary['experimental_time'] = timedelta(seconds=sum([sample.estimated_run_length.total_seconds() for sample in context.ami.samples]))
        context.printer('EM: sort samples by PQ in decending order',
         'EM: sort samples by PQ in decending order')
        # context.ami.sort_samples()

    def start_instrument(self, context:objects.Context):
        """determine if the output of the instrument is good"""
        context.printer("EM: [green]Start Instrument[/green]", 'EM: Start Instrument')
        context.instrument.start()

    def sample_change_logic(self, context:objects.Context):
        """Sample change logic"""
        # TODO: add algorithm to config
        # TODO: add back time estimation
        num_samples_done = len(context.agenda.event_timeline)
        if num_samples_done >= 2:
            this_run_pq = context.agenda.event_timeline[num_samples_done-1].sample.preformance_quality
            this_run_length = context.agenda.event_timeline[num_samples_done-1].duration
            last_run_pq = context.agenda.event_timeline[num_samples_done-2].sample.preformance_quality
            last_run_length = context.agenda.event_timeline[num_samples_done-2].duration
            pq_delta:float = round(last_run_pq - this_run_pq,5)
            context.printer(f"EM: Preformance Quality Delta {'[green]'if (pq_delta > 0) else '[red]'}{pq_delta}", f'EM: Preformance Quality Delta {pq_delta}')
            run_length_delta:timedelta = timedelta(seconds=abs(last_run_length.total_seconds() - this_run_length.total_seconds()))
            context.printer(f"EM: Run Length Delta [green]{run_length_delta}", f'EM: Run Length Delta {run_length_delta}')
            estimated_delta_seconds_per_pq:float = round(abs(run_length_delta.total_seconds()/pq_delta))
            context.printer(f"EM: Estimated Delta Seconds Per PQ [green]{estimated_delta_seconds_per_pq}", f'EM: Estimated Delta Seconds Per PQ {estimated_delta_seconds_per_pq}')


            for s, sample in enumerate(context.ami.samples):
                if sample.completed is False:
                    sample.estimated_run_length = timedelta(seconds=(sample.duration.total_seconds() + round((((1+s)*pq_delta) * estimated_delta_seconds_per_pq))))


            estimated_run_length_map = [timedelta(seconds=(sample.duration.total_seconds() + round((((1+s)*pq_delta) * estimated_delta_seconds_per_pq)))) for s, sample in enumerate(context.ami.samples) if sample.completed is False]
            
            
            
            context.printer(f"EM: Estimated Run Length Map [green]{[str(run_length) for run_length in estimated_run_length_map]}", f'EM: Estimated Run Length Map {estimated_run_length_map}')
            estimated_total_time_for_remaining_samples:timedelta = reduce(lambda a, b: a + b, estimated_run_length_map)
            context.printer(f"EM: Estimated Total Time for Remaining Samples [green]{estimated_total_time_for_remaining_samples}[/green]", f'EM: Estimated Total Time for Remaining Samples {estimated_total_time_for_remaining_samples}')
            time_remaining:timedelta = context.agenda.experimental_time - context.current_time
            context.printer(f"EM: Time Remaining [green]{time_remaining}", f'EM: Time Remaining {time_remaining}')
            projected_seconds_overtime:float = time_remaining.total_seconds() - estimated_total_time_for_remaining_samples.total_seconds()
            context.printer(f"EM: Projected Seconds Overtime {'[green]' if (projected_seconds_overtime > 0) else '[red]'}{projected_seconds_overtime}{'[/green]' if (projected_seconds_overtime > 0) else '[/red]'}", f'EM: Projected Seconds Overtime {projected_seconds_overtime}')
            
            
            # Increase error threshold to save time

            
            if projected_seconds_overtime < 0:
                context.printer("EM: [red]*** WERE GOING TO RUN OUT OF TIME! ***[/red]", 'EM: *** WERE GOING TO RUN OUT OF TIME! ***')
                if context.agent_da.target_error == context['data_analysis']['target_error'] * 10:
                    context.printer("EM: [red]!!!!!! Uh oh! Theres no room to increase error_threshold!!!", 'EM: !!!!!! Uh oh! Theres no room to increase error_threshold!!!')
                else:

                    #  array_check_point = self.previous_sample.duration.total_seconds() - self.amount_of_time_to_save.total_seconds()
                    temp_check = abs(projected_seconds_overtime) / len(estimated_run_length_map)
                    # while temp_check > self.previous_sample.duration.total_seconds():
                    #     temp_check = temp_check / 2
                    array_check_point = None
                    if temp_check < this_run_length.total_seconds():
                        array_check_point = this_run_length.total_seconds() - temp_check
                    else:
                        array_check_point = this_run_length.total_seconds()

                    # Seconds overtime / samples remaining + buffer (*2)
                    context.printer(f"EM: [yellow]++++++ Searching for error to save {array_check_point} seconds", f'EM: ++++++ Resetting error_threshold to {context.agent_da.target_error}')
                    previous_value = None
                    for value in self.previous_sample.error_time_array:
                        previous_value = value[0]
                        if value[1].total_seconds() > (array_check_point):
                            break
                    context.agent_da.target_error = previous_value

                    # context.agent_da.target_error+=context['data_analysis']['target_error']
                    # context.agent_da.target_error = self.new_error_value
                    context.printer(f"EM: [yellow]++++++ Resetting error_threshold to {context.agent_da.target_error}", f'EM: ++++++ Resetting error_threshold to {context.agent_da.target_error}')
            elif projected_seconds_overtime > 500:
                error_change = context['data_analysis']['target_error']
                context.printer(f"EM: [yellow]'Were going to have more than an hour extra time; reducing error threshold by {error_change}", 'EM: Were going to have more than an hour extra time; reducing error threshold by {error_change}')
                if context.agent_da.target_error == context['data_analysis']['target_error']:
                    context.printer("EM: [yellow]...... No room to reduce error_threshold", 'EM: ...... No room to reduce error_threshold')
                else:
                    context.agent_da.target_error = context['data_analysis']['target_error']
                    # context.agent_da.target_error-=context['data_analysis']['target_error']
                    context.printer(f"EM: [yellow]------ Resetting error_threshold to {context.agent_da.target_error}", f'EM: ------ Resetting error_threshold to {context.agent_da.target_error}')
            if context.agent_da.target_error < 0.001:
                context.printer(f"EM: [yellow]------ Forcing error target back to 0.001  {context.agent_da.target_error}", f'EM: ------ Resetting error_threshold to {context.agent_da.target_error}')
                context.agent_da.target_error = 0.001

    def check_if_next_run_can_be_started(self, context:objects.Context) -> bool:
        """Check to see if the sample needs to be changed if so wait"""
        next_sample:objects.SampleData
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
                if context['settings']['save_type'][0] == enums.SaveType.DETAILED:
                    context.file_write(f"Instrument transition: {self.current_transition_time}")
            if self.current_transition_time > timedelta(0):
                if self.previous_transition_check is None:
                    self.previous_transition_check = context.current_time
                else:
                    context.messages.concat(f"Instrument transition: [blue]{self.current_transition_time}[/blue]\n")
                    self.current_transition_time -= context.current_time - self.previous_transition_check
                    self.previous_transition_check = context.current_time
                    return False
            else:
                self.previous_transition_check = None
                self.current_transition_time = None
                if context['experiment_manager']['adjust_error']:
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
            if context['experiment_manager']['adjust_error']:
                self.sample_change_logic(context)
            return True
        else:
            context.messages.concat(f"Sample: {0 if context.instrument.current_sample is None else context.instrument.current_sample + 1}, Setting up: [blue]{self.current_sample_switch_time}[/blue]\n")
            return False

    def tell_operator_start_data_collection(self, context:objects.Context):
        """Communicate with operator to start collecting data"""
        if context.agent_op.start_peak_chasing(context):
            context.printer("EM: [green]Communicate with Operator[/green]", 'EM: Communicate with Operator')
        else:
            context.messages.concat("EM: [blue]Instrument cannot start[/blue]")

    def check_if_data_is_sufficient(self, context:objects.Context):
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
            context.printer("EM: [green]Ask DA if data is sufficient[/green]", "EM: Ask DA if data is sufficient")
            if context.agent_da.check_if_data_is_sufficient(context):
                context.printer("EM: [blue]Tell operator to stop collecting data[/blue]", "EM: Tell operator to stop collecting data")
                context.agent_op.stop_collecting_data(context)
            # TODO _: Does operator keep going until told to stop or do they need to be told to keep going
