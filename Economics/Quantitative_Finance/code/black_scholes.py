import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import norm

n = norm.pdf
N = norm.cdf

def d1(S, K, r, sigma, T):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, r, sigma, T):
    return (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def logmoneyness(S, K): 
    return np.log(S/K)

def black_scholes(S, K, r, sigma, T, call=True): 
    lm = np.log(S/K) 
    d1 = (lm + (r + sigma ** 2 /2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if call: 
        return N(d1) * S - N(d2) * K * np.exp(-r * T)
    else: 
        return -N(-d1) * S + N(-d2) * K * np.exp(-r * T)




# Creating dataset 
underlying_space = np.linspace(1, 13, 100)  
theos_call = black_scholes(underlying_space, 6, 0.01, 0.5, 1, call=True) 
deltas_call = delta(underlying_space, 6, 0.01, 0.5, 1, call=True) 
theos_put = black_scholes(underlying_space, 6, 0.01, 0.5, 1, call=False) 
deltas_put = delta(underlying_space, 6, 0.01, 0.5, 1, call=False) 
gammas = gamma(underlying_space, 6, 0.01, 0.5, 1) 
rhos = rho(underlying_space, 6, 0.01, 0.5, 1)  
vegas = vega(underlying_space, 6, 0.01, 0.5, 1)

for vol in [0.5, 0.3, 0.2, 0.1]: 
    vegas = vega(underlying_space, 6, 0.01, vol, 1)
    plt.plot(underlying_space, vegas, label=f"vol={vol}")
plt.legend() 
plt.show() 
