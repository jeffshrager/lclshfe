"""Collection of functions"""
from __future__ import annotations
from typing import TYPE_CHECKING, List
from math import e, pi, sqrt
import plotly.express as px
import pandas as pd
from termcolor import colored
if TYPE_CHECKING:
    from model.library.objects import Context, AMI, SampleData

def get_simulation_parameters(context:Context) -> str:
    """get the simulation parameters"""
    return (f"Functional Acuity = {context.agent_op.functional_acuity} "+
        f"stream_shift_amount= {context.instrument_cxi.stream_status.stream_shift_amount}, "+
        f"p_stream_shift={context.instrument_cxi.stream_status.p_stream_shift}, "+
        f"beam_shift_amount={context.instrument_cxi.beam_status.beam_shift_amount}, "+
        f"p_crazy_ivan={context.instrument_cxi.stream_status.p_crazy_ivan}")

def calculate_roi(ami:AMI) -> str:
    """Determine the retun of investment data / time"""
    return f'{sum(len(sample[0].data) >= sample[0].datapoints_needed for sample in ami.samples)/len(ami.samples):.0%}'

def get_line() -> str:
    """return string line"""
    return "--------------------------------------------------------------------------------------------------"

def goal_agenda_plan(context:Context) -> str:
    "Return out GAP: Goal Agenda Plan"
    return (f"{get_simulation_parameters(context)}\n{context.ami}\n"+
    f"Current Time: {context.current_time} {context.agent_em.agenda}\n{get_line()}")

def experiment_stats(context:Context) -> str:
    "Write out statistics of the experiment"
    return (f"{context.ami}\nCurrent Time: {context.current_time} {context.agent_em.agenda}\n"+
    f"{get_line()}\nROI: {calculate_roi(context.ami)}\n{context.agent_em.agenda.get_timeline()}")

def experiment_is_not_over(context:Context) -> bool:
    """True: Experiment is over, False: Experiment is still running"""
    return (context.current_time < context.agent_em.agenda.experimental_time
    ) and (len(context.agent_em.agenda.event_timeline) != len(context.ami.samples))

def create_experiment_figure(context:Context, display:bool):
    """Create plotly timeline figure and display it"""
    data_frame = pd.DataFrame([])
    for event in context.agent_em.agenda.event_timeline:
        data_frame = pd.concat([data_frame, pd.DataFrame.from_records([{
            "Start":f"{context.start_time + event['start_time']}",
            "Finish":f"{context.start_time + event['end_time']}",
            "Task": "task",
            "Run": f"Run: {event['run_number']}"}])])
    fig = px.timeline(data_frame,
        x_start="Start", x_end="Finish",
        y="Task", hover_name="Run")
    fig.update_yaxes(autorange="reversed")
    if display:
        fig.show()

def get_all_datapoints(context:Context) -> str:
    """get all datapoints of all samples in a string"""
    line_counter:int = 0
    return_string = "\n"
    for sample in context.ami.samples:
        s_goal:SampleData = sample[0]
        return_string += f"{s_goal.type}\n"
        for data in s_goal.data:
            if data.quality >= s_goal.preformance_quality:
                return_string += f"{colored(f'{data}', 'green')}, "
            elif data.quality >= get_gaussian(0.03):
                return_string += f"{colored(f'{data}', 'yellow')}, "
            else:
                return_string += f"{colored(f'{data}', 'red')}, "
            line_counter += 1
            if line_counter == 20:
                line_counter = 0
                return_string += "\n"
        break
    return_string += "\n"
    return return_string

def get_current_datapoints(context:Context) -> str:
    """Gets the datapoints live"""
    row_counter:int = 0
    line_counter:int = 0
    return_string = ""
    s_goal:SampleData = context.ami.samples[context.instrument_cxi.current_sample][0]
    for data in s_goal.data[::-1]:
        if data.quality >= s_goal.preformance_quality:
            return_string += f"{colored(f'{data}', 'green')}, "
        elif data.quality >= get_gaussian(0.03):
            return_string += f"{colored(f'{data}', 'yellow')}, "
        else:
            return_string += f"{colored(f'{data}', 'red')}, "
        row_counter += 1
        if row_counter == 20:
            row_counter = 0
            return_string += "\n"
            line_counter += 1
        if line_counter == 3:
            break
    return return_string

def get_gaussian(distance:float) -> float:
    """given distance calculate gaussian according to this:
    https://www.desmos.com/calculator/1dc980vuj1"""
    value_floor = 1.0 - (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(0 / 0.05, 2))
    data_distance = (0.125 / (0.05 * sqrt(2 * pi))) * pow(e, -0.5 * pow(distance / 0.05, 2))
    return data_distance + value_floor

def generate_samples() -> List[SampleData]:
    """generate samples"""
    return None
