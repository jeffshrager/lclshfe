"""Configuration Functions"""
import itertools
from math import sqrt
import os
import pickle
from statistics import stdev
from typing import List
from numpy import mean
from termcolor import colored
from src.library.objects.objs import AMI, SampleData

def cartesian_product(kwargs):
    """This returns a list of dictionaries with single value keys
    as a result of the cartesian product of the values

    eg:
    'a': [1, 2, 3]
    'b': [4, 5, 6]

    result = [{'a': 1, 'b': 4},
              {'a': 1, 'b': 5},
              {'a': 1, 'b': 6},"""
    keys, values = kwargs.keys(), kwargs.values()
    values_choices = (cartesian_product(v) if isinstance(v, dict) else v for v in values)
    for comb in itertools.product(*values_choices):
        yield dict(zip(keys, comb))

def write_summary_file(config:dict, folder:str, runs:List[dict], independent_variable:str):
    """Write Summary File"""
    # TODO: which 2 things im running against
    os.makedirs(os.path.dirname(f"results/{folder}/summary.tsv"), exist_ok=True)
    with open(f"results/{folder}/summary.tsv", "w", encoding="utf-8") as file:
        file.write(f"average\tstdev\tn\terr\tpq\t{independent_variable}\n")
        n_list = []
        pq_list = []
        sample:SampleData
        if isinstance(config['settings']['save_type'], list):
            config['settings']['save_type'] = config['settings']['save_type'][0]
        for samples in config['samples']['samples']:
            if isinstance(samples, list):
                for sample in samples:
                    pq_list.append(sample.preformance_quality)
            else:
                pq_list.append(samples.preformance_quality)
        for pq in pq_list:
            # Decollapse OND's
            if isinstance(config['operator'][f"{independent_variable}"], list):
                for ond in config['operator'][f"{independent_variable}"]:
                    ond_list = []
                    for run in runs:
                        if run[f"{independent_variable}"] == ond:
                            for index, sample_pq in enumerate(run['pq']):
                                if sample_pq == pq:
                                    ond_list.append(run['N'][index])
                    n_list.append([round(mean(ond_list)), round(stdev(ond_list)), len(ond_list), stdev(ond_list)/sqrt(len(ond_list)), pq, ond])
            else:
                ond_list = []
                for run in runs:
                    for count in run['N']:
                        ond_list.append(count)
                n_list.append([ond_list[0], ond_list[0], len(ond_list), '-', pq, config['operator'][f"{independent_variable}"]])
        for l in n_list:
            for item in l:
                file.write(f"{item}\t")
            file.write("\n")

def sort_combinations(override_dictionary:dict, dictionary:dict, raw_combinations:list):
    """sort combinations"""
    combinations = []
    temp_list = list(cartesian_product(override_dictionary)) if override_dictionary else {
    'settings':{'name': dictionary['settings']['name'][0]}}
    number_of_combinations:int = len(temp_list) // len(dictionary['reps'])
    for com in range(number_of_combinations):
        for rep in dictionary['reps']:
            combinations.append(raw_combinations[com+(rep*number_of_combinations)])
    return combinations

def collapsed_file_setup(dictionary:dict, folder:str) -> bool:
    """If savetype is collapsed setup file"""
    os.makedirs(os.path.dirname(f"results/{folder}/collapsed.tsv"), exist_ok=True)
    with open(f"results/{folder}/collapsed.tsv", "w", encoding="utf-8") as file:
        for key, value in dictionary.items():
            if key != 'samples' and key != 'settings':
                if isinstance(value, dict):
                    for k, v in value.items():
                        file.write(f"{k}\t")
                else:
                    file.write(f"{key}\t")
        file.write("run\tN\twall_hits\tmean\tstdev\terr\tvar\tpq")
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

def name_check(override:dict) -> bool:
    """Check if name is new"""
    if 'settings' in override:
        if 'name' in override['settings']:
            if override['settings']['name'][0] in os.listdir('results'):
                print(f"{override['settings']['name'][0]} {colored('has been used before.', 'red')}")
                val = input(f"{colored('Want to change it?', 'red')} y/n: ")
                if val == "y":
                    change_confirm = False
                    while change_confirm is False:
                        override['settings']['name'][0] = input("Enter new name: ")
                        if override['settings']['name'][0] in os.listdir('results'):
                            print(f"{override['settings']['name'][0]} {colored('has been used before.', 'red')}")
                            val = input(f"{colored('Want to change it?', 'red')} y/n: ")
                            if val == "y":
                                change_confirm = False
                            else:
                                change_confirm = True
                        else:
                            change_confirm = True

def combination_check(combinations:list) -> bool:
    """Show user the combinations to run and ask if correct"""
    for com in combinations:
        if 'settings' in com:
            if 'name' in com['settings']:
                del com['settings']['name']
            if 'save_type' in com['settings']:
                del com['settings']['save_type']

    print(*(config_print(combination) for combination in combinations), sep='\n')
    print(colored(f'number of combinations: {len(combinations)}', 'green'))
    val = input("run y/n: ")
    if val != "y":
        exit()

def trim_override(dictionary:dict) -> dict:
    """Removing non repetitive items from dictionary"""
    if 'settings' in dictionary:
        del dictionary['settings']
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
            return_string += config_print(v)
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

    y_axis = [y for y in range(len(config['reps']))]
    # y_axis = [0, 1, 2, 3]

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
