"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from datetime import timedelta
import os
from typing import List
import src.library.enums as enums
import src.library.functions as functions
import src.library.objects as objects

class Config:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    override_dictionary = None
    default_dictionary = None

    def __init__(self, override_dictionary):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
            returned.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

        Raises:
            IOError: An error occurred accessing the smalltable.
        """
        self.default_dictionary = {
        'settings': {
            'name': ['default_run'],
            'save_type': enums.SaveType.COLLAPSED,
            'display': True,
            'cycle_sleep_time': 0.0,
        },
        'reps': [0],
        'experimental_time': timedelta(hours=5),
        'step_through_time': timedelta(seconds=1),
        'samples': {
            'number_of_samples': 5,
            'samples': [objects.SampleData(0.90, enums.SampleImportance.IMPORTANT, enums.SampleType.TAPE)],
            'random_samples': False,
        },
        'cognative_degredation': True,
        'person':{
            # TODO
            'functional_acuity': 0.1, # Important
            'noticing_delay': 1.0,
            'decision_delay': 1.0,
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
        'instrument': {
            'tanh_curve': True,
            'data_per_second': 100,
            'time_out_value': 600000,
            'stream_shift_amount': 0.05,
            'p_stream_shift': 0.5,
            'p_crazy_ivan': 0.0000,
            'crazy_ivan_shift_amount': 0.2,
            'beam_shift_amount': 0.1,
            'physical_acuity': 0.2,
            'sample_transition_time': timedelta(minutes=1),
        },
        }
        self.override_dictionary = override_dictionary
        self.default_dictionary = functions.update_dict(self.default_dictionary, self.override_dictionary)

    def __getitem__(self, key):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
            returned.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

        Raises:
            IOError: An error occurred accessing the smalltable.
        """
        return self.default_dictionary[key]

    def make_dirs(self, directorys:List[str]) -> List[str]:
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
            returned.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

        Raises:
            IOError: An error occurred accessing the smalltable.
        """
        return_list:List[str]= []
        for directory in directorys:
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            return_list.append(directory)
        return return_list

    def __str__(self):
        """Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.

        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
            row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
            returned.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

        Raises:
            IOError: An error occurred accessing the smalltable.
        """
        return_string = ""
        for key, value in self.default_dictionary.items():
            return_string += f'{key}\t{value}\n'
        return return_string
