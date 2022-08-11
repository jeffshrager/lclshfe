"""Misc objects used in the simulation
"""
from __future__ import annotations
from math import sqrt
from typing import TYPE_CHECKING, List
from io import TextIOWrapper
import random
from datetime import datetime, timedelta
import numpy as np
import sim.model.enums as enums
import sim.model.functions as functions
if TYPE_CHECKING:
    import sim.model.settings as settings
    import sim.model.objects as objects

class CommunicationObject:
    """Used to print messages from each agent

    Used to print messages from each agent
    """
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
    """Determines the status of the instrument

    Object that stores the current status regarding the instrument

    Attributes:
        hits: The number of hits
        misses: The number of misses
        msg: The message to display
        is_running: The state of the instrument
        n_crazy_ivans: The number of crazy ivans
    """
    def __init__(self):
        self.hits:int = 0
        self.misses:int = 0
        self.msg:str = ""
        self.is_running:enums.InstrumentRunState = enums.InstrumentRunState.STOPPED
        # These are counted over all reps and then the mean is display at the end
        self.n_crazy_ivans:int = 0

    def start(self):
        """Start the Instrumnet"""
        self.is_running = enums.InstrumentRunState.RUNNING

    def stop(self):
        """Stop the Instrumnet"""
        self.is_running = enums.InstrumentRunState.STOPPED

class Stream:
    """The stream comming from the instrument

    We have a stream (aka. jet) which shifts around in accord with these params.
    The stream_shift_time_slice is a bit obscure. The idea is that

    Warning: The stream shift amount should be an integer multiple of the beam_shift_amount,
    otherwisethe likelihood that they overlap (based on acuity) will be reduced.
    Usually these will be the same

    A crazy ivan is when the stream goes haywire; It should happen very rarely.

    Attributes:
        stream_shift_amount: The amount the stream shifts each time slice
        p_stream_shift: The probability of a stream shift
        p_crazy_ivan: The probability of a crazy ivan
        crazy_ivan_shift_amount: The amount the crazy ivan shifts each time slice
        default_max_cycles: The maximum number of cycles to run before stopping
        stream_pos: The current position of the stream
        allow_response_cycle: The number of cycles to allow a response
        cycle: The current cycle
    """

    def __init__(self, config:settings.Config):
        self.stream_shift_amount = config['instrument']['stream_shift_amount']
        self.p_stream_shift = config['instrument']['p_stream_shift']
        self.p_crazy_ivan = config['instrument']['p_crazy_ivan']
        self.crazy_ivan_shift_amount = config['instrument']['crazy_ivan_shift_amount']
        # If the beam doesn't hit a wall before this, we cut the run off here.
        self.default_max_cycles:int = 10000
        self.stream_pos:float = 0.0
        self.allow_response_cycle:int = 99999999999
        self.cycle:int = 1

class Beam:
    """The beam that is lined up with the stream

    And the beam, which is under the control of the operator (or automation),
    which can be shifted in accord with these params:
    You may want to have more or less fine control of the beam vs. the stream's shiftiness

    There are two different and wholly separate senses of acuity:
    physical_acuity: Whether the beam is physically on target, and functional_acuity:
    whether the operator can SEE that it is!
    Nb. Whole scale is -1...+1
    You want this a little larger than the shift so that it allows for near misses

    Attributes:
        beam_pos: The current position of the beam
        beam_shift_amount: The amount the beam shifts each time slice
        physical_acuity: The acuity of the beam
    """   

    def __init__(self, config:settings.Config):
        self.beam_pos = 0.0
        self.beam_shift_amount = 0.0
        self.physical_acuity = 0.02
        self.beam_shift_amount = config['instrument']['beam_shift_amount']
        self.physical_acuity = config['instrument']['physical_acuity']

class DataPoint:
    """Data objects

    Contains the quality of the data from the instrument

    Attributes:
        quality: The quality of the data
        data: The data stored in a 2*2 array TODO
    """
    # """Object to store all the data for each beam point"""
    # TODO: Tik Tak Toe Board
    # t = [ [0]*3 for i in range(3)]

    def __init__(self, quality, data):
        self.quality:float = quality
        self.data:List[List[float]] = data

    def __str__(self):
        return f'{self.quality:.2f}'

    def get_data(self) -> str:
        """Tik Tak Toe Board data"""
        return str(self.data)

