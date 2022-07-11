"""Collection of functions"""
from __future__ import annotations
from typing import TYPE_CHECKING
from math import e, pi, sqrt
import plotly.express as px
import pandas as pd
from termcolor import colored
if TYPE_CHECKING:
    from model.library.objects import Context, AMI

def get_parameters(context:Context) -> str:
    """get the simulation parameters"""
    return (f"Functional Acuity = {context.agent_op.functional_acuity} "+
        f"stream_shift_amount= {context.instrument.stream_status.stream_shift_amount}, "+
        f"p_stream_shift={context.instrument.stream_status.p_stream_shift}, "+
        f"beam_shift_amount={context.instrument.beam_status.beam_shift_amount}, "+
        f"p_crazy_ivan={context.instrument.stream_status.p_crazy_ivan}")

def calculate_roi(ami:AMI) -> str:
    """Determine the retun of investment data / time"""
    return (sum(sample.compleated for sample in ami.samples) / len(ami.samples
    ) if len(ami.samples) > 0 else 0)

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
    """True: Experiment is not over, False: Experiment is over"""
    return (context.current_time < context.agenda.experimental_time
    ) and (len(context.agenda.event_timeline) != len(context.ami.samples)
    ) if (len(context.agenda.event_timeline) != 0
    ) else True

def get_current_datapoints(context:Context) -> str:
    """Gets the datapoints live"""
    current_sample = context.ami.get_current_sample(context)
    return_string = ""
    for index, data in enumerate(current_sample.data[-60:]):
        return_string += (colored(f'{data}', 'green'
        if data.quality >= aquire_data(0.001, current_sample.preformance_quality
        ) else 'yellow' if data.quality >= aquire_data(0.03, current_sample.preformance_quality
        ) else 'red') + ("\n" if index == 19 or index == 39 else " "))
    return return_string

def aquire_data(distance:float, preformance_quality:float) -> float:
    """given distance calculate gaussian according to this:
    https://www.desmos.com/calculator/1dc980vuj1"""
    # Ones with bad PQ have shallower slopes
    # QQQ: Why is it not taking less time for HIgh quality samples
    # a = 1 - preformance_quality
    a = 0.05
    if preformance_quality < 0.85:
        slope = -0.1
    else:
        slope = -0.0001
    data_distance = (0.12283 / (a * sqrt(2 * pi))) * pow(e, slope * pow(distance / a, 2))
    return data_distance

def cognative_temperature_curve(x_pos:float) -> float:
    """Agent cognitive temperature decrease
    https://www.desmos.com/calculator/cva2pdjqvq"""
    return 0.9 * pow(x_pos, 2) - 1.9 * x_pos + 1

def clamp(num:float, min_value:float, max_value:float):
    """Clamp a number to a minimum and maximum value"""
    return max(min(num, max_value), min_value)

def create_experiment_figure(context:Context, display:bool):
    """Create plotly timeline figure and display it"""
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
