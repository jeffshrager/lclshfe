"""
High Level Controller
Round Robbin processes of classes, Synchronous simulation
"""
from datetime import timedelta
import os
import time
import agent
from data import Goal, Agenda
import instrument
from termcolor import colored

DATAPOINTS_NEEDED_PER_SAMPLE = 10000
NUMBER_OF_SAMPLES = 10
EXPERIMENT_TIME:timedelta = timedelta(hours=10)

def run():
    """Run CXI Simulation"""
    goal = Goal(DATAPOINTS_NEEDED_PER_SAMPLE, NUMBER_OF_SAMPLES)
    agenda = Agenda(EXPERIMENT_TIME)

    # Instantiate Agents
    # agent_da = agent.DataAnalyst()
    agent_em = agent.ExperimentManager()
    agent_op = agent.Operator()

    # Instantiate Instrument
    instrument_cxi = instrument.CXI()

    # File to write results to
    file = open("results/r" + str(time.time()) + ".tsv", "w", encoding="utf-8")
    file.write(f"{goal}\n{agenda}\n----------------------------------------------\n")

    # Experiment Run Cycle
    while agenda.current_time < agenda.experimental_time and goal.status != "compleated":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(goal)
        print(agenda)
        print("----------------------------------------------")
        if instrument_cxi.is_running():
            if not instrument_cxi.is_collecting_data():
                # if not first run
                # Operator ask DA if last run was good
                # Handle this
                agent_em.tell_operator_start_data_collection(agent_op, instrument_cxi,
                                                                agenda.current_time, file)
        else:
            agent_em.start_experiment(instrument_cxi, file)
        # TODO: finish simulation
        instrument_cxi.update(agenda.current_time, goal, agenda)
        agenda.current_time += timedelta(minutes=1)
        time.sleep(1)

    os.system('cls' if os.name == 'nt' else 'clear')
    roi = 0
    for i in goal.samples:
        if i > goal.datapoints_needed_per_sample:
            roi += 1
    percent_string = '{:.0%}'
    file.write(f"\n{goal}\n{agenda}\n----------------------------------------------\n"+
          f"ROI: {percent_string.format(roi/len(goal.samples))}\n{agenda.print_timeline()}\n"+
          f"{'Finished'}")
    print(f"{goal}\n{agenda}\n----------------------------------------------\n"+
          f"ROI: {percent_string.format(roi/len(goal.samples))}\n{agenda.print_timeline()}\n"+
          f"{colored('Finished', 'green')}")
run()
