# Todo:
#    -- Where exact beam|jet match is tested with ==, replace with a more "perceptually" accurate model

from scipy.stats import sem
import numpy
import random
import time
from datetime import datetime, date
random.seed(datetime.now())


class Status:
  hits=0
  misses=0
  msg=""
  
  
class Task:
  default_reps = 20
  default_max_cycles=10000 # If the beam doesn't hit a wall before this, we cut the run off here.
  
  
class Stream:
  # We have a stream (aka. jet) which shifts around in accord with these
  # params. The stream_shift_time_slice is a bit obscure. The idea is
  # that.

  # Warning: The stream shift amount should be an integer multiple of
  # the beam_shift_amount, otherwise the liklihood that they overlap
  # (based on acuity) will be reduced. Usually these will be the same.

  stream_shift_amount=0.01 # Minimal unit of stream shift
  p_stream_shift=0.15 # prob. of stream shift per cycle

  # A crazy ivan is when the stream goes haywire; It should happen very rarely.

  p_crazy_ivan=0.001 # About 0.0001 gives you one/10k
  crazy_ivan_shift_amount=0.2
  n_crazy_ivans = 0 # !!!! YOU DON'T MEAN TO BE CHANGING THIS! IT'S THE P_ ABOVE!!!!

  
class Beam:
  # And the beam, which is under the control of the operator (or
  # automation), which can be shifted in accord with these params:
  beam_shift_amount=0.01 # You may want to have more or less fine control of the beam vs. the stream's shiftiness

  
class Operation:
  # Operator reponse delay combines noticing, attention shifting to button, decision delay, moving to the button, and pressing it
  # (Possibly also need attention shift into the display, but we're leaving that out bcs it can be arbitrarily large)
  noticing_delay = 1 # 100 ms
  decision_delay = 1 # 100 ms -- FFF incorporate differential switch time
  # attention shifting to button has to be computed from where we are and where the buttons are
  # current_eye_position = 0 
  # left_button_position = -2 # we're actually not gonna use these but just use a fixed shift time
  # right_button_position = +2
  switch_button_delay_per_cm = 1 # ms
  button_press_delay = 1 # ms
  button_distance = 0 # cm
  which_button_were_on = "<<" # or ">>"


# There are two different and wholly separate senses of acutity:
# functional_acuity: Whether the beam is physically on target, and physical_acuity: whether the operator
# can SEE that it is! Nb. Whole scale is -1...+1

functional_acuity=0.01
physical_acuity=0.02 # You want this a little larger than the shift so that it allows for near misses

def run_stream(show_f=False):
  global hits, misses, default_max_cycles, n_crazy_ivans, functional_acuity
  hits = 0  #Status
  misses = 0  #Status
  stream_pos = 0.0 
  beam_pos = 0.0 
  allow_response_cycle = 99999999999 
  cycle = 1
  if show_f:
    max_cycles=1000
  else:
    max_cycles=default_max_cycles  #Task
  msg=""
  while (cycle <= max_cycles) and (abs(stream_pos) < 1.0): # Stop if it hits the wall on either side
    # Decide if the stream is going to shift:
    if random.random() < p_crazy_ivan:  #Stream
        n_crazy_ivans = n_crazy_ivans +1  #Stream
        msg=msg+"!!!"  #Status
        stream_pos=round(stream_pos+(crazy_ivan_shift_amount*porm()),4) 
        if allow_response_cycle==99999999999:
          allow_response_cycle=cycle+operator_response_delay(stream_pos,beam_pos)
    elif random.random() < p_stream_shift:
        stream_pos=round(stream_pos+(stream_shift_amount*porm()),4)
        if allow_response_cycle==99999999999:
          allow_response_cycle=cycle+operator_response_delay(stream_pos,beam_pos)
    update_stats(stream_pos,beam_pos)
    if show_f:
        showpos(stream_pos,beam_pos,show_f,cycle)
    if cycle >= allow_response_cycle:
        msg=msg+"<?>"
        # Warning! WWW This used to truncate, but that interacts badly
        # with computer math bcs occassionally you'll end up with
        # 0.6999999 which truncation makes 0.6 instead of 0.7, and it
        # loops out.
        beam_pos=round(track(stream_pos,beam_pos),4)
    if abs(beam_pos-stream_pos)<functional_acuity: 
        allow_response_cycle=99999999999
    cycle=cycle+1

# ORD() uses the current eye position and button distances to decide
# how many cycles it takes to hit the button, which is either short
# (you're there already), or long (you're not), the longer using the
# button distance to delay. It return an integer number of cycles to
# wait before the input arrives.

def operator_response_delay(stream_pos,beam_pos):  #OperationParameters
  global switch_button_delay_per_cm, button_press_delay, button_distance, which_button_were_on, msg
  way = which_way_do_we_need_to_shift(stream_pos, beam_pos)
  if way == which_button_were_on:
    msg=msg+"["+str(button_press_delay+decision_delay+noticing_delay)+"]"
    return(button_press_delay+decision_delay+noticing_delay)
  else:
    which_button_were_on = way
    msg=msg+"["+str((button_distance*switch_button_delay_per_cm)+button_press_delay+decision_delay+noticing_delay)+"]"
    return((button_distance*switch_button_delay_per_cm)+button_press_delay+decision_delay+noticing_delay)
  
