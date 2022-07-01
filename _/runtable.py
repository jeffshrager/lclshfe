"""RunTable Generator Tool"""
import csv
from datetime import datetime, timedelta
from os import walk
import plotly.express as px
import pandas as pd

# Set path with run csv files
PATH = "run_tables"

# Get all files in given path
filenames = next(walk(PATH), (None, None, []))[2]
df = pd.DataFrame([])
for x, file in enumerate(filenames):
# Read the CSV with headers
    with open(f"{PATH}/{file}",'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = [{h:x for (h,x) in zip(headers,row)} for row in reader]
    for entry in data:
        start = datetime.strptime(
            entry["RunStart"], '%b/%d/%Y %H:%M:%S') if "RunStart" in entry else datetime.strptime(
            entry["run start"], '%b/%d/%Y %H:%M:%S')
        duration = timedelta(
            seconds=int(entry["RunDuration"].split('.')[0]),
            milliseconds=int(entry["RunDuration"].split('.')[1])
            ) if "RunDuration" in entry else timedelta(
                seconds=int(entry["Duration of run"].split('.')[0]),
                milliseconds=int(entry["Duration of run"].split('.')[1]))
        Comment = entry["Comment"] if "Comment" in entry else entry["Comments"]
        Run = entry["Run"]
        df = pd.concat([df, pd.DataFrame.from_records([{
            "Task":f"{file[:len(file) - 4]}",
            "Start":f"{start}",
            "Finish":f"{start + duration}",
            "Resource":f"{file[:len(file) - 4]}",
            "Run": f"Run: {Run}",
            "Nevents": entry["N events"] if "N events" in entry else "",
            "Ndamaged": entry["N damaged"] if "N damaged" in entry else "",
            "ShutterIn": entry["ShutterIn"] if "ShutterIn" in entry else "",
            "WaveplateAngle": entry["WaveplateAngle"] if "WaveplateAngle" in entry else "",
            "GasCell-Pressure": entry["GasCell-Pressure"] if "GasCell-Pressure" in entry else
                                entry["GasCell Pressure"] if "GasCell Pressure" in entry else "",
            "JungFrau-Z": entry["JungFrau-Z"] if "JungFrau-Z" in entry else
                          entry["Junfrau Z"] if "Junfrau Z" in entry else "",
            "Pinhole-X": entry["Pinhole-X"] if "Pinhole-X" in entry else
                         entry["Pinhole X"] if "Pinhole X" in entry else "",
            "Pinhole-Y": entry["Pinhole-Y"] if "Pinhole-Y" in entry else
                         entry["Pinhole Y"] if "Pinhole Y" in entry else "",
            "GasCell-X": entry["GasCell-X"] if "GasCell-X" in entry else
                         entry["GasCell X"] if "GasCell X" in entry else "",
            "GasCell-Y": entry["GasCell-Y"] if "GasCell-Y" in entry else
                         entry["GasCell Y"] if "GasCell Y" in entry else "",
            "GasCell-Z": entry["GasCell-Z"] if "GasCell-Z" in entry else "",
            "GasCell Yaw": entry["GasCell Yaw"] if "GasCell Yaw" in entry else "",
            "GasCell Pitch": entry["GasCell Pitch"] if "GasCell Pitch" in entry else "",
            "Photonenergy": entry["Photon energy"] if "Photon energy" in entry else "",
            "Comment": f"{Comment}"}])])
fig = px.timeline(df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Resource",
            hover_name="Run",
            hover_data=["Nevents",
            "Ndamaged","ShutterIn",
            "WaveplateAngle","GasCell-Pressure",
            "JungFrau-Z","Pinhole-X","Pinhole-Y",
            "GasCell-X","GasCell-Y","GasCell-Z",
            "GasCell Yaw","GasCell Pitch",
            "Photonenergy","Comment"])
fig.update_yaxes(autorange="reversed")
fig.show()
