"""High Level Controller: Round Robbin processes of classes, Synchronous simulation"""
import copy
import os
from time import sleep
from termcolor import colored
from model.agent import DataAnalyst, ExperimentManager, Operator
from model.instrument import CXI
from model.library.functions import create_experiment_figure, \
    experiment_stats, goal_agenda_plan, experiment_is_not_over
from model.library.objects import Agenda, CommunicationObject, Config, Context, AMI

# c:Config = Config(str(time()), 5, timedelta(hours=5), timedelta(seconds=1),
#                   0, True, '', [], True, 0.001, 1, 1, 0, 100,
#                   600000, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0)
# model(c)

def model(config:Config) -> AMI:
    """Run CXI Simulation"""
    dirs = config.make_dirs([f"results{config.folder}/model/r{Config.start_time}.tsv",
                             f"results{config.folder}/data/r{Config.start_time}.tsv"])
    with open(dirs[0], "w", encoding="utf-8") as file:
        with open(dirs[1], "w", encoding="utf-8") as data_file:
            context:Context = Context( AMI(config), Agenda(config), DataAnalyst(config),
                ExperimentManager(), Operator(config), CXI(config), CommunicationObject(),
                config, file, data_file)
            context.file.write(f"{goal_agenda_plan(context)}\n")
            while experiment_is_not_over(context):
                os.system('cls' if os.name == 'nt' else 'clear')
                context.messages.reset()
                print(goal_agenda_plan(context) if config.display else 'running')
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
                print(context.messages if config.display else 'running')
                context.agent_da.check_if_experiment_is_compleated(context)
                context.current_time += config.step_through_time
                sleep(config.cycle_sleep_time)
            os.system('cls' if os.name == 'nt' else 'clear')
            context.file.write(f"\n{experiment_stats(context)}\nFinished")
            print(f"{experiment_stats(context)}\n"+
            f"{colored('Finished','green')}" if config.display else '-')
            create_experiment_figure(context, False)
            return copy.deepcopy(context.ami)
