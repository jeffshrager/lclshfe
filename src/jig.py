"""Jig"""
import os
import pickle
from statistics import stdev
from time import time
from numpy import mean, sqrt, std
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.library.enums.jig_enums import SaveType
from src.library.functions.conf_func import add_time_num, cartesian_product, \
    collapsed_file_setup, combination_check, dictionary_dump, \
    runs_to_xyz, sort_combinations, trim_override, write_summary_file
from src.model import model
from src.settings.config import Config

def jig(override:dict) -> str:
    """Jig"""
    start_time = time()
    config = Config(override)
    folder = f"{config['settings']['name'][0]}/{str(start_time)}"
    settings_config = override['settings']
    override = trim_override(override)
    combinations = sort_combinations(override, config, list(
        cartesian_product(override)) if override else [
            {'settings':{'name': config['settings']['name'][0]}}])
    combination_check(combinations)
    for combination in combinations:
        combination.update({'settings': settings_config})
    dictionary_dump(config, 'config', folder)
    os.makedirs(os.path.dirname(f"results/{folder}/config.tsv"), exist_ok=True)
    with open(f"results/{folder}/config.tsv", "w", encoding="utf-8") as file:
        file.write(str(config))
        if isinstance(config['settings']['save_type'], list):
            config.default_dictionary.update({
                'settings':{'save_type':config['settings']['save_type'][0]}})
    if config['settings']['save_type'] == SaveType.COLLAPSED:
        collapsed_file_setup(override, folder)
    runs = [model(Config(add_time_num(combination, start_time, run_number))
        ) for run_number, combination in enumerate(combinations)]
    dictionary_dump(runs, 'runs', folder)
    write_summary_file(override, folder, runs)
    return folder

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
    write_summary_file(config, folder, runs)
    # for rep_count in range(len(config['reps'])):
    #     total_data = []
    #     for run in runs:
    #         for data in run.samples[rep_count].data:
    #             total_data.append(data.quality)
    #     number_samples = [len(run.samples[rep_count].data) for run in runs]
    #     print(f"{number_samples}:\nmean - {mean(number_samples)}, stdev - {stdev(number_samples)},"+
    #     f" var - {var(number_samples)}\nmean - {mean(total_data)}, stdev - {stdev(total_data)},"+
    #     f"var - {var(total_data)}\n")

def display(folder:str) -> bool:
    """Pivot Table Display"""
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)
    print(config)
    print(runs)

def depriciated_display(folder:str) -> bool:
    """Display"""
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)

    if config['settings']['save_type'][0] == SaveType.DETAILED:
        (x_axis, y_axis, z_axis) = runs_to_xyz(config, runs)
        fig = go.Figure(go.Surface(
            x=x_axis,
            y=y_axis,
            z=z_axis,
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
    elif config['settings']['save_type'][0] == SaveType.COLLAPSED:
        if len(config['samples']['samples'][0]) > 1:

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

            data_frame = pd.DataFrame(data=computed_run)
            print(data_frame)
            fig = px.line(data_frame, x='noticing_delay', y='N', color='noticing_delay',
                error_y='err', color_discrete_sequence=px.colors.qualitative.G10)
            # fig = px.line_3d(data_frame, x='pq', y='noticing_delay', z='mean',
            # color='noticing_delay',error_z='err',
            # color_discrete_sequence=px.colors.qualitative.G10)
            colors = px.colors.qualitative.G10
            fig.update_traces(showlegend=False, error_y_color='red', marker=dict(color=colors))
            fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
                scene = {
                    "xaxis": {"title": 'preformance quality', "nticks": len(config['samples']['samples'])},
                    "zaxis": {"title": 'N', "nticks": 10},
                    "yaxis": {"title": 'noticing delay', "nticks":len(config['op_noticing_delay'])},
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
