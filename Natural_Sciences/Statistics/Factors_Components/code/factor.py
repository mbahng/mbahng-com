import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# Generate synthetic data
np.random.seed(42)
n = 200  # number of samples
k = 2    # number of factors
d = 3    # number of observed variables

# True parameters
eta = np.random.randn(n, k)  # factors (isotropic gaussian)
Lambda_true = np.array([[0.8, 0.3],
                       [0.6, 0.7], 
                       [0.9, 0.2]])  # loading matrix (3x2)

# Generate noise with different std devs
noise_std = np.array([0.3, 0.5, 0.2])
epsilon = np.random.randn(n, d) * noise_std

# Generate observed data
X = eta @ Lambda_true.T + epsilon
X = X - np.mean(X, axis=0)  # center data

# Iterated Principal Factors Algorithm
def iterated_principal_factors(X, k, max_iter=1000, tol=1e-6):
   n, d = X.shape
   
   # Compute correlation matrix
   R = np.corrcoef(X.T)
   
   # Initialize communalities
   h2 = 1 - 1/np.diag(R)
   
   for iteration in range(max_iter):
       h2_old = h2.copy()
       
       # Create reduced correlation matrix
       R_star = R.copy()
       np.fill_diagonal(R_star, h2)
       
       # Eigendecomposition
       eigenvals, eigenvecs = eigh(R_star)
       
       # Sort in descending order
       idx = np.argsort(eigenvals)[::-1]
       eigenvals = eigenvals[idx]
       eigenvecs = eigenvecs[:, idx]
       
       # Extract first k factors
       Lambda = eigenvecs[:, :k] @ np.diag(np.sqrt(np.maximum(eigenvals[:k], 0)))
       
       # Update communalities
       h2 = np.sum(Lambda**2, axis=1)
       
       # Check convergence
       if np.linalg.norm(h2 - h2_old) < tol:
           break
   
   # Compute uniquenesses
   psi = 1 - h2
   
   return Lambda, psi, iteration + 1

# Fit the model
Lambda_est, psi_est, iterations = iterated_principal_factors(X, k=2)

# Find optimal rotation R such that Lambda_est @ R ≈ Lambda_true
U, s, Vt = np.linalg.svd(Lambda_est.T @ Lambda_true)
R = U @ Vt

# Apply rotation
Lambda_rotated = Lambda_est @ R

print("True loadings:")
print(Lambda_true)
print("\nEstimated Loading Matrix:")
print(Lambda_est)
print("\nRotation matrix R:")
print(R)
print("\nRotated estimated loadings:")
print(Lambda_rotated)

exit()

print(f"Converged in {iterations} iterations")
print("\nTrue Loading Matrix:")
print(Lambda_true)
print("\nEstimated Loading Matrix:")
print(Lambda_est)
print("\nTrue uniquenesses:", noise_std**2)
print("Estimated uniquenesses:", psi_est)

# Compute reconstruction error
X_reconstructed = (X @ Lambda_est) @ Lambda_est.T
mse = np.mean((X - X_reconstructed)**2)
print(f"\nReconstruction MSE: {mse:.4f}")

# Add this visualization code after fitting the model

from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure(figsize=(15, 6))

def plot_subspace(ax, Lambda, color, title):
   # Create grid for subspace visualization
   u = np.linspace(-3, 3, 10)
   v = np.linspace(-3, 3, 10)
   U, V = np.meshgrid(u, v)
   
   # Points on the 2D factor subspace
   X_sub = Lambda[0, 0] * U + Lambda[0, 1] * V
   Y_sub = Lambda[1, 0] * U + Lambda[1, 1] * V
   Z_sub = Lambda[2, 0] * U + Lambda[2, 1] * V
   
   # Plot subspace as wireframe
   ax.plot_wireframe(X_sub, Y_sub, Z_sub, alpha=0.3, color=color)
   
   # Plot factor vectors
   scale = 2
   for i in range(2):
       ax.quiver(0, 0, 0, Lambda[0, i]*scale, Lambda[1, i]*scale, Lambda[2, i]*scale, 
                color=color, arrow_length_ratio=0.1, linewidth=3)
       ax.text(Lambda[0, i]*scale*1.2, Lambda[1, i]*scale*1.2, Lambda[2, i]*scale*1.2, 
              f'F{i+1}', color=color, fontsize=10)
   
   ax.set_title(title)

# Left plot: True subspace
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, s=30)
plot_subspace(ax1, Lambda_true, 'red', 'True Factor Subspace')
ax1.set_xlabel('X1')
ax1.set_ylabel('X2')
ax1.set_zlabel('X3')

# Right plot: Estimated subspace
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, s=30)
plot_subspace(ax2, Lambda_est, 'blue', 'Estimated Factor Subspace')
ax2.set_xlabel('X1')
ax2.set_ylabel('X2')
ax2.set_zlabel('X3')

plt.tight_layout()
plt.show()
