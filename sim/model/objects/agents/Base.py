"""The agents represented in the model

In the model, there are three primary agents responsible for the operation of the
instrument. The Operator is directly in controll of the beamline of the instrument.
The Data Analyst observes the AMI and determines when the data is good enough to
stop the run as well as gives updates to the Experiment Manager when there is a problem.
The Experiment Manager is responsible for the overall control of the experiment and
communicates with both the Operator and the Data Analyst to understand the state of 
the Experiment as well as make changes at a high level to improve the quality and
efficiency of the experiment.

  Typical usage example:

  DA = DataAnalyst()
  DA.check_if_enough_data_to_analyse(context)

  bar = foo.FunctionBar()
"""
from datetime import timedelta
import sim.model.enums as enums
import sim.model.functions as functions
import sim.model.objects as objects

class Person:
    """The base agent class

    TODO: Add system stability affect attention level
    If the system is unstable attention should increase, if system is stable attention
    will decrease, We know what the status of the system is use this to callibrate
    the system, begining they will be focused, not exausted yet, 4pm things go
    wrong and they are tired

    TODO: Analygous attentional properties will attach to data analyst
    Hot vs cold cognition, hot rappid makes more mistakes, cold slower more accurate
    Eventually check when worrying check all the time, when not check once in a while
    TODO: Attention/ exaustion/ focus controlls for ever person
    TODO _: Add Attention
    TODO: begining they will be focused, not exausted yet, 4pm things go wrong and they are tired

    1.0 / 0.002 = 8.3, total level of energy / minutes = 8.3 total hours of energy

    Attributes:
        energy_degradation: float, the amount of energy lost each cycle
        agent_type: enums.AgentType, the type of agent
        cognitive_temperature: float, the level of cognition
        cogtemp_curve: float, the curve of cognition
        attention_meter: float, the level of attention
        previous_check: timedelta, the time of the last check
        noticing_delay: float, the delay of noticing
        decision_delay: float, the delay of decision making
        functional_acuity: float, the level of functional acuity
    """
    # attention_meter:float = None
    # previous_check:timedelta = None
    def __init__(self, agent_type:enums.AgentType):
        self.energy_degradation:float = 0.002
        self.agent_type:enums.AgentType = agent_type
        self.cognative_temperature:float = 1.0
        self.cogtemp_curve:float = 0.0
        self.attention_meter:float = 1.0
        self.previous_check:timedelta = timedelta(0)
        self.noticing_delay:float = 1.0  # 100 ms
        self.decision_delay:float = 1.0  # 100 ms -- FFF incorporate differential switch time
        self.functional_acuity:float = 0.01

    def get_energy(self):
        """get the level of energy"""
        return self.cognative_temperature

    def get_attention(self):
        """get the level of attention"""
        return self.cogtemp_curve

    def update(self, context:objects.Context):
        """Calculate agents attention and focus each cycle

        Goes through each sample and determines if they all were compleated.
        If they were, the ROI would be 100%, if not the roi percent
        is calculated.

        Args:
            ami: an AMI object which contains all the data and the state
            that the sample is in.

        Returns:
            A string that is the ROI of the experiment. In percent.
        """
        # TODO _: energy degredation on a curve
        # TODO: coupled also on a curve
        if context['cognative_degredation']:
            delta:timedelta = context.current_time - self.previous_check
            if delta >= timedelta(minutes=1):
                self.cogtemp_curve = functions.clamp(self.cogtemp_curve + self.energy_degradation, 0.0, 1.0)
                self.cognative_temperature = functions.clamp(functions.cognative_temperature_curve(self.cogtemp_curve), 0.01, 1.0)
                self.previous_check = context.current_time
            self.noticing_delay = 1 + (1 - self.cognative_temperature)
            self.decision_delay = 1 + (1 - self.cognative_temperature)

class RemoteUser(Person):
    """TODO the remote user

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # FFF: Who is communicating with the remote user from inside the hutch
    def __init__(self):
        super().__init__(enums.AgentType.RU)

class ACROperator(Person):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    # FFF: who is the person talking to the ACR operator in
    # the situation that the beam dissapears or has problems
    # FFF: or they want to change the photon energy level
    def __init__(self):
        super().__init__(enums.AgentType.ACR)
