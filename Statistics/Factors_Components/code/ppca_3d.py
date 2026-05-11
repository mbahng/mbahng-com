import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42)
n = 150
z1 = np.random.normal(0, 1, n)
z2 = np.random.normal(0, 1, n)
z = np.column_stack([z1, z2])
W_true = np.array([[1, 0.5], [0.8, 1], [0.3, 0.7]])
mu_true = np.array([1, 2, 0.5])
X_clean = z @ W_true.T + mu_true
X = X_clean + np.random.normal(0, 0.3, X_clean.shape)

# Shared preprocessing
mu = np.mean(X, axis=0)
X_centered = X - mu
Sigma_hat = X_centered.T @ X_centered / n
eigenvals, V = np.linalg.eigh(Sigma_hat)
idx = np.argsort(eigenvals)[::-1]
eigenvals, V = eigenvals[idx], V[:, idx]

d, k = 3, 2
V_k = V[:, :k]

# PPCA
sigma2_hat = np.sum(eigenvals[k:]) / (d - k)
Lambda_adjusted = np.maximum(eigenvals[:k] - sigma2_hat, 0)
W_ppca = V_k @ np.diag(np.sqrt(Lambda_adjusted))

M = W_ppca.T @ W_ppca + sigma2_hat * np.eye(k)
z_recon = X_centered @ W_ppca @ np.linalg.inv(M)
X_ppca_recon = z_recon @ W_ppca.T + mu

# Regular PCA
W_pca = V_k @ np.diag(np.sqrt(eigenvals[:k]))
U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)
X_pca_recon = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :] + mu

# Print W matrices
print("PPCA W matrix:")
print(W_ppca)
print(f"Column norms: {np.linalg.norm(W_ppca, axis=0)}")
print()
print("PCA W matrix:")
print(W_pca)
print(f"Column norms: {np.linalg.norm(W_pca, axis=0)}")
print()
print("Ratio of norms (PPCA/PCA):")
print(np.linalg.norm(W_ppca, axis=0) / np.linalg.norm(W_pca, axis=0))
print()

# Plot both
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), subplot_kw={'projection': '3d'})

# PPCA plot
ax1.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, label='Data', s=20)
ax1.scatter(X_ppca_recon[:, 0], X_ppca_recon[:, 1], X_ppca_recon[:, 2], alpha=0.6, label='Reconstruction', s=20)

u = np.linspace(-2, 2, 8)
v = np.linspace(-2, 2, 8)
U_grid, V_grid = np.meshgrid(u, v)
plane_coords = np.column_stack([U_grid.flatten(), V_grid.flatten()])
plane_ppca = plane_coords @ W_ppca.T + mu
plane_ppca = plane_ppca.reshape(U_grid.shape + (3,))
ax1.plot_surface(plane_ppca[:,:,0], plane_ppca[:,:,1], plane_ppca[:,:,2], alpha=0.2, color='red')

scale = 0.5
ax1.quiver(mu[0], mu[1], mu[2], W_ppca[0,0], W_ppca[1,0], W_ppca[2,0], 
          length=scale, color='blue', arrow_length_ratio=0.1, linewidth=3, 
          label=f'1st PC (||w1||={np.linalg.norm(W_ppca[:, 0]):.2f})')
ax1.quiver(mu[0], mu[1], mu[2], W_ppca[0,1], W_ppca[1,1], W_ppca[2,1], 
          length=scale, color='green', arrow_length_ratio=0.1, linewidth=3, 
          label=f'2nd PC (||w2||={np.linalg.norm(W_ppca[:, 1]):.2f})')
ax1.set_title('PPCA')
ax1.legend()

# PCA plot
ax2.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, label='Data', s=20)
ax2.scatter(X_pca_recon[:, 0], X_pca_recon[:, 1], X_pca_recon[:, 2], alpha=0.6, label='Reconstruction', s=20)

plane_pca = mu.reshape(1, 1, 3) + U_grid[:,:,None] * W_pca[:, 0] + V_grid[:,:,None] * W_pca[:, 1]
ax2.plot_surface(plane_pca[:,:,0], plane_pca[:,:,1], plane_pca[:,:,2], alpha=0.2, color='orange')

ax2.quiver(mu[0], mu[1], mu[2], W_pca[0,0], W_pca[1,0], W_pca[2,0], 
          length=scale, color='red', arrow_length_ratio=0.1, linewidth=3, 
          label=f'1st PC (||w1||={np.linalg.norm(W_pca[:, 0]):.2f})')
ax2.quiver(mu[0], mu[1], mu[2], W_pca[0,1], W_pca[1,1], W_pca[2,1], 
          length=scale, color='purple', arrow_length_ratio=0.1, linewidth=3, 
          label=f'2nd PC (||w2||={np.linalg.norm(W_pca[:, 1]):.2f})')
ax2.set_title('Regular PCA')
ax2.legend()

plt.tight_layout()
plt.show()
