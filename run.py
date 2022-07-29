"""Run File: A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from src.jig import display, display_new, jig, rollup, stats
import src.settings.overrides as overrides

jig(overrides.macro_test, True, 'functional_acuity')


# display_new(jig(overrides.over180, True, 'functional_acuity'), 'functional_acuity')
# rollup("fnc_ond_tanh_false_cog_false/1658732176.595285")
# stats("fnc_ond_tanh_false_cog_false/1658732176.595285")
# display("fnc_ond1_tanh_false_cog_false/1658810656.175882")
# display_new("fnc_ond1_tanh_true_cog_true/1658863335.323498")



# III: Data Analyst: Every cycle just store the error thresholds in an array. Just store them
# We can actually read off the table from previous run and understand where 0.002 will get us to
# Pair of cycle time and error threshold


# Given previous run how do we save this many seconds, Experiment manager - Data Analyst
# Just move up and down by 0.001















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

# Good Bad
# 5 care, 5 not
# PQ does down by .25


# Run 1s until stability
# then run 2s after stable
# only controll after switching is error threshold
# Also prediction is important

# At the higher level, over the whole 3-4 days
# 25 samples, 5 different importance levels,
# pq counting down by .1 for each sample
# Importance is a step scale
# 5 is most important 1 is least

# 15 min delay

# Label this one is done,

# Map stability curve on experiment
# very unstable


# Run lowest preformance to take out the instability
# get a sence of how long each sample takes once reaches asemptote
# Then start running important sample

# Running out with water instability
# IF the thing is stable put most important sample in
# Understand how long they are taking
# Run one lowest quality
# see how fast the error rate goes down update estimate
# if its more than an hour for all of them, accept more error


# Data input file, dict keys, reads through and prints them on tabs between them


# Say X
# Y i alwayse samples

# Print Number
# FFF: folders for each type

# TODO: NUmpy array comprehension, compression method

# TODO: Compress every run into single number, Mean, Stdev, Var
# TODO: Label means as noticing delay [number of reps]

# FFF: accessor function and mutate to change to new value
# # With accessors and mutators, the dictionary key would actually be an accessor function

# standard deviation the color, keep both

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

# TODO: Add all data parameters in object
# TODO: Mean of results over the set of number of runs
# Repeat the simulation with the same samples