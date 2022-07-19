"""Run File"""
import dash
from dash import html
import dash_pivottable
from datetime import timedelta
from src.settings.jig import depriciated_display, jig, stats
from src.enums.jig_enums import SaveType
from src.library.objects.objs import SampleData

override_dictionary = {
    'name_of_experiment': ['op_delay1-20'],
    'save_type': [SaveType.COLLAPSED],
    'reps': [x for x in range(20)],
    'op_noticing_delay': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0],
    'samples': [
        [SampleData(0.45, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.50, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.55, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.60, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.65, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.70, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.75, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.80, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.85, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.90, 0.80, timedelta(minutes=1)) for _ in range(10)],
        [SampleData(0.95, 0.80, timedelta(minutes=1)) for _ in range(10)],
    ],
}

# display(jig(override_dictionary))
jig(override_dictionary)
# stats("Big_Set_1657959904.283649")
# depriciated_display("op_delay1-7/1658207804.691573")









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
