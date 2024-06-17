import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import norm

n = norm.pdf
N = norm.cdf

def d1(S, K, r, sigma, T):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, r, sigma, T):
    return (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def black_scholes(S, K, r, sigma, T, call=True): 
    lm = np.log(S/K) 
    d1 = (lm + (r + sigma ** 2 /2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if call: 
        return N(d1) * S - N(d2) * K * np.exp(-r * T)
    else: 
        return -N(-d1) * S + N(-d2) * K * np.exp(-r * T)

def delta(S, K, r, sigma, T, call=True): 
    lm = np.log(S/K) 
    d1 = (lm + (r + sigma ** 2 /2) * T) / (sigma * np.sqrt(T))
    if call: 
        return np.exp(-r * T) * N(d1)
    else:
        return - np.exp(-r * T) * N(-d1)

def gamma(S, K, r, sigma, T): 
    lm = np.log(S/K) 
    d1 = (lm + (r + sigma ** 2 /2) * T) / (sigma * np.sqrt(T))
    return np.exp(-r * T) * n(d1) / (sigma * np.sqrt(T))


def theta_call(S, K, T, r, sigma):
    p1 = - S*n(d1(S, K, T, r, sigma))*sigma / (2 * np.sqrt(T))
    p2 = r*K*np.exp(-r*T)*N(d2(S, K, T, r, sigma)) 
    return p1 - p2

def theta_put(S, K, T, r, sigma):
    p1 = - S*n(d1(S, K, T, r, sigma))*sigma / (2 * np.sqrt(T))
    p2 = r*K*np.exp(-r*T)*N(-d2(S, K, T, r, sigma)) 
    return p1 + p2

def rho(S, K, r, sigma, T, call=True):
    d_2 = d2(S, K, r, sigma, T)
    if call:
        return K * T * np.exp(-r * T) * norm.cdf(d_2)
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d_2)

def vega(S, K, r, sigma, T):
    d_1 = d1(S, K, r, sigma, T)
    return S * np.sqrt(T) * norm.pdf(d_1)



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
