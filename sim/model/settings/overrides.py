"""The overrides to run the simulation with.

This file contains variables that you can override the simulation with to
run different experiments with. These were settings that have been used previously.

  Typical usage example:

    sim.jig(sim.overrides.ADJ_True_Stop_True, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_False_Stop_True, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_True_Stop_False, True, 'noticing_delay')
    sim.jig(sim.overrides.ADJ_False_Stop_False, True, 'noticing_delay')
"""
from datetime import timedelta
import sim.model.enums as enum
import sim.model.objects as objects

over180 = {
    'settings': {'name':['over180'],'save_type':[enum.SaveType.COLLAPSED], 'cycle_sleep_time': 0.0,},
    'reps': [x for x in range(2)],
    'operator': {
        'noticing_delay': [100.0],
        'functional_acuity': [100.0],
        'button_distance': [10],},
    'samples': {'samples': [
        [objects.SampleData(0.40, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.35, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.30, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.25, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.20, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
macro_test = {
    'settings': {
        'name':['macro_test'],
        'save_type':[enum.SaveType.DETAILED]},
    'reps': [x for x in range(1)],
    'operator': {
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=49)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.875, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.85, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.825, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.8, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.775, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.725, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.7, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.675, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
# --------------------------------------------------------------------------------------------------
fnc_ond_tanh_true_cog_true = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'instrument': {'tanh_curve': [True]}
}
fnc_ond_tanh_false_cog_true = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'instrument': {'tanh_curve': [False]}
}
fnc_ond_tanh_true_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [True]}
}
fnc_ond_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(3)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
fnc_ond1_tanh_false_cog_false_30mins = {
    'settings': {'name':['fnc_ond1_tanh_false_cog_false_30mins'],'save_type':[enum.SaveType.COLLAPSED], 'display': True,},
    'reps': [x for x in range(1)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=22)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
fnc_ond10_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(9)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [10.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
fnc_ond20_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(9)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [20.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
button_distance = {
    'settings': {'name':['button_distance'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'button_distance': [0.1, 1.0, 2.0],
        'noticing_delay': [1.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
fnc_ond1_tanh_true_cog_true = {
    'settings': {'name':['fnc_ond1_tanh_true_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'instrument': {'tanh_curve': [True]}
}
fnc_ond1_tanh_false_cog_true = {
    'settings': {'name':['fnc_ond1_tanh_false_cog_true'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(5)],
    'operator': {
        'functional_acuity': [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
        'noticing_delay': [1.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [True],
    'instrument': {'tanh_curve': [False]}
}
fnc_ond1_tanh_true_cog_false = {
    'settings': {'name':['fnc_ond1_tanh_true_cog_false'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(10)],
    'operator': {
        'functional_acuity': [0.1, 0.5, 1.0],
        'noticing_delay': [1.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [True]}
}
fnc_ond1_tanh_false_cog_false = {
    'settings': {'name':['fnc_ond1_tanh_false_cog_false'],'save_type':[enum.SaveType.COLLAPSED]},
    'reps': [x for x in range(10)],
    'operator': {
        'functional_acuity': [0.1, 0.5, 1.0],
        'noticing_delay': [1.0]},
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
tiny_test = {
    'settings': {'name':['tiny_test'],'save_type':[enum.SaveType.DETAILED]},
    'reps': [x for x in range(1)],
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0, 2.0]},
    'experimental_time': [timedelta(minutes=22)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
        objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}
# --------------------------------------------------------------------------------------------------
ErrorChangeTest = {
    'settings': {
        'name':['ErrorChangeTest'],
        'save_type':[enum.SaveType.DETAILED],
        'display': True,
        'ask_to_continue': {
            'sample':True,
            'run': True,
        }},
    'reps': [x for x in range(10)],
    'operator': {
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=20)],
    'samples': {'samples': [
        [objects.SampleData(0.9, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.85, enum.SampleImportance.UNIMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.8, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.7, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT),
         objects.SampleData(0.65, enum.SampleImportance.IMPORTANT, enum.SampleType.INSTANT)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
# --------------------------------------------------------------------------------------------------
ADJ_True_Stop_True = {
    'settings': {
        'name':['ADJ_True_Stop_True_10'],
        'save_type':[enum.SaveType.COLLAPSED],
        'display': False,
        'strict_time': True,
        'ask_to_continue': {
            'sample': False,
        }},
    'reps': [x for x in range(9)],
    'experiment_manager': {
        'adjust_error': [True],
    },
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=10)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
ADJ_False_Stop_True = {
    'settings': {
        'name':['ADJ_False_Stop_True_10'],
        'save_type':[enum.SaveType.COLLAPSED],
        'display': False,
        'strict_time': True,
        'ask_to_continue': {
            'sample': False,
        }},
    'reps': [x for x in range(9)],
    'experiment_manager': {
        'adjust_error': [False],
    },
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=10)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
ADJ_True_Stop_False = {
    'settings': {
        'name':['ADJ_True_Stop_False_10'],
        'save_type':[enum.SaveType.COLLAPSED],
        'display': False,
        'strict_time': False,
        'ask_to_continue': {
            'sample': False,
        }},
    'reps': [x for x in range(9)],
    'experiment_manager': {
        'adjust_error': [True],
    },
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=10)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
ADJ_False_Stop_False = {
    'settings': {
        'name':['ADJ_False_Stop_False_10'],
        'save_type':[enum.SaveType.COLLAPSED],
        'display': False,
        'strict_time': False,
        'ask_to_continue': {
            'sample': False,
        }},
    'reps': [x for x in range(9)],
    'experiment_manager': {
        'adjust_error': [False],
    },
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0]},
    'experimental_time': [timedelta(minutes=10)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {
        'tanh_curve': [False],
        'sample_transition_time': [timedelta(seconds=1)]}
}
# --------------------------------------------------------------------------------------------------
fnc1_ond_tanh_false_cog_false = {
    'settings': {
        'name':['fnc1_ond_tanh_false_cog_false'],
        'save_type':[enum.SaveType.COLLAPSED],
        'display': False,
    },
    'reps': [x for x in range(10)],
    'operator': {
        'functional_acuity': [0.1],
        'noticing_delay': [1.0, 5.0, 10.0]},
    'experimental_time': [timedelta(minutes=20)],
    'samples': {'samples': [
        [objects.SampleData(0.90, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.85, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.80, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.75, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE),
         objects.SampleData(0.70, enum.SampleImportance.IMPORTANT, enum.SampleType.TAPE)]
    ],},
    'cognative_degredation': [False],
    'instrument': {'tanh_curve': [False]}
}