import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


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


def generate_sample_data(n_samples=50, noise_level=0.1):
  X = np.random.uniform(-2, 2, n_samples)
  
  p_true = S2.normalize(np.array([1, 0, 0]))
  v_true = S2.normalize(np.array([0, 1, 0.2]))
  v_true = S2.project_to_tangent(p_true, v_true) * 0.5
  
  Y = []
  for x in X:
    y_clean = S2.exp(p_true, v_true * x)
    
    noise = np.random.normal(0, noise_level, 3)
    noise = S2.project_to_tangent(y_clean, noise)
    y_noisy = S2.exp(y_clean, noise)
    y_noisy = S2.normalize(y_noisy)
    
    Y.append(y_noisy)
  
  return X, np.array(Y), p_true, v_true


class GeodesicRegression:
  def __init__(self):
    self.p = None
    self.v = None
  
  def _geodesic_point(self, p, v, x):
    return S2.exp(p, v * x)
  
  def _objective(self, params, X, Y):
    p_flat = params[:3]
    v_flat = params[3:6]
    
    p_flat = S2.normalize(p_flat)
    v_flat = S2.project_to_tangent(p_flat, v_flat)
    
    total_loss = 0.0
    for i in range(len(X)):
      pred = self._geodesic_point(p_flat, v_flat, X[i])
      loss = S2.distance(pred, Y[i])**2
      total_loss += loss
    
    return total_loss / len(X)
  
  def fit(self, X, Y, p_init=None, v_init=None, method='BFGS'):
    X = np.array(X)
    Y = np.array(Y)
    
    if p_init is None:
      p_init = S2.normalize(np.array([1, 0, 0]))
    if v_init is None:
      v_init = np.array([0, 0.1, 0])
    
    v_init = S2.project_to_tangent(p_init, v_init)
    
    initial_params = np.concatenate([p_init, v_init])
    
    result = minimize(
      self._objective,
      initial_params,
      args=(X, Y),
      method=method,
      options={'disp': False}
    )
    
    if result.success:
      self.p = S2.normalize(result.x[:3])
      self.v = S2.project_to_tangent(self.p, result.x[3:6])
      return result
    else:
      raise RuntimeError(f"Optimization failed: {result.message}")
  
  def predict(self, X):
    X = np.array(X)
    predictions = []
    
    for x in X:
      pred = self._geodesic_point(self.p, self.v, x)
      predictions.append(pred)
    
    return np.array(predictions)
  
  def score(self, X, Y):
    predictions = self.predict(X)
    total_loss = 0.0
    
    for i in range(len(Y)):
      loss = S2.distance(predictions[i], Y[i])**2
      total_loss += loss
    
    return total_loss / len(Y)


def visualize_sphere_regression(X, Y, model, p_true, v_true, title="Geodesic Regression on S^2"):
  fig = plt.figure(figsize=(12, 8))
  ax = fig.add_subplot(111, projection='3d')
  
  u = np.linspace(0, 2 * np.pi, 50)
  v = np.linspace(0, np.pi, 50)
  x_sphere = np.outer(np.cos(u), np.sin(v))
  y_sphere = np.outer(np.sin(u), np.sin(v))
  z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
  
  ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.3, color='lightblue')
  
  colors = plt.cm.viridis((X - X.min()) / (X.max() - X.min()))
  
  for i, (point, color) in enumerate(zip(Y, colors)):
    ax.scatter(point[0], point[1], point[2], c=[color], s=50, alpha=0.8)
  
  X_pred = np.linspace(X.min(), X.max(), 100)
  Y_pred = model.predict(X_pred)
  
  ax.plot(Y_pred[:, 0], Y_pred[:, 1], Y_pred[:, 2], 'r-', linewidth=3, label='Fitted Geodesic')
  
  Y_true = []
  for x in X_pred:
    y_true = S2.exp(p_true, v_true * x)
    Y_true.append(y_true)
  Y_true = np.array(Y_true)
  
  ax.plot(Y_true[:, 0], Y_true[:, 1], Y_true[:, 2], 'g-', linewidth=3, label='True Geodesic')
  
  ax.scatter(model.p[0], model.p[1], model.p[2], c='red', s=100, marker='*', label='Estimated Base Point')
  ax.scatter(p_true[0], p_true[1], p_true[2], c='green', s=100, marker='*', label='True Base Point')
  
  ax.set_xlim([-1.2, 1.2])
  ax.set_ylim([-1.2, 1.2])
  ax.set_zlim([-1.0, 1.0])
  
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  ax.set_title(title)
  ax.legend()
  
  sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=X.min(), vmax=X.max()))
  sm.set_array([])
  cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
  cbar.set_label('X values')
  
  plt.show()


if __name__ == "__main__":
  np.random.seed(42)
  
  X_train, Y_train, p_true, v_true = generate_sample_data(n_samples=30)
  X_test, Y_test, _, _ = generate_sample_data(n_samples=10)
  
  model = GeodesicRegression()
  
  print("Fitting geodesic regression model on S^2...")
  result = model.fit(X_train, Y_train)
  
  print(f"Training MSE: {model.score(X_train, Y_train):.6f}")
  print(f"Test MSE: {model.score(X_test, Y_test):.6f}")
  
  print("\nTrue parameters:")
  print("p_true:", p_true)
  print("v_true:", v_true)
  
  print("\nEstimated parameters:")
  print("p_estimated:", model.p)
  print("v_estimated:", model.v)
  
  visualize_sphere_regression(X_train, Y_train, model, p_true, v_true, "Geodesic Regression on Unit Sphere S^2")