def update_stats(stream_pos, beam_pos):
  global physical_acuity, hits, misses
  delta = abs(beam_pos-stream_pos)
  if delta<physical_acuity:
    hits=hits+1
  else:
    misses=misses+1

# (This is ultra-ugly! There must be a better idiom for this!)
def porm():
  if random.random()<0.5:
    return(+1)
  else:
    return(-1)

# Both the beam and stream are positional to two decimal digits.
def trunc2(n):
  return(int(n*100.0)/100.0)

# FFF This should use a model of visual UI-mediated visual acuity,
# rather than just exact operators.

def track(stream_pos, beam_pos):
  global functional_acuity, msg
  which_way = which_way_do_we_need_to_shift(stream_pos, beam_pos)
  if which_way == "none":
    msg=msg+"(FA)"
    return(beam_pos)
  elif which_way == "<<":
    msg=msg+"<<"
    return(beam_pos-beam_shift_amount)
  else:
    msg=msg+">>"
    return(beam_pos+beam_shift_amount)

# Used in various places, returns "<<", ">>", "none"

def which_way_do_we_need_to_shift(stream_pos, beam_pos):  #OperationParameters
  global functional_acuity, msg
  delta = abs(beam_pos-stream_pos)
  if delta<functional_acuity:
    return("none")
  elif beam_pos>stream_pos:
    return("<<")
  else:
    return(">>")

# The display and hit-counting logic are intertwined. Maybe they
# shouldn't be. Pretty straight-forward refactoring would pull them
# apart. Also, the hit scoring is unfortunately, based on whether a *
# would be displayed, which in turn depends on the display increment,
# which is clearly wrong. UUU FFF Clean this up!!

show_width=40
show_incr=2.0/show_width

def showpos(stream_pos, beam_pos, show_f, cycle):
    global show_width, show_incr, msg
    if show_f:
        print(f'{cycle: >6}:[',end="")
    beam_shown_f = False
    stream_shown_f = False
    sp = -1.0
    for i in range(show_width):
        miss = False
        sp = sp+show_incr
        if stream_shown_f and beam_shown_f: 
            char = " "
        # This is a rather obscure way of simply asking if the beam is on the stream:
        elif (not stream_shown_f) and (not beam_shown_f) and (sp >= stream_pos) and (sp >= beam_pos):
            stream_shown_f=True
            beam_shown_f=True
            char="*"
        elif (not stream_shown_f) and (sp >= stream_pos):
            stream_shown_f=True
            char="|"
        elif (not beam_shown_f) and (sp >= beam_pos):
            beam_shown_f=True
            char="x"
        else:
            char=" "
        if show_f:
            print(f'{char}',end="")
    if show_f:
        print(f'] s:{stream_pos} b:{beam_pos} {msg}')
        msg=""

button_distances = 10

def run(show_f): # _f is a flag
  f = open("results/r"+str(time.time())+".tsv", "w")
  global functional_acuity, n_crazy_ivans, default_reps, hits, misses, button_distances, button_distance
  if show_f:
    reps = 1
  else:
    reps=default_reps
  f.write(f"Functional Acuity = {functional_acuity} stream_shift_amount= {stream_shift_amount}, p_stream_shift={p_stream_shift}, beam_shift_amount={beam_shift_amount}, p_crazy_ivan={p_crazy_ivan}\n")
  print(f"Functional Acuity = {functional_acuity} stream_shift_amount= {stream_shift_amount}, p_stream_shift={p_stream_shift}, beam_shift_amount={beam_shift_amount}, p_crazy_ivan={p_crazy_ivan}")
  f.write("operator_response_delay\tmean\tsem\tn_crazy_ivans\n")
  for local_button_distance in range(button_distances):
    button_distance = 4+local_button_distance
    n_crazy_ivans = 0 # These are counted over all reps and then the mean is display at the end
    results = []
    for rep in range(reps):
      run_stream(show_f)
      frac = hits/(hits+misses)
      if show_f:
        print(f"============================================\nHits={hits}, Misses={misses}, Win fraction={frac}\n")
      results=results+[frac]
    print(f"@ button_distance={button_distance} mean hit fraction = {format(numpy.mean(results),'.2f')} [se={format(sem(results),'.2f')}], crazy_ivans/reps = {n_crazy_ivans/reps}")
    f.write(f"{button_distance}\t{format(numpy.mean(results),'.2f')}\t{format(sem(results),'.2f')}\t{n_crazy_ivans/reps}\n")
  f.close()

# If display is true, we only do one rep and only allow it to run 1000 cycles

p_crazy_ivan=0.00 # 0.01 is good
run(False) 

