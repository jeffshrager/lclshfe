import pandas as pd
import matplotlib.pyplot as plt
from numpy import mean

df = pd.read_excel('Sys_Stability.xlsx', header=None, index_col=None, usecols="A")
system_stability = df[0]
cognitive_zoom = [1] * len(system_stability)
cognitive_zoom_2 = [1] * len(system_stability)
weight = [1/5, 1/4, 1/3, 1/2, 1]

for i in range(len(system_stability)):
    if i <= 5:
        cognitive_zoom[i] = min((100/mean(system_stability[0:i])), 2)
        cognitive_zoom_2[i] = min(100/mean(system_stability[0:i]), 2)
    else:
        cognitive_zoom[i] = min(100/mean(system_stability[i-5:i]), 2)
        cognitive_zoom_2[i] = min(100/(system_stability[i-5:i].mul(weight).div(sum(weight)).sum()), 2)

fig, axs = plt.subplots(3, sharex=True)
axs[0].plot(system_stability)
axs[0].set_title('System Stability')
axs[0].set_ylabel('Stability')
axs[1].plot(cognitive_zoom)
axs[1].set_ylabel('by Average')
axs[1].set_title('Cognitive Zoom')
# axs[1].set_xlabel('Time')
axs[2].plot(cognitive_zoom_2)
axs[2].set_ylabel('by 1/x')
# axs[2].set_title('Cognitive Zoom')
axs[2].set_xlabel('Time')
plt.show()
