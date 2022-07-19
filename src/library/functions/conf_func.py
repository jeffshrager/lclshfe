"""Configuration Functions"""
import itertools

from src.library.objects.objs import AMI

def cartesian_product(**kwargs):
    """This returns a list of dictionaries with single value keys
    as a result of the cartesian product of the values

    eg:
    'a': [1, 2, 3]
    'b': [4, 5, 6]

    result = [{'a': 1, 'b': 4},
              {'a': 1, 'b': 5},
              {'a': 1, 'b': 6},"""
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))

def config_print(dictionary:dict) -> str:
    """Config print"""
    return_string = ""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            config_print(v)
        else:
            if isinstance(v, list):
                list_string = ""
                for item in v:
                    list_string += f"{item}, "
                return_string += f"{k}: {list_string}"
            else:
                return_string += (f"{k} : {v}, ")
    return return_string

def runs_to_xyz(config, runs):
    """Runs to xyz"""

    # y_axis = [y for y in range(len(config['reps']))]
    y_axis = [0, 1, 2, 3]

    max_count = 0
    run:AMI
    for sample in y_axis:
        sample_max = 0
        for run in runs:
            if len(run.samples[sample].data) > max_count:
                sample_max = len(run.samples[sample].data)
        max_count += sample_max
    x_axis = [x for x in range(max_count)]

    runs_per_rep:int = len(config['reps'])
    current_run:int = 0
    z_axis = []
    total_range = len(runs) // runs_per_rep
    for run in range(total_range):
        temp_z = []
        for j, _ in enumerate(runs[current_run].samples):
            for i, _ in enumerate(runs[current_run].samples[j].data):
                mean_value = 0
                temp_count = 0

                continue_var = True
                for r in range(runs_per_rep):
                    current_run_object = runs[current_run + r]
                    current_sample = current_run_object.samples[j]
                    if i > len(current_sample.data):
                        continue_var = False
                        break
                    continue_var = True
                if continue_var:
                    for r in range(runs_per_rep):
                        current_run_object = runs[current_run + r]
                        current_sample = current_run_object.samples[j]
                        if i < len(current_sample.data):
                            temp_count += 1
                            current_data = current_sample.data[i]
                            mean_value += current_data.quality
                    mean_value /= temp_count
                    temp_z.append(mean_value)
        z_axis.append(temp_z)
        current_run += runs_per_rep
    return x_axis, y_axis, z_axis
