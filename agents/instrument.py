"""
Instrument
"""

from enum import Enum
import random
import agent

class InstrumentType(Enum):
    """Enum to mark the different hutches"""
    CXI = "CXI"

class Instrument:
    """Instrument Parent Class"""
    instrument_type = ""
    status = {
        "hits": 0,
        "misses": 0,
        "msg": "",
        "n_crazy_ivans": 0,  # These are counted over all reps and then the mean is display at the end
    }
    beam = {
        # And the beam, which is under the control of the operator (or automation),
        # which can be shifted in accord with these params:
        "beam_shift_amount": 0.01,  # You may want to have more or less fine control of the beam vs. the stream's shiftiness

        # There are two different and wholly separate senses of acuity:
        # physical_acuity: Whether the beam is physically on target, and functional_acuity:
        # whether the operator can SEE that it is!
        # Nb. Whole scale is -1...+1
        "physical_acuity": 0.02,  # You want this a little larger than the shift so that it allows for near misses
    }
    stream = {
        # We have a stream (aka. jet) which shifts around in accord with these params.
        # The stream_shift_time_slice is a bit obscure. The idea is that.

        # Warning: The stream shift amount should be an integer multiple of the beam_shift_amount, otherwise
        # the likelihood that they overlap (based on acuity) will be reduced. Usually these will be the same.

        "stream_shift_amount": 0.01,  # Minimal unit of stream shift
        "p_stream_shift": 0.15,  # prob. of stream shift per cycle

        # A crazy ivan is when the stream goes haywire; It should happen very rarely.
        "p_crazy_ivan": 0.01,  # About 0.0001 gives you one/10k
        "crazy_ivan_shift_amount": round(random.uniform(0.1, 0.2), 2),  # 0.2

        "default_max_cycles": 10000,  # If the beam doesn't hit a wall before this, we cut the run off here.
        "stream_pos": 0.0,
        "beam_pos": 0.0,
        "allow_response_cycle": 99999999999,
        "cycle": 1,
    }

    def __init__(self, instrument_type):
        self.instrument_type = instrument_type

    def run_stream(self, show_f):
        """Run the stream"""
        self.status["hits"] = 0
        self.status["misses"] = 0
        self.status["msg"] = ""

        if show_f:
            max_cycles = 1000
        else:
            max_cycles = self.stream["default_max_cycles"]

        while (self.stream["cycle"] <= max_cycles) and (abs(self.stream["stream_pos"]) < 1.0):  # Stop if it hits the wall on either side
            # Decide if the stream is going to shift:
            if random.random() < self.stream["p_crazy_ivan"]:
                self.status["n_crazy_ivans"] = self.status["n_crazy_ivans"] + 1
                self.status["msg"] = self.status["msg"] + "!!!"
                # If response target has not already been set, it will be 99999999999.
                # If it has been set, it will be whatever number it is (e.g., now+20)
                # Only change the response cycle if it has not been set (i.e., 99999999999)
                self.stream["stream_pos"] = round(self.stream["stream_pos"] + (
                        self.stream["crazy_ivan_shift_amount"] * random.choice([i for i in range(-1, 2) if i not in [0]])), 4)
                if self.stream["allow_response_cycle"] == 99999999999:
                    # o = operator(self.stream["stream_pos"], self.stream["beam_pos"])
                    o = agent.Operator(self.stream["stream_pos"], self.stream["beam_pos"])
                    self.stream["allow_response_cycle"] = self.stream["cycle"] + o.operator_response_delay(self)
            elif random.random() < self.stream["p_stream_shift"]:
                self.stream["stream_pos"] = round(self.stream["stream_pos"] + (
                        self.stream["stream_shift_amount"] * random.choice([i for i in range(-1, 2) if i not in [0]])), 4)
                if self.stream["allow_response_cycle"] == 99999999999:
                    o = agent.Operator(self.stream["stream_pos"], self.stream["beam_pos"])
                    self.stream["allow_response_cycle"] = self.stream["cycle"] + o.operator_response_delay(self)
            self.update_stats()
            if show_f:
                self.show_pos(show_f)
            if self.stream["cycle"] >= self.stream["allow_response_cycle"]:
                self.status["msg"] = self.status["msg"] + "<?>"
                # Warning! WWW This used to truncate, but that interacts badly with computer math
                # bcs occassionally you'll end up with 0.6999999 which truncation makes 0.6 instead of 0.7,
                # and it loops out.
                self.stream["beam_pos"] = round(self.track(self.stream_pos, self.beam_pos), 4)
            if abs(self.stream["beam_pos"] - self.stream["stream_pos"]) < agent.Operator.functional_acuity:
                self.stream["allow_response_cycle"] = 99999999999
            self.stream["cycle"] = self.stream["cycle"] + 1

    def update_stats(self):
        """Update Status"""
        delta = abs(self.stream["beam_pos"] - self.stream["stream_pos"])
        if delta < self.beam["physical_acuity"]:
            self.status["hits"] = self.status["hits"] + 1
        else:
            self.status["misses"] = self.status["misses"] + 1

    def show_pos(self, if_show):
        """The display and hit-counting logic are intertwined. Maybe they shouldn't be.
        Pretty straight-forward refactoring would pull them apart. Also, the hit scoring is unfortunately,
        based on whether a * would be displayed, which in turn depends on the display increment,
        which is clearly wrong. UUU FFF Clean this up!!"""
        show_width = 40
        show_incr = 2.0 / show_width

        if if_show:
            print(f'{self.stream["cycle"]: >6}:[', end="")

        beam_shown_f = False
        stream_shown_f = False
        sp = -1.0
        for _ in range(show_width):
            # miss = False
            sp = sp + show_incr
            if stream_shown_f and beam_shown_f:
                char = " "
            # This is a rather obscure way of simply asking if the beam is on the stream:
            elif (not stream_shown_f) and (not beam_shown_f) and (sp >= self.stream["stream_pos"]) and (sp >= self.stream["beam_pos"]):
                stream_shown_f = True
                beam_shown_f = True
                char = "*"
            elif (not stream_shown_f) and (sp >= self.stream["stream_pos"]):
                stream_shown_f = True
                char = "|"
            elif (not beam_shown_f) and (sp >= self.stream["beam_pos"]):
                beam_shown_f = True
                char = "x"
            else:
                char = " "
            if if_show:
                print(f'{char}', end="")
        if if_show:
            print(f'] s:{self.stream["stream_pos"]} b:{self.stream["beam_pos"]} {self.stream["msg"]}')
            self.status["msg"] = ""

    # FFF This should use a model of visual UI-mediated visual acuity,
    # rather than just exact operators.

    def track(self, stream_pos, beam_pos):
        """Track"""
        o = agent.Operator(stream_pos, beam_pos)
        which_way = o.which_way_do_we_need_to_shift()
        if which_way == "none":
            self.status["msg"] = self.status["msg"] + "(FA)"
            return beam_pos
        elif which_way == "<<":
            self.status["msg"] = self.status["msg"] + "<<"
            return beam_pos - self.beam["beam_shift_amount"]
        else:
            self.status["msg"] = self.status["msg"] + ">>"
            return beam_pos + self.beam["beam_shift_amount"]

class CXI(Instrument):
    """CXI"""
    def __init__(self):
        super().__init__(InstrumentType.CXI)
