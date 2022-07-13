"""Jig"""
from datetime import timedelta
from time import time
from numpy import mean
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from model.library.objects import AMI, Config, DataPoint, SampleData
from run import model

# samples = [SampleData(clamp(random.gauss(0.80, 0.2), 0.01, 0.99),
#                 random.gauss(0.80, 0.20), timedelta(minutes=random.gauss(1, 0.5)))
#                 for _ in range(5)]

line:bool = False
c:Config = Config(str(time()), 5, timedelta(hours=5), timedelta(seconds=1),
           0, True, f"/{str(time())}",
           [SampleData(0.99, 0.80, timedelta(minutes=1)),
            SampleData(0.97, 0.80, timedelta(minutes=1)),
            SampleData(0.93, 0.80, timedelta(minutes=1))],
           False, 0.001, 1, 1, 0, 100, 600000, 0, 0.0,
           0.0, 0.0, 0.0, 0.0, 0.2, 0.0)
runs = [[model(c) for _ in range(2)] for _ in range(2)]

x = []
y = []
z = []
run:AMI
for i, run in enumerate(runs):
    count = 1
    temp_z = []
    temp_x = []
    temp_y = []
    ami:AMI
    for ami in run:
        sample:SampleData
        for s_count, samples in enumerate(ami.samples):
            data:DataPoint
            for d_count, data in enumerate(samples.data):
                count += 1
                temp_x.append(count)
                temp_z.append(data.quality)
                temp_y.append(i+1)
                if len(z) >= s_count + 1:
                    if len(z[s_count]) >= d_count + 1:
                        z[s_count][d_count] = (z[s_count][d_count] + data.quality) / 2
    x.append(temp_x)
    z.append(temp_z)
    y.append(temp_y)

# TODO: Standard Deviation
for s in range(len(c.samples)):
    ns = [len(run.samples[s].data) for run in runs[0]]
    print(f"{ns}: {mean(ns)}")

if line:
    df = pd.DataFrame(dict(X=x[0],Y=y[0],Z=z[0],))
    fig = px.line_3d(df, x="X", y="Y", z="Z")
else:
    fig = go.Figure(data=[go.Surface(z=z)])

fig.update_layout(title='Model', autosize=True, margin=dict(l=65, r=50, b=65, t=90),
    scene = {
        "xaxis": {"nticks": 20, "autorange":'reversed'},
        "zaxis": {"nticks": 4},
        'camera_eye': {"x": 1.2, "y": 1.2, "z": 0.5},
        "aspectratio": {"x": 1, "y": 1, "z": 0.4}
    })
fig.show()


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


# TODO: Add all data parameters in object
# TODO: Mean of results over the set of number of runs
# Repeat the simulation with the same samples
# TODO: array of samples replace number of samples

# FFF QQQ: Auto Remove outliers
# TODO: PUll out erros from runs
# TODO: print out the mean and deviation of N of all runs
# Make the output a spreadsheet
