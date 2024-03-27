"""The primary functions of the model used to configure and run the jig.

The contained methods are used to interact with the model. These are the
only functions that should be run by the user from a separate script.
There is the primary jig method as well as other methods for processing
data as well as creating and displaying graphs.

supressed:
    Supressing the jig will prevent any input from being asked from the user.
independent_variable:
    The variable that is used from the override dictionary to create
    graphs and data summarys.

  Typical usage example:

  jig(override, supressed, independent_variable)
  stats(folder, independent_variable)
  rollup(folder, independent_variable)
  display(folder, independent_variable)
  display_new(folder, independent_variable)
"""
import os
import pickle
from statistics import stdev
from time import time
from numpy import mean, sqrt, std
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model as model
import sim.model.settings as settings

def jig(override:dict, supressed:bool, independent_variable:str) -> str:
    """Runs the model using the override dictionary.

    Using the override dictionary, creates all the configurations using
    the cartisian product and runs the model for each configuration.
    The models return an AMI object which is the result of the run.
    This method then handles output file creation as well as dumping
    the resulting obejcts to files for use later.

    Args:
        config: The set of variables used to run the experiment, each of
        the configs passed to the model only contain one parameter for
        each setting.

    Returns:
        A AMI object which contains the configuration of the simulation
        as well as all of the data generated during the simulation.
    """
    start_time = time()
    config = settings.Config(override)
    folder = f"{config['settings']['name'][0]}/{str(start_time)}"
    settings_config = None
    job_progress = Progress("{task.description}",SpinnerColumn(),BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"))
    if not supressed:
        functions.name_check(override)
    if 'settings' in override:
        settings_config = override['settings']
    override = functions.trim_override(override)
    combinations = functions.sort_combinations(config, list(
        functions.cartesian_product(override)) if override else [
            {'settings':{'name': config['settings']['name'][0]}}])
    for run_number, combination in enumerate(combinations):
        job_progress.add_task(f"[green]{run_number}", total=combination['experimental_time'].total_seconds())
    total = sum(task.total for task in job_progress.tasks)
    overall_progress = Progress()
    overall_task = overall_progress.add_task("All Jobs", total=int(total))
    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)),
        Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)))
    with Live(Layout() if config['settings']['display'] else progress_table, refresh_per_second=60, screen=False if config['settings']['display'] else False) as live:
        if not supressed:
            functions.combination_check(combinations)
        if settings_config:
            for combination in combinations:
                combination.update({'settings': settings_config})
        functions.dictionary_dump(config, 'config', folder)
        os.makedirs(os.path.dirname(f"results/{folder}/config.tsv"), exist_ok=True)
        with open(f"results/{folder}/config.tsv", "w", encoding="utf-8") as file:
            file.write(str(config))
            if isinstance(config['settings']['save_type'], list):
                config.default_dictionary.update({
                    'settings':{'save_type':config['settings']['save_type'][0]}})
        # if config['settings']['save_type'] == enums.SaveType.COLLAPSED:
        functions.collapsed_file_setup(override, folder)
    # TODO: add multiprocessing
    # runs = [product(settings.Config(functions.add_time_num(combination, start_time, run_number)), job_progress, overall_progress, overall_task) for run_number, combination in enumerate(combinations)]
    # queries = [settings.Config(functions.add_time_num(combination, start_time, run_number)) for run_number, combination in enumerate(combinations)]
    # with Pool() as pool:
    #     args = ((args, 1) for args in product(queries))
    #     results = pool.map(model.run, args)
    # with Pool() as p:
    #     p.map(model.run, [product(settings.Config(functions.add_time_num(combination, start_time, run_number)) for run_number, combination in enumerate(combinations)])
        # print(p.map(f, [1, 2, 3]))
        runs = [model.run(settings.Config(functions.add_time_num(combination, start_time, run_number)), live, job_progress, overall_progress, overall_task, len(combinations)) for run_number, combination in enumerate(combinations)]
        functions.dictionary_dump(runs, 'runs', folder)
        functions.write_summary_file(config, folder, runs, independent_variable)
    return folder

