"""
RunTable Generator Tool
"""

import csv
from datetime import datetime, timedelta
from os import walk
import matplotlib.pyplot as plt
import numpy as np

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


# Set path with run csv files
PATH = "run_tables"

# Get all files in given path
filenames = next(walk(PATH), (None, None, []))[2]  
# Create plot
fig, axs = plt.subplots(len(filenames), sharex=True, figsize=(12, 6))
for x, file in enumerate(filenames):
    # Remove y Ticks
    axs.yaxis.set_ticks([]) if len(filenames) == 1 else axs[x].yaxis.set_ticks([])
    # Set labels for each run
    axs.set_ylabel(file[:len(file) - 4]) if len(filenames) == 1 else axs[x].set_ylabel(file[:len(file) - 4])
    # Read the CSV with headers
    with open(f"{PATH}/{file}",'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = [{h:x for (h,x) in zip(headers,row)} for row in reader]
    events = []
	# Extract data from csv generated data structure
    for entry in data:
        if "RunStart" in entry:
            events.append(Event(datetime.strptime(entry["RunStart"], '%b/%d/%Y %H:%M:%S'),
                          timedelta(seconds=int(entry["RunDuration"].split('.')[0]),
			                        milliseconds=int(entry["RunDuration"].split('.')[1]))))
        if "Duration of run" in entry:
            events.append(Event(datetime.strptime(entry["run start"], '%b/%d/%Y %H:%M:%S'),
                          timedelta(seconds=int(entry["Duration of run"].split('.')[0]),
			                        milliseconds=int(entry["Duration of run"].split('.')[1]))))
    positions = []
    thickness = []
    for event in events:
        positions.append([event.run_end])
        thickness.append(event.thickness)

	# Create subplot
    if (len(filenames) == 1):
	       axs.eventplot(
	              positions = np.array(positions),
	              orientation="horizontal",
	              lineoffsets = 3,
	              linelengths = 3,
	              linewidths=np.array(thickness),
	              colors=['C{}'.format(i) for i in range(len(positions))])
    else:
	       axs[x].eventplot(
	              positions = np.array(positions),
	              orientation="horizontal",
	              lineoffsets = 3,
	              linelengths = 3,
	              linewidths=np.array(thickness),
	              colors=['C{}'.format(i) for i in range(len(positions))])
axs.set_title('Run Tables') if len(filenames) == 1 else axs[0].set_title('Run Tables')
axs.set_xlabel('Time ->') if len(filenames) == 1 else axs[len(filenames)-1].set_xlabel('Time ->')
plt.show()
