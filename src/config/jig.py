"""Jig"""
import os
import pickle
from statistics import stdev
from time import time
from numpy import mean, var
import plotly.graph_objects as go
from src.library.functions.conf_func import cartesian_product, config_print, runs_to_xyz
from src.library.objects.objs import AMI, Config
from src.model import model

def jig(override_dictionary:dict) -> str:
    """Jig"""
    combinations = list(cartesian_product(**override_dictionary))
    print(*(config_print(combination) for combination in combinations), sep='\n')
    val = input("run y/n: ")
    if val != "y":
        exit()

    start_time = str(time())
    top_level_config = Config(override_dictionary, start_time, 0)
    experiment_folder = f"{top_level_config['name_of_experiment'][0]}_{top_level_config['start_time']}"
    os.makedirs(f"results/{experiment_folder}/dictionaries", exist_ok=True)
    with open(f'results/{experiment_folder}/dictionaries/config.dictionary', 'wb') as config_dictionary_file:
        pickle.dump(top_level_config, config_dictionary_file)
    os.makedirs(os.path.dirname(f"results/{experiment_folder}/config.tsv"), exist_ok=True)
    with open(f"results/{experiment_folder}/config.tsv", "w", encoding="utf-8") as file:
        file.write(str(top_level_config))
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
    """Display"""
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)

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
            "aspectratio": {"x": 3, "y": 1, "z": 0.8}
        })
    fig.show()
