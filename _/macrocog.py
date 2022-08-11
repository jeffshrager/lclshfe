# Correctly estimate error_threshold time savings per pq (currently set at 300)

# This is intended to model end-to-end decision-making for an LCLS
# experiment.

# Samples have a performance quality (pq) and an importance. These are
# anti-correlated; the important samples have the worst (lowest) pq.

from functools import reduce
from numpy import arange
from random import randint


def showsamples(samples):
    [print(str(sample)) for sample in samples]

n_samples_at_each_importance = 5
sample_pq_delta = 0.025
n_importance_levels = 2
pqs = [0.9-delta for delta in arange(0.0,((n_importance_levels*n_samples_at_each_importance)*sample_pq_delta),sample_pq_delta)]
samples = [{"importance":1+importance} for importance in range(n_importance_levels)
           for ns in range(n_samples_at_each_importance)]
n_samples = len(samples)
time_delta=(3600-300)/(len(pqs)-1)
# Given a sample, we (supposedly) start collecting samples. Now, this
# doesn't actually collect samples and do all the AMI junk. All it
# does is uses the pq to estimate how long it's going to take to reach
# the target err by selection from a table that just associates pqs
# with a range of times (in seconds) from about 5 minutes (300s) for
# the highest pq to around 3600s (60 minutes) for the worst.
estimated_run_lengths = [round(t) for t in arange(300,len(pqs)*time_delta,time_delta)]
# Now spread the pqs across the samples
for (sample,pq,estimated_run_length) in zip(samples, pqs, estimated_run_lengths):
    sample["pq"]=pq
    sample["estimated_run_length"]=estimated_run_length
showsamples(samples)
cumulative_estimated_run_length = reduce(lambda a, b: a + b, [s["estimated_run_length"] for s in samples])
print("cumulative_estimated_run_length = "+str(cumulative_estimated_run_length))

# The general plan is to run the less important samples first, until
# we get a sense of how long this is going to take for a given sample
# at a given pq. Conveniently, the samples are created in importance
# order (although FFF we probably shouldn't depends upon that!)  We
# supposedly continue to sample until we reach the target error
# threshold, or run out of time (or predict that we're going to run
# out of time based on data taking so far.) The times that the samples
# are going to take is already calculated in (and, !!!, in fact we
# don't even actually need the pqs, as it turns out, except for show).

error_threshold = 0.001

# Overall timings
n_shifts = 1
shift_length_seconds = 12 * 60 * 60 # 12 hour shifts

# So the master loop runs through the samples in order (which is
# conveniently in unimportance-order -- that is, the least important
# sample, that also has the best pq is first, and the most import
# sample, with the worst pq is last, and that's the order we want to
# do these, but we don't want to run out of time.

# So what we do is take the samples one at a time, run them, and then
# estimate (actually, just read off) the time is takes plus some
# noise, then we use that to estimate the whole run, and adjust the
# acceptable error accordingly.

