"""High Level Controller
Round Robbin processes of classes, Synchronous simulation"""
from datetime import timedelta
import os
from time import sleep, time
from termcolor import colored
from model.agent import DataAnalyst, ExperimentManager, Operator
from model.instrument import CXI
from model.library.functions import create_experiment_figure, experiment_stats, \
    goal_agenda_plan, experiment_is_not_over
from model.library.objects import CommunicationObject, Context, Goal

NUMBER_OF_SAMPLES:int = 18
EXPERIMENT_TIME:timedelta = timedelta(hours=8)
STEP_THROUGH_TIME:timedelta = timedelta(seconds=5)
CYCLE_SLEEP_TIME:int = 0

def run(display:bool):
    """Run CXI Simulation"""
    filename = f"results/r{str(time())}.tsv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        context:Context = Context(
            Goal(NUMBER_OF_SAMPLES),
            DataAnalyst(),
            ExperimentManager(EXPERIMENT_TIME),
            Operator(),
            CXI(),
            CommunicationObject(),
            file)
        context.file.write(f"{goal_agenda_plan(context)}\n")
        while experiment_is_not_over(context):
            print(goal_agenda_plan(context))
            context.update()
            if not context.agent_em.agenda.is_started():
                context.agent_em.agenda.start_experiment()
            elif context.agent_em.agenda.is_started():
                if not context.instrument_cxi.is_running():
                    context.agent_em.start_experiment(context)
                elif context.instrument_cxi.is_running():
                    if not context.instrument_cxi.is_collecting_data():
                        if context.agent_em.check_if_next_run_can_be_started(context):
                            context.agent_em.tell_operator_start_data_collection(context)
                    elif context.instrument_cxi.is_collecting_data():
                        context.agent_op.track_stream_position(context)
                        context.agent_em.check_if_data_is_sufficient(context)
            print(context.messages)
            context.agent_da.check_if_experiment_is_compleated(context)
            context.current_time += STEP_THROUGH_TIME
            sleep(CYCLE_SLEEP_TIME)
            os.system('cls' if os.name == 'nt' else 'clear')
        context.file.write(f"\n{experiment_stats(context)}\nFinished")
        print(f"{experiment_stats(context)}\n{colored('Finished', 'green')}")
        create_experiment_figure(context, display)
run(False)

# TODO: Attention/ exaustion/ focus controlls for ever person
# TODO: operator noise and ✓(detector noise)
# TODO: Data analyst improved determening if data is good or not

# TODO: Analygous attentional properties will attach to data analyst
# Hot vs cold cognition, hot rappid makes more mistakes, cold slower more accurate
# Eventually check when worrying check all the time, when not check once in a while

# TODO: Add system stability affect attention level
# If the system is unstable attention should increase, if system is stable attention will decrease
# If something happens for a shift there is a transition time
# We know what the status of the system is use this to callibrate the system
# begining they will be focused, not exausted yet, 4pm things go wrong and they are tired







# TODO: Improve graph at end with extra values
# TODO: Current Sample needs to be updated in a different place so that nowhere needs current sample + 1
# TODO: Dont worry about but only gets a subset of samples
# TODO: After the production is done shortly after then they can analyse
# TODO: Dynamic sample scheduling
# TODO: nth dimentional models


# TODO: Data quality that comes off the machine
# then data quality that the data analist has

# ----------------------

# Based on the button distance getting worse and worse scans
# Kinda a cheat different purpose, model how bad the UI would be if buttons were far away
# Data to be being read by the DA at a fixed button distance
# Can use button distance as a proxy for the experiment not doing well
# Signal Noise Ratio, as the operator was changing stuff, data analyst was looking at
# data saying background was high
# EM was saying to get more data
# Smoothest thing to use is data quality
# X axis should be data quality
# We have to decide weather im going to take more data or abort and fix something
# As peak chasing gets harder because the buttons are father apart, like power is too low
# Could rename Button distance to something like, difficulty
# Data analyst looking at the number
# Mike being tired or data being difficult to get or anything else
# Data analyst reading data as it comes off
# Agent reading the means
# Each of the reps the quality of the data will get better and better

# EM tells the OP to stop or to take more data
# Taking more data
# A bunch of low quality data, suppose data quality was low enough
# RULE is to extend if quality is low
# Calculate data quality not just points
# Data quality per measurement

# Suppose 100 measurements total
# Want to get high data quality for all 100
# Mean is 100 regardless of how many you take
# Should we go longer, even if you double it you can only get 50 not 100
# Data quality within measurement is very low or high = number of runs, length

# Number of samples taken / Number of measurements
# Each of the runs
# Declare single noise ratio above 1
# down at 0.1 it would be 50 mins
# At the top of the curve that should be calibrated at 0.9, 5 mins
# At 0.9, 300 * 36 = 10,000 good observations * 0,9 = 9,000
# As you collect data points it approaches 9000

# DA reads the mean of the number, reports to the EM
# up to 10000 so keep going, as the number is going operator wants to keep going until sum of 9000
# constrain the total time

# Say how many measurements you got vs how much you expected
# If you were expecting 120 measurements, 1 less than 1% ROI

# Data quality was so low, OP had to keep going to get up to 10000

# Curve is going to float

# Attention distracted and tired
