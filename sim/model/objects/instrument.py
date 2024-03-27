"""The instruments represented in the model

This contains the parent and child objects of the instrument. Right now there
is just CXI but this can be extended to include other instruments in the future
that have different properties.

  Typical usage example:

  CXI = CXI()
"""
import random
from datetime import timedelta
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model.objects as objects
import sim.model.settings as settings

class Instrument:
    """The parent object for the insturments

    The parent object for the insturments

    Attributes:
        instrument_type (str): The type of instrument
        run_number (int): The run number of the instrument
        instrument_status (InstrumentStatus): The status of the instrument
        stream_status (Stream): The status of the stream
        beam_status (Beam): The status of the beam
        time_out_value (int): The time out value for the instrument
        current_sample (int): The current sample
        position_display (str): The position display for the instrument
        data_stream (list): The data stream for the instrument
        collecting_data (bool): Whether the instrument is collecting data
    """
    instrument_type = ""
    instrument_status:objects.InstrumentStatus = None
    stream_status:objects.Stream = None
    time_out_value:int = None
    beam_status:objects.Beam = None
    collecting_data = False
    run_start_time:timedelta = None
    run_number:int = None
    run_start_frame = False
    data_per_second:int = None
    last_data_update:timedelta = None
    current_sample:int = None
    # TODO _: add system stability
    # System is unstable then gets to a stable period
    # then it fluctuates
    system_stability = None
    data_stream:str = ""
    position_display:str = ""


    def __init__(self, instrument):
        self.instrument_type = instrument
        self.run_number = 0
        # self.instrument_status = InstrumentStatus()
        # self.stream_status = Stream()
        # self.beam_status = Beam()
        # self.time_out_value = 600000

    def start(self):
        """Start the Instrumnet"""
        self.instrument_status.start()

    def stop(self):
        """Stop the Instrumnet"""
        self.instrument_status.stop()

    def is_running(self):
        """Check if the instrument is running"""
        return self.instrument_status.is_running.value

    def is_collecting_data(self):
        """Check if the instrument is collecting data"""
        return self.collecting_data

    def show_pos(self):
        """The display and hit-counting logic are intertwined. Maybe they shouldn't be.
        Pretty straight-forward refactoring would pull them apart. Also, the hit scoring
        is unfortunately, based on whether a * would be displayed, which in turn depends
        on the display increment, which is clearly wrong. UUU FFF Clean this up!!"""
        # FFF: Where exact beam|jet match is tested with ==, replace with a
        # more "perceptually" accurate model
        return_string = ""
        show_width = 60
        show_incr = 2.0 / show_width
        return_string += f"{self.stream_status.cycle: >3}:["
        beam_shown_f = False
        stream_shown_f = False
        stream_position = -1.0
        for _ in range(show_width):
            # miss = False
            stream_position = stream_position + show_incr
            if stream_shown_f and beam_shown_f:
                char = " "
            # This is a rather obscure way of simply asking if the beam is on the stream:
            elif (not stream_shown_f) and (not beam_shown_f) and (
                    stream_position >= self.stream_status.stream_pos) and (
                    stream_position >= self.beam_status.beam_pos):
                stream_shown_f = True
                beam_shown_f = True
                char = "*"
            elif (not stream_shown_f) and (stream_position >= self.stream_status.stream_pos):
                stream_shown_f = True
                char = "|"
            elif (not beam_shown_f) and (stream_position >= self.beam_status.beam_pos):
                beam_shown_f = True
                char = "x"
            else:
                char = " "
            return_string += f"{char}"
        return_string += (f"] stream:{self.stream_status.stream_pos} "+
            f"beam:{self.beam_status.beam_pos} {self.instrument_status.msg}")
        self.instrument_status.msg = ""
        return return_string

    def stream_frame_update(self, context:objects.Context):
        """stream"""
        self.instrument_status.hits = 0
        self.instrument_status.misses = 0
        self.instrument_status.msg = ""
        # Stop if it hits the wall on either side
        if abs(self.stream_status.stream_pos)>1.0:
            context.ami.samples[self.current_sample].wall_hits += 1
            # FFF: End run and handle all events that would end the run early
            return
        if random.random() < self.stream_status.p_crazy_ivan:
            self.instrument_status.n_crazy_ivans = self.instrument_status.n_crazy_ivans + 1
            self.instrument_status.msg = self.instrument_status.msg + "!!!"
            self.stream_status.stream_pos = round(self.stream_status.stream_pos + (
                self.stream_status.crazy_ivan_shift_amount * random.choice(
                    [i for i in range(-1, 2) if i not in [0]])), 4)
        elif random.random() < self.stream_status.p_stream_shift:
            self.stream_status.stream_pos = round(self.stream_status.stream_pos + (
                self.stream_status.stream_shift_amount * random.choice(
                    [i for i in range(-1, 2) if i not in [0]])), 4)
        # context.messages.concatbegining(f"{self.show_pos()}\n")
        self.position_display = self.show_pos()
        self.data_stream = functions.get_current_datapoints(context)
        if self.stream_status.cycle >= self.stream_status.allow_response_cycle:
            self.instrument_status.msg = self.instrument_status.msg + "<?>"
            # Warning! WWW This used to truncate, but that interacts badly with computer math
            # bcs occassionally you'll end up with 0.6999999 which truncation makes 0.6 instead
            # of 0.7, and it loops out.
        self.stream_status.cycle = self.stream_status.cycle + 1

    def update(self, context:objects.Context):
        "update vars in relation to time"
        if self.collecting_data:
            self.stream_frame_update(context)
            if self.run_start_frame:
                self.run_start_frame = False
            else:
                context.messages.concat(f"Run {self.run_number} "+"[green]Collecting Data[/green]\n")
            
            current_sample = context.ami.samples[self.current_sample]
            if len(current_sample.data) > self.time_out_value:
                context.printer("[yellow]Warning[/yellow]: To many data points timeout", "Warning: To many data points timeout")
                context.agenda.add_event(context.instrument.run_number, context.instrument.run_start_time, context.current_time, current_sample, True)
                current_sample.timeout = True
                self.collecting_data = False
            else:
                # Normal Distribution of quality based on how far away beam pos(user controller)
                # is away from the stream pos (instrument beam)
                # Farthest away is 2 beam on one side and stream on other
                # Closest is 0 right on top of each other
                # FFF: allow this to work with less than 1 second time steps
                delta:timedelta = context.current_time - self.last_data_update
                current_sample.duration = current_sample.duration + delta
                distance = abs(self.stream_status.stream_pos - self.beam_status.beam_pos)
                for _ in range(int(delta.total_seconds()) * self.data_per_second):
                    datapoint:objects.DataPoint = objects.DataPoint(functions.clamp(functions.aquire_data(distance,
                            current_sample.preformance_quality, context) \
                            # QQQ: Do we need this, line below?
                            # * current_sample.preformance_quality \
                            # Additional pipeline noise not dependent on the sample or anything else
                            # FFF: Model this someday
                            # III: Bring these back in
                            + (random.uniform(-0.01, 0.01) if random.randrange(1, 5) == 1 else 0) \
                            + (random.uniform(-0.1, 0.1) if random.randrange(1, 1000) == 1 else 0)
                            , 0.0, 1.0),
                            # Tik Tak Toe Board Data
                            [[1.0, 0.0, 1.0], [0.0, None, 0.0], [1.0, 0.0, 1.0]]
                            )
                    if context['settings']['save_type'][0] == enums.SaveType.DETAILED:
                        open(context.data_file.name, 'a', encoding="utf-8").write(f"{self.current_sample}\t{current_sample.count}\t{datapoint.quality:.15f}\t{current_sample.file_string()}\n")
                    current_sample.append(datapoint, context)
                self.last_data_update = context.current_time

class CXI(Instrument):
    """CXI Instrument

    The object for the CXI instrument.

    Attributes:
        data_per_second (int): The number of data points to be collected per second.
        instrument_status (InstrumentStatus): The status of the instrument.
    """
    transition_write:bool = False
    previous_transition_check:timedelta = None 
    previous_sample:objects.SampleData = None

    def __init__(self, config:settings.Config):
        super().__init__(enums.InstrumentType.CXI)
        self.data_per_second = config['instrument']['data_per_second']
        self.instrument_status = objects.InstrumentStatus()
        self.stream_status = objects.Stream(config)
        self.beam_status = objects.Beam(config)
        self.time_out_value = config['instrument']['time_out_value']

    def run_peak_chasing(self, context:objects.Context) -> bool:
        """True: peak chasing started, False: not started"""
        self.transition_write = False
        self.previous_transition_check = None
        self.run_number += 1
        context.ami.samples[self.run_number-2].running = False
        context.ami.samples[self.run_number-1].running = True
        context.printer(f"[green]Start[/green] Run {self.run_number}",
            f"Start Run {self.run_number}")
        self.run_start_time = context.current_time
        self.collecting_data = True
        self.run_start_frame = True
        self.last_data_update = context.current_time
        self.stream_status.cycle = 0
        for index, sample_goal in enumerate(context.ami.samples):
            if not sample_goal.completed and not sample_goal.timeout:
                self.current_sample = index
                break
        if context['settings']['save_type'][0] == enums.SaveType.DETAILED:
            open(context.data_file.name, 'a', encoding="utf-8").write("sample #\tcount\tdata\tpreformance quality\tweight\tmean\tm2\tvariance\tsdev\terr\n")
        self.previous_sample = context.ami.samples[self.current_sample]
        return True
