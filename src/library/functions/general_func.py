"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from src.library.enums.jig_enums import SaveType
from src.library.functions.func import goal_agenda_plan
from src.library.objects.agent import DataAnalyst, ExperimentManager, Operator
from src.library.objects.instrument import CXI
from src.library.objects.objs import AMI, Agenda, CommunicationObject, Context
from src.settings.config import Config

def context_setup(config:Config) -> Context:
    """Setup the context"""
    c_file, c_data_file = None, None
    if config['settings']['save_type'][0] == SaveType.DETAILED:
        experiment_folder:str = f"results/{config['settings']['name'][0]}/{config['start_time']}/run_{config['run_number'] + 1}"
        config.make_dirs([f"{experiment_folder}/model/r{config['start_time']}.tsv", f"{experiment_folder}/data/r{config['start_time']}.tsv"])
        with open(f"{experiment_folder}/config.tsv", "w", encoding="utf-8") as config_file:
            config_file.write(str(config))
        with open(f"{experiment_folder}/model/r{config['start_time']}.tsv", "w", encoding="utf-8") as file:
            c_file = file
        with open(f"{experiment_folder}/data/r{config['start_time']}.tsv", "w", encoding="utf-8") as data_file:
            c_data_file = data_file
    context = Context(AMI(config), Agenda(config), DataAnalyst(config),
        ExperimentManager(config), Operator(config), CXI(config), CommunicationObject(),
        config, c_file, c_data_file)
    if context['settings']['save_type'][0] == SaveType.DETAILED:
        open(context.file.name, 'a', encoding="utf-8").write(f"{goal_agenda_plan(context)}\n")
    return context
