import random

hits=0
misses=0

max_cycles=10000
stream_shift_time_slice=100
stream_p_shift=0.05
stream_shift_amount=0.01
beam_shift_amount=0.05*stream_shift_amount
stream_shift_low_rand_int=stream_shift_time_slice*stream_p_shift
beam_pos=0.0

operator_response_delay=0 # cycles

def run_stream(show_p=False, tracking_strategy="directed_shift"):
  global hits, misses, beam_pos
  hits = 0
  misses = 0
  stream_pos = 0.0
  beam_pos = 0.0
  allow_response_cycle = 99999999999
  cycle = 1
  while (cycle <= max_cycles) and (abs(stream_pos) < 1.0): # Stop if it hits the wall on either side
    if random.randrange(stream_shift_time_slice) < stream_shift_low_rand_int:
        if 0==random.randrange(2):
            porm=+1
        else:
            porm=-1
        stream_pos=trunc2(stream_pos+(stream_shift_amount*porm))
        allow_response_cycle=cycle+operator_response_delay
    else:
        showpos(stream_pos,beam_pos,show_p)
    if cycle >= allow_response_cycle:
        beam_pos=trunc2(track(stream_pos,beam_pos,tracking_strategy))
    if beam_pos == stream_pos:
        allow_response_cycle=99999999999
    cycle=cycle+1
  print(f'============================================\nHits={hits}, Misses={misses}, Win fraction={hits/(hits+misses)}\n')

def trunc2(n):
  return(int(n*100.0)/100.0)

def track(stream_pos, beam_pos, tracking_strategy):
    if 0==random.randrange(2):
        porm=+1
    else:
        porm=-1
    if tracking_strategy=="static":
        return(beam_pos)
    elif tracking_strategy=="random_shift":
        if random.rangrange(2)==0:
            return beam_pos+(stream_shift_amount*porm)
        else:
            return(beam_pos)
    elif tracking_strategy=="directed_shift":
        if beam_pos==stream_pos:
            return(beam_pos)
        else:
            return(beam_pos+(beam_shift_amount*porm))
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

def run(show_p=False):
  for p in range(10):
      global operator_response_delay
      operator_response_delay=p
      print(f'operator_response_delay={operator_response_delay}')
      run_stream(show_p)

run(False)
