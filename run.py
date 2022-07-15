"""Run File"""
from datetime import timedelta
from src.config.jig import display, jig, stats
from src.library.objects.objs import SampleData

override_dictionary = {
    'name_of_experiment': ['scanning_pq'],
    'reps': [x for x in range(2)],
    'op_noticing_delay': [1.0, 3.0],
    'samples': [[
        SampleData(0.90, 0.80, timedelta(minutes=1)),
        SampleData(0.80, 0.80, timedelta(minutes=1)),
        SampleData(0.70, 0.80, timedelta(minutes=1)),
    ]],
}

# display(jig(override_dictionary))
jig(override_dictionary)
stats("scanning_pq_1657920105.986521")
display("scanning_pq_1657915832.266093")


# 'samples' : [[
#     SampleData(clamp(random.gauss(0.80, 0.2), 0.01, 0.99),
#     random.gauss(0.80, 0.20),
#     timedelta(minutes=random.gauss(1, 0.5))) for _ in range(5)]
# ]],

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
