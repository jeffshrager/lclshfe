"""Collection of overrides for the default behavior of the model."""
from src.library.enums.jig_enums import SaveType
from src.library.enums.model_enums import SampleImportance, SampleType
from src.library.objects.objs import SampleData


# Run dense wide , PQ 90 85 80 75 70 | OND 1 5 10 15 20 25 | FUNC 0.1 0.3 0.5 0.7 0.9 1.0 | Run for 10 everything off
# Tanh  | Cogdev |
# False | False  | ✓
# False | True   | ✓
# True  | False  | ✓
# True  | True   | ✓

fnc_ond_tanh_true_cog_true = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [SampleData(0.90, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.85, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.80, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.75, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.70, SampleImportance.IMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'cxi': {'tanh_curve': [True]}
}

fnc_ond_tanh_false_cog_true = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [SampleData(0.90, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.85, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.80, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.75, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.70, SampleImportance.IMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'cxi': {'tanh_curve': [False]}
}

fnc_ond_tanh_true_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [SampleData(0.90, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.85, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.80, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.75, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.70, SampleImportance.IMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'cxi': {'tanh_curve': [True]}
}

fnc_ond_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [SampleData(0.90, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.85, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.80, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.75, SampleImportance.IMPORTANT, SampleType.TAPE),
         SampleData(0.70, SampleImportance.IMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'cxi': {'tanh_curve': [False]}
}
