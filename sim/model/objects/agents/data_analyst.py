"""The Data Analyst agent

The Data Analyst agents is responsible for monitoring the AMI and determining the quality
of the data being produced. This is used to inform the Experiment Manager and using this
information the error thrreshold can be changed.

  Typical usage example:

  DA = DataAnalyst()
  DA.check_if_enough_data_to_analyse(context)
"""
from scipy.stats import linregress
import sim.model.enums as enums
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.objects.agents.base as base

class DataAnalyst(base.Person):
    """The Data Analyst will be able to predict the error of the current sample

    The Data Analyst agents is responsible for monitoring the AMI and determining the quality
    of the data being produced. This is used to inform the Experiment Manager and using this
    information the error thrreshold can be changed.

    Attributes:
        Person: A boolean indicating if we like SPAM or not.
    """
    # """Retrives data from the instrument"""
    projected_intercept:float = None
    target_error:float = None
    predictions:list = []

    def __init__(self, config:settings.Config):
        super().__init__(enums.AgentType.DA)
        self.last_sample_with_enough_data = None
        self.target_error = config['data_analysis']['target_error']

    def check_if_enough_data_to_analyse(self, context:objects.Context) -> bool:
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
                    context.printer(f"[default]DA: Data from run {context.instrument.run_number} [green]has enough data to analyse", f"DA: Data from run {context.instrument.run_number} has enough data to analyse")
            return True
        return False

    def check_if_data_is_sufficient(self, context:objects.Context) -> bool:
        """If there is enough data True, else False to ask to keep running"""
        # TODO: Ask Instrument scientist to see what is the real decision logic stopping criteria
        current_sample = context.ami.samples[context.instrument.current_sample]
        # TODO: DA does not have access to preformance quality
        #  Determine that the mean is settling
        if current_sample.err <= self.target_error:
            context.printer(f"DA: Data from run {context.instrument.run_number} [green]is good[/green]", f"DA: Data from run {context.instrument.run_number} is good")
            context.agenda.add_event(context.instrument.run_number, context.instrument.run_start_time, context.current_time, current_sample, False)
            current_sample.completed = True
            self.projected_intercept = None
            return True
        context.printer(f"DA: [yellow]More data needed from run[/yellow] {context.instrument.run_number}", f"DA: More data needed from run {context.instrument.run_number}")
        return False

    def check_if_experiment_is_completed(self, context:objects.Context):
        """Check if experiment is completed"""
        current_sample = None
        for index, sample_goal in enumerate(context.ami.samples):
            if not sample_goal.completed:
                current_sample = index
                break
        if current_sample is None:
            context.agenda.finished()