def stats(folder:str, independent_variable:str) -> bool:
    """Creates a summary file of the data.

    Goes through the data and averages the data for each combination,
    resulting in a summary file.

    Args:
        folder: The folder containing the data to be summarized.
        independent_variable: The variable that is used from the override
    """
    # FFF QQQ: Auto Remove outliers
    # TODO: PUll out erros from runs
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)
    functions.write_summary_file(config, folder, runs, independent_variable)
    # for rep_count in range(len(config['reps'])):
    #     total_data = []
    #     for run in runs:
    #         for data in run.samples[rep_count].data:
    #             total_data.append(data.quality)
    #     number_samples = [len(run.samples[rep_count].data) for run in runs]
    #     print(f"{number_samples}:\nmean - {mean(number_samples)}, stdev - {stdev(number_samples)},"+
    #     f" var - {var(number_samples)}\nmean - {mean(total_data)}, stdev - {stdev(total_data)},"+
    #     f"var - {var(total_data)}\n")

def old_display(folder:str) -> bool:
    """Old_Display the data in a graph

    Display the data in a graph

    Args:
        folder: the folder to display the data from
        independent_variable: the independent variable to display the data from

    Returns:
        Shows a graph in a web browser
    """
    config = None
    runs = None
    with open(f"results/{folder}/dictionaries/config.dictionary", 'rb') as config_dictionary_file:
        config = pickle.load(config_dictionary_file)
    with open(f"results/{folder}/dictionaries/runs.dictionary", 'rb') as runs_dictionary_file:
        runs = pickle.load(runs_dictionary_file)

    if config['settings']['save_type'][0] == enums.SaveType.DETAILED:
        (x_axis, y_axis, z_axis) = functions.runs_to_xyz(config, runs)
        fig = go.Figure(go.Surface(
            x=x_axis,
            y=y_axis,
            z=z_axis,
        ))
        fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
            scene = {
                "xaxis": {"title": 'cycles', "nticks": 20, 'autorange': 'reversed'},
                "zaxis": {"title": 'data quality', "nticks": 10},
                "yaxis": {"title": 'means', "nticks": len(config['reps'])},
                'camera_eye': {"x": 2.2, "y": 2.2, "z": 0.5},
                "aspectratio": {"x": 3, "y": 1, "z": 0.6}
            })
        fig.show()
    elif config['settings']['save_type'][0] == enums.SaveType.COLLAPSED:
        if len(config['samples']['samples'][0]) > 1:

            computed_run = {
                'noticing_delay': [],
                'functional_acuity': [],
                'N': [],
                # 'err': [],
                'pq': [],

            }
            # for sample in range(len(config['samples'][0])):
            for run in runs:
                for value in range(len(run['N'])):
                    computed_run['noticing_delay'].append(run['noticing_delay'])
                    computed_run['functional_acuity'].append(run['functional_acuity'])
                    computed_run['N'].append(run['N'][value])
                    # computed_run['err'].append((run['err'][value]))
                    computed_run['pq'].append(run['pq'])
            
            compressed_run = {
                'noticing_delay': [],
                'functional_acuity': [],
                'N': [],
                'err': [],
                'pq': [],
            }
            # temp_ond = 0
            # temp_func = 0
            # n_average = 0
            # n_count = 0
            # for index, _ in enumerate(computed_run['N']):
            #     if computed_run['functional_acuity'][index] == temp_func:
            #         n_average += computed_run['N'][index]
            #     else:
            #         # computed_run['noticing_delay'].append(run['noticing_delay'])
            #         # compressed_run.append([temp_ond, temp_func, n_average])
            #         temp_ond = computed_run['noticing_delay'][index]
            #         temp_func = computed_run['functional_acuity'][index]
            #         n_average = 0

                # compressed_run.append(values)
            data_frame = pd.DataFrame(data=computed_run)
            print(data_frame)
            fig = px.line(data_frame, x='pq', y='N', color='functional_acuity',
                error_y='err', color_discrete_sequence=px.colors.qualitative.G10)
            for each in fig.data:
                each.error_y.thickness = 2
                each.error_y.width = 0.8
            # fig = go.Figure(data=go.Scatter(
            #     x='pq',
            #     y='N',
            #     error_y=dict(
            #         type='err',
            #         symmetric=False,
            #         value=15,
            #         valueminus=25)
            # ))
            # fig = px.line_3d(data_frame, x='pq', y='noticing_delay', z='mean',
            # color='noticing_delay',error_z='err',
            # color_discrete_sequence=px.colors.qualitative.G10)
            colors = px.colors.qualitative.G10
            fig.update_traces(showlegend=True, error_y_color='red', marker=dict(color=colors))
            fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
                scene = {
                    "xaxis": {"title": 'preformance quality', "nticks": len(config['samples']['samples']), 'autorange': 'reversed'},
                    "zaxis": {"title": 'N', "nticks": 10},
                    "yaxis": {"title": 'noticing delay', "nticks":len(config['operator']['noticing_delay'])},
                    'camera_eye': {"x": 2.2, "y": 2.2, "z": 0.5},
                    "aspectratio": {"x": 2, "y": 0.5, "z": 0.6}
                })
            fig.show()
        else:
            computed_list = []
            for conf in config['operator']['functional_acuity']:
                temp_computed_list = []
                for run in runs:
                    if run['functional_acuity'] == conf:
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
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=config['operator']['functional_acuity'], y=means_list,
                    mode='lines+markers',
                    name='lines',
                    error_y=dict(
                        type='data', # value of error bar given in data coordinates
                        array=err_list,
                        visible=True)
                ))
            # fig = go.Figure(data=go.Scatter(
            #         x=config['operator']['functional_acuity'],
            #         mode='lines+markers',
            #         y=means_list,
            #         error_y=dict(
            #             type='data', # value of error bar given in data coordinates
            #             array=err_list,
            #             visible=True)
            #     ))
            fig.show()

