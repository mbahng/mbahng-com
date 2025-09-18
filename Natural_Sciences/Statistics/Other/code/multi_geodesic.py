import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class S2:
  @staticmethod
  def exp(p, v):
    v_norm = np.linalg.norm(v)
    if v_norm < 1e-8:
      return p
    return np.cos(v_norm) * p + np.sin(v_norm) * v / v_norm
  
  @staticmethod
  def log(p, q):
    cos_dist = np.clip(np.dot(p, q), -1, 1)
    if np.abs(cos_dist - 1) < 1e-8:
      return np.zeros_like(p)
    
    theta = np.arccos(cos_dist)
    sin_theta = np.sin(theta)
    
    if sin_theta < 1e-8:
      return np.zeros_like(p)
    
    return theta * (q - cos_dist * p) / sin_theta
  
  @staticmethod
  def distance(p, q):
    cos_dist = np.clip(np.dot(p, q), -1, 1)
    return np.arccos(cos_dist)
  
  @staticmethod
  def project_to_tangent(p, v):
    return v - np.dot(v, p) * p
  
  @staticmethod
  def normalize(x):
    return x / np.linalg.norm(x)


def generate_sample_data(n_samples=50, n_features=2, noise_level=0.1):
  X = np.random.uniform(-1, 1, (n_samples, n_features))
  
  p_true = S2.normalize(np.array([1, 0, 0]))
  V_true = np.array([[0, 0.3], [0.5, -0.2], [0.2, 0.4]])
  
  for i in range(n_features):
    V_true[:, i] = S2.project_to_tangent(p_true, V_true[:, i])
  
  Y = []
  for x in X:
    tangent_vec = V_true @ x
    y_clean = S2.exp(p_true, tangent_vec)
    
    noise = np.random.normal(0, noise_level, 3)
    noise = S2.project_to_tangent(y_clean, noise)
    y_noisy = S2.exp(y_clean, noise)
    y_noisy = S2.normalize(y_noisy)
    
    Y.append(y_noisy)
  
  return X, np.array(Y), p_true, V_true


class MultipleGeodesicRegression:
  def __init__(self, n_features):
    self.n_features = n_features
    self.p = None
    self.V = None
  
  def _geodesic_point(self, p, V, x):
    tangent_vec = V @ x
    return S2.exp(p, tangent_vec)
  
  def _objective(self, params, X, Y):
    p_flat = params[:3]
    V_flat = params[3:].reshape(3, self.n_features)
    
    p_flat = S2.normalize(p_flat)
    
    for i in range(self.n_features):
      V_flat[:, i] = S2.project_to_tangent(p_flat, V_flat[:, i])
    
    total_loss = 0.0
    for i in range(len(X)):
      pred = self._geodesic_point(p_flat, V_flat, X[i])
      loss = S2.distance(pred, Y[i])**2
      total_loss += loss
    
    return total_loss / len(X)
  
  def fit(self, X, Y, p_init=None, V_init=None, method='BFGS'):
    X = np.array(X)
    Y = np.array(Y)
    
    if p_init is None:
      p_init = S2.normalize(np.array([1, 0, 0]))
    if V_init is None:
      V_init = np.random.normal(0, 0.1, (3, self.n_features))
    
    for i in range(self.n_features):
      V_init[:, i] = S2.project_to_tangent(p_init, V_init[:, i])
    
    initial_params = np.concatenate([p_init, V_init.flatten()])
    
    result = minimize(
      self._objective,
      initial_params,
      args=(X, Y),
      method=method,
      options={'disp': False}
    )
    
    if result.success:
      self.p = S2.normalize(result.x[:3])
      self.V = result.x[3:].reshape(3, self.n_features)
      
      for i in range(self.n_features):
        self.V[:, i] = S2.project_to_tangent(self.p, self.V[:, i])
      
      return result
    else:
      raise RuntimeError(f"Optimization failed: {result.message}")
  
  def predict(self, X):
    X = np.array(X)
    predictions = []
    
    for x in X:
      pred = self._geodesic_point(self.p, self.V, x)
      predictions.append(pred)
    
    return np.array(predictions)
  
  def score(self, X, Y):
    predictions = self.predict(X)
    total_loss = 0.0
    
    for i in range(len(Y)):
      loss = S2.distance(predictions[i], Y[i])**2
      total_loss += loss
    
    return total_loss / len(Y)


