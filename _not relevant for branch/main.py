"""Main"""

import csv
from datetime import datetime, timedelta


# Set path with run csv files
PATH = "run_tables"
DATA_PER_SECOND = 36

class Event:
    """Stores all the information about each experiment run"""
    run_start:datetime
    run_end:datetime
    translated_position:datetime
    run_duration:timedelta
    thickness:float

    def __init__(self, run_start:datetime, run_duration:timedelta):
        self.run_start = run_start
        self.run_end = run_start + run_duration
        self.run_duration = run_duration
        # Thickness is centered, moving each position x + (duration / 2)
        self.translated_position = run_start + run_duration / 2
        self.thickness = run_duration.total_seconds()/100

    def __str__(self):
        return (f"Start Time: {self.run_start}, "+
		        f"Duration: {self.run_duration}, "+
		        f"Translated Position: {self.translated_position}, "+
		        f"Thickness: {self.thickness}")

with open(f"{PATH}/cxilx6320.csv",'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    data = [{h:x for (h,x) in zip(headers,row)} for row in reader]

events = []
for entry in data:
    if "RunStart" in entry:
        events.append(Event(datetime.strptime(entry["RunStart"], '%b/%d/%Y %H:%M:%S'),
                        timedelta(seconds=int(entry["RunDuration"].split('.')[0]),
                                milliseconds=int(entry["RunDuration"].split('.')[1]))))
    if "Duration of run" in entry:
        events.append(Event(datetime.strptime(entry["run start"], '%b/%d/%Y %H:%M:%S'),
                        timedelta(seconds=int(entry["Duration of run"].split('.')[0]),
                                milliseconds=int(entry["Duration of run"].split('.')[1]))))

totalDuration = timedelta(0, 0, 0)
event:Event
for event in events:
    totalDuration += event.run_duration
    print(event)

print((totalDuration.total_seconds() * DATA_PER_SECOND) * 0.79)
print(totalDuration)
