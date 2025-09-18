import numpy as np
import matplotlib.pyplot as plt

def true_function(x1, x2):
  return (2 * np.sin(x1) * np.cos(x2) + 
         1.5 * np.exp(-(x1**2 + x2**2)/8) + 
         0.8 * np.sin(2*x1) * np.sin(2*x2) +
         0.5 * np.cos(x1 + x2) - 
         0.3 * (x1**2 + x2**2)/10)

n_samples = 300
X1 = np.random.uniform(-5, 5, n_samples)
X2 = np.random.uniform(-5, 5, n_samples)
Y = true_function(X1, X2) + np.random.normal(0, 0.5, n_samples)

def gaussian_kernel(u):
  return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * u**2)

def kernel_regression_2d(x1, x2, bandwidth):
  x1 = np.atleast_1d(x1)
  x2 = np.atleast_1d(x2)
  predictions = []
  
  for x1_point, x2_point in zip(x1, x2):
    distances = np.sqrt((x1_point - X1)**2 + (x2_point - X2)**2) / bandwidth
    weights = gaussian_kernel(distances)
    prediction = np.sum(weights * Y) / np.sum(weights)
    predictions.append(prediction)
  
  return np.array(predictions)

# Create evaluation grid
x1_space = np.linspace(-5, 5, 40)
x2_space = np.linspace(-5, 5, 40)
X1_grid, X2_grid = np.meshgrid(x1_space, x2_space)
x1_flat = X1_grid.flatten()
x2_flat = X2_grid.flatten()

# True function surface
Y_true = true_function(X1_grid, X2_grid)

# Figure 1: Data and True Function
fig1 = plt.figure(figsize=(12, 5))

ax1 = fig1.add_subplot(121, projection='3d')
ax1.scatter(X1, X2, Y, alpha=0.6, s=15, c='gray')
ax1.set_title('Training Data')
ax1.set_xlabel('X1')
ax1.set_ylabel('X2')
ax1.set_zlabel('Y')

ax2 = fig1.add_subplot(122, projection='3d')
ax2.plot_surface(X1_grid, X2_grid, Y_true, alpha=0.9, cmap='viridis')
ax2.set_title('True Function')
ax2.set_xlabel('X1')
ax2.set_ylabel('X2')
ax2.set_zlabel('Y')

plt.tight_layout()
plt.show()

# Figure 2: Kernel Regression with Different Bandwidths
bandwidths = [0.3, 0.8, 1.5]
fig2 = plt.figure(figsize=(15, 5))

for i, bandwidth in enumerate(bandwidths):
 y_pred_flat = kernel_regression_2d(x1_flat, x2_flat, bandwidth)
 Y_pred = y_pred_flat.reshape(X1_grid.shape)
 
 ax = fig2.add_subplot(1, 3, i+1, projection='3d')
 ax.plot_surface(X1_grid, X2_grid, Y_pred, alpha=0.9, cmap='plasma')
 ax.set_title(f'Kernel Regression (h={bandwidth})')
 ax.set_xlabel('X1')
 ax.set_ylabel('X2')
 ax.set_zlabel('Y')

plt.tight_layout()
plt.show()
