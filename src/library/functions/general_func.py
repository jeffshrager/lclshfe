"""General Func"""
from src.library.enums.jig_enums import SaveType
from src.library.functions.func import goal_agenda_plan
from src.library.objects.agent import DataAnalyst, ExperimentManager, Operator
from src.library.objects.instrument import CXI
from src.library.objects.objs import AMI, Agenda, CommunicationObject, Context
from src.settings.config import Config

def context_setup(config:Config) -> Context:
    """Setup the context"""
    c_file, c_data_file = None, None
    if config['settings']['save_type'] == SaveType.DETAILED:
        experiment_folder:str = f"results/{config['settings']['name']}/{config['start_time']}/run_{config['run_number'] + 1}"
        config.make_dirs([f"{experiment_folder}/model/r{config['start_time']}.tsv", f"{experiment_folder}/data/r{config['start_time']}.tsv"])
        with open(f"{experiment_folder}/config.tsv", "w", encoding="utf-8") as config_file:
            config_file.write(str(config))
        with open(f"{experiment_folder}/model/r{config['start_time']}.tsv", "w", encoding="utf-8") as file:
            c_file = file
        with open(f"{experiment_folder}/data/r{config['start_time']}.tsv", "w", encoding="utf-8") as data_file:
            c_data_file = data_file
    context = Context(AMI(config), Agenda(config), DataAnalyst(config),
        ExperimentManager(), Operator(config), CXI(config), CommunicationObject(),
        config, c_file, c_data_file)
    if context['settings']['save_type'] == SaveType.DETAILED:
        context.file.write(f"{goal_agenda_plan(context)}\n")
    return context