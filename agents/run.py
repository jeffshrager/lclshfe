"""
High Level Controller
Round Robbin processes of classes, Synchronous simulation
"""

import time
import agent
import instrument

def run(value):
    """Run CXI Simulation"""
    reps = value
    experimental_time = ""
    goal = ""
    agenda = ""

    # Store results to file
    f = open("results/r" + str(time.time()) + ".tsv", "w")

    # Instantiate Agents
    agent_da = agent.DataAnalyst()
    agent_em = agent.ExperimentManager()
    agent_op = agent.Operator()

    # Instantiate Instrument
    instrument_cxi = instrument.CXI()

    instrument_cxi.run_stream(True)

    for rep in range(reps):
        agent_em.plan()
        agent_op.manipulate_system()
        agent_op.run_peak_chasing(instrument_cxi)
        agent_da.analyse_data()

run(1)

# Add agenda - does the EM have the agenda
# Jet Tracking - current 10 - 15 mins
# 12 hour scale add that layer to the program
# System stability, affect attention level
# If the system is unstable attention should increase, if system is stable attention will decrease
# If something happens for a shift there is a transition time
# We know what the status of the system is use this to callibrate the system
# begining they will be focused, not exausted yet, 4pm things go wrong and they are tired