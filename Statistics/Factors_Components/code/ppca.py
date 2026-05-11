import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 100
z = np.random.normal(1, 2, n)
W_true = np.array([[2], [1]])
X_clean = z.reshape(-1, 1) @ W_true.T
X = X_clean + np.random.normal(0, 0.8, X_clean.shape)

# MLE of mu: mu_hat = (1/n) sum x^(i)
mu_hat = np.mean(X, axis=0)
X_centered = X - mu_hat

# Compute sample covariance Sigma_hat
Sigma_hat = X_centered.T @ X_centered / n

# Eigendecomposition: Sigma_hat = V Lambda V^T
eigenvals, V = np.linalg.eigh(Sigma_hat)
idx = np.argsort(eigenvals)[::-1]
eigenvals, V = eigenvals[idx], V[:, idx]

# Parameters
d, k = X.shape[1], 1

# MLE of sigma^2: sigma^2_hat = (1/(d-k)) sum_{j=k+1}^d lambda_j
sigma2_hat = np.sum(eigenvals[k:]) / (d - k)

# V_k: first k columns of V
V_k = V[:, :k]

# MLE of W: W_hat = (Sigma_hat - sigma^2_hat*I_d)^(1/2) V_k
Lambda_adjusted = np.maximum(eigenvals - sigma2_hat, 0)
sqrt_Lambda = np.diag(np.sqrt(Lambda_adjusted))
W_hat = V @ sqrt_Lambda @ V.T @ V_k

# Reconstruction
M = W_hat.T @ W_hat + sigma2_hat * np.eye(k)
z_recon = X_centered @ W_hat @ np.linalg.inv(M)
X_recon = z_recon @ W_hat.T + mu_hat

# Plot
plt.scatter(X[:, 0], X[:, 1], alpha=0.6, label='Noisy data')
plt.scatter(X_recon[:, 0], X_recon[:, 1], alpha=0.6, label='PPCA reconstruction')

t = np.linspace(-3, 3, 100)
true_line = mu_hat.reshape(1, -1) + t.reshape(-1, 1) @ W_true.T
est_line = mu_hat.reshape(1, -1) + t.reshape(-1, 1) @ W_hat.T

plt.plot(true_line[:, 0], true_line[:, 1], 'g--', linewidth=2, label='True subspace')
plt.plot(est_line[:, 0], est_line[:, 1], 'r--', linewidth=2, label='Estimated subspace')

plt.legend()
plt.axis('equal')
plt.show()
