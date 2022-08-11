"""Functions Unit Tests"""
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.enums as enums

class TestConfig:
    """test"""

    def test_get_item(self):
        """Cartesian Product"""
        test_config:settings.Config = settings.Config({})
        assert test_config['settings']['name'] == ['default_run']
    
    def test_make_dirs(self):
        """Cartesian Product"""
        test_config:settings.Config = settings.Config({})
        assert test_config['settings']['name'] == ['default_run'] 
    
    def test_str(self):
        """Cartesian Product"""
        test_config:settings.Config = settings.Config({})
        print(str(test_config))
        assert str(test_config)[0:7] == "setting"
