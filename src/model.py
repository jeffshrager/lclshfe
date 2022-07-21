"""High Level Controller: Round Robbin processes of classes, Synchronous simulation"""
import copy
import os
from time import sleep
from termcolor import colored
from src.library.enums.jig_enums import SaveType
from src.library.objects.objs import AMI, Agenda, CommunicationObject, Context
from src.library.objects.agent import DataAnalyst, ExperimentManager, Operator
from src.library.objects.instrument import CXI
from src.library.functions.func import create_experiment_figure, experiment_is_not_over, \
    experiment_stats, goal_agenda_plan
from src.settings.config import Config

def model(config:Config) -> AMI:
    """Run CXI Simulation"""
    c_file = None
    c_data_file = None
    context:Context = None
    if config['save_type'] == SaveType.DETAILED:
        config.make_dirs([f"results/{config['experiment_name']}/{config['start_time']}/run_{config['run_number'] + 1}/model/r{config['start_time']}.tsv",
            f"results/{config['experiment_name']}_{config['start_time']}/run_{config['run_number'] + 1}/data/r{config['start_time']}.tsv"])
        with open(f"results/{config['experiment_name']}/{config['start_time']}/run_{config['run_number'] + 1}/config.tsv", "w", encoding="utf-8") as config_file:
            config_file.write(str(config))
        with open(f"results/{config['experiment_name']}/{config['start_time']}/run_{config['run_number'] + 1}/model/r{config['start_time']}.tsv", "w", encoding="utf-8") as file:
            c_file = file
        with open(f"results/{config['experiment_name']}/{config['start_time']}/run_{config['run_number'] + 1}/data/r{config['start_time']}.tsv", "w", encoding="utf-8") as data_file:
            c_data_file = data_file

    context = Context( AMI(config), Agenda(config), DataAnalyst(config),
        ExperimentManager(), Operator(config), CXI(config), CommunicationObject(),
        config, c_file, c_data_file)
    if config['save_type'] == SaveType.DETAILED:
        context.file.write(f"{goal_agenda_plan(context)}\n")

    while experiment_is_not_over(context):
        os.system('cls' if os.name == 'nt' else 'clear')
        context.messages.reset()
        print(goal_agenda_plan(context) if config['display'] else 'running')
        context.update()
        if context.agenda.is_started():
            if context.instrument.is_running():
                if context.instrument.is_collecting_data():
                    context.agent_op.track_stream_position(context)
                    context.agent_em.check_if_data_is_sufficient(context)
                else:
                    if context.agent_em.check_if_next_run_can_be_started(context):
                        context.agent_em.tell_operator_start_data_collection(context)
            else:
                context.agent_em.start_instrument(context)
        else:
            context.agent_em.start_experiment(context)
        print(context.messages if config['display'] else 'running')
        context.agent_da.check_if_experiment_is_compleated(context)
        context.current_time += config['step_through_time']
        sleep(config['cycle_sleep_time'])

    os.system('cls' if os.name == 'nt' else 'clear')
    if config['save_type'] == SaveType.DETAILED:
        context.file.write(f"\n{experiment_stats(context)}\nFinished")
    print(f"{context.config.override_dictionary}\n{experiment_stats(context)}\n"+
    f"{colored('Finished','green')}" if config['display'] else '-')
    create_experiment_figure(context, False)
    if config['save_type'] == SaveType.DETAILED:
        return copy.deepcopy(context.ami)
    elif config['save_type'] == SaveType.COLLAPSED:
        header_list = []
        value_list = []

        for key, value in config.override_dictionary.items():
            if key == 'samples':
                header_list.append(key)
                value_list.append(value)
            else:
                header_list.append(key)
                value_list.append([value])

        header_list.append('N')
        value_list.append(context.ami.get_n())
        header_list.append('wall_hits')
        value_list.append(context.ami.get_wall_hits())
        header_list.append('run')
        value_list.append(context.config['run_number'])
        # TODO: this should all be from sample
        header_list.append('mean')
        value_list.append(context.ami.get_mean())
        header_list.append('stdev')
        value_list.append(context.ami.get_stdev())
        header_list.append('err')
        value_list.append(context.ami.get_err())
        header_list.append('varr')
        value_list.append(context.ami.get_var())
        header_list.append('pq')
        value_list.append(config['samples'][0].preformance_quality)
        condensed_dict = dict(zip(header_list, value_list))

        if isinstance(config['experiment_name'], list):
            config.default_dictionary.update({'experiment_name':config['experiment_name'][0]})
        with open(f"results/{config['experiment_name']}/{config['start_time']}/collapsed.tsv", "a", encoding="utf-8") as file:
            for sample_index, _ in enumerate(config.default_dictionary['samples']):
                for index, _ in enumerate(header_list):
                    if isinstance(value_list[index], list):
                        if len(value_list[index]) == len(config.default_dictionary['samples']):
                            file.write(f"{value_list[index][sample_index]}\t")
                        else:
                            file.write(f"{value_list[index][0]}\t")
                    else:
                        file.write(f"{value_list[index]}\t")
                file.write('\n')
        return condensed_dict
