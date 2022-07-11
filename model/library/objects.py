"""Collection of objects"""
from __future__ import annotations
from math import sqrt
from typing import TYPE_CHECKING, List
from io import TextIOWrapper
import random
from datetime import datetime, timedelta
from model.library.enums import ExperimentState, InstrumentRunState
from model.library.functions import clamp
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
    p_crazy_ivan = 0.0001  # About 0.0001 gives you one/10k
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
    data:List[DataPoint] = []

    # TODO: make weights affect rescheduling
    # TODO: What was this N shaped dynamics
    def __init__(self, preformance_quality:float,
            weight:float, setup_time:timedelta):
        self.compleated:bool = False
        self.timeout:bool = False
        self.preformance_quality:float = preformance_quality
        self.weight:float = weight
        self.setup_time:timedelta = setup_time
        self.data:List[DataPoint] = []
        self.count:float = 0.0
        self.mean:float = 0.0
        self.m_2:float = 0.0
        self.variance:float = 0.0
        self.sdev:float = 0.0
        self.err:float = 0.0
        self.count_array = []
        self.err_array = []

    def append(self, data:DataPoint):
        """Append new data point run Welford's algorithm calculations
        https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance"""
        self.count += 1
        delta = data.quality - self.mean
        self.mean += delta / self.count
        delta2 = data.quality - self.mean
        self.m_2 += delta * delta2
        self.data.append(data)

        self.variance = self.m_2 / self.count
        self.sdev = sqrt(self.variance)
        self.err = self.sdev / sqrt(self.count)
        self.count_array.append(self.count)
        self.err_array.append(self.err)

    def reset(self):
        """Reset the data"""
        self.compleated = False
        self.timeout = False
        self.data = []
        self.count = 0.0
        self.mean = 0.0
        self.m_2 = 0.0
        self.variance = 0.0
        self.sdev = 0.0
        self.err = 0.0
        self.count_array = []
        self.err_array = []

    def file_string(self) -> str:
        """Return a string that can be written to a file"""
        return f'{self.preformance_quality}, {self.weight}, {self.mean:.15f}, {self.m_2:.15f}, {self.variance:.15f}, {self.sdev:.15f}, {self.err:.15f}'

    def __str__(self):
        return (f"pq:{self.preformance_quality:.6f}, mean:{self.mean:.6f}, err:{self.err:.6f},"+
            f" var:{self.variance:.6f}, dev:{self.sdev:.6f}" if self.count != 0 else
            "pq:0.000000, mean:0.000000, err:0.000000, var:0.000000, dev:0.000000")

class AMI:
    """Contains the data of the samples"""
    # FFF: AMI only gets a subset of samples
    # AMI is different than data pipeline

    # TODO: Wan-Lin's discomfort: seperate PQ and Importance
    # Were using PQ as double meaning, one is quality of sample,
    # also using as inverse proxy as importance
    samples:List[SampleData] = []
    random_samples:bool = None

    def __init__(self, samples, random_samples):
        self.samples:List[SampleData] = []
        self.random_samples = random_samples
        if not random_samples:
            sample:SampleData
            for sample in samples:
                sample.reset()
            self.samples = samples

    def load_samples(self, number_of_samples:int):
        """Load the samples using a random distribution"""
        if self.random_samples: 
            self.samples = [SampleData(clamp(random.gauss(0.90, 0.2), 0.00, 0.99),
                random.gauss(0.80, 0.20), timedelta(minutes=random.gauss(1, 0.5)))
                for _ in range(number_of_samples)]

    def sort_samples(self):
        """Sort the samples by PQ"""
        self.samples.sort(key=lambda x: x.preformance_quality)

    def get_current_sample(self, context:Context) -> SampleData:
        """Get current Sample"""
        return self.samples[context.instrument.current_sample]

    def __str__(self):
        return_string = ""
        for sample in self.samples:
            # pq, mean, err, var, dev
            return_string += f'N: {len(sample.data): >6} - {sample}\n'
        return return_string

