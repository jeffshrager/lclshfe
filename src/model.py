"""High Level Controller: Round Robbin processes of classes, Synchronous simulation"""
import copy
import os
from time import sleep
from termcolor import colored
from src.library.objects.objs import AMI, Agenda, CommunicationObject, Config, Context
from src.library.objects.agent import DataAnalyst, ExperimentManager, Operator
from src.library.objects.instrument import CXI
from src.library.functions.func import create_experiment_figure, experiment_is_not_over, \
    experiment_stats, goal_agenda_plan

def model(config:Config) -> AMI:
    """Run CXI Simulation"""
    config.make_dirs([f"results/{config['name_of_experiment']}_{config['start_time']}/run_{config.run_number + 1}/model/r{config['start_time']}.tsv",
                      f"results/{config['name_of_experiment']}_{config['start_time']}/run_{config.run_number + 1}/data/r{config['start_time']}.tsv"])
    with open(f"results/{config['name_of_experiment']}_{config['start_time']}/run_{config.run_number + 1}/config.tsv", "w", encoding="utf-8") as config_file:
        config_file.write(str(config))
    with open(f"results/{config['name_of_experiment']}_{config['start_time']}/run_{config.run_number + 1}/model/r{config['start_time']}.tsv", "w", encoding="utf-8") as file:
        with open(f"results/{config['name_of_experiment']}_{config['start_time']}/run_{config.run_number + 1}/data/r{config['start_time']}.tsv", "w", encoding="utf-8") as data_file:
            context:Context = Context( AMI(config), Agenda(config), DataAnalyst(config),
                ExperimentManager(), Operator(config), CXI(config), CommunicationObject(),
                config, file, data_file)
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
            context.file.write(f"\n{experiment_stats(context)}\nFinished")
            print(f"{context.config.override_dictionary}\n{experiment_stats(context)}\n"+
            f"{colored('Finished','green')}" if config['display'] else '-')
            create_experiment_figure(context, False)
            return copy.deepcopy(context.ami)
