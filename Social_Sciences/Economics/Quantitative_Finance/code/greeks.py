import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import norm
import os, sys
sys.path.append(".")

n = norm.pdf
N = norm.cdf

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