class SampleData:
    """Sample Data Objects

    Store all information about the sample as well as the datapoints
    Sample attributes are stored in dict sampleTypeMapper
    Preformance Quality, different natural signal response
    when data is on peak data * PQ

    Attributes:
        compleated: Whether the sample is completed
        timeout: if the sample has timed out
        preformance_quality: the quality of the sample
        importance: the importance of the sample
        setup_time: how long it takes to set up the sample
        data: the data points
        count: the number of data points
        mean: the mean of the data points
        m_2: the mean of the data points squared
        variance: the variance of the data points
        sdev: the standard deviation of the data points
        err: the error of the data points
        count_array: the number of data points in each array
        err_array: the error of the data points in each array
        projected_intercept: the projected intercept of the data points
        wall_hits: the number of wall hits
        estimated_run_length: the estimated run length of the data points
        duration: the duration of the data points
        running: the state of the sample
        error_time_array: the error of the time array
    """
    # TODO: make weights affect rescheduling
    # QQQ: What was this N shaped dynamics
    def __init__(self, preformance_quality:float,
            importance:enums.SampleImportance, setup_time:enums.SampleType):
        self.compleated:bool = False
        self.timeout:bool = False
        self.preformance_quality:float = preformance_quality
        self.importance:enums.SampleImportance = importance
        self.setup_time:timedelta = setup_time.value['setup_time']
        self.data:List[DataPoint] = []
        self.count:float = 0.0
        self.mean:float = 0.0
        self.m_2:float = 0.0
        self.variance:float = 0.0
        self.sdev:float = 0.0
        self.err:float = 0.0
        self.count_array:List = []
        self.err_array:List = []
        self.projected_intercept:float = 0.0
        self.wall_hits:float = 0.0
        self.estimated_run_length:timedelta = timedelta(seconds=0)
        self.duration:timedelta = timedelta(seconds=0)
        self.running:bool = False
        self.error_time_array:List = []

    def append(self, data:DataPoint, context:Context):
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

        self.error_time_array.append([self.err, context.current_time])

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
        self.wall_hits = 0.0
        self.duration:timedelta = timedelta(seconds=0)
        self.estimated_run_length = timedelta(seconds=0)

    def file_string(self) -> str:
        """Return a string that can be written to a file"""
        return (f'{self.preformance_quality}\t{self.importance}\t{self.mean:.15f}\t'+
        f'{self.m_2:.15f}\t{self.variance:.15f}\t{self.sdev:.15f}\t{self.err:.15f}')
    
    def __str__(self):
        return f"{self.preformance_quality:.2f}"

    def get_stats(self) -> list[str]:
        """Return the stats of the data"""
        return (
            f"[{self.importance.value['color']} not dim]{self.importance.name:<11}",
            f"[default dim]pq:[rgb({functions.rgb(self.preformance_quality)}) not dim]{self.preformance_quality:.3f}",
            f"[italic yellow dim]est:[not dim]{str(self.estimated_run_length).split('.', maxsplit=1)[0]:<6}",
            f"[italic green dim]actual:[not dim]{str(self.duration).split('.', maxsplit=1)[0]:<6}",
            "[default]|",
            f"[dim]mean:[not dim]{(self.mean if self.count != 0 else 0.000):.3f}",
            f"[default dim]err:[not dim]{(self.err  if self.count != 0 else 0.000000):.6f}",
            f"[default dim]var:[not dim]{(self.variance if self.count != 0 else 0.000):.3f}",
            f"[default dim]dev:[not dim]{(self.sdev if self.count != 0 else 0.000):.3f}",
            f"[default dim]intercept:[not dim]{(self.projected_intercept if self.count != 0 else 0.000):.3f}")

