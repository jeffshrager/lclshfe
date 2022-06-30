"""Collection of functions"""
from model.library.objects import Context, Goal, SampleData

def get_simulation_parameters(context:Context) -> str:
    """get the simulation parameters"""
    return (f"Functional Acuity = {context.agent_op.functional_acuity} "+
        f"stream_shift_amount= {context.instrument_cxi.stream_status.stream_shift_amount}, "+
        f"p_stream_shift={context.instrument_cxi.stream_status.p_stream_shift}, "+
        f"beam_shift_amount={context.instrument_cxi.beam_status.beam_shift_amount}, "+
        f"p_crazy_ivan={context.instrument_cxi.stream_status.p_crazy_ivan}")

def calculate_roi(goal:Goal) -> str:
    """Determine the retun of investment data / time"""
    roi = 0
    for i in goal.samples:
        s_goal:SampleData = i[0]
        if len(s_goal.data) >= s_goal.datapoints_needed:
            roi += 1
    percent_string = '{:.0%}'
    return percent_string.format(roi/len(goal.samples))

def get_line() -> str:
    """return string line"""
    return "-------------------------------------------------"

def goal_agenda_plan(context:Context) -> str:
    "Return out GAP: Goal Agenda Plan"
    return (f"{get_simulation_parameters(context)}\n{context.goal}\n"+
    f"Current Time: {context.current_time} {context.agent_em.agenda}\n{get_line()}")

def experiment_stats(context:Context) -> str:
    "Write out statistics of the experiment"
    return (f"{context.goal}\nCurrent Time: {context.current_time} {context.agent_em.agenda}\n"+
    f"{get_line()}\nROI: {calculate_roi(context.goal)}\n{context.agent_em.agenda.get_timeline()}")

def experiment_is_not_over(context:Context) -> bool:
    """True: Experiment is over, False: Experiment is still running"""
    return (context.current_time < context.agent_em.agenda.experimental_time
    ) and (len(context.agent_em.agenda.event_timeline) != len(context.goal.samples))
