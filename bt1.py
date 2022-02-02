# Todo:
#    -- Where exact beam|jet match is tested with ==, replace with a more "perceptually" accurate model

from scipy.stats import sem
import numpy
import random
import time
from datetime import datetime, date

# random.seed(datetime.now())
random.seed(a=None, version=2)


class Status:
    hits = 0
    misses = 0
    msg = ""
    n_crazy_ivans = 0  # These are counted over all reps and then the mean is display at the end

    def __init__(self):
        pass

class Beam:
    # And the beam, which is under the control of the operator (or automation), which can be shifted in accord with these params:
    beam_shift_amount = 0.01  # You may want to have more or less fine control of the beam vs. the stream's shiftiness

    # There are two different and wholly separate senses of acuity:
    # physical_acuity: Whether the beam is physically on target, and functional_acuity: whether the operator can SEE that it is!
    # Nb. Whole scale is -1...+1
    physical_acuity = 0.02  # You want this a little larger than the shift so that it allows for near misses


class Operation:
    # Operator reponse delay combines noticing, attention shifting to button, decision delay, moving to the button, and pressing it
    # (Possibly also need attention shift into the display, but we're leaving that out bcs it can be arbitrarily large)
    noticing_delay = 1  # 100 ms
    decision_delay = 1  # 100 ms -- FFF incorporate differential switch time
    # attention shifting to button has to be computed from where we are and where the buttons are
    # current_eye_position = 0
    # left_button_position = -2 # we're actually not gonna use these but just use a fixed shift time
    # right_button_position = +2
    switch_button_delay_per_cm = 1  # ms
    button_press_delay = 1  # ms
    button_distance = 0  # cm
    which_button_were_on = "<<"  # or ">>"
    functional_acuity = 0.01

    def __init__(self, x, y):
        self.par_stream_pos = x
        self.par_beam_pos = y

    # Used in various places, returns "<<", ">>", "none"
    def which_way_do_we_need_to_shift(self):
        delta = abs(self.par_beam_pos - self.par_stream_pos)
        if delta < self.functional_acuity:
            return "none"
        elif self.par_beam_pos > self.par_stream_pos:
            return "<<"
        else:
            return ">>"

    # operator_response_delay() uses the current eye position and button distances to decide
    # how many cycles it takes to hit the button, which is either short
    # (you're there already), or long (you're not), the longer using the
    # button distance to delay. It return an integer number of cycles to
    # wait before the input arrives.
    def operator_response_delay(self):
        way = self.which_way_do_we_need_to_shift()
        if way == self.which_button_were_on:
            Status.msg = Status.msg + "[" + str(
                self.button_press_delay + self.decision_delay + self.noticing_delay) + "]"
            return self.button_press_delay + self.decision_delay + self.noticing_delay
        else:
            self.which_button_were_on = way
            Status.msg = Status.msg + "[" + str((self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay) + "]"
            return (self.button_distance * self.switch_button_delay_per_cm) + self.button_press_delay + self.decision_delay + self.noticing_delay


class Stream:
    # We have a stream (aka. jet) which shifts around in accord with these params.
    # The stream_shift_time_slice is a bit obscure. The idea is that.

    # Warning: The stream shift amount should be an integer multiple of the beam_shift_amount, otherwise
    # the likelihood that they overlap (based on acuity) will be reduced. Usually these will be the same.

    stream_shift_amount = 0.01  # Minimal unit of stream shift
    p_stream_shift = 0.15  # prob. of stream shift per cycle

    # A crazy ivan is when the stream goes haywire; It should happen very rarely.
    p_crazy_ivan = 0.01  # About 0.0001 gives you one/10k
    crazy_ivan_shift_amount = round(random.uniform(0.1, 0.2), 2)    # 0.2

    default_max_cycles = 10000  # If the beam doesn't hit a wall before this, we cut the run off here.
    stream_pos = 0.0
    beam_pos = 0.0
    allow_response_cycle = 99999999999
    cycle = 1

    def run_stream(self, show_f):
        Status.hits = 0
        Status.misses = 0
        Status.msg = ""

        if show_f:
            max_cycles = 1000
        else:
            max_cycles = self.default_max_cycles

        while (self.cycle <= max_cycles) and (abs(self.stream_pos) < 1.0):  # Stop if it hits the wall on either side
            # Decide if the stream is going to shift:
            if random.random() < self.p_crazy_ivan:
                Status.n_crazy_ivans = Status.n_crazy_ivans + 1
                Status.msg = Status.msg + "!!!"
                # If response target has not already been set, it will be 99999999999.
                # If it has been set, it will be whatever number it is (e.g., now+20)
                # Only change the response cycle if it has not been set (i.e., 99999999999)
                self.stream_pos = round(self.stream_pos + (
                        self.crazy_ivan_shift_amount * random.choice([i for i in range(-1, 2) if i not in [0]])), 4)
                if self.allow_response_cycle == 99999999999:
                    o = Operation(self.stream_pos, self.beam_pos)
                    self.allow_response_cycle = self.cycle + o.operator_response_delay()
            elif random.random() < self.p_stream_shift:
                self.stream_pos = round(self.stream_pos + (
                        self.stream_shift_amount * random.choice([i for i in range(-1, 2) if i not in [0]])), 4)
                if self.allow_response_cycle == 99999999999:
                    o = Operation(self.stream_pos, self.beam_pos)
                    self.allow_response_cycle = self.cycle + o.operator_response_delay()
            self.update_stats()
            if show_f:
                self.show_pos(show_f)
            if self.cycle >= self.allow_response_cycle:
                Status.msg = Status.msg + "<?>"
                # Warning! WWW This used to truncate, but that interacts badly
                # with computer math bcs occassionally you'll end up with
                # 0.6999999 which truncation makes 0.6 instead of 0.7, and it
                # loops out.
                self.beam_pos = round(self.track(self.stream_pos, self.beam_pos), 4)
            if abs(self.beam_pos - self.stream_pos) < Operation.functional_acuity:
                self.allow_response_cycle = 99999999999
            self.cycle = self.cycle + 1

    def update_stats(self):
        delta = abs(self.beam_pos - self.stream_pos)
        if delta < Beam.physical_acuity:
            Status.hits = Status.hits + 1
        else:
            Status.misses = Status.misses + 1

    def show_pos(self, if_show):
        # The display and hit-counting logic are intertwined. Maybe they shouldn't be.
        # Pretty straight-forward refactoring would pull them apart. Also, the hit scoring is unfortunately,
        # based on whether a * would be displayed, which in turn depends on the display increment, which is clearly wrong. UUU FFF Clean this up!!
        show_width = 40
        show_incr = 2.0 / show_width

        if if_show:
            print(f'{self.cycle: >6}:[', end="")

        beam_shown_f = False
        stream_shown_f = False
        sp = -1.0
        for i in range(show_width):
            # miss = False
            sp = sp + show_incr
            if stream_shown_f and beam_shown_f:
                char = " "
            # This is a rather obscure way of simply asking if the beam is on the stream:
            elif (not stream_shown_f) and (not beam_shown_f) and (sp >= self.stream_pos) and (sp >= self.beam_pos):
                stream_shown_f = True
                beam_shown_f = True
                char = "*"
            elif (not stream_shown_f) and (sp >= self.stream_pos):
                stream_shown_f = True
                char = "|"
            elif (not beam_shown_f) and (sp >= self.beam_pos):
                beam_shown_f = True
                char = "x"
            else:
                char = " "
            if if_show:
                print(f'{char}', end="")
        if if_show:
            print(f'] s:{self.stream_pos} b:{self.beam_pos} {Status.msg}')
            Status.msg = ""

    # FFF This should use a model of visual UI-mediated visual acuity,
    # rather than just exact operators.

    def track(self, stream_pos, beam_pos):
        o = Operation(stream_pos, beam_pos)
        which_way = o.which_way_do_we_need_to_shift()
        if which_way == "none":
            Status.msg = Status.msg + "(FA)"
            return beam_pos
        elif which_way == "<<":
            Status.msg = Status.msg + "<<"
            return beam_pos - Beam.beam_shift_amount
        else:
            Status.msg = Status.msg + ">>"
            return beam_pos + Beam.beam_shift_amount

def run(show_f):  # _f is a flag
    default_reps = 20
    button_distances = 10

    f = open("results/r" + str(time.time()) + ".tsv", "w")
    if show_f:
        reps = 1
    else:
        reps = default_reps
    f.write(
        f"Functional Acuity = {Operation.functional_acuity} stream_shift_amount= {Stream.stream_shift_amount}, "
        f"p_stream_shift={Stream.p_stream_shift}, beam_shift_amount={Beam.beam_shift_amount}, p_crazy_ivan={Stream.p_crazy_ivan}\n")
    print(
        f"Functional Acuity = {Operation.functional_acuity} stream_shift_amount= {Stream.stream_shift_amount}, "
        f"p_stream_shift={Stream.p_stream_shift}, beam_shift_amount={Beam.beam_shift_amount}, p_crazy_ivan={Stream.p_crazy_ivan}")
    f.write("operator_response_delay\tmean\tsem\tn_crazy_ivans\n")

    for local_button_distance in range(button_distances):
        Operation.button_distance = 4 + local_button_distance
        Status.n_crazy_ivans = 0
        results = []
        for rep in range(reps):
            s = Stream()
            s.run_stream(show_f)
            frac = Status.hits / (Status.hits + Status.misses)
            if show_f:
                print(
                    f"============================================\nHits={Status.hits}, Misses={Status.misses}, Win fraction={frac}\n")
            results = results + [frac]
        print(
            f"@ button_distance={Operation.button_distance} mean hit fraction = "
            f"{format(numpy.mean(results), '.2f')} [se={format(sem(results), '.2f')}], crazy_ivans/reps = {Status.n_crazy_ivans / reps}")
        f.write(
            f"{Operation.button_distance}\t{format(numpy.mean(results), '.2f')}\t{format(sem(results), '.2f')}\t{Status.n_crazy_ivans / reps}\n")
    f.close()


# If display is true, we only do one rep and only allow it to run 1000 cycles

# p_crazy_ivan = 0.00  # 0.01 is good
run(False)
