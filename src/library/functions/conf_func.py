"""Configuration Functions"""
import itertools
import os
import pickle

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

def sort_combinations(override_dictionary:dict, dictionary:dict, raw_combinations:list):
    """sort combinations"""
    combinations = []
    temp_list = list(cartesian_product(**override_dictionary)) if override_dictionary else {
    'experiment_name': dictionary['experiment_name'][0]}
    number_of_combinations:int = len(temp_list)
    for com in range(number_of_combinations):
        for rep in dictionary['reps']:
            combinations.append(raw_combinations[com+(rep*number_of_combinations)])
    return combinations

def collapsed_file_setup(dictionary:dict, folder:str) -> bool:
    """If savetype is collapsed setup file"""
    os.makedirs(os.path.dirname(f"results/{folder}/collapsed.tsv"), exist_ok=True)
    with open(f"results/{folder}/collapsed.tsv", "w", encoding="utf-8") as file:
        for key in dictionary.keys():
            file.write(f"{key}\t")
        file.write("N\twall_hits\trun\tmean\tstdev\terr\tvar\tpq")
        file.write("\n")

def add_time_num(dictionary:dict, time:float, run_number:int) -> dict:
    """Add Start Time and Run Number"""
    dictionary.update({'start_time': time})
    dictionary.update({'run_number': run_number})
    return dictionary

def dictionary_dump(dictionary:dict, name:str, folder:str) -> bool:
    """pickle dump dictionary"""
    os.makedirs(f"results/{folder}/dictionaries", exist_ok=True)
    with open(f'results/{folder}/dictionaries/{name}.dictionary', 'wb') as file:
        pickle.dump(dictionary, file)

def combination_check(combinations:list):
    """Show user the combinations to run and ask if correct"""
    print(*(config_print(combination) for combination in combinations), sep='\n')
    print(len(combinations))
    val = input("run y/n: ")
    if val != "y":
        exit()

def trim_override_dictionary(dictionary:dict) -> dict:
    """Removing non repetitive items from dictionary"""
    if 'reps' in dictionary:
        del dictionary['reps']
    if 'save_type' in dictionary:
        del dictionary['save_type']
    if 'start_time' in dictionary:
        del dictionary['start_time']
    if 'run_number' in dictionary:
        del dictionary['run_number']
    return dictionary

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
