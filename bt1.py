# Todo:
#    -- Where exact beam|jet match is tested with ==, replace with a more "perceptually" accurate model
#    -- Calibate cycles (esp. operator_response_delay) to human reponse times (e.g., 1 cycle == 100ms or whatever)

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

# Warning: The stream shift amount should be an integer multiple of
# the beam_shift_amount, otherwise the liklihood that they overlap
# (based on acuity) will be reduced. Usually these will be the same.

stream_shift_amount=0.01 # Minimal unit of stream shift
p_stream_shift=0.95 # prob. of stream shift per cycle

# A crazy ivan is when the stream goes haywire; It should happen very rarely.

p_crazy_ivan=0.001
crazy_ivan_shift_amount=0.2
n_crazy_ivans = 0

# And the beam, which is under the control of the operator (or
# automation), which can be shifted in accord with these params:

beam_shift_amount=0.025 # You may want to have more or less fine control of the beam vs. the stream's shiftiness
operator_response_delay=0 # cycles before the operator can respond to a stream shift

max_cycles=10000 # If the beam doesn't hit a wall before this, we cut the run off here.

acuity=0.01 # The whole scale is -1...+1

def run_stream(show_p=False, tracking_strategy="directed"):
  global hits, misses, max_cycles, operator_response_delay, n_crazy_ivans
  hits = 0
  misses = 0
  stream_pos = 0.0
  beam_pos = 0.0
  allow_response_cycle = 99999999999
  cycle = 1
  while (cycle <= max_cycles) and (abs(stream_pos) < 1.0): # Stop if it hits the wall on either side
    # Decide if the stream is going to shift:
    if random.random() < p_crazy_ivan:
        n_crazy_ivans = n_crazy_ivans +1
        stream_pos=trunc2(stream_pos+(crazy_ivan_shift_amount*porm()))
        if allow_response_cycle==99999999999:
          allow_response_cycle=cycle+operator_response_delay
    elif random.random() < p_stream_shift:
        stream_pos=trunc2(stream_pos+(stream_shift_amount*porm()))
        if allow_response_cycle==99999999999:
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

# FFF This should use a model of visual UI-mediated visual acuity, rather than just exact operators.

def track(stream_pos, beam_pos, tracking_strategy):
    if tracking_strategy=="static":
      return(beam_pos)
    elif tracking_strategy=="random":
      return(beam_pos+(stream_shift_amount*porm()))
    elif tracking_strategy=="directed":
      delta = abs(beam_pos-stream_pos)
      if delta<acuity:
        return(beam_pos)
      # ??? Since the acuity relates to the equality, I don't think we
      # need it in the > and < tests -- they are protected by the ==
      # test ???
      elif beam_pos>stream_pos:
        return(beam_pos-beam_shift_amount)
      else:
        return(beam_pos+beam_shift_amount)
    else:
      raise Exception('In TRACK: Invalid tracking strategy:', tracking_strategy)

# The display and hit-counting logic are intertwined. Maybe they
# shouldn't be. Pretty straight-forward refactoring would pull them
# apart. Also, the hit scoring is unfortunately, based on whether a *
# would be displayed, which in turn depends on the display increment,
# which is clearly wrong. UUU FFF Clean this up!!

show_width=40
show_incr=2.0/show_width

def showpos(stream_pos, beam_pos, show_p):
    global hits,misses, show_width, show_incr
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
            char = ">"
        # This is a rather obscure way of simply asking if the beam is on the stream:
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
            char="<"
        if show_p:
            print(f'{char}',end="")
        #sp=sp+show_incr
    if show_p:
        print(f'] s:{stream_pos} b:{beam_pos}')

def run(show_p, tracking_strategy):
  global operator_response_delay, acuity, n_crazy_ivans
  operator_response_delay=0 # !!! If you're testing the display code, you'll want to set this to 2 or greater !!!
  n_ord_values_to_try=40
  ord_delta=1
  reps=20
  print(f'Tracking strategy is {tracking_strategy}, Acuity = {acuity} stream_shift_amount= {stream_shift_amount}, p_stream_shift={p_stream_shift}, beam_shift_amount={beam_shift_amount}')
  for p in range(n_ord_values_to_try):
    n_crazy_ivans = 0 # These are counted over all reps and then the mean is display at the end
    results = []
    for rep in range(reps):
      #print(f'operator_response_delay={operator_response_delay}')
      run_stream(show_p, tracking_strategy)
      frac = hits/(hits+misses)
      if show_p:
        print(f'============================================\nHits={hits}, Misses={misses}, Win fraction={frac}\n')
      results=results+[frac]
    print(f'@ operator_response_delay={operator_response_delay} fraction mean = {numpy.mean(results)}, stderr = {sem(results)}, mean n_crazy_ivans = {n_crazy_ivans/reps}')
    operator_response_delay=operator_response_delay+ord_delta

run(False,"directed") # "static" "random" "directed"
#run(False,"static") # "static" "random" "directed"
#run(False,"random") # "static" "random" "directed"
