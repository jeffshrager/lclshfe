"""Collection of overrides for the default behavior of the model."""
from datetime import timedelta
from src.library.enums.jig_enums import SaveType
from src.library.enums.model_enums import SampleImportance, SampleType
from src.library.objects.objs import SampleData

over180 = {
    'settings': {'name':['over180'],'save_type':[SaveType.COLLAPSED], 'cycle_sleep_time': 0.0,},
    'reps': [x for x in range(2)],
    'operator': {
        'noticing_delay': [100.0],
        'functional_acuity': [100.0],
        'button_distance': [10],},
    'samples': {'samples': [
        [SampleData(0.40, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.35, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.30, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.25, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.20, SampleImportance.UNIMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'cxi': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
macro_test = {
    'settings': {'name':['macro_test'],'save_type':[SaveType.COLLAPSED], 'cycle_sleep_time': 0.1,},
    'reps': [x for x in range(1)],
    'operator': {
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(seconds=19500)],
    'samples': {'samples': [
        [SampleData(0.90, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.85, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.80, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.75, SampleImportance.UNIMPORTANT, SampleType.TAPE),
         SampleData(0.70, SampleImportance.UNIMPORTANT, SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'cxi': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------------------------
fnc_ond1_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(9)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
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
fnc_ond10_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(9)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [10.0]},
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
fnc_ond20_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(9)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [20.0]},
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
# --------------------------------------------------------------------------------------------------
button_distance = {
    'settings': {'name':['button_distance'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'button_distance': [0.1, 1.0, 2.0],
        'noticing_delay': [1.0]},
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
# --------------------------------------------------------------------------------------------------
fnc_ond1_tanh_true_cog_true = {
    'settings': {'name':['fnc_ond1_tanh_true_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
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
fnc_ond1_tanh_false_cog_true = {
    'settings': {'name':['fnc_ond1_tanh_false_cog_true'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
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
fnc_ond1_tanh_true_cog_false = {
    'settings': {'name':['fnc_ond1_tanh_true_cog_false'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(10)],
    'operator': {
        'functional_acuity': [0.1, 0.5, 1.0],
        'noticing_delay': [1.0]},
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
fnc_ond1_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond1_tanh_false_cog_false'],'save_type':[SaveType.COLLAPSED]},
    'reps': [x for x in range(10)],
    'operator': {
        'functional_acuity': [0.1, 0.5, 1.0],
        'noticing_delay': [1.0]},
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
