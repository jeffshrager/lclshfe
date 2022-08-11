"""Run the simulation

The main method is used to run method from the jig including the
simulation. This should be the only file that is run.

  Typical usage example:

  sim.jig(sim.overrides.macro_test, True, 'functional_acuity')
  sim.stats('fnc_ond1_tanh_false_cog_false_30mins/1659488027.688672', 'functional_acuity')
  sim.display(sim.jig(sim.overrides.fnc1_ond_tanh_false_cog_false, True, 'noticing_delay'), 'noticing_delay')
"""
import sys
import sim

def main() -> int:
    """Run the Jig"""
    # TODO: Fix Suppressed
    sim.jig(sim.overrides.ADJ_True_Stop_True, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_False_Stop_True, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_True_Stop_False, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_False_Stop_False, True, 'noticing_delay')
    # sim.jig(sim.overrides.TF, True, 'noticing_delay')
    # sim.jig(sim.overrides.FT, True, 'noticing_delay')
    # sim.jig(sim.overrides.FF, True, 'noticing_delay')

    # sim.display(sim.jig(sim.overrides.fnc1_ond_tanh_false_cog_false, True, 'noticing_delay'), 'noticing_delay')
    # sim.stats('Poster1/1659637732.51549', 'noticing_delay')
    # sim.stats('Poster2/1659638382.7977269', 'noticing_delay')
    # sim.stats('Poster3/1659726202.022182', 'noticing_delay')
    # sim.display('fnc_ond1_tanh_false_cog_false/1658879734.700448', 'functional_acuity')

    # sim.display('Poster3/1659726202.022182', 'noticing_delay')
    # sim.stats('fnc_ond1_tanh_false_cog_false_30mins_for_tomorow/1659508987.5486', 'functional_acuity')
    return 0

if __name__ == '__main__':
    sys.exit(main())

# III: If PQ Delta is 0 divide by 0 error

# TODO: Display when running show current run number on left side


# Add Adjenda to display
# Record all of the data - Detailed
# Set the time that it has to oscelate the error
# Only moves a little
# fnc_ond1_tanh_false_cog_false
# collect: Average of last error term
# Fix time things
# Last number try with off and on
# Add mean and deviation of the last error value,
# average over under in time

# III: Timing Thing - Fix
# III: Comments
# III: Unit Tests








# III: Data Analyst: Every cycle just store the error thresholds in an array. Just store them
# We can actually read off the table from previous run and understand where 0.002 will get us to
# Pair of cycle time and error threshold

# Y is measure of overall run efficency
# Worse data you can get it faster, total time for run independant variable
# We really let it run, do planning as though it would get cut off but not

# How effective is it to add reasoning support at these different levels
# Over some set of parameterization it would change overall run preformance

# Dependent accis is the avereage overall data quality modulated by importance
# perfect is in time alloted 0.001 on all samples

# use the esitmate for higher quality data
# If it gets cut off you end with the data quality point you were at

# 2 ways to get cut off the end, the EM might say this is going to take too long,

# Command to cut off and switch samples

# EM this is taking so long not able to take all bump error threshold,
#   peak chasing end of experiment
# EM has decision to change it, DA changes it
# EM says to change it to 0.002

# III
# - Up Side
# - What I have now and scheduling
# - Sorting the samples by pq as a proxy for importance
# Scheduling, most data on most important things
# Quality assurance error to 0.001
# Very low quality data not important, you would abort that and do high importance
# Oportunistic planning - Alwayse doing this
# opportunity to replan
# Stability of the machine
# Data aquasition randomness

# Run 1s until stability
# then run 2s after stable
# only controll after switching is error threshold
# Also prediction is important

# At the higher level, over the whole 3-4 days
# 25 samples, 5 different importance levels,
# pq counting down by .1 for each sample
# Importance is a step scale
# 5 is most important 1 is least

# Running out with water instability
# IF the thing is stable put most important sample in
# Understand how long they are taking
# Run one lowest quality
# see how fast the error rate goes down update estimate
# if its more than an hour for all of them, accept more error

# TODO: Based on the button distance getting worse and worse scans
# Kinda a cheat different purpose, model how bad the UI would be if buttons were far away
# Can use button distance as a proxy for the experiment not doing well
# Signal Noise Ratio, as the operator was changing stuff, data analyst was looking at
# As peak chasing gets harder because the buttons are father apart, like power is too low
