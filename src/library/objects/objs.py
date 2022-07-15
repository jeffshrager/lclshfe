"""Collection of objects"""
from __future__ import annotations
from math import sqrt
import os
from time import time
from typing import TYPE_CHECKING, List
from io import TextIOWrapper
import random
from datetime import datetime, timedelta
from src.library.objects.enums import ExperimentState, InstrumentRunState
from src.library.functions.func import clamp
if TYPE_CHECKING:
    from src.library.objects.agent import DataAnalyst, ExperimentManager, Operator
    from src.library.objects.instrument import CXI

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

    stream_shift_amount:float = 0.0  # Minimal unit of stream shift
    p_stream_shift:float = 0.0  # prob. of stream shift per cycle
    # A crazy ivan is when the stream goes haywire; It should happen very rarely.
    p_crazy_ivan:float = 0.0  # About 0.0001 gives you one/10k
    crazy_ivan_shift_amount:float = round(random.uniform(0.1, 0.2), 2)  # 0.2
    # If the beam doesn't hit a wall before this, we cut the run off here.
    default_max_cycles:int = 10000
    stream_pos:float = 0.0
    allow_response_cycle:int = 99999999999
    cycle:int = 1

    def __init__(self, config:Config):
        self.stream_shift_amount = config['cxi_stream_shift_amount']
        self.p_stream_shift = config['cxi_p_stream_shift']
        self.p_crazy_ivan = config['cxi_p_crazy_ivan']
        # self.crazy_ivan_shift_amount = config['cxi_crazy_ivan_shift_amount']

class Beam:
    """And the beam, which is under the control of the operator (or automation),
    which can be shifted in accord with these params:"""
     # You may want to have more or less fine control of the beam vs. the stream's shiftiness
    beam_shift_amount = 0.0

    # There are two different and wholly separate senses of acuity:
    # physical_acuity: Whether the beam is physically on target, and functional_acuity:
    # whether the operator can SEE that it is!
    # Nb. Whole scale is -1...+1
    # You want this a little larger than the shift so that it allows for near misses
    physical_acuity = 0.02
    beam_pos = 0.0

    def __init__(self, config:Config):
        self.beam_shift_amount = config['cxi_beam_shift_amount']
        self.physical_acuity = config['cxi_physical_acuity']

class DataPoint:
    """Object to store all the data for each beam point"""
    # TODO: Tik Tak Toe Board
    quality:float = None
    data:List[List[float]] = [[]]
    # t = [ [0]*3 for i in range(3)]

    def __init__(self, quality, data):
        self.quality = quality
        self.data = data

    def __str__(self):
        return f'{self.quality:.2f}'

    def get_data(self) -> str:
        """Tik Tak Toe Board data"""
        return str(self.data)

class SampleData:
    """Store all information about the sample as well as the datapoints
    Sample attributes are stored in dict sampleTypeMapper
    Preformance Quality, different natural signal response
    when data is on peak data * PQ"""
    data:List[DataPoint] = []

    # TODO: make weights affect rescheduling
    # QQQ: What was this N shaped dynamics
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
        self.projected_intercept = 0.0

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
        return (f'{self.preformance_quality}\t{self.weight}\t{self.mean:.15f}\t'+
        f'{self.m_2:.15f}\t{self.variance:.15f}\t{self.sdev:.15f}\t{self.err:.15f}')

    def __str__(self):
        return (f"pq:{self.preformance_quality:.6f}, mean:{self.mean:.6f}, err:{self.err:.6f},"+
            f" var:{self.variance:.6f}, dev:{self.sdev:.6f} intercept:{self.projected_intercept}"
            if self.count != 0 else "pq:0.0, mean:0.0, err:0.0, var:0.0, dev:0.0, intercept:0.0")

