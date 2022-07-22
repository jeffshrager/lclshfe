"""Run File"""
import numpy as np
from src.jig import depriciated_display, jig, stats
from src.library.enums.jig_enums import SaveType
from src.library.enums.model_enums import SampleImportance, SampleType
from src.library.objects.objs import SampleData

override_dictionary = {
    'settings': {'name': ['test'],'save_type': [SaveType.COLLAPSED],},
    'reps': [x for x in range(3)],
    'operator': {'noticing_delay': [1.0, 5.0, 10.0]},
    # 'experimental_time': [timedelta(seconds=2500)],
    'samples': {'samples': [
        [SampleData(round(0.95 - i, 2), SampleImportance.IMPORTANT, SampleType.TAPE) for i in np.arange(0.0, 0.125, 0.025)],
        # [SampleData(round(0.95 - i, 2), SampleImportance.UNIMPORTANT, SampleType.TAPE) for i in np.arange(0.0, 0.125, 0.025)],
    ],},
    'cognative_degredation': [False],
    'cxi': {'tanh_curve': [True]}
}

# jig({})
jig(override_dictionary)
# display(jig(override_dictionary))
# stats("to_delete/1658518293.767295")
# depriciated_display("op_delay1-7/1658207804.691573")



# Jig generalization,
# Every 50 added mean and stddev for the whole thing
# PQ ond,
# Create a dictionary whos index is a tag array and has all the results of the run in it

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


# Precision calculation - goes into ROI



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
# III: Any var to scan
# TODO: When it hits the wall it aborts check this
# TODO: Add hit wall counter

# TODO: all overrides go in file


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
# TODO: array of samples replace number of samples

# 'samples' : [[
#     SampleData(clamp(random.gauss(0.80, 0.2), 0.01, 0.99),
#     random.gauss(0.80, 0.20),
#     timedelta(minutes=random.gauss(1, 0.5))) for _ in range(5)]
# ]],