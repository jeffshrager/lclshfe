"""Jig"""
import os
import pickle
from statistics import stdev
from time import time
from numpy import mean, sqrt, std, var
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.library.enums.jig_enums import SaveType
from src.library.functions.conf_func import add_time_num, cartesian_product, \
    collapsed_file_setup, combination_check, dictionary_dump, \
    runs_to_xyz, sort_combinations, trim_override_dictionary
from src.model import model
from src.settings.config import Config

def jig(override_dictionary:dict) -> str:
    """Jig"""
    start_time = time()
    top_level_config = Config(override_dictionary)
    experiment_folder = f"{top_level_config['experiment_name'][0]}/{str(start_time)}"
    override_dictionary = trim_override_dictionary(override_dictionary)
    combinations = sort_combinations(override_dictionary, top_level_config, list(
        cartesian_product(**override_dictionary)) if override_dictionary else [
            {'experiment_name': top_level_config['experiment_name'][0]}])
    combination_check(combinations)
    dictionary_dump(top_level_config, 'config', experiment_folder)
    os.makedirs(os.path.dirname(f"results/{experiment_folder}/config.tsv"), exist_ok=True)
    with open(f"results/{experiment_folder}/config.tsv", "w", encoding="utf-8") as file:
        file.write(str(top_level_config))
        if isinstance(top_level_config['save_type'], list):
            top_level_config.default_dictionary.update(
                {'save_type':top_level_config['save_type'][0]})
    if top_level_config['save_type'] == SaveType.COLLAPSED:
        collapsed_file_setup(override_dictionary, experiment_folder)
    runs = [model(Config(add_time_num(combination, start_time, run_number))
        ) for run_number, combination in enumerate(combinations)]
    dictionary_dump(runs, 'runs', experiment_folder)
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
