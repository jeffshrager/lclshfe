"""Functions Unit Tests"""
import sim.model.functions as functions
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.enums as enum

# class TestClass:
#     """test"""
#     def test_calculate_roi(self):
#         """test"""
#         Test = {
#             'settings': {'name':['over180'],'save_type':[enum.SaveType.COLLAPSED], 'cycle_sleep_time': 0.0,},
#             'reps': [x for x in range(1)],
#             'operator': {'functional_acuity': [100.0]},
#             'samples': {'samples': [
#                 objects.SampleData(0.90, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE),
#                 objects.SampleData(0.85, enum.SampleImportance.UNIMPORTANT, enum.SampleType.TAPE)
#             ],},
#             'cognative_degredation': [False],
#             'instrument': {'tanh_curve': [False]}
#         }
#         test_AMI:objects.AMI = objects.AMI(setting.Config(Test))
#         test_AMI.samples[0].compleated = True
#         assert function.calculate_roi(test_AMI) == 0.5

class TestConfigFunctions:
    """test"""

    # def setup_class(self):
    #     print("setup_class called once for the class")

    # def teardown_class(self):
    #     print("teardown_class called once for the class")

    # def setup_method(self):
    #     print("  setup_method called for every method")

    # def teardown_method(self):
    #     print("  teardown_method called for every method")

    def test_cartesian_product(self):
        """Cartesian Product"""
        test = {
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        }
        result = [{'a': 1, 'b': 4},
                  {'a': 1, 'b': 5},
                  {'a': 1, 'b': 6},
                  {'a': 2, 'b': 4},
                  {'a': 2, 'b': 5},
                  {'a': 2, 'b': 6},
                  {'a': 3, 'b': 4},
                  {'a': 3, 'b': 5},
                  {'a': 3, 'b': 6}]
        assert list(functions.cartesian_product(test)) == result
    
    def test_sort_combinations(self):
        """Sort Combinations"""
        assert functions.sort_combinations()
