# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
import numpy as np

def update(existingAggregate, newValues):
  """Update"""
  if isinstance(newValues, (int, float, complex)):
      # Handle single digits.
      newValues = [newValues]

  (count, mean, M2) = existingAggregate
  count += len(newValues) 
  # newvalues - oldMean
  delta = np.subtract(newValues, [mean] * len(newValues))
  mean += np.sum(delta / count)
  # newvalues - newMeant
  delta2 = np.subtract(newValues, [mean] * len(newValues))
  M2 += np.sum(delta * delta2)

  return (count, mean, M2)

def finalize(existingAggregate):
  """Finalize"""
  (count, mean, M2) = existingAggregate
  (mean, variance, sampleVariance) = (mean, M2/count, M2/(count - 1))
  if count < 2:
    return float('nan')
  else:
      return (mean, variance, sampleVariance)



x = [1.0, 3.0]
mean = np.mean(x)
count = len(x)
m2 = np.sum(np.subtract(x, [mean] * count)**2)

a = (count, mean, m2)
print(a)
# new batch of values.
b = [5, 3]

result_batch = update(a, b)
# result_batch1 = update(a, b[0])

print(finalize(result_batch))
# print(finalize(result_batch1))