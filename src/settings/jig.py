"""Jig"""
import copy
import os
import pickle
from statistics import stdev
from time import time
from numpy import mean, sqrt, std, var
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.enums.jig_enums import SaveType
from src.library.functions.conf_func import cartesian_product, config_print, runs_to_xyz
from src.model import model
from src.settings.config import Config

def jig(override_dictionary:dict) -> str:
    """Jig"""
    combinations = []
    raw_combinations = list(cartesian_product(**override_dictionary))
    trimmed_combinations = copy.deepcopy(override_dictionary)
    if 'reps' in trimmed_combinations:
        del trimmed_combinations['reps']
    if 'name_of_experiment' in trimmed_combinations:
        del trimmed_combinations['name_of_experiment']
    if 'save_type' in trimmed_combinations:
        del trimmed_combinations['save_type']
    temp_list = list(cartesian_product(**trimmed_combinations))
    number_of_combinations:int = len(temp_list)

    for com in range(number_of_combinations):
        for rep in override_dictionary['reps']:
            combinations.append(raw_combinations[com + (rep * number_of_combinations)])

    print(*(config_print(combination) for combination in combinations), sep='\n')
    print(len(combinations))
    val = input("run y/n: ")
    if val != "y":
        exit()

    start_time = str(time())
    top_level_config = Config(override_dictionary, start_time, 0)
    experiment_folder = f"{top_level_config['name_of_experiment'][0]}/{top_level_config['start_time']}"
    os.makedirs(f"results/{experiment_folder}/dictionaries", exist_ok=True)
    with open(f'results/{experiment_folder}/dictionaries/config.dictionary', 'wb') as config_dictionary_file:
        pickle.dump(top_level_config, config_dictionary_file)
    os.makedirs(os.path.dirname(f"results/{experiment_folder}/config.tsv"), exist_ok=True)
    with open(f"results/{experiment_folder}/config.tsv", "w", encoding="utf-8") as file:
        file.write(str(top_level_config))

    if top_level_config['save_type'] == SaveType.COLLAPSED:
        os.makedirs(os.path.dirname(f"results/{experiment_folder}/collapsed.tsv"), exist_ok=True)
    with open(f"results/{experiment_folder}/collapsed.tsv", "w", encoding="utf-8") as file:
        for key in override_dictionary.keys():
            file.write(f"{key}\t")
        file.write("N\twall_hits\trun\tmean\tstdev\terr\tvar\tpq")
        file.write("\n")
        # file.write("N\tnoticing_delay\twall_hits\trun\tmean\tstdev\terr\tvarr\tpq\n")
    runs = [model(Config(combination, start_time, run_number)) for run_number, combination in enumerate(combinations)]
    with open(f'results/{experiment_folder}/dictionaries/runs.dictionary', 'wb') as runs_dictionary_file:
        pickle.dump(runs, runs_dictionary_file)
    return experiment_folder

def stats(folder:str) -> bool:
    """Standard Deviation"""
    # FFF QQQ: Auto Remove outliers
    # TODO: PUll out erros from runs
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)
    
    for s in range(len(config['reps'])):
        total_data = []
        for run in runs:
            for data in run.samples[s].data:
                total_data.append(data.quality)
        ns = [len(run.samples[s].data) for run in runs]
        print(f"{ns}:\nmean - {mean(ns)}, stdev - {stdev(ns)}, var - {var(ns)}\nmean - {mean(total_data)}, stdev - {stdev(total_data)}, var - {var(total_data)}\n")

def display(folder:str) -> bool:
    pass
    # """Pivot Table Display"""
    # config = None
    # runs = None
    # with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
    #     config = pickle.load(config_dictionary_file)
    # with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
    #     runs = pickle.load(runs_dictionary_file)

def depriciated_display(folder:str) -> bool:
    """Display"""
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)
    
    if config['save_type'][0] == SaveType.DETAILED:
        (x, y, z) = runs_to_xyz(config, runs)
        fig = go.Figure(go.Surface(
            x=x,
            y=y,
            z=z,
        ))
        fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
            scene = {
                "xaxis": {"title": 'cycles', "nticks": 20, "autorange":'reversed'},
                "zaxis": {"title": 'data quality', "nticks": 10},
                "yaxis": {"title": 'means', "nticks": len(config['reps'])},
                'camera_eye': {"x": 2.2, "y": 2.2, "z": 0.5},
                "aspectratio": {"x": 3, "y": 1, "z": 0.6}
            })
        fig.show()
    elif config['save_type'][0] == SaveType.COLLAPSED:
        if len(config['samples'][0]) > 1:

            computed_run = {
                'noticing_delay': [],
                'N': [],
                'err': [],
                'pq': [],

            }
            # for sample in range(len(config['samples'][0])):
            for run in runs:
                for value in range(len(run['N'])):
                    computed_run['noticing_delay'].append(run['op_noticing_delay'][0])
                    computed_run['N'].append(run['N'][value])
                    computed_run['err'].append(run['err'][value])
                    computed_run['pq'].append(run['pq'])

            df = pd.DataFrame(data=computed_run)
            print(df)
            fig = px.line(df, x='noticing_delay', y='N', color='noticing_delay',error_y='err',
                        color_discrete_sequence=px.colors.qualitative.G10)
            # fig = px.line_3d(df, x='pq', y='noticing_delay', z='mean', color='noticing_delay',error_z='err',
            #             color_discrete_sequence=px.colors.qualitative.G10)
            colors = px.colors.qualitative.G10
            fig.update_traces(showlegend=False, error_y_color='red', marker=dict(color=colors))
            fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
                scene = {
                    "xaxis": {"title": 'preformance quality', "nticks": len(config['samples'])},
                    "zaxis": {"title": 'N', "nticks": 10},
                    "yaxis": {"title": 'noticing delay', "nticks": len(config['op_noticing_delay'])},
                    'camera_eye': {"x": 2.2, "y": 2.2, "z": 0.5},
                    "aspectratio": {"x": 2, "y": 0.5, "z": 0.6}
                })
            fig.show()
        else:
            computed_list = []
            for conf in config['op_noticing_delay']:
                temp_computed_list = []
                for run in runs:
                    if run['noticing_delay'] == conf:
                        temp_computed_list.append(run['N'][0])
                # temp_computed_list = [x for x in temp_computed_list if (x > 100000)]
                computed_list.append(temp_computed_list)
            means_list = []
            for comp_list in computed_list:
                means_list.append(mean(comp_list))
            stdev_list = []
            for comp_list in computed_list:
                stdev_list.append(stdev(comp_list))
            err_list = []
            for comp_list in computed_list:
                err_list.append(std(comp_list) / sqrt(len(comp_list)))
            fig = go.Figure(data=go.Scatter(
                    x=config['op_noticing_delay'],
                    y=means_list,
                    error_y=dict(
                        type='data', # value of error bar given in data coordinates
                        array=err_list,
                        visible=True)
                ))
            fig.show()
