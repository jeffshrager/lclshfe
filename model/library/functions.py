"""Collection of functions"""
from __future__ import annotations
from typing import TYPE_CHECKING
from math import e, pi, sqrt
import plotly.express as px
import pandas as pd
from termcolor import colored
if TYPE_CHECKING:
    from model.library.objects import Context, AMI, SampleData

def get_parameters(context:Context) -> str:
    """get the simulation parameters"""
    return (f"Functional Acuity = {context.agent_op.functional_acuity} "+
        f"stream_shift_amount= {context.instrument.stream_status.stream_shift_amount}, "+
        f"p_stream_shift={context.instrument.stream_status.p_stream_shift}, "+
        f"beam_shift_amount={context.instrument.beam_status.beam_shift_amount}, "+
        f"p_crazy_ivan={context.instrument.stream_status.p_crazy_ivan}")

def calculate_roi(ami:AMI) -> str:
    """Determine the retun of investment data / time"""
    return sum(len(sample.data) >= sample.data_needed for sample in ami.samples) / len(ami.samples)

def get_line() -> str:
    """return string line"""
    return "---------------------------------------------------------------------------------------"

def goal_agenda_plan(context:Context) -> str:
    "Return out GAP: Goal Agenda Plan"
    return (f"{get_parameters(context)}\n{context.ami}\nCurrent Time: {context.current_time} "+
    f"{context.agenda}\n{get_line()}")

def experiment_stats(context:Context) -> str:
    "Write out statistics of the experiment"
    return (f"{context.ami}\nCurrent Time: {context.current_time} {context.agenda}\n"+
    f"{get_line()}\nROI: {calculate_roi(context.ami):.0%}\n{context.agenda.get_timeline()}")

def experiment_is_not_over(context:Context) -> bool:
    """True: Experiment is over, False: Experiment is still running"""
    return (context.current_time < context.agenda.experimental_time
    ) and (len(context.agenda.event_timeline) != len(context.ami.samples))

def get_current_datapoints(context:Context) -> str:
    """Gets the datapoints live"""
    return_string = ""
    for index, data in enumerate(context.ami.get_current_sample(context).data[-60:]):
        return_string += (colored(f'{data}', 'green'
        if data.quality >= context.ami.get_current_sample(context).preformance_quality
        else 'yellow' if data.quality >= get_gaussian(0.03) else 'red') +
        ("\n" if index == 19 or index == 39 else " "))
    return return_string

def get_gaussian(distance:float) -> float:
    """given distance calculate gaussian according to this:
    https://www.desmos.com/calculator/1dc980vuj1"""
    value_floor = 1.0 - (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(0 / 0.05, 2))
    data_distance = (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(distance / 0.05, 2))
    return data_distance + value_floor

def create_experiment_figure(context:Context, display:bool):
    """Create plotly timeline figure and display it"""
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
    if display:
        fig.show()
