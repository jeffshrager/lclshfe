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
import time
from typing import TYPE_CHECKING, List
from rich.table import Table
from rich import box
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.layout import Layout
from rich.panel import Panel
from rich.pretty import Pretty
from functools import reduce
from numpy import arange, random
import plotly.express as px
import pandas as pd
if TYPE_CHECKING:
    import sim.model.objects as objects

def rgb(p):# <-- percentage as parameter
    """Get RGB values from a percentage"""
    p = p * 70
    #Starting with color red
    d = [255,0,0]
    #formula for finding green value by percentage
    d[1] = int((510*p)/100)
    # print(d[1])
    #if green value more than 255
    #set green value 255
    #reduce the red value from remaining green value
    if d[1]>255:
        d[0] -= d[1]-255
        d[1] = 255
    return f"{d[0]},{d[1]},{d[2]}"

def calculate_roi(ami:objects.AMI) -> str:
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

def cumulative_estimated_run_length(context:objects.Context) -> timedelta:
    """Cumulative estimated run length"""
    return timedelta(seconds=sum([sample.estimated_run_length.total_seconds() for sample in context.ami.samples]))

def generate_layout(context:objects.Context, overall_progress, number_of_combinations:int) -> Layout:
    """Generate a layout for the model."""
    layout = Layout()
    layout.split_row(
    Layout(name="left", ratio=4),
    Layout(name="right", ratio=6))

    layout["right"].split_column(
    Layout(goal_agenda_plan(context), name="time", size=4),
    Layout(generate_table(context), name="table"))

    layout["left"].split_row(
    Layout(get_run_sequence(context, number_of_combinations), name="run number", size=4),
    Layout(name="info"))

    layout["info"].split_column(
    Layout(Panel(overall_progress, box=box.SIMPLE), name="position", size=3),
    Layout(name="information"))

    layout["information"].split_column(
    Layout(get_position_display(context), name="position", size=3),
    Layout(name="instrument"))

    layout["instrument"].split_row(
    Layout(get_config_string(context), name="config", size=38),
    Layout(name="data_messages"))

    layout["data_messages"].split_row(
    Layout(get_data_stream_display(context), name="data", size=8),
    Layout(get_messages(context), name="messages"))
    return layout

def get_run_sequence(context:objects.Context, number_of_combinations:int) -> Panel:
    """Get the other string"""
    return_string = ""
    for run in range (number_of_combinations):
        return_string += f"{'[green]' if context.config['run_number'] == run else '[default]'}{run}\n"
    # [return_string f"{run}\n" for run in range(number_of_combinations)]
    # {['[green]'] if context.config['run_number'] == run else ['default']}
    return Panel(return_string, box=box.SIMPLE, padding=0)
    # return Panel("1\n2\n3\n4\n5\n6\n7\n8", box=box.SIMPLE, padding=0)

def get_other(context:objects.Context) -> Panel:
    """Get the other string"""
    return Panel(f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    f"  Current Time: {context.current_time} | {context.agenda}", padding=0)

def get_messages(context:objects.Context) -> Panel:
    """Get the config string"""
    panel = Panel(str(context.messages), box=box.SIMPLE, padding=0)
    return panel

def get_position_display(context:objects.Context) -> Panel:
    """Get the config string"""
    panel = Panel(str(context.instrument.position_display), box=box.SIMPLE, padding=0)
    return panel

def get_data_stream_display(context:objects.Context) -> Panel:
    """Get the config string"""
    panel = Panel(str(context.instrument.data_stream), box=box.MARKDOWN, padding=0)
    return panel


def config_str(d:dict) -> dict:
    """Config string"""
    return (f := lambda d: {k: f(v) for k, v in d.items()} if type(d) == dict else [str(i) for i in d] if isinstance(d, list) else d)(d)

# def config_str(dictionary:dict) -> dict:
#     """Config print"""
#     return_dict = ""
#     for k, v in dictionary.items():
#         # if k != 'samples' and k != 'start_time' and k != 'experimental_time':
#         if isinstance(v, dict):
#             return_dict += config_print(v)
#         else:
#             if isinstance(v, list):
#                 list_string = ""
#                 for item in v:
#                     list_string += f"{item}, "
#                 return_dict += f"{k}: {list_string}"
#             else:
#                 return_dict += (f"{k}:{v}, ")
#     return return_dict

