"""The main run loop for a simulation which calls each object

The High Level Logic of the entire simulation is here this is where the
einstrument is turned on the experiment started and the data collected.
This runs synchronous cycles until the experiment is over handling
calling each part of the experiment in a round robbin execution pattern

  Typical usage example:

  ami = model(config(...))
"""
import copy
import random
import time
import rich
from rich.prompt import Prompt
from rich.live import Live
from rich.progress import Progress
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model.objects as objects
import sim.model.settings as settings

def run(config:settings.Config, live:Live, job_progress:Progress, overall_progress:Progress, overall_task, number_of_combinations:int) -> objects.AMI:
    """Runs the experiment and returns an AMI object

    Runs the model using the given configuration and puts all of the
    data recived into the AMI object. This is the main function of the
    model. This is where each of the agents are called during a given cycle.

    Args:
        config: The set of variables used to run the experiment, each of
        the configs passed to the model only contain one parameter for
        each setting.

    Returns:
        A AMI object which contains the configuration of the simulation
        as well as all of the data generated during the simulation.
    """
    random.seed(round(time.time()))
    context = functions.context_setup(config)
    run_started_tracker:bool = False
    while not functions.experiment_is_over(context):
        context.messages.reset()
        context.update()
        if context.agenda.is_started():
            if context.instrument.is_running():
                if context.instrument.is_collecting_data():
                    context.agent_op.track_stream_position(context)
                    context.agent_em.check_if_data_is_sufficient(context)
                else:
                    if context.agent_em.check_if_next_run_can_be_started(context):
                        run_started_tracker = True
                        context.agent_em.tell_operator_start_data_collection(context)
            else:
                context.agent_em.start_instrument(context)
        else:
            context.agent_em.start_experiment(context)
        if context['settings']['display']:
            live.update(functions.generate_layout(context, overall_progress, number_of_combinations))
        if run_started_tracker and config['settings']['ask_to_continue']['sample']:
                Prompt.ask("[cyan]continue?['magenta'](y/n)", default="y")
                run_started_tracker = False
        context.agent_da.check_if_experiment_is_compleated(context)
        context.current_time += context['step_through_time']
        job_progress.update(config['run_number'], advance=config['step_through_time'].total_seconds())
        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)
        time.sleep(context['settings']['cycle_sleep_time'])
    if config['settings']['ask_to_continue']['run']:
        Prompt.ask("[cyan]continue?['magenta'](y/n)", default="y")
    if context['settings']['save_type'][0] == enums.SaveType.DETAILED:
        open(context.data_file.name, 'a', encoding="utf-8").write(f"\n{functions.experiment_stats(context)}\nFinished")
    if context['settings']['display']:
        rich.print(f"{functions.config_print(context.config.override_dictionary)}\n{functions.experiment_stats(context)}\n"+"[green]Finished")
    functions.create_experiment_figure(context, False)
    if isinstance(context['settings']['save_type'], list):
        context['settings']['save_type'] = context['settings']['save_type'][0]
    header_list = []
    value_list = []
    for key, value in config.override_dictionary.items():
        if key != 'samples' and key != 'start_time':
            if isinstance(value, dict):
                for k, v in value.items():
                    if k != 'name' and k != 'save_type':
                        header_list.append(f"{k}")
                        value_list.append(v)
            else:
                header_list.append(key)
                value_list.append([value])
    header_list.append('N')
    value_list.append(context.ami.get_n())
    header_list.append('wall_hits')
    value_list.append(context.ami.get_wall_hits())
    header_list.extend(context.ami.get_headers())
    value_list.extend(context.ami.get_values())
    condensed_dict = dict(zip(header_list, value_list))
    if isinstance(context['settings']['name'], list):
        config.default_dictionary.update({'settings':{'name':context['settings']['name'][0]}})
    with open(f"results/{context['settings']['name']}/{context['start_time']}/collapsed.tsv",
        "a", encoding="utf-8") as file:
        for sample_index, _ in enumerate(config.default_dictionary['samples']['samples']):
            for index, _ in enumerate(header_list):
                if isinstance(value_list[index], list):
                    if len(value_list[index]) == len(config.default_dictionary['samples']['samples']):
                        file.write(f"{value_list[index][sample_index]}\t")
                    else:
                        file.write(f"{value_list[index][0]}\t")
                else:
                    file.write(f"{value_list[index]}\t")
            file.write('\n')
    return [condensed_dict, copy.deepcopy(context.ami)]
