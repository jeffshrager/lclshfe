"""Config File"""
from datetime import timedelta
import os
from time import time
from typing import List
from src.library.enums.jig_enums import SaveType
from src.library.enums.model_enums import SampleImportance, SampleType
from src.library.functions.func import update_dict
from src.library.objects.objs import SampleData

class Config:
    """Contains the configuration of the experiment"""
    override_dictionary = None
    default_dictionary = None

    def __init__(self, override_dictionary):
        # TODO: Add tangent default off
        # TODO: Tired
        self.default_dictionary = {
        'settings': {
            'name': ['default_run'],
            'save_type': SaveType.COLLAPSED,
            'display': True,
            'cycle_sleep_time': 0.0,
        },
        'reps': [0],
        # 'save_type': SaveType.COLLAPSED,
        'experimental_time': timedelta(hours=5),
        'step_through_time': timedelta(seconds=1),
        # 'cycle_sleep_time': 0.0,
        # 'display': True,
        'samples': {
            'number_of_samples': 5,
            'samples': [SampleData(0.90, SampleImportance.IMPORTANT, SampleType.TAPE)],
            'random_samples': False,
        },
        'data_analysis': {
            'target_error': 0.001,
        },
        'operator': {
            'switch_button_delay_per_cm': 1,
            'button_press_delay': 1,
            'button_distance': 0.1,
            'functional_acuity': 0.1, # Important
            'noticing_delay': 1.0,
            'decision_delay': 1.0,
        },
        'cxi': {
            'data_per_second': 100,
            'time_out_value': 600000,
            'stream_shift_amount': 0.05,
            'p_stream_shift': 0.5,
            'p_crazy_ivan': 0.0000,
            'crazy_ivan_shift_amount': 0.2,
            'beam_shift_amount': 0.1,
            'physical_acuity': 0.2,
        },
        }
        self.override_dictionary = override_dictionary
        self.default_dictionary = update_dict(self.default_dictionary, self.override_dictionary)
        # self.default_dictionary.update(self.override_dictionary)

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
