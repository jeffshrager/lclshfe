"""Config File"""
from datetime import timedelta
import os
from time import time
from typing import List
from src.library.enums.jig_enums import SaveType
from src.library.objects.objs import SampleData

class Config:
    """Contains the configuration of the experiment"""
    override_dictionary = None
    default_dictionary = None

    def __init__(self, override_dictionary):
        self.default_dictionary = {
        'experiment_name': ['default_run'],
        'reps': [0],
        'save_type': SaveType.COLLAPSED,
        'experimental_time': timedelta(hours=5),
        'step_through_time': timedelta(seconds=1),
        'cycle_sleep_time': 0.0,
        'display': True,
        'number_of_samples': 5,
        'samples': [SampleData(0.90, 0.80, timedelta(minutes=1))],
        'random_samples': False,
        'da_target_error': 0.001,
        'op_switch_button_delay_per_cm': 1,
        'op_button_press_delay': 1,
        'op_button_distance': 0.1,
        'op_functional_acuity': 0.1, # Important
        'op_noticing_delay': 1.0,
        'op_decision_delay': 1.0,
        'cxi_data_per_second': 100,
        'cxi_time_out_value': 600000,
        'cxi_stream_shift_amount': 0.05,
        'cxi_p_stream_shift': 0.5,
        'cxi_p_crazy_ivan': 0.0000,
        'cxi_crazy_ivan_shift_amount': 0.0,
        'cxi_beam_shift_amount': 0.1,
        'cxi_physical_acuity': 0.2,
        }
        self.override_dictionary = override_dictionary
        self.default_dictionary.update(self.override_dictionary)

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
