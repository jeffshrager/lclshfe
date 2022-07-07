"""Jig"""
from datetime import timedelta
import plotly.graph_objects as go
from model.library.objects import AMI, DataPoint, SampleData
from run import model

runs = [model(False, 50, timedelta(hours=1), timedelta(seconds=5), 0) for _ in range(10)]

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