def run():
    global shift_length_seconds, n_shifts, n_samples, error_threshold
    # FFF For the moment we don't consider shift changes FFF
    #total_available_time = shift_length_seconds * n_shifts 
    total_available_time = cumulative_estimated_run_length
    print("total_available_time = "+str(total_available_time))
    cumulative_time_used = 0
    global samples
    runs = []
    seconds_saved_from_error_threshold_001_delta = False
    n_samples_left=len(samples)
    for nth_sample in range(n_samples_left):
        sample=samples[nth_sample]
        n_samples_left-=1
        print("\nSAMPLE #"+str(nth_sample)+":"+str(sample))
        print("  error_threshold = "+str(error_threshold))
        srl = sample["estimated_run_length"]
        # *** III !!! The error_threshold has to be increased into
        # this using the same estimate that's used in
        # recalibrate_error_threshold(...)
        uncorrected_run_length = srl + randint(1,int(0.3*srl))-int(0.15*srl) 
        print("uncorrected_run_length (including noise)="+str(uncorrected_run_length))
        # Correct for error threshold delta
        run_length_correction_from_error_threshold=0
        if seconds_saved_from_error_threshold_001_delta: # Will be False if not yet set
            run_length_correction_from_error_threshold=round(seconds_saved_from_error_threshold_001_delta*(error_threshold-0.001)*1000)
        print("run_length_correction_from_error_threshold="+str(run_length_correction_from_error_threshold))
        actual_run_length=uncorrected_run_length-run_length_correction_from_error_threshold
        print("--> actual run length (including error threshold correction)= "+str(actual_run_length))
        cumulative_time_used += actual_run_length
        sample["actual_run_length"]=actual_run_length
        print("cumulative_time_used = "+str(cumulative_time_used)+" [projection(cumulative_estimated_run_length):"+str(cumulative_estimated_run_length))
        runs=[[sample,actual_run_length]]+runs
        # Once we have two samples we can start estimating the amount
        # of time each pq delta costs. For the moment we just use the
        # last two to figure this. This isn't actually unreasonable
        # given instrument float.
        if (len(runs)>1 and nth_sample<n_samples-1):
            this_run_pq = runs[0][0]["pq"]
            this_run_length = runs[0][1]
            last_run_pq = runs[1][0]["pq"]
            last_run_length = runs[1][1]
            pq_delta = round(last_run_pq - this_run_pq,5)
            print(" pq_delta="+str(pq_delta))
            run_length_delta = abs(last_run_length - this_run_length)
            print(" run_length_delta="+str(run_length_delta))
            estimated_delta_seconds_per_pq = round(abs(run_length_delta/pq_delta))
            print(" estimated_delta_seconds_per_pq="+str(estimated_delta_seconds_per_pq))
            # Okay, so now we think we know how long per pq we have
            # (and nb. we're using only the latest run data because
            # that's the best estimate of the general state of things,
            # rather than, for example, incorporating information from
            # previous runs, which wouldn't estimate the current state
            # of experience and of the machine and instrument).  So,
            # anyway, now we use this seconds/pq to estimate how long
            # the whole rest of the run is going to take.
            print(" n_samples_left = "+str(n_samples_left))
            # This assumes that the delta pq is fixed (@0.025) FFF Someday calculate it! FFF
            estimated_run_length_map = [actual_run_length + round((((1+s)*pq_delta) * estimated_delta_seconds_per_pq)) for s in range(n_samples_left)]
            print(" estimated_run_length_map = "+str(estimated_run_length_map))
            # We replace the sample estimates with the estmates we just made (FFF Nb. PQs are wrongly assumed = 0.025! FFF)
            for (sample,estimated_run_length) in zip([samples[1+n+nth_sample] for n in range(n_samples_left)],estimated_run_length_map):
                sample["estimated_run_length"]=estimated_run_length
            print("New sample set (revised estimated_run_lengths):")
            showsamples(samples)
            # Now figure out if we're going to run out of time
            estimated_total_time_for_remaining_samples = reduce(lambda a, b: a + b, estimated_run_length_map)
            print(" estimated_total_time_for_remaining_samples = "+str(estimated_total_time_for_remaining_samples))
            time_remaining = total_available_time - cumulative_time_used
            print(" time_remaining = "+str(time_remaining))
            # This will be NEGATIVE iff there's a shortfall
            projected_seconds_overtime = time_remaining - estimated_total_time_for_remaining_samples
            print(" projected_seconds_overtime="+str(projected_seconds_overtime)+" [+ is short (under-run=good), - is long (over-run=bad)")
            # This should be calculated, but at the moment, it's just hacked to five minutes
            seconds_saved_from_error_threshold_001_delta = 300 
            #seconds_saved_from_error_threshold_001_delta = (last_run_length/2)/((0.01-error_threshold)*1000)
            print(" seconds_saved_from_error_threshold_001_delta ="+str(seconds_saved_from_error_threshold_001_delta))
            print(">> TIME ANALYSIS <<")
            if projected_seconds_overtime < 0:
                print("  *** WE'RE GOING TO RUN OUT OF TIME! ***")
                # Simple error threshold recalibration just incfs or
                # decfs the error_threshold by 0.001 depending on whether we're
                # going to be short or long
                if (error_threshold==0.01):
                    print("    !!!!!! Uh oh! There's no room to increase error_threshold!!!")
                else:
                    error_threshold+=0.001
                    print("    ++++++ Resetting error_threshold to "+str(error_threshold))
            elif (projected_seconds_overtime > 3600): 
                print("  We're going to have more than an hour extra time; reducing error threshold by 0.001")
                if (error_threshold==0.001):
                    print("    ...... No room to reduce error_threshold.")
                else:
                    error_threshold-=0.001
                    print("    ------ Resetting error_threshold to "+str(error_threshold))
            else:
                print("Still Safe, and within 1 hour of the target, so not changing error threshold.")
    showsamples(samples)

# More complex error threshold calibration: delta we need to have
# either run several samples with different error rates, or more like
# what we're going to do here, calculate it based on a power function
# assumption, so that we assume we started at t=0 with infinte error
# and then it declines rapidly. Rather than model the power
# function,we're just going to assume that the latter 1/2 of a run
# gets you from 0.010 to 0.001, so it's really easy to estimate how
# much time you're going to get back from each 10th of that half run
# on a per second basis. There's a bit of tricky bookkeeping here
# becuase we need to calibrate against the actual most recent error
# threshold, which might no longer be 0.001

run()