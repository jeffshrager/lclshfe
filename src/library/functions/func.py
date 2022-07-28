"""Collection of functions"""
from __future__ import annotations
import collections.abc
from math import tanh
from typing import TYPE_CHECKING
from numpy import random
import plotly.express as px
import pandas as pd
from termcolor import colored
if TYPE_CHECKING:
    from src.library.objects.objs import Context, AMI

def calculate_roi(ami:AMI) -> str:
    """Determine the retun of investment data / time"""
    # TODO: Precision calculation - goes into ROI
    return (sum(sample.compleated for sample in ami.samples) / len(ami.samples
    ) if len(ami.samples) > 0 else 0)

def update_dict(d, u):
    """Update a dictionary with another dictionary"""
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def get_line() -> str:
    """return string line"""
    return "---------------------------------------------------------------------------------------"

def config_print(dictionary:dict) -> str:
    """Config print"""
    return_string = ""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            return_string += config_print(v)
        else:
            if isinstance(v, list):
                list_string = ""
                for item in v:
                    list_string += f"{item}, "
                return_string += f"{k}: {list_string}"
            else:
                return_string += (f"{k} : {v}, ")
    return return_string

def goal_agenda_plan(context:Context) -> str:
    "Return out GAP: Goal Agenda Plan"
    return (f"{config_print(context.config.override_dictionary)}\n{get_line()}\n{context.ami}\n"+
    f"Current Time: {context.current_time} {context.agenda}\n{get_line()}")

def experiment_stats(context:Context) -> str:
    "Write out statistics of the experiment"
    return (f"{context.ami}\nCurrent Time: {context.current_time} {context.agenda}\n"+
    f"{get_line()}\nROI: {calculate_roi(context.ami):.0%}\n{context.agenda.get_timeline()}")

def experiment_is_not_over(context:Context) -> bool:
    """True: Experiment is not over, False: Experiment is over"""
    return (context.current_time < context.agenda.experimental_time
    ) and (len(context.agenda.event_timeline) != len(context.ami.samples)
    ) if (len(context.agenda.event_timeline) != 0) else True

def get_current_datapoints(context:Context) -> str:
    """Gets the datapoints live"""
    current_sample = context.ami.get_current_sample(context)
    return_string = ""
    for index, data in enumerate(current_sample.data[-60:]):
        return_string += (colored(f'{data}', 'green'
        if data.quality >= aquire_data(0.001, current_sample.preformance_quality, context
        ) else 'yellow' if data.quality >= aquire_data(0.03, current_sample.preformance_quality, context
        ) else 'red') + ("\n" if index == 19 or index == 39 else " "))
    return return_string

def aquire_data(distance:float, preformance_quality:float, context:Context) -> float:
    """given distance calculate gaussian according to this:
    https://www.desmos.com/calculator/1dc980vuj1"""
    preformance_disquality = 1 - preformance_quality
    # cumulative_deviation = (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(distance/ 0.05, 2))
    # FFF: Figure out what this should really be
    # print(context.current_time.total_seconds()/1000)
    # TODO: Add instument instability to config
    # Have this reset for every shift change
    instrument_instability = (1 - tanh(context.current_time.total_seconds()/10000)) if context['cxi']['tanh_curve'] else 0
    cumulative_deviation = preformance_disquality + distance + instrument_instability
    # Gaussian distribution
    # https://towardsdatascience.com/gaussian-mixture-models-with-python-36dabed6212a
    # Add system stability, hyperbolic tangent
    data = random.normal(loc=1.0, scale=cumulative_deviation)
    return data

def cognative_temperature_curve(x_pos:float) -> float:
    """Agent cognitive temperature decrease
    https://www.desmos.com/calculator/cva2pdjqvq"""
    return 0.9 * pow(x_pos, 2) - 1.9 * x_pos + 1

def clamp(num:float, min_value:float, max_value:float):
    """Clamp a number to a minimum and maximum value"""
    return max(min(num, max_value), min_value)

def create_experiment_figure(context:Context, display:bool):
    """Depriciated: Create plotly timeline figure and display it"""
    if display:
        data_frame = pd.DataFrame([])
        for event in context.agenda.event_timeline:
            data_frame = pd.concat([data_frame, pd.DataFrame.from_records([{
                "Start":f"{context.start_time + event.start_time}",
                "Finish":f"{context.start_time + event.end_time}",
                "Task": "task",
                "Run": f"Run: {event.run_number}"}])])
        fig = px.timeline(data_frame,
            x_start="Start", x_end="Finish",
            y="Task", hover_name="Run")
        fig.update_yaxes(autorange="reversed")
        fig.show()
