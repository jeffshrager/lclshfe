"""Contains stateless functions that are used in the model.

This is used to simplify the model code. All functions that do not
require state should be placed here. These will not contain the self
attribute and will be called as functions.

  Typical usage example:

  roi = calculate_roi(ami)
  line = get_line()
"""
from __future__ import annotations
import collections.abc
from datetime import timedelta
from math import tanh
from typing import TYPE_CHECKING
from functools import reduce
from numpy import arange, random
import plotly.express as px
import pandas as pd
from termcolor import colored
if TYPE_CHECKING:
    from src.library.objects.objs import Context, AMI

def calculate_roi(ami:AMI) -> str:
    """Determine the retun of investment data / time.

    Goes through each sample and determines if they all were compleated.
    If they were, the ROI would be 100%, if not the roi percent
    is calculated.

    Args:
        ami: an AMI object which contains all the data and the state
        that the sample is in.

    Returns:
        A string that is the ROI of the experiment. In percent.
    """
    # TODO: Precision calculation - goes into ROI
    return (sum(sample.compleated for sample in ami.samples) / len(ami.samples
    ) if len(ami.samples) > 0 else 0)

def update_dict(d, u):
    """Recursively update nested dicts

    Update nested dicts with the values from the second nested dict.

    Args:
        d: Dictionary to update
        {
            'a': {'c': 1, 'd': 3},
            'b': 2,
        }
        u: Dictionary to update with
        {
            'a': {'c': 2, 'd': 3, e': 4},
            'b': 1,
        }

    Returns:
        A new dictionary with the updated values.
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:
        {
            'a': {'c': 2,'d': 3, 'e': 4},
            'b': 1,
        }
    """
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
        if k != 'samples' and k != 'start_time' and k != 'experimental_time':
            if isinstance(v, dict):
                return_string += config_print(v)
            else:
                if isinstance(v, list):
                    list_string = ""
                    for item in v:
                        list_string += f"{item}, "
                    return_string += f"{k}: {list_string}"
                else:
                    return_string += (f"{k}:{v}, ")
    return return_string

def cumulative_estimated_run_length(context:Context) -> timedelta:
    """Cumulative estimated run length"""
    return timedelta(seconds=sum([sample.run_length.total_seconds() for sample in context.ami.samples]))

def goal_agenda_plan(context:Context) -> str:
    "Return out GAP: Goal Agenda Plan"
    return (f"{config_print(context.config.override_dictionary)}\n{get_line()}\n{context.ami}\n"+
    f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    f"  Current Time: {context.current_time} | {context.agenda}\n{get_line()}")

def experiment_stats(context:Context) -> str:
    "Write out statistics of the experiment"
    return (f"{context.ami}\n"+
    f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    f"  Current Time: {context.current_time} {context.agenda}\n"+
    f"{get_line()}\nROI: {calculate_roi(context.ami):.0%}\n{context.agenda.get_timeline()}")

def experiment_is_not_over(context:Context) -> bool:
    """True: Experiment is not over, False: Experiment is over"""
    # Time does not affect it
    return (len(context.agenda.event_timeline) != len(context.ami.samples)
    ) if (len(context.agenda.event_timeline) != 0) else True
    # return (context.current_time < context.agenda.experimental_time
    # ) and (len(context.agenda.event_timeline) != len(context.ami.samples)
    # ) if (len(context.agenda.event_timeline) != 0) else True

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
    """Calculate the quality of the data given the distance and preformance quality

    Used this gaussian curve: https://www.desmos.com/calculator/1dc980vuj1
    using distance and preformance quality to determine where the quality
    for this given data point is on the curve.

    Args:
        distance: an AMI object which contains all the data and the state
        preformance_quality: the quality of the preformance of the agent
        context: the context of the agent

    Returns:
        A string that is the ROI of the experiment. In percent.
    """
    preformance_disquality = 1 - preformance_quality
    # cumulative_deviation = (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(distance/ 0.05, 2))
    # FFF: Figure out what this should really be
    # print(context.current_time.total_seconds()/1000)
    # TODO: Add instument instability to config
    # Have this reset for every shift change
    instrument_instability = (1 - tanh(context.current_time.total_seconds()/10000)) if context['instrument']['tanh_curve'] else 0
    cumulative_deviation = preformance_disquality + distance + instrument_instability
    # Gaussian distribution
    # https://towardsdatascience.com/gaussian-mixture-models-with-python-36dabed6212a
    # Add system stability, hyperbolic tangent
    data = random.normal(loc=1.0, scale=cumulative_deviation)
    return data

def cognative_temperature_curve(x_pos:float) -> float:
    """Agent cognitive temperature decrease

    Used this curve: https://www.desmos.com/calculator/cva2pdjqvq
    using distance and preformance quality to determine where the quality
    for this given data point is on the curve.

    Args:
        distance: an AMI object which contains all the data and the state
        preformance_quality: the quality of the preformance of the agent
        context: the context of the agent

    Returns:
        A string that is the ROI of the experiment. In percent.
    """
    return 0.9 * pow(x_pos, 2) - 1.9 * x_pos + 1

def clamp(num:float, min_value:float, max_value:float):
    """Clamp a number to a minimum and maximum value

    Update nested dicts with the values from the second nested dict.

    Args:
        d: Dictionary to update
        {
            'a': {'c': 1, 'd': 3},
            'b': 2,
        }
        u: Dictionary to update with
        {
            'a': {'c': 2, 'd': 3, e': 4},
            'b': 1,
        }

    Returns:
        A new dictionary with the updated values.
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:
        {
            'a': {'c': 2,'d': 3, 'e': 4},
            'b': 1,
        }
    """
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