class AMI:
    """Contains the data of the samples

    FFF: AMI only gets a subset of samples
    AMI is different than data pipeline

    TODO: Wan-Lin's discomfort: seperate PQ and Importance
    Were using PQ as double meaning, one is quality of sample,
    also using as inverse proxy as importance
    """
    samples:List[SampleData] = []
    random_samples:bool = None

    def __init__(self, config:settings.Config):
        self.samples:List[SampleData] = []
        self.random_samples = config['samples']['random_samples']
        if not config['samples']['random_samples']:
            sample:SampleData
            for sample in config['samples']['samples']:
                sample.reset()
            self.samples = config['samples']['samples']

    def load_samples(self, context:Context):
        """Load the samples using a random distribution"""
        if self.random_samples:
            self.samples = [SampleData(functions.clamp(random.gauss(0.90, 0.2), 0.00, 0.99),
                random.gauss(0.80, 0.20), timedelta(minutes=random.gauss(1, 0.5)))
                for _ in range(context.agenda.number_of_samples)]
        self.calculate_run_length(context)

    def calculate_run_length(self, context:Context):
        """Calculate the run length of the samples"""
        for sample in context.ami.samples:
            # QQQ: Better Prediction
            sample.estimated_run_length = timedelta(seconds=(1 - sample.preformance_quality) * 1400)

    def sort_samples(self):
        """Sort the samples by PQ"""
        self.samples.sort(key=lambda x: x.preformance_quality, reverse=True)

    def get_current_sample(self, context:Context) -> SampleData:
        """Get current Sample"""
        return self.samples[context.instrument.current_sample]

    def get_headers(self) -> List[str]:
        """Return the headers for the file"""
        return ['mean', 'stdev', 'err', 'var', 'pq']
    
    def get_values(self) -> List[any]:
        """Return the values for the file"""
        return [self.get_mean(), self.get_stdev(), self.get_err(), self.get_var(), self.get_pq()]

    def get_mean(self) -> List[float]:
        """Return the mean of the samples"""
        return [np.mean([data.quality for data in sample.data]) for sample in self.samples]

    def get_stdev(self) -> List[float]:
        """Return the standard deviation of the samples"""
        return [np.std([data.quality for data in sample.data]) for sample in self.samples]

    def get_err(self) -> List[float]:
        """Return the error of the samples"""
        return [(np.std([data.quality for data in sample.data]
        ) / sqrt(len(sample.data))) for sample in self.samples]

    def get_var(self) -> List[float]:
        """Return the variance of the samples"""
        return [np.var([data.quality for data in sample.data]) for sample in self.samples]

    def get_n(self) -> List[float]:
        """Return the number of samples"""
        return [len(sample.data) for sample in self.samples]

    def get_pq(self) -> List[float]:
        """Return the number of samples"""
        return [sample.preformance_quality for sample in self.samples]

    def get_wall_hits(self) -> List[float]:
        """Return the number of samples"""
        return [sample.wall_hits for sample in self.samples]

    def __str__(self):
        return_string = ""
        for index, sample in enumerate(self.samples):
            # pq, mean, err, var, dev
            return_string += f"{'[green dim]' if sample.compleated else ('[bold green]' if sample.running else '[default dim]')}{str(index): >2} |N: [default not dim]{len(sample.data): >6} [dim]- {sample.get_stats()}\n"
            # return_string += f"{'[default dim]' if not sample.compleated else ('[green bold not dim]' if sample.running else '[green dim]')}{str(index): >2} |N: [default not dim]{len(sample.data): >6} [dim]- {sample.get_stats()}\n"
        return return_string

class Agenda:
    """The timeline of events for the experiment

    High Level Schedule of events for acheiving the goal

    Attributes:
        experimental_time: The time the experiment will take
        number_of_samples: The number of samples to take
        event_timeline: The events in the timeline
        experiment_status: The status of the experiment
    """
    experimental_time:timedelta = timedelta(0)
    number_of_samples:int = 0

    def __init__(self, config:settings.Config):
        self.experimental_time:timedelta = config['experimental_time']
        self.event_timeline:List[Event] = []
        self.experiment_status:enums.ExperimentState = enums.ExperimentState.STOPED
        self.status = None
        self.number_of_samples = config['samples']['number_of_samples']

    def start_experiment(self):
        """Start the experiment if it has not been started"""
        if not self.experiment_status.value:
            self.experiment_status = enums.ExperimentState.STARTED

    def is_started(self):
        """check if experiment has been started"""
        return self.experiment_status.value

    def finished(self):
        """Finished experiment"""
        self.status = "compleated"

    def __str__(self):
        return f"Experimental Time: {self.experimental_time}"

    def add_event(self, run_number:int, start_time:timedelta, end_time:timedelta, current_sample:SampleData, time_out:bool):
        """Add event to agenda timeline"""
        self.event_timeline.append(Event(run_number, start_time, end_time, current_sample, time_out))

    def get_timeline(self):
        """return final timeline string"""
        return ''.join(map(str, self.event_timeline))

