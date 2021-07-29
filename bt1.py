from scipy.stats import sem
import numpy
import random

from datetime import datetime
random.seed(datetime.now())

hits=0
misses=0

# We have a stream (aka. jet) which shifts around in accord with these
# params. The stream_shift_time_slice is a bit obscure. The idea is
# that.

stream_shift_amount=0.1 # Minimal unit of stream shift
p_stream_shift=0.1 # prob. of stream shift per cycle

# And the beam, which is under the control of the operator (or
# automation), which can be shifted in accord with these params:

beam_shift_amount=0.11 # You may want to have more or less fine control of the beam vs. the stream's shiftiness
operator_response_delay=0 # cycles before the operator can respond to a stream shift

max_cycles=10000 # If the beam doesn't hit a wall before this, we cut the run off here.

def run_stream(show_p=False, tracking_strategy="directed_shift"):
  global hits, misses, max_cycles, operator_response_delay
  hits = 0
  misses = 0
  stream_pos = 0.0
  beam_pos = 0.0
  allow_response_cycle = 99999999999
  cycle = 1
  while (cycle <= max_cycles) and (abs(stream_pos) < 1.0): # Stop if it hits the wall on either side
    # Decide if the stream is going to shift:
    if random.random() < p_stream_shift:
        stream_pos=trunc2(stream_pos+(stream_shift_amount*porm()))
        allow_response_cycle=cycle+operator_response_delay
    else:
        showpos(stream_pos,beam_pos,show_p)
    if cycle >= allow_response_cycle:
        beam_pos=trunc2(track(stream_pos,beam_pos,tracking_strategy))
    if beam_pos == stream_pos:
        allow_response_cycle=99999999999
    cycle=cycle+1

# (This is ultra-ugly! There must be a better idiom for this!)
def porm():
  if random.random()<0.5:
    return(+1)
  else:
    return(-1)

# Both the beam and stream are positional to two decimal digits.
def trunc2(n):
  return(int(n*100.0)/100.0)

def track(stream_pos, beam_pos, tracking_strategy):
    if tracking_strategy=="static":
        return(beam_pos)
    elif tracking_strategy=="random_shift":
        if random.randrange(2)==0:
            return beam_pos+(stream_shift_amount*porm())
        else:
            return(beam_pos)
    elif tracking_strategy=="directed_shift":
        if beam_pos==stream_pos:
            return(beam_pos)
        else:
            return(beam_pos+(beam_shift_amount*porm()))
    else:
            raise Exception('In TRACK: Invalid tracking strategy:', tracking_strategy)

show_width=40
show_incr=2.0/show_width

def showpos(stream_pos, beam_pos, show_p):
    global hits,misses
    if show_p:
        print('[',end="")
    beam_shown_p = False
    stream_shown_p = False
    sp = -1.0
    for i in range(show_width):
        miss = False
        sp = sp+show_incr
        # We have to go through the motions here in order to update the stats!
        if stream_shown_p and beam_shown_p: 
            char = " "
        elif (not stream_shown_p) and (not beam_shown_p) and (sp >= stream_pos) and (sp >= beam_pos):
            stream_shown_p=True
            beam_shown_p=True
            hits=hits+1
            hit=True
            char="*"
        elif (not stream_shown_p) and (sp >= stream_pos):
            stream_shown_p=True
            misses=misses+1
            char="|"
        elif (not beam_shown_p) and (sp >= beam_pos):
            beam_shown_p=True
            misses=misses+1
            char="x"
        else:
            char=" "
        if show_p:
            print(f'{char}',end="")
        sp=sp+show_incr
    if show_p:
        print(f'] s:{stream_pos} b:{beam_pos}')

def run(show_p, tracking_strategy):
  global operator_response_delay
  operator_response_delay=0
  n_ord_values_to_try=10
  ord_delta=2
  reps=10
  for p in range(n_ord_values_to_try):
    results = []
    for rep in range(reps):
      #print(f'operator_response_delay={operator_response_delay}')
      run_stream(show_p, tracking_strategy)
      frac = hits/(hits+misses)
      #print(f'============================================\nHits={hits}, Misses={misses}, Win fraction={frac}\n')
      results=results+[frac]
    print(f'@ operator_response_delay={operator_response_delay} fraction mean = {numpy.mean(results)}, stderr = {sem(results)}')
    operator_response_delay=operator_response_delay+ord_delta

run(False,"random_shift") # "static" "random_shift" "directed_shift"
