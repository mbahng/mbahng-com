import numpy as np
import matplotlib.pyplot as plt

MSEs = []

for d in range(1, 1000): 
  n = 200
  beta_true = np.ones(d)
  X = np.random.randn(n, d)
  Y = X.dot(beta_true) + 0.1 * np.random.randn(n) 
  beta_hat = np.linalg.inv(X.T @ X) @ X.T @ Y  
  mse = (1/n) * np.linalg.norm(Y - X @ beta_hat) 
  MSEs.append(mse)
  

RSSs = []
R2s = []
TSS = np.var(Y)
RSSs.append(TSS)
R2s.append(0)

for k in range(1, 11): 
    RSS = np.var(Y - X.dot(beta_hat)) 
    R2 = 1 - RSS/TSS  
    RSSs.append(RSS) 
    R2s.append(R2)

# Create subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot RSS on left subplot
ax1.plot(range(11), RSSs, 'r-', marker='o')
ax1.set_title('Residual Sum of Squares (RSS)')
ax1.set_xlabel('Number of Features')
ax1.set_ylabel('RSS')
ax1.grid(True, alpha=0.3)

# Plot R² on right subplot
ax2.plot(range(11), R2s, 'b-', marker='o')
ax2.set_title('R-squared')
ax2.set_xlabel('Number of Features')
ax2.set_ylabel('R²')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
