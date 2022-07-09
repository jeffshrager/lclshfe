"""High Level Controller: Round Robbin processes of classes, Synchronous simulation"""
import copy
from datetime import timedelta
import os
from time import sleep, time
from termcolor import colored
from model.agent import DataAnalyst, ExperimentManager, Operator
from model.instrument import CXI
from model.library.functions import create_experiment_figure, \
    experiment_stats, goal_agenda_plan, experiment_is_not_over
from model.library.objects import Agenda, CommunicationObject, Context, AMI

NUMBER_OF_SAMPLES:int = 10
EXPERIMENT_TIME:timedelta = timedelta(hours=5)
STEP_THROUGH_TIME:timedelta = timedelta(seconds=5)
CYCLE_SLEEP_TIME:float = 0

def model(display:bool, number_of_samples:int,
          experiment_time:timedelta, step_through_time:timedelta,
          cycle_sleep_time:float) -> AMI:
    """Run CXI Simulation"""
    filename = str(time())
    os.makedirs(os.path.dirname(f"results/model/r{filename}.tsv"), exist_ok=True)
    os.makedirs(os.path.dirname(f"results/data/r{filename}.tsv"), exist_ok=True)
    with open(f"results/model/r{filename}.tsv", "w", encoding="utf-8") as file:
        with open(f"results/data/r{filename}.tsv", "w", encoding="utf-8") as data_file:
            context:Context = Context(
                AMI(), Agenda(experiment_time, number_of_samples),
                DataAnalyst(), ExperimentManager(), Operator(),
                CXI(), CommunicationObject(), file, data_file)
            context.file.write(f"{goal_agenda_plan(context)}\n")
            while experiment_is_not_over(context):
                os.system('cls' if os.name == 'nt' else 'clear')
                context.messages.reset()
                print(goal_agenda_plan(context) if display else 'running')
                context.update()
                if not context.agenda.is_started():
                    context.agent_em.start_experiment(context)
                elif context.agenda.is_started():
                    if not context.instrument.is_running():
                        context.agent_em.start_instrument(context)
                    elif context.instrument.is_running():
                        if not context.instrument.is_collecting_data():
                            if context.agent_em.check_if_next_run_can_be_started(context):
                                context.agent_em.tell_operator_start_data_collection(context)
                        elif context.instrument.is_collecting_data():
                            context.agent_op.track_stream_position(context)
                            context.agent_em.check_if_data_is_sufficient(context)
                print(context.messages if display else 'running')
                context.agent_da.check_if_experiment_is_compleated(context)
                context.current_time += step_through_time
                sleep(cycle_sleep_time)
            os.system('cls' if os.name == 'nt' else 'clear')
            context.file.write(f"\n{experiment_stats(context)}\nFinished")
            print(f"{experiment_stats(context)}\n{colored('Finished','green')}" if display else '--')
            create_experiment_figure(context, False)
            return copy.deepcopy(context.ami)
model(True, NUMBER_OF_SAMPLES, EXPERIMENT_TIME, STEP_THROUGH_TIME, CYCLE_SLEEP_TIME)

# TODO: Improve graph at end with extra values
# TODO: After the production is done shortly after then they can analyse
# TODO: Dynamic sample scheduling
# TODO: Data quality that comes off the machine
# then data quality that the data analist has

# TODO: We have to decide weather im going to take more data or abort and fix something
# TODO: Each of the reps the quality of the data will get better and better

# TODO: Based on the button distance getting worse and worse scans
# Kinda a cheat different purpose, model how bad the UI would be if buttons were far away
# Data to be being read by the DA at a fixed button distance
# Can use button distance as a proxy for the experiment not doing well
# Signal Noise Ratio, as the operator was changing stuff, data analyst was looking at
# As peak chasing gets harder because the buttons are father apart, like power is too low
# Could rename Button distance to something like, difficulty