class Event:
    """Single events for a sample

    Object to specify the information from each event(run)

    Attributes:
        run_number: The run number of the event
        start_time: The time the event started
        end_time: The time the event ended
        duration: The duration of the event
        sample: The sample that the event is for
        time_out: If the event was a time out
    """
    def __init__(self, run_number:int, start_time:timedelta, end_time:timedelta, sample:SampleData, time_out:bool):
        self.run_number:int = run_number
        self.start_time:timedelta = start_time
        self.end_time:timedelta = end_time
        self.duration:timedelta = end_time - start_time
        self.sample:SampleData = sample
        self.time_out:bool = time_out

    def __str__(self):
        return (f"Run: {self.run_number: >2}, Timeout: {self.time_out}, Start: {self.start_time}, "+
            f"End: {self.end_time}, Duration: {self.end_time - self.start_time}\n")

class Context:
    """Simulation State Container

    Using the Context Pattern (http://www.corej2eepatterns.com/ContextObject.htm)
    to store the state of the simulation on a protocal independant way.
    A context is instantiated with each run of the simulation and is used
    to access each of the modifyable objects.

    Attributes:
        start_time: System time at start of simulation
        current_time: The timedelta that the simulation is on, indipendent of the system time.
        ami: The object with the samples and data
        agenda: To store events and information about the experiment
        agent_da: Data Analyst Agent
        agent_em: Experiment Manager Agent
        agent_op: Operator Agent
        instrument: The instrument used in the experiment
        messages: The comunication between the agents
        config: The configuration of the experiment
        file: Stores the messages and experiment information
        data_file: Stores the actual data from the instrument
    """

    def __init__(self, ami:AMI, agenda:Agenda, agent_da:objects.DataAnalyst, agent_em:objects.ExperimentManager,
            agent_op:objects.Operator, instrument:objects.CXI, messages:CommunicationObject, config:settings.Config,
            file:TextIOWrapper, data_file:TextIOWrapper):
        self.start_time:datetime = datetime.now()
        self.current_time:timedelta = timedelta(0)
        self.ami:AMI = ami
        self.agenda:Agenda = agenda
        self.agent_da:objects.DataAnalyst = agent_da
        self.agent_em:objects.ExperimentManager = agent_em
        self.agent_op:objects.Operator = agent_op
        self.instrument:objects.CXI = instrument
        self.messages:CommunicationObject = messages
        self.config:settings.Config = config
        self.file:TextIOWrapper = file
        self.data_file:TextIOWrapper = data_file

    def file_write(self, message:str):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.

        Returns:
            A dict mapping keys to the corresponding table row data
        """
        open(self.file.name, 'a', encoding="utf-8").write(f"{self.current_time} |"+
        f" DA_E:{self.agent_da.get_energy():.2f} "+
        f" OP_E:{self.agent_da.get_attention():.2f} | {message}\n")

    def printer(self, console:str, file:str):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.

        Returns:
            A dict mapping keys to the corresponding table row data
        """
        self.messages.concat(f"{console}\n")
        if self.config['settings']['save_type'][0] == enums.SaveType.DETAILED:
            self.file_write(file)

    def __getitem__(self, key):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.

        Returns:
            A dict mapping keys to the corresponding table row data
        """
        return self.config[key]

    def update(self):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.

        Returns:
            A dict mapping keys to the corresponding table row data
        """
        self.instrument.update(self)
        self.agent_da.update(self)
        self.agent_op.update(self)
