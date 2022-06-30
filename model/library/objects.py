"""Collection of objects"""
from __future__ import annotations
from io import TextIOWrapper
from typing import TYPE_CHECKING, List
from datetime import timedelta
import random
import numpy
from model.library.enums import InstrumentRunState, SampleType
if TYPE_CHECKING:
    from model.agent import DataAnalyst, ExperimentManager, Operator
    from model.instrument import CXI

class CommunicationObject:
    """Object that stores the communication"""
    messages = ""

    def __init__(self):
        pass

    def reset(self):
        """Reset the messages string"""
        self.messages = ""

    def concat(self, add:str):
        """Add string to message"""
        self.messages += add

    def __str__(self):
        return self.messages

class InstrumentStatus:
    """Object that stores the current status regarding the instrument"""
    hits = 0
    misses = 0
    msg = ""
    is_running = InstrumentRunState.STOPPED
    # These are counted over all reps and then the mean is display at the end
    n_crazy_ivans = 0

    def __init__(self):
        pass

    def start(self):
        """Start the Instrumnet"""
        self.is_running = InstrumentRunState.RUNNING

    def stop(self):
        """Stop the Instrumnet"""
        self.is_running = InstrumentRunState.STOPPED

class Stream:
    """We have a stream (aka. jet) which shifts around in accord with these params.
    The stream_shift_time_slice is a bit obscure. The idea is that.

    Warning: The stream shift amount should be an integer multiple of the beam_shift_amount,
    otherwisethe likelihood that they overlap (based on acuity) will be reduced.
    Usually these will be the same."""

    stream_shift_amount = 0.01  # Minimal unit of stream shift
    p_stream_shift = 0.15  # prob. of stream shift per cycle
    # A crazy ivan is when the stream goes haywire; It should happen very rarely.
    p_crazy_ivan = 0.01  # About 0.0001 gives you one/10k
    crazy_ivan_shift_amount = round(random.uniform(0.1, 0.2), 2)  # 0.2
    # If the beam doesn't hit a wall before this, we cut the run off here.
    default_max_cycles = 10000
    stream_pos = 0.0
    allow_response_cycle = 99999999999
    cycle = 1

    def __init__(self):
        pass

class Beam:
    """And the beam, which is under the control of the operator (or automation),
    which can be shifted in accord with these params:"""
     # You may want to have more or less fine control of the beam vs. the stream's shiftiness
    beam_shift_amount = 0.01

    # There are two different and wholly separate senses of acuity:
    # physical_acuity: Whether the beam is physically on target, and functional_acuity:
    # whether the operator can SEE that it is!
    # Nb. Whole scale is -1...+1
    # You want this a little larger than the shift so that it allows for near misses
    physical_acuity = 0.02
    beam_pos = 0.0

class DataPoint:
    """Object to store all the data for each beam point"""
    quality:float = None

    def __init__(self, quality):
        self.quality = quality

class SampleData:
    """Store all information about the sample as well as the datapoints"""
    # TODO: Preformance Quality, different natural signal response
    # TODO: when data is on peak data * PQ
    sampleTypeMapper = {
        SampleType.S1: {'preformance_quality': 0.95,
                        'datapoints_needed': 10000,
                        'setup_time': timedelta(minutes=10)},
        SampleType.S2: {'preformance_quality': 0.90,
                        'datapoints_needed': 11000,
                        'setup_time': timedelta(minutes=15)},
        SampleType.S3: {'preformance_quality': 0.85,
                        'datapoints_needed': 12000,
                        'setup_time': timedelta(minutes=12)}}

    def __init__(self, sample_type:SampleType):
        values = self.sampleTypeMapper.get(sample_type)
        self.preformance_quality:float = values.get("preformance_quality")
        self.datapoints_needed:int = values.get("datapoints_needed")
        self.setup_time:timedelta = values.get("setup_time")
        self.type:SampleType = sample_type
        self.data:List[DataPoint] = []
        self.hit_number:int = 0
        self.miss_number:int = 0

    def append(self, datapoint:DataPoint):
        """Append new data point and camculate new Mean Hit Fraction"""
        # TODO: How do we know if it hit?
        varry_amount = 0.1
        if datapoint.quality >= (1.0 * self.preformance_quality) - varry_amount and datapoint.quality <= (1.0 * self.preformance_quality) + varry_amount:
            self.hit_number += 1
        else:
            self.miss_number += 1
        self.data.append(datapoint)

    def get_mean_hit_fraction(self) -> str:
        """return hits / hits + misses"""
        if self.hit_number + self.miss_number > 0:
            return format(numpy.mean(self.hit_number / (self.hit_number + self.miss_number)), '.2f')
        else:
            return 0

    def __str__(self):
        return f"{len(self.data)}"

class Goal:
    """Defines what is supposed to be acomplished"""
    samples:List[SampleData] = []
    status = None

    def __init__(self, number_of_samples:int):
        self.samples = [[SampleData(SampleType.S1)] for _ in range(0, number_of_samples//3)]
        self.samples += [[SampleData(SampleType.S2)] for _ in range((number_of_samples//3)+1, ((number_of_samples//3)*2) + 1)]
        self.samples += [[SampleData(SampleType.S3)] for _ in range(((number_of_samples//3)*2) + 2, number_of_samples+2)]
        # self.samples = [[SampleData(SampleType.S1)] for _ in range(0, 1)]
        # self.samples += [[SampleData(SampleType.S2)] for _ in range(2, 10)]

    def finished(self):
        """Finished experiment"""
        self.status = "compleated"

    def __str__(self):
        # TODO: clean this up
        return_string = "["
        for index, sample in enumerate(self.samples):
            if index == len(self.samples)-1:
                s_goal:SampleData = sample[0]
                return_string += f'{s_goal.type.value: >5}'
            else:
                s_goal:SampleData = sample[0]
                return_string += f'{s_goal.type.value: >5},'
        return_string += "]\n["
        for index, sample in enumerate(self.samples):
            if index == len(self.samples)-1:
                s_goal:SampleData = sample[0]
                return_string += f'{len(s_goal.data): >5}'
            else:
                s_goal:SampleData = sample[0]
                return_string += f'{len(s_goal.data): >5},'
        return_string += "]\n["
        for index, sample in enumerate(self.samples):
            if index == len(self.samples)-1:
                s_goal:SampleData = sample[0]
                return_string += f'{s_goal.get_mean_hit_fraction(): >5}'
            else:
                s_goal:SampleData = sample[0]
                return_string += f'{s_goal.get_mean_hit_fraction(): >5},'
        return_string += "]\n"
        return return_string

class Agenda:
    """High Level Schedule of events for acheiving the goal"""
    experimental_time = timedelta(0)
    event_timeline = []

    def __init__(self, experimental_time):
        self.experimental_time = experimental_time

    # TODO: event object
    def add_event(self, run_number:int, start_time:timedelta, end_time:timedelta):
        """Add event to agenda timeline"""
        self.event_timeline.append({"run_number":run_number,
                "start_time":start_time, "end_time":end_time})

    def __str__(self):
        return f"Experimental Time: {self.experimental_time}"

    def get_timeline(self):
        """return final timeline string"""
        return_string = ""
        for event in self.event_timeline:
            return_string+=(f"Run: {event['run_number']: >2},"+
                f" Start: {event['start_time']}, End: {event['end_time']},"+
                f" Duration: {event['end_time'] - event['start_time']}\n")
        return return_string

class Context:
    """http://www.corej2eepatterns.com/ContextObject.htm"""
    current_time:timedelta = None
    goal:Goal = None
    agent_da:DataAnalyst = None
    agent_em:ExperimentManager= None
    agent_op:Operator = None
    instrument_cxi:CXI = None
    messages:CommunicationObject = None
    file:TextIOWrapper = None

    def __init__(self, goal:Goal, agent_da:DataAnalyst, agent_em:ExperimentManager,
            agent_op:Operator, instrument_cxi:CXI, messages:CommunicationObject,
            file:TextIOWrapper):
        self.current_time = timedelta(0)
        self.goal = goal
        self.agent_da = agent_da
        self.agent_em = agent_em
        self.agent_op = agent_op
        self.instrument_cxi = instrument_cxi
        self.messages = messages
        self.file = file
