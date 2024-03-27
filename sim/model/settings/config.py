"""The configuration object

The Configuration Object and its methods are usedto store the settings
for the simulation.

  Typical usage example:

  config = Config(overrides)
  system_parameter = config['system_parameter']['sub_parameter']
"""
from datetime import timedelta
from typing import List
import os
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model.objects as objects

class Config:
    """The config contains all the parameters that are used in the simulation.

    The config has the default values that are used to run the simulation. These
    values can be overridden by the by the override dictionary when the config is
    created. The default values are sensible values for a standard run. The config
    can either be used as a total config containing all values each parameter is
    run with, or as a single config containing only the values that are used in the
    current run.

    Attributes:
        override_dictionary: The dictonary that was used to override the default values.
        default_dictionary: A dictionary containing the default values for the config.
    """
    override_dictionary = None
    default_dictionary = None

    def __init__(self, override_dictionary):
        """Initializes the config object.

        The configuration object for the simulation that is used to store the
        settings for the entire simulation as well as the settings for the
        current run.

        Args:
            override_dictionary: Overrides corresponding values in the default dictionary.

        Returns:
            A object with both the override dictionary - the dictonary passed into
            the object and the default dictionary - which is the new object with the
            dictionary to be used.
        """
        # FFF: accessor function and mutate to change to new value
        # With accessors and mutators, the dictionary key would actually be an accessor function
        self.default_dictionary = {
        'settings': {
            'name': ['default_run'],
            'save_type': enums.SaveType.COLLAPSED,
            'display': True,
            'cycle_sleep_time': 0.0,
            'strict_time': True,
            'ask_to_continue': {
                'sample': False,
                'run': False,
            }
        },
        'reps': [0],
        'experimental_time': timedelta(hours=5),
        'step_through_time': timedelta(seconds=1),
        'samples': {
            'number_of_samples': 5,
            'samples': [objects.SampleData(0.90,\
                enums.SampleImportance.IMPORTANT, enums.SampleType.TAPE)],
            'random_samples': False,
        },
        'cognative_degredation': True,
        'person':{
            'energy_degradation': 0.002, #TODO
            'functional_acuity': 0.1, # TODO
            'noticing_delay': 1.0, # TODO
            'decision_delay': 1.0, # TODO
            'verbose': True, #TODO
        },
        'experiment_manager': {
            'experimental_time_to_prediction': True,
            'adjust_error': True,
            'dynamic_scheduling': True, #TODO
            'algorithm': enums.ExperimentManagerAlgorithm, #TODO
            'person':{
                'energy_degradation': None, #TODO
                'functional_acuity': None, # TODO
                'noticing_delay': None, # TODO
                'decision_delay': None, # TODO
                'verbose': None, #TODO
            },
        },
        'data_analysis': {
            'target_error': 0.001,
            'person':{
                'energy_degradation': None, #TODO
                'functional_acuity': None, # TODO
                'noticing_delay': None, # TODO
                'decision_delay': None, # TODO
                'verbose': None, #TODO
            },
        },
        'operator': {
            'switch_button_delay_per_cm': 1,
            'button_press_delay': 1,
            'button_distance': 0.1,
            'functional_acuity': 0.1,
            'noticing_delay': 1.0,
            'decision_delay': 1.0,
            'person':{
                'energy_degradation': None, #TODO
                'functional_acuity': None, # TODO
                'noticing_delay': None, # TODO
                'decision_delay': None, # TODO
                'verbose': None, #TODO
            },
        },
        'instrument': {
            'tanh_curve': False,
            'data_per_second': 100,
            'time_out_value': 600000,
            'stream_shift_amount': 0.05,
            'p_stream_shift': 0.5,
            'p_crazy_ivan': 0.0000,
            'crazy_ivan_shift_amount': 0.2,
            'beam_shift_amount': 0.1,
            'physical_acuity': 0.2,
            'sample_transition_time': timedelta(minutes=0),
        },
        }
        self.override_dictionary = override_dictionary
        self.default_dictionary = functions.update_dict(self.default_dictionary,\
            self.override_dictionary)

    def __getitem__(self, key):
        """Gets items from the directory.

        Overrides the getitem method to return the value of the key from the
        settings directory. These values are used as parameters for the simulation.

        Args:
            key: The key to get the value for. This also works with nested keys.

        Returns:
            The value corresponding to the key in the dictionary.
        """
        return self.default_dictionary[key]

    def make_dirs(self, directorys:List[str]) -> List[str]:
        """Fetches rows from a Smalltable."""
        return_list:List[str]= []
        for directory in directorys:
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            return_list.append(directory)
        return return_list

    def __str__(self):
        """Formats the config object as a string.

        Goes through the config object and formats it as a string.

        Returns:
            A string representation of the config object.
        """
        return_string = ""
        for key, value in self.default_dictionary.items():
            return_string += f'{key}\t{value}\n'
        return return_string
