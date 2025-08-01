import numpy as np
import matplotlib.pyplot as plt

def true_function(x):
  return 0.3 * x**3 - 0.5 * x**2 + 2 * x + 1 + 2 * np.sin(2 * x)

# Generate data
np.random.seed(42)
n_samples = 150
X = np.random.uniform(-3, 3, n_samples)
Y = true_function(X) + np.random.normal(0, 1.0, n_samples)

def gaussian_kernel(u):
  return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * u**2)

def local_constant_regression(x, bandwidth):
  distances = (x - X) / bandwidth
  weights = gaussian_kernel(distances)
  return np.sum(weights * Y) / np.sum(weights)

def local_linear_regression(x, bandwidth):
  distances = (x - X) / bandwidth
  weights = gaussian_kernel(distances)
  
  # Set up weighted least squares: minimize sum(w_i * (y_i - β₀ - β₁(x_i - x))²)
  W = np.diag(weights)
  design_matrix = np.column_stack([np.ones(len(X)), X - x])
  
  # Solve: (X^T W X) β = X^T W Y
  XTW = design_matrix.T @ W
  beta = np.linalg.solve(XTW @ design_matrix, XTW @ Y)
  
  return beta[0]  # Return β₀(x)

# Evaluation points
x_eval = np.linspace(-3, 3, 200)
y_true = true_function(x_eval)

bandwidth = 0.4
y_constant = [local_constant_regression(x, bandwidth) for x in x_eval]
y_linear = [local_linear_regression(x, bandwidth) for x in x_eval]

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(X, Y, alpha=0.6, s=20, color='gray', label='Data')
plt.plot(x_eval, y_true, 'black', linewidth=2, label='True function')
plt.plot(x_eval, y_constant, 'blue', linewidth=2, label=f'Local constant (h={bandwidth})')
plt.plot(x_eval, y_linear, 'red', linewidth=2, label=f'Local linear (h={bandwidth})')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Local Constant vs Local Linear Regression')
plt.tight_layout()
plt.show()