def display(folder:str, independent_variable:str) -> bool:
    """Display the data in a graph

    Display the data in a graph

    Args:
        folder: the folder to display the data from
        independent_variable: the independent variable to display the data from

    Returns:
        Shows a graph in a web browser
    """
    # import_file = {}
    data_frame = pd.read_csv(f"results/{folder}/summary.tsv", sep='\t', index_col=False)
    print(data_frame)
    fig = px.line(data_frame, x='pq', y='average', color=f'{independent_variable}',
    error_y='err', color_discrete_sequence=px.colors.qualitative.G10)
    colors = px.colors.qualitative.G10
    fig.update_traces(showlegend=True, error_y_color='red', marker=dict(color=colors))
    fig.update_layout(title=folder, autosize=True, margin=dict(l=65, r=50, b=65, t=90),
        scene = {
            "xaxis": {"title": 'preformance quality','autorange': 'reversed'},
            "zaxis": {"title": 'N', "nticks": 10},
            "yaxis": {"title": 'noticing delay'},
            'camera_eye': {"x": 2.2, "y": 2.2, "z": 0.5},
            "aspectratio": {"x": 2, "y": 0.5, "z": 0.6}
        })
    fig.show()
    # with open(f"results/{folder}/summary.tsv",) as f:
    #     records = csv.DictReader(f)
    #     for row in records:
    #         print(row)
    # with open(f"results/{folder}/summary.tsv", newline='') as csv_f:
    #     for row in csv.DictReader(csv_f, delimiter='\t'):
    #         # header = row['average'] + ' ' + row['stdev'] + ' ' + row['n'] + ' ' + row['err'] + ' ' + row['functional_acuity']
    #         import_file[row['average']] = float(row['pq'])
    # print(import_file)