class Agenda:
    """High Level Schedule of events for acheiving the goal"""
    experimental_time:timedelta = timedelta(0)
    number_of_samples:int = 0
    event_timeline:List[Event] = []
    experiment_status:ExperimentState = ExperimentState.STOPED
    status = None

    def __init__(self, experimental_time, number_of_samples):
        self.experimental_time:timedelta = experimental_time
        self.event_timeline:List[Event] = []
        self.experiment_status:ExperimentState = ExperimentState.STOPED
        self.status = None
        self.number_of_samples = number_of_samples

    def start_experiment(self):
        """Start the experiment if it has not been started"""
        if not self.experiment_status.value:
            self.experiment_status = ExperimentState.STARTED

    def is_started(self):
        """check if experiment has been started"""
        return self.experiment_status.value

    def finished(self):
        """Finished experiment"""
        self.status = "compleated"

    def __str__(self):
        return f"Experimental Time: {self.experimental_time}"

    def add_event(self, run_number:int, start_time:timedelta, end_time:timedelta, time_out:bool):
        """Add event to agenda timeline"""
        self.event_timeline.append(Event(run_number, start_time, end_time, time_out))

    def get_timeline(self):
        """return final timeline string"""
        return ''.join(map(str, self.event_timeline))

class Event:
    """Object to specify the information from each event(run)"""
    run_number:int = None
    start_time:timedelta = None
    end_time:timedelta = None
    time_out:bool = None

    def __init__(self, run_number:int, start_time:timedelta, end_time:timedelta, time_out:bool):
        self.run_number = run_number
        self.start_time = start_time
        self.end_time = end_time
        self.time_out = time_out

    def __str__(self):
        return (f"Run: {self.run_number: >2}, Timeout: {self.time_out}, Start: {self.start_time}, "+
            f"End: {self.end_time}, Duration: {self.end_time - self.start_time}\n")

class Context:
    """http://www.corej2eepatterns.com/ContextObject.htm"""
    current_time:timedelta = None
    ami:AMI = None
    agenda:Agenda = None
    agent_da:DataAnalyst = None
    agent_em:ExperimentManager= None
    agent_op:Operator = None
    instrument:CXI = None
    messages:CommunicationObject = None
    file:TextIOWrapper = None
    data_file:TextIOWrapper = None
    start_time:datetime = None

    def __init__(self, ami:AMI, agenda:Agenda, agent_da:DataAnalyst, agent_em:ExperimentManager,
            agent_op:Operator, instrument:CXI, messages:CommunicationObject, file:TextIOWrapper, data_file:TextIOWrapper):
        self.current_time = timedelta(0)
        self.ami = ami
        self.agenda = agenda
        self.agent_da = agent_da
        self.agent_em = agent_em
        self.agent_op = agent_op
        self.instrument = instrument
        self.messages = messages
        self.file = file
        self.data_file = data_file
        self.start_time = datetime.now()

    def file_write(self, message:str):
        """write file method"""
        self.file.write(f"{self.current_time} |"+
        f" DA_E:{self.agent_da.get_energy():.2f} "+
        f" OP_E:{self.agent_da.get_attention():.2f} | {message}\n")
        # self.file.write(f"{self.current_time} |"+
        # f" DA_E:{self.agent_da.get_energy():.2f} "+
        # f"DA_A:{self.agent_da.noticing_delay:.2f},"+
        # f" OP_E:{self.agent_op.get_energy():.2f} "+
        # f"OP_A:{self.agent_op.noticing_delay:.2f} | {message}\n")

    def printer(self, console:str, file:str):
        """Print message to console"""
        self.messages.concat(f"{console}\n")
        self.file_write(file)

    def update(self):
        """Make sure all objects are updated"""
        self.instrument.update(self)
        self.agent_da.update(self)
        self.agent_op.update(self)
