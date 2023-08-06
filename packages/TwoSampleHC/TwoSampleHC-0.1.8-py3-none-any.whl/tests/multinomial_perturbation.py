from TwoSampleHC import two_sample_pvals
from TwoSampleHC import HC
import numpy as np

N = 1000 # number of features
n = 5 * N #number of samples

P = 1 / np.arange(1,N+1) # Zipf base distribution
P = P / P.sum()

np.random.seed(0)
smp_P = np.random.multinomial(n, P)  # sample form P
smp_Q = np.random.multinomial(n, P)  # sample from Q

pv = two_sample_pvals(smp_Q, smp_P) # binomial P-values
hc = HC(pv)
hcv, p_th = hc.HCstar(gamma = 0.25) # Higher Criticism test

self.assertTrue(np.abs(hcv - -2.8) < .1)
self.assertTrue(np.abs(p_th-0.00388) < .0001)

