import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from os import walk

path = "run_tables"
filenames = next(walk(path), (None, None, []))[2]

fig, axs = plt.subplots(len(filenames), sharex=True, figsize=(12, 6))
for x, file in enumerate(filenames):
       axs[x].yaxis.set_ticks([])
       axs[x].set_ylabel(file[:len(file) - 4])
       with open(f"{path}/{file}",'r') as f:
              reader = csv.reader(f)
              headers = next(reader)
              data = [{h:x for (h,x) in zip(headers,row)} for row in reader]
       positions = []
       thickness = []
       for entry in data:
              if "RunStart" in entry:
                     positions.append([datetime.strptime(entry["RunStart"], '%b/%d/%Y %H:%M:%S')])
              if "run start" in entry:
                     positions.append([datetime.strptime(entry["run start"], '%b/%d/%Y %H:%M:%S')])
              if "RunDuration" in entry:
                     thickness.append(float(entry["RunDuration"]))
              if "Duration of run" in entry:
                     thickness.append(float(entry["Duration of run"]))
       axs[x].eventplot(
              positions = np.array(positions), 
              orientation="horizontal",
              linewidths=np.array(thickness),
              colors=['C{}'.format(i) for i in range(len(positions))])
axs[0].set_title('Run Tables')
axs[len(filenames)-1].set_xlabel('Time ->')
plt.show()
