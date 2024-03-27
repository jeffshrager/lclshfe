"""Functions Unit Tests"""
import sim.model.objects as objects
import sim.model.settings as settings
import sim.model.enums as enums

class TestAMI:
    """test"""

    # def setup_class(self):
    #     print("setup_class called once for the class")

    # def teardown_class(self):
    #     print("teardown_class called once for the class")

    # def setup_method(self):
    #     print("  setup_method called for every method")

    # def teardown_method(self):
    #     print("  teardown_method called for every method")

    def test_get_mean(self):
        """Cartesian Product"""
        test_ami:objects.AMI = objects.AMI(settings.Config({}))
        test_ami.samples[0].data = [objects.DataPoint(0.5, 0.5), objects.DataPoint(1.0, 1.0)]
        assert test_ami.get_mean() == [0.75]
        test_ami.samples.append(objects.SampleData(0.8,
        enums.SampleImportance.UNIMPORTANT, enums.SampleType.OTHER))
        test_ami.samples[1].data = [objects.DataPoint(1.0, 1.0), objects.DataPoint(2.0, 2.0)]
        assert test_ami.get_mean() == [0.75, 1.5]

    def test_get_stdev(self):
        """Cartesian Product"""
        test_ami:objects.AMI = objects.AMI(settings.Config({}))
        test_ami.samples[0].data = [objects.DataPoint(0.5, 0.5), objects.DataPoint(1.0, 1.0)]
        assert test_ami.get_stdev() == [0.25]
        test_ami.samples.append(objects.SampleData(0.8,
        enums.SampleImportance.UNIMPORTANT, enums.SampleType.OTHER))
        test_ami.samples[1].data = [objects.DataPoint(1.0, 1.0), objects.DataPoint(2.0, 2.0)]
        assert test_ami.get_stdev() == [0.25, 0.5]

    def test_get_err(self):
        """Cartesian Product"""
        test_ami:objects.AMI = objects.AMI(settings.Config({}))
        test_ami.samples[0].data = [objects.DataPoint(0.5, 0.5), objects.DataPoint(1.0, 1.0)]
        assert test_ami.get_err() == [0.17677669529663687]
        test_ami.samples.append(objects.SampleData(0.8,
        enums.SampleImportance.UNIMPORTANT, enums.SampleType.OTHER))
        test_ami.samples[1].data = [objects.DataPoint(1.0, 1.0), objects.DataPoint(2.0, 2.0)]
        assert test_ami.get_err() == [0.17677669529663687, 0.35355339059327373]

    def test_get_var(self):
        """Cartesian Product"""
        test_ami:objects.AMI = objects.AMI(settings.Config({}))
        test_ami.samples[0].data = [objects.DataPoint(0.5, 0.5), objects.DataPoint(1.0, 1.0)]
        assert test_ami.get_var() == [0.0625]
        test_ami.samples.append(objects.SampleData(0.8,
        enums.SampleImportance.UNIMPORTANT, enums.SampleType.OTHER))
        test_ami.samples[1].data = [objects.DataPoint(1.0, 1.0), objects.DataPoint(2.0, 2.0)]
        assert test_ami.get_var() == [0.0625, 0.25]
