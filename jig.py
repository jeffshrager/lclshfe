"""Jig"""
from datetime import timedelta
from numpy import mean
import plotly.graph_objects as go
from model.library.objects import AMI, DataPoint, SampleData
from run import model

# TODO: Mean of results over the set of number of runs

# Repeat the simulation with the same samples
# TODO: array of samples replace number of samples
number = 2
runs = [model(True, number, timedelta(hours=5), timedelta(seconds=5), 0) for _ in range(5)]

# TODO: Add abort for overruns - 500,000 cycles
# FFF QQQ: Auto Remove outliers
# Samples with higher PQ, should run for less time beacause it should take less time

# TODO: PUll out erros from runs

# TODO: print out the mean and deviation of N of all runs
# Make the output a spreadsheet

# mean = 0.0
# TODO: Standard Deviation
for s in range(number):
    ns = [len(run.samples[s].data) for run in runs]
    print(f"{ns}: {mean(ns)}")
    # for r in runs:
    #     mean += r.samples[s].data
        # print(runs[s].samples[s].mean())

# for run in runs:
#     for sample in samples:


x = []
y = []
z = []
run:AMI
for i, run in enumerate(runs):
    y.append(i+1)
    counter = 1
    temp_z = []
    temp_x = []
    sample:SampleData
    for samples in run.samples:
        data:DataPoint
        for data in samples.data:
            counter += 1
            temp_x.append(counter)
            temp_z.append(data.quality)
    x.append(temp_x)
    z.append(temp_z)

fig = go.Figure(data=[go.Surface(z=z)])
fig.update_layout(title='Model', autosize=True, margin=dict(l=65, r=50, b=65, t=90),
    scene = {
        "xaxis": {"nticks": 20, "autorange":'reversed'},
        "zaxis": {"nticks": 4},
        'camera_eye': {"x": 1.2, "y": 1.2, "z": 0.5},
        "aspectratio": {"x": 1, "y": 1, "z": 0.4}
    })
fig.show()
