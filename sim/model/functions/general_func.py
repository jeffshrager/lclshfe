"""General Functions for the simulation

General functions that are used for setup and parameterization
of the given simulation.

  Typical usage example:

  context = functions.context_setup(config)
"""
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.objects.agents as agents

def context_setup(config:settings.Config) -> objects.Context:
    """Setup the context object for the simulation

    Will create folders and objects and create a context object
    that has refrences to all states for the simulation.
    This is using the context pattern.

    Args:
        config: The configuration object for the simulation.

    Returns:
        Context: The context object for the simulation.
    """
    c_file, c_data_file = None, None
    if config['settings']['save_type'][0] == enums.SaveType.DETAILED:
        experiment_folder:str = f"results/{config['settings']['name'][0]}/{config['start_time']}/run_{config['run_number'] + 1}"
        config.make_dirs([f"{experiment_folder}/model/r{config['start_time']}.tsv", f"{experiment_folder}/data/r{config['start_time']}.tsv"])
        with open(f"{experiment_folder}/config.tsv", "w", encoding="utf-8") as config_file:
            config_file.write(str(config))
        with open(f"{experiment_folder}/model/r{config['start_time']}.tsv", "w", encoding="utf-8") as file:
            c_file = file
        with open(f"{experiment_folder}/data/r{config['start_time']}.tsv", "w", encoding="utf-8") as data_file:
            c_data_file = data_file
    context = objects.Context(objects.AMI(config), objects.Agenda(config), agents.data_analyst(config),
        agents.experiment_manager(config), agents.operator(config), objects.CXI(config), objects.CommunicationObject(),
        config, c_file, c_data_file)
    if context['settings']['save_type'][0] == enums.SaveType.DETAILED:
        open(context.file.name, 'a', encoding="utf-8").write(f"{functions.goal_agenda_plan(context)}\n")
    return context