def visualize_multiple_regression(X, Y, model, p_true, V_true, title="Multiple Geodesic Regression on S^2"):
  fig = plt.figure(figsize=(10, 5))
  
  # Plot 1: 3D sphere with data points colored by first covariate
  ax1 = fig.add_subplot(121, projection='3d')
  
  u = np.linspace(0, 2 * np.pi, 30)
  v = np.linspace(0, np.pi, 30)
  x_sphere = np.outer(np.cos(u), np.sin(v))
  y_sphere = np.outer(np.sin(u), np.sin(v))
  z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
  
  ax1.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='lightblue')
  
  colors1 = plt.cm.viridis((X[:, 0] - X[:, 0].min()) / (X[:, 0].max() - X[:, 0].min()))
  for i, (point, color) in enumerate(zip(Y, colors1)):
    ax1.scatter(point[0], point[1], point[2], c=[color], s=30, alpha=0.8)
  
  ax1.scatter(model.p[0], model.p[1], model.p[2], c='red', s=80, marker='*', label='Estimated p')
  ax1.scatter(p_true[0], p_true[1], p_true[2], c='green', s=80, marker='*', label='True p')
  
  # Add first tangent vector
  scale = 1.3
  ax1.quiver(model.p[0], model.p[1], model.p[2], 
             model.V[0, 0]*scale, model.V[1, 0]*scale, model.V[2, 0]*scale, 
             color='red', alpha=0.8, arrow_length_ratio=0.1, linewidth=2)
  ax1.quiver(p_true[0], p_true[1], p_true[2], 
             V_true[0, 0]*scale, V_true[1, 0]*scale, V_true[2, 0]*scale, 
             color='green', alpha=0.8, arrow_length_ratio=0.1, linewidth=2)
  
  ax1.set_xlim([-1.2, 1.2])
  ax1.set_ylim([-1.2, 1.2])
  ax1.set_zlim([-1.0, 1.0])
  ax1.set_title('Colored by X1')
  ax1.legend()
  
  # Plot 2: 3D sphere with data points colored by second covariate
  ax2 = fig.add_subplot(122, projection='3d')
  ax2.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='lightblue')
  
  colors2 = plt.cm.plasma((X[:, 1] - X[:, 1].min()) / (X[:, 1].max() - X[:, 1].min()))
  for i, (point, color) in enumerate(zip(Y, colors2)):
    ax2.scatter(point[0], point[1], point[2], c=[color], s=30, alpha=0.8)
  
  ax2.scatter(model.p[0], model.p[1], model.p[2], c='red', s=80, marker='*', label='Estimated p')
  ax2.scatter(p_true[0], p_true[1], p_true[2], c='green', s=80, marker='*', label='True p')
  
  # Add second tangent vector
  scale = 1.0
  ax2.quiver(model.p[0], model.p[1], model.p[2], 
             model.V[0, 1]*scale, model.V[1, 1]*scale, model.V[2, 1]*scale, 
             color='red', alpha=0.8, arrow_length_ratio=0.1, linewidth=2)
  ax2.quiver(p_true[0], p_true[1], p_true[2], 
             V_true[0, 1]*scale, V_true[1, 1]*scale, V_true[2, 1]*scale, 
             color='green', alpha=0.8, arrow_length_ratio=0.1, linewidth=2)
  
  ax2.set_xlim([-1.2, 1.2])
  ax2.set_ylim([-1.2, 1.2])
  ax2.set_zlim([-1.0, 1.0])
  ax2.set_title('Colored by X2')
  ax2.legend()
  
  
  plt.tight_layout()
  plt.show()


def visualize_prediction_surface(X, Y, model, p_true, V_true, title="Prediction vs True Surface"):
  fig = plt.figure(figsize=(8, 6))
  ax = fig.add_subplot(111, projection='3d')
  
  # Draw sphere
  u = np.linspace(0, 2 * np.pi, 30)
  v = np.linspace(0, np.pi, 30)
  x_sphere = np.outer(np.cos(u), np.sin(v))
  y_sphere = np.outer(np.sin(u), np.sin(v))
  z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
  
  ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='lightblue')
  
  # Create a grid for prediction surface
  x1_grid = np.linspace(X[:, 0].min(), X[:, 0].max(), 10)
  x2_grid = np.linspace(X[:, 1].min(), X[:, 1].max(), 10)
  X1_grid, X2_grid = np.meshgrid(x1_grid, x2_grid)
  
  X_grid = np.column_stack([X1_grid.ravel(), X2_grid.ravel()])
  Y_pred = model.predict(X_grid)
  
  ax.scatter(Y_pred[:, 0], Y_pred[:, 1], Y_pred[:, 2], c='red', s=10, alpha=0.6, label='Predicted Surface')
  
  # True surface
  Y_true_grid = []
  for x in X_grid:
    tangent_vec = V_true @ x
    y_true = S2.exp(p_true, tangent_vec)
    Y_true_grid.append(y_true)
  Y_true_grid = np.array(Y_true_grid)
  
  ax.scatter(Y_true_grid[:, 0], Y_true_grid[:, 1], Y_true_grid[:, 2], c='green', s=10, alpha=0.6, label='True Surface')
  
  # Original data points
  for point in Y:
    ax.scatter(point[0], point[1], point[2], c='black', s=20, alpha=0.4)
  
  ax.set_xlim([-1.2, 1.2])
  ax.set_ylim([-1.2, 1.2])
  ax.set_zlim([-1.0, 1.0])
  ax.set_title(title)
  ax.legend()
  
  plt.tight_layout()
  plt.show()


if __name__ == "__main__":
  np.random.seed(42)
  
  n_features = 2
  X_train, Y_train, p_true, V_true = generate_sample_data(n_samples=50, n_features=n_features)
  X_test, Y_test, _, _ = generate_sample_data(n_samples=20, n_features=n_features)
  
  model = MultipleGeodesicRegression(n_features=n_features)
  
  print("Fitting multiple geodesic regression model on S^2...")
  result = model.fit(X_train, Y_train)
  
  print(f"Training MSE: {model.score(X_train, Y_train):.6f}")
  print(f"Test MSE: {model.score(X_test, Y_test):.6f}")
  
  print("\nTrue parameters:")
  print("p_true:", p_true)
  print("V_true:")
  print(V_true)
  
  print("\nEstimated parameters:")
  print("p_estimated:", model.p)
  print("V_estimated:")
  print(model.V)
  
  visualize_multiple_regression(X_train, Y_train, model, p_true, V_true)
  visualize_prediction_surface(X_train, Y_train, model, p_true, V_true)