def get_config_string(context:objects.Context) -> Panel:
    """Get the config string"""
    pretty = Pretty(config_str(context.config.override_dictionary))
    panel = Panel(pretty, box.MINIMAL)
    return panel

def generate_table(context:objects.Context) -> Panel:
    """Make a new table."""
    # table = Table(box=box.HORIZONTALS)
    table = Table(show_header=True, box=box.SIMPLE_HEAVY, padding=0)
    table.add_column("")
    table.add_column("mean")
    table.add_column("")
    table.add_column("")
    table.add_column("")
    table.add_column("time")
    table.add_column("")
    table.add_column("")
    table.add_column("data")
    table.add_column("")
    table.add_column("")
    table.add_column("")
    table.add_column("")

    for index, sample in enumerate(context.ami.samples):
        values = sample.get_stats()
        table.add_row(
            f"{'[green dim]' if sample.compleated else ('[bold green]' if sample.running else '[default dim]')}{str(index): >2} |N:", f" [default not dim]{len(sample.data): >6}", "[dim]-", f"{values[0]}", f"{values[1]}", f"{values[2]}", f"{values[3]}", f"{values[4]}", f"{values[5]}", f"{values[6]}", f"{values[7]}", f"{values[8]}", f"{values[9]}"
        )
    return Panel(table, box=box.SIMPLE)

def ami_sample_table(context:objects.Context):
    """Return a table of the AMI samples"""
    return context.ami

def goal_agenda_plan(context:objects.Context) -> Panel:
    "Return out GAP: Goal Agenda Plan"
    # return (f"{config_print(context.config.override_dictionary)}\n{get_line()}\n"+
    # f"{ami_sample_table(context)}\n"+
    return Panel(f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    f"  Current Time: {context.current_time} | {context.agenda}", box=box.SIMPLE)
    # return (f"{config_print(context.config.override_dictionary)}\n{get_line()}\n{context.ami}\n"+
    # f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    # f"  Current Time: {context.current_time} | {context.agenda}\n{get_line()}")

def experiment_stats(context:objects.Context) -> str:
    "Write out statistics of the experiment"
    return ""
    # return (f"{context.ami}\n"+
    # f"Estimated Time: {str(cumulative_estimated_run_length(context)).split('.', maxsplit=1)[0]} | Error Threshold - Target: {context['data_analysis']['target_error']} Current {context.agent_da.target_error}\n"+
    # f"  Current Time: {context.current_time} {context.agenda}\n"+
    # f"{get_line()}\nROI: {calculate_roi(context.ami):.0%}\n{context.agenda.get_timeline()}")

def experiment_is_over(context:objects.Context) -> bool:
    """Determines if the experiment is over

    If strict time is enabled - when the experiment reaches the
    end time it will stop regardless if the samples have finished
    collecting data. If strict time is disabled - The experiment
    will finish collecting data on all the samples and will stop
    after the last sample has finished collecting data.

    Args:
        context: Context object for access to run data

    Returns:
        False: Experiment is not over
        True: Experiment is over
    """
    return (context.current_time >= context.agenda.experimental_time \
    if context['settings']['strict_time'] else False or
    len(context.agenda.event_timeline) == len(context.ami.samples) \
    if context.agenda.event_timeline else False)

def get_current_datapoints(context:objects.Context) -> str:
    """Gets the datapoints live"""
    current_sample = context.ami.get_current_sample(context)
    return_string = ""
    for data in current_sample.data[-70:]:
        return_string += f"{'[green]' if data.quality >= aquire_data(0.001, current_sample.preformance_quality, context) else '[yellow]' if data.quality >= aquire_data(0.03, current_sample.preformance_quality, context) else '[red]'}{data}\n"
    return return_string

def aquire_data(distance:float, preformance_quality:float, context:objects.Context) -> float:
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

def create_experiment_figure(context:objects.Context, display:bool):
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