class AMI:
    """Contains the data of the samples"""
    # FFF: AMI only gets a subset of samples
    # AMI is different than data pipeline

    # TODO: Wan-Lin's discomfort: seperate PQ and Importance
    # Were using PQ as double meaning, one is quality of sample,
    # also using as inverse proxy as importance
    samples:List[SampleData] = []
    random_samples:bool = None

    def __init__(self, config:Config):
        self.samples:List[SampleData] = []
        self.random_samples = config['random_samples']
        if not config['random_samples']:
            sample:SampleData
            for sample in config['samples']:
                sample.reset()
            self.samples = config['samples']

    def load_samples(self, number_of_samples:int):
        """Load the samples using a random distribution"""
        if self.random_samples:
            self.samples = [SampleData(clamp(random.gauss(0.90, 0.2), 0.00, 0.99),
                random.gauss(0.80, 0.20), timedelta(minutes=random.gauss(1, 0.5)))
                for _ in range(number_of_samples)]

    def sort_samples(self):
        """Sort the samples by PQ"""
        self.samples.sort(key=lambda x: x.preformance_quality, reverse=True)

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

    def __init__(self, config:Config):
        self.experimental_time:timedelta = config['experimental_time']
        self.event_timeline:List[Event] = []
        self.experiment_status:ExperimentState = ExperimentState.STOPED
        self.status = None
        self.number_of_samples = config['number_of_samples']

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

class Config:
    """Contains the configuration of the experiment"""
    override_dictionary = None
    run_number:int = None
    default_dictionary = None

    def __init__(self, override_dictionary, start_time, run_number):
        self.default_dictionary = {
        'name_of_experiment': 'run',
        'start_time': start_time,
        'reps': 1,
        'number_of_samples': 5,
        'experimental_time': timedelta(hours=5),
        'step_through_time': timedelta(seconds=1),
        'cycle_sleep_time': 0.0,
        'display': True,
        'folder': f"/{str(time())}",
        'samples': [[SampleData(0.90, 0.80, timedelta(minutes=1))]],
        'random_samples': False,
        'da_target_error': 0.001,
        'op_switch_button_delay_per_cm': 1,
        'op_button_press_delay': 1,
        'op_button_distance': 0,
        'op_functional_acuity': 0.8, # Important
        'op_noticing_delay': 1.0,
        'op_decision_delay': 1.0,
        'cxi_data_per_second': 100,
        'cxi_time_out_value': 600000,
        'cxi_stream_shift_amount': 0.05,
        'cxi_p_stream_shift': 0.15,
        'cxi_p_crazy_ivan': 0.0001,
        'cxi_crazy_ivan_shift_amount': 0.0,
        'cxi_beam_shift_amount': 0.1,
        'cxi_physical_acuity': 0.2,
        }
        self.override_dictionary = override_dictionary
        self.default_dictionary.update(self.override_dictionary)
        self.run_number = run_number

    def __getitem__(self, key):
        return self.default_dictionary[key]

    def make_dirs(self, directorys:List[str]) -> List[str]:
        """Make directories"""
        return_list:List[str]= []
        for directory in directorys:
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            return_list.append(directory)
        return return_list
    
    def __str__(self):
        return_string = ""
        for key, value in self.default_dictionary.items():
            return_string += f'{key}\t{value}\n'
        return return_string

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
    config:Config = None
    file:TextIOWrapper = None
    data_file:TextIOWrapper = None
    start_time:datetime = None

    def __init__(self, ami:AMI, agenda:Agenda, agent_da:DataAnalyst, agent_em:ExperimentManager,
            agent_op:Operator, instrument:CXI, messages:CommunicationObject, config:Config,
            file:TextIOWrapper, data_file:TextIOWrapper):
        self.current_time = timedelta(0)
        self.ami = ami
        self.agenda = agenda
        self.agent_da = agent_da
        self.agent_em = agent_em
        self.agent_op = agent_op
        self.instrument = instrument
        self.messages = messages
        self.config = config
        self.file = file
        self.data_file = data_file
        self.start_time = datetime.now()

    def file_write(self, message:str):
        """write file method"""
        self.file.write(f"{self.current_time} |"+
        f" DA_E:{self.agent_da.get_energy():.2f} "+
        f" OP_E:{self.agent_da.get_attention():.2f} | {message}\n")

    def printer(self, console:str, file:str):
        """Print message to console"""
        self.messages.concat(f"{console}\n")
        self.file_write(file)

    def update(self):
        """Make sure all objects are updated"""
        self.instrument.update(self)
        self.agent_da.update(self)
        self.agent_op.update(self)