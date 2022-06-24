"""Instrument"""
from datetime import timedelta
from termcolor import colored
from pandas import Timedelta
from data import InstrumentStatus, InstrumentType, Goal, Agenda

class Instrument:
    """Instrument Parent Class"""
    instrument_type = ""
    instrument_status = InstrumentStatus.STOPPED
    collecting_data = False
    run_start_time:Timedelta = None
    run_timedelta:Timedelta = timedelta(minutes=5)
    run_number:int = None
    run_start_frame = False
    data_per_second:int = None
    last_data_update:Timedelta = None

    def __init__(self, instrument):
        self.instrument_type = instrument
        self.run_number = 0

    def start(self):
        """Start the Instrumnet"""
        self.instrument_status = InstrumentStatus.RUNNING

    def stop(self):
        """Stop the Instrumnet"""
        self.instrument_status = InstrumentStatus.STOPPED

    def is_running(self):
        """Check if the instrument is running"""
        return self.instrument_status.value

    def is_collecting_data(self):
        """Check if the instrument is collecting data"""
        return self.collecting_data

    def update(self, current_time, goal:Goal, agenda:Agenda):
        "update vars in relation to time"
        if self.collecting_data:
            if self.run_start_frame:
                self.run_start_frame = False
            else:
                print(f"Run {self.run_number} {colored('Collecting Data', 'green')}")
                if current_time > (self.run_start_time + self.run_timedelta):
                    self.collecting_data = False
                    agenda.add_event(self.run_number, self.run_start_time, current_time)
                else:
                    current_sample = None
                    for index, sample_goal in enumerate(goal.samples):
                        if sample_goal < goal.datapoints_needed_per_sample:
                            current_sample = index
                            break
                    delta:Timedelta = current_time - self.last_data_update
                    if current_sample is None:
                        goal.finished()
                        # agenda.add_event(self.run_number, self.run_start_time, current_time)
                    else:
        # TODO: add simulation and determine the multiple of this as a function of the simulation
                        goal.samples[current_sample] += delta.total_seconds() * self.data_per_second
                    self.last_data_update = current_time

class CXI(Instrument):
    """CXI"""
    def __init__(self):
        super().__init__(InstrumentType.CXI)
        self.data_per_second = 36

    def run_peak_chasing(self, start_time):
        """Start collecting data"""
        self.run_number += 1
        print(f"{colored('Start', 'green')} Run {self.run_number}")
        self.run_start_time = start_time
        self.collecting_data = True
        self.run_start_frame = True
        self.last_data_update = start_time
