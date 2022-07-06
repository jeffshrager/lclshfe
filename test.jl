using Random, Distributions, Dates, Printf
Random.seed!(Dates.value(now()))
d = Normal(3.1416,0.31416)
noise = Normal(0.0,1.0)
x = rand(d, 1000)
fit(Normal, x)
# Welford's algorithm (from wikipedia)
function test()
  count=0.0
  mean=0.0
  M2=0.0
  n=1000000
  show=n/10000
  for i in 1:n
    count = count+1
    newValue=rand(d)+rand(noise)
    delta = newValue - mean
    mean = mean + (delta / count)
    delta2 = newValue - mean
    M2 = M2 + (delta * delta2)
    if (count>1) && (count%show==0)
      variance = M2 / count
      sdev=sqrt(variance)
      err=sdev/sqrt(count)
      @printf("count=%f, M2=%f, mean=%f, err=%f, variance=%f, dev=%f\n",
              count,M2,mean,err,variance,sdev)
      if err < 0.001; break; end
    end
  end
end
test()