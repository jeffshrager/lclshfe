"""Instrument"""
import random
from datetime import timedelta
from termcolor import colored
from model.library.enums import InstrumentType
from model.library.objects import Beam, Context, DataPoint, InstrumentStatus, SampleData, Stream

class Instrument:
    """Instrument Parent Class"""
    instrument_type = ""
    instrument_status:InstrumentStatus = None
    stream_status:Stream = None
    beam_status:Beam = None
    collecting_data = False
    run_start_time:timedelta = None
    run_timedelta:timedelta = timedelta(minutes=5)
    run_number:int = None
    run_start_frame = False
    data_per_second:int = None
    last_data_update:timedelta = None
    current_sample:int = None
    # TODO: add system stability
    system_stability = None

    def __init__(self, instrument):
        self.instrument_type = instrument
        self.run_number = 0
        self.instrument_status = InstrumentStatus()
        self.stream_status = Stream()
        self.beam_status = Beam()

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
        return_string = ""
        show_width = 40
        show_incr = 2.0 / show_width
        return_string += f"{self.stream_status.cycle: >6}:["
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
        return_string += f"] stream:{self.stream_status.stream_pos} beam:{self.beam_status.beam_pos} {self.instrument_status.msg}"
        self.instrument_status.msg = ""
        return return_string

    def stream_frame_update(self):
        """stream"""
        self.instrument_status.hits = 0
        self.instrument_status.misses = 0
        self.instrument_status.msg = ""
        # Stop if it hits the wall on either side
        if abs(self.stream_status.stream_pos)>1.0:
            # TODO: End run
            return
        if random.random() < self.stream_status.p_crazy_ivan:
            self.instrument_status.n_crazy_ivans = self.instrument_status.n_crazy_ivans + 1
            self.instrument_status.msg = self.instrument_status.msg + "!!!"
            # If response target has not already been set, it will be 99999999999.
            # If it has been set, it will be whatever number it is (e.g., now+20)
            # Only change the response cycle if it has not been set (i.e., 99999999999)
            self.stream_status.stream_pos = round(self.stream_status.stream_pos + (
                self.stream_status.crazy_ivan_shift_amount * random.choice(
                    [i for i in range(-1, 2) if i not in [0]])), 4)
            if self.stream_status.allow_response_cycle == 99999999999:
                self.stream_status.allow_response_cycle = self.stream_status.cycle
        elif random.random() < self.stream_status.p_stream_shift:
            self.stream_status.stream_pos = round(self.stream_status.stream_pos + (
                self.stream_status.stream_shift_amount * random.choice(
                    [i for i in range(-1, 2) if i not in [0]])), 4)
            if self.stream_status.allow_response_cycle == 99999999999:
                self.stream_status.allow_response_cycle = self.stream_status.cycle
        print(self.show_pos())
        if self.stream_status.cycle >= self.stream_status.allow_response_cycle:
            self.instrument_status.msg = self.instrument_status.msg + "<?>"
            # Warning! WWW This used to truncate, but that interacts badly with computer math
            # bcs occassionally you'll end up with 0.6999999 which truncation makes 0.6 instead
            # of 0.7, and it loops out.
        self.stream_status.cycle = self.stream_status.cycle + 1

    def update(self, context:Context):
        "update vars in relation to time"
        if self.collecting_data:
            if self.run_start_frame:
                self.stream_frame_update()
                self.run_start_frame = False
            else:
                context.messages.concat(f"Run {self.run_number} {colored('Collecting Data', 'green')}\n")
                self.stream_frame_update()
                delta:timedelta = context.current_time - self.last_data_update
                # Only collect data is the beam is on the stream
                # TODO: The farther away you are from the center the worse the quality Gausian
                # TODO: Add noise to the data point
                data_quality = 0
                if self.stream_status.stream_pos == self.beam_status.beam_pos:
                    data_quality = 1.0
                else:
                    data_quality = 0.0
                for _ in range(int(delta.total_seconds()) * self.data_per_second):
                    s_goal:SampleData = context.goal.samples[self.current_sample][0]
                    if random.randrange(1, 1000) == 1:
                        s_goal.append(DataPoint(data_quality * s_goal.preformance_quality * random.uniform(-1.0, 1.0)))
                    else:
                        s_goal.append(DataPoint(data_quality * s_goal.preformance_quality))
                self.last_data_update = context.current_time

class CXI(Instrument):
    """CXI"""
    transition_write:bool = False
    previous_transition_check:timedelta = None
    previous_sample:SampleData = None

    def __init__(self):
        super().__init__(InstrumentType.CXI)
        # TODO: Need to get n events, from elog data
        self.data_per_second = 100

    def run_peak_chasing(self, context:Context) -> bool:
        """True: peak chasing started, False: not started"""
        self.transition_write = False
        self.previous_transition_check = None
        self.run_number += 1
        context.file.write(f"{context.current_time} | Start Run {self.run_number}\n")
        context.messages.concat(f"{colored('Start', 'green')} Run {self.run_number}\n")
        self.run_start_time = context.current_time
        self.collecting_data = True
        self.run_start_frame = True
        self.last_data_update = context.current_time
        self.stream_status.cycle = 0
        for index, sample_goal in enumerate(context.goal.samples):
            s_goal:SampleData = sample_goal[0]
            if len(s_goal.data) < s_goal.datapoints_needed:
                self.current_sample = index
                break
        self.previous_sample = context.goal.samples[self.current_sample][0]
        return True
