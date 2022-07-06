"""Collection of objects"""
from __future__ import annotations
from math import sqrt
from typing import TYPE_CHECKING, List
from io import TextIOWrapper
from datetime import datetime, timedelta
import random
from model.library.enums import ExperimentState, InstrumentRunState, SampleType
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

    def concatbegining(self, add:str):
        """Add string to message"""
        self.messages = add + self.messages

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
    p_crazy_ivan = 0.001  # About 0.0001 gives you one/10k
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

    def __str__(self):
        return f'{self.quality:.2f}'

class SampleData:
    """Store all information about the sample as well as the datapoints
    Sample attributes are stored in dict sampleTypeMapper
    Preformance Quality, different natural signal response
    when data is on peak data * PQ"""
    # TODO: Add weights
    # Dozens of targets
    # N shaped dynamics

    def __init__(self, sample_type:SampleType, preformance_quality:float,
            weight:float, data_needed:float, setup_time:timedelta):
        self.preformance_quality:float = preformance_quality
        # TODO: Remove This
        self.data_needed:int = data_needed
        self.weight:float = weight
        self.setup_time:timedelta = setup_time
        self.type:SampleType = sample_type
        self.data:List[DataPoint] = []
        self.hit_number:int = 0
        self.miss_number:int = 0
        self.count:float = 0.0
        self.mean:float = 0.0
        self.m_2:float = 0.0
        self.variance:float = 0.0
        self.sdev:float = 0.0
        self.err:float = 0.0

    def append(self, data:DataPoint):
        """Append new data point run Welford's algorithm calculations
        https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance"""
        self.count += 1
        delta = data.quality - self.mean
        self.mean += delta /self.count
        delta2 = data.quality - self.mean
        self.m_2 += delta * delta2
        self.data.append(data)
        self.variance = self.m_2 / self.count
        self.sdev = sqrt(self.variance)
        self.err = self.sdev/sqrt(self.count)

    def __str__(self):
        # TODO: Clean this up
        if self.count == 0:
            return "mean:0, err:0, var:0, dev:0"
        return (f"mean:{self.mean:.6f}, err:{self.err:.6f},"+
            f" var:{self.variance:.6f}, dev:{self.sdev:.6f}")

class AMI:
    """Contains the data of the samples"""
    samples:List[SampleData] = []

    def __init__(self, number_of_samples:int):
        self.samples = [SampleData(SampleType.S1, random.gauss(0.90, 0.08),
            random.gauss(0.80, 0.20), int(random.gauss(150000, 500)),
            timedelta(minutes=random.gauss(1, 0.5))) for _ in range(0, number_of_samples)]

    def get_current_sample(self, context:Context) -> SampleData:
        """Get current Sample"""
        return self.samples[context.instrument.current_sample]

    def __str__(self):
        # TODO: Clean this up
        return_string = "["
        for sample in self.samples:
            return_string += f'{sample.type.value: >5}'
        return_string += "]\n["
        for sample in self.samples:
            return_string += f'{len(sample.data): >5}'
        return_string += "]\n["
        for sample in self.samples:
            return_string += f'{sample} '
        return return_string + "]\n"

class Agenda:
    """High Level Schedule of events for acheiving the goal"""
    experimental_time:timedelta = timedelta(0)
    event_timeline:List[Event] = []
    experiment_status:ExperimentState = ExperimentState.STOPED
    status = None

    def __init__(self, experimental_time):
        self.experimental_time = experimental_time

    def start_experiment(self):
        """Start the experiment if it has not been started"""
        if not self.experiment_status:
            self.experiment_status = ExperimentState.STARTED

    def is_started(self):
        """check if experiment has been started"""
        return self.experiment_status

    def finished(self):
        """Finished experiment"""
        self.status = "compleated"

    def __str__(self):
        return f"Experimental Time: {self.experimental_time}"

    def add_event(self, run_number:int, start_time:timedelta, end_time:timedelta):
        """Add event to agenda timeline"""
        self.event_timeline.append(Event(run_number, start_time, end_time))

    def get_timeline(self):
        """return final timeline string"""
        return ''.join(map(str, self.event_timeline))

class Event:
    """Object to specify the information from each event(run)"""
    run_number:int = None
    start_time:timedelta = None
    end_time:timedelta = None

    def __init__(self, run_number:int, start_time:timedelta, end_time:timedelta):
        self.run_number = run_number
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (f"Run: {self.run_number: >2}, Start: {self.start_time}, "+
            f"End: {self.end_time}, Duration: {self.end_time - self.start_time}\n")

class Context:
    """http://www.corej2eepatterns.com/ContextObject.htm"""
    current_time:timedelta = None
    ami:AMI = None
    agenda:Agenda = None # TODO: does the EM have the agenda
    agent_da:DataAnalyst = None
    agent_em:ExperimentManager= None
    agent_op:Operator = None
    instrument:CXI = None
    messages:CommunicationObject = None
    file:TextIOWrapper = None
    start_time:datetime = None

    def __init__(self, ami:AMI, agenda:Agenda, agent_da:DataAnalyst, agent_em:ExperimentManager,
            agent_op:Operator, instrument:CXI, messages:CommunicationObject, file:TextIOWrapper):
        self.current_time = timedelta(0)
        self.ami = ami
        self.agenda = agenda
        self.agent_da = agent_da
        self.agent_em = agent_em
        self.agent_op = agent_op
        self.instrument = instrument
        self.messages = messages
        self.file = file
        self.start_time = datetime.now()

    def file_write(self, message:str):
        """write file method"""
        self.file.write(f"{self.current_time} |"+
        f" DA_E:{self.agent_da.get_energy():.2f} "+
        f"DA_A:{self.agent_da.noticing_delay:.2f},"+
        f" OP_E:{self.agent_op.get_energy():.2f} "+
        f"OP_A:{self.agent_op.noticing_delay:.2f} | {message}\n")

    def update(self):
        """Make sure all objects are updated"""
        self.instrument.update(self)
        self.agent_da.update(self)
        self.agent_op.update(self)
