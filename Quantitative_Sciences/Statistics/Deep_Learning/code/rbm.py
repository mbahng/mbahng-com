import torch
import torch.nn as nn 
import torch.nn.functional as F
import numpy as np 
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture 


class DataLoader:
    def __init__(self, data, batch_size=32):
        self.data = data
        self.batch_size = batch_size
        
    def __iter__(self):
        n_samples = len(self.data)
        indices = torch.randperm(n_samples)
        for start in range(0, n_samples, self.batch_size):
            end = min(start + self.batch_size, n_samples)
            batch_indices = indices[start:end]
            yield self.data[batch_indices]


def create_mixture_of_gaussians_dataset(n_samples=1000, n_components=3, random_state=42):
    np.random.seed(random_state)
    torch.manual_seed(random_state)
    
    # Define mixture parameters
    means = np.array([[-2, -2], [2, 2], [0, 3]])
    covariances = np.array([[[0.5, 0.1], [0.1, 0.5]], 
                           [[0.8, -0.3], [-0.3, 0.8]], 
                           [[0.3, 0], [0, 1.2]]])
    weights = np.array([0.4, 0.35, 0.25])
    
    # Generate samples manually from the mixture
    samples = []
    n_per_component = (n_samples * weights).astype(int)
    n_per_component[-1] = n_samples - n_per_component[:-1].sum()  # Ensure exact total
    
    for i in range(n_components):
        component_samples = np.random.multivariate_normal(
            means[i], covariances[i], size=n_per_component[i]
        )
        samples.append(component_samples)
    
    # Combine all samples and shuffle
    all_samples = np.vstack(samples)
    shuffle_idx = np.random.permutation(len(all_samples))
    data = all_samples[shuffle_idx]
    
    # Create a fitted GaussianMixture for visualization purposes
    true_gmm = GaussianMixture(n_components=n_components, random_state=random_state)
    true_gmm.fit(data)  # Fit to the generated data
    
    return torch.tensor(data, dtype=torch.float32), true_gmm


class RBM(nn.Module): 

  def __init__(self, x_dim: int, z_dim: int, k: int): 
    super().__init__()
    self.W = nn.Parameter(torch.randn(x_dim, z_dim) * 0.1) 
    self.b = nn.Parameter(torch.randn(x_dim) * 0.1) 
    self.c = nn.Parameter(torch.randn(z_dim) * 0.1)  
    self.k = k

  def sample(self, p): 
    return p.bernoulli()

  def P_z_x(self, x): 
    return torch.sigmoid(F.linear(x, self.W.t(), self.c))

  def P_x_z(self, z): 
    return torch.sigmoid(F.linear(z, self.W, self.b)) 

  def free_energy(self, x): 
    # average free energy F(x) =  c^T x + \sum \softplus(Wx + b)
    # where p(x) = \exp(-F(x))/Z 

    # For a single point x (1D tensor)
    if x.dim() == 1:
        bias_term = torch.dot(x, self.b)
        hidden_term = torch.sum(torch.log(1 + torch.exp(F.linear(x, self.W.t(), self.c))))
    # For batch of points x (2D tensor)
    else:
        bias_term = torch.mv(x, self.b)  # This is correct for 2D x
        hidden_term = torch.sum(torch.log(1 + torch.exp(F.linear(x, self.W.t(), self.c))), dim=1)
    
    return -bias_term - hidden_term

  def unnorm_prob(self, x): 
    return torch.exp(self.free_energy(x))
    
  def forward(self, x): 
    x_sample = x

    for _ in range(self.k): 
      pzx = self.P_z_x(x)  
      z_sample = self.sample(pzx) 
      pxz = self.P_x_z(z_sample)  
      x_sample = self.sample(pxz)

    return x_sample, pxz

  def train_step(self, batch, lr=0.01):
    # Positive phase
    pos_v = batch
    pos_h_probs = self.P_z_x(pos_v)
    pos_h = self.sample(pos_h_probs)
    
    # Negative phase (k-step contrastive divergence)
    neg_v = pos_v
    for _ in range(self.k):
      neg_h_probs = self.P_z_x(neg_v)
      neg_h = self.sample(neg_h_probs)
      neg_v_probs = self.P_x_z(neg_h)
      neg_v = self.sample(neg_v_probs)
    
    neg_h_probs = self.P_z_x(neg_v)
    
    # Update parameters
    with torch.no_grad():
      # Weight updates
      pos_associations = torch.mm(pos_v.t(), pos_h_probs)
      neg_associations = torch.mm(neg_v.t(), neg_h_probs)
      self.W.data += lr * (pos_associations - neg_associations) / batch.size(0)
      
      # Bias updates
      self.b.data += lr * torch.mean(pos_v - neg_v, 0)
      self.c.data += lr * torch.mean(pos_h_probs - neg_h_probs, 0)
    
    # Reconstruction error
    error = torch.mean((pos_v - neg_v) ** 2)
    return error.item()

  def train_rbm(self, data, epochs=100, batch_size=32, lr=0.01):
    dataloader = DataLoader(data, batch_size)
    errors = []
    
    for epoch in range(epochs):
      epoch_errors = []
      for batch in dataloader:
        error = self.train_step(batch, lr)
        epoch_errors.append(error)
      
      avg_error = np.mean(epoch_errors)
      errors.append(avg_error)
      
      if (epoch + 1) % 20 == 0:
        print(f'Epoch {epoch+1}/{epochs}, Reconstruction Error: {avg_error:.4f}')
    
    return errors


def plot_distributions(true_gmm, trained_rbm, data_samples, extent=[-5, 5, -5, 5], resolution=50):
    # Use a simpler approach to avoid matplotlib compatibility issues
    plt.rcParams['figure.max_open_warning'] = 0  # Suppress warnings
    
    # Plot 1: Original data samples
    plt.figure(figsize=(12, 10))
    plt.subplot(2, 2, 1)
    plt.scatter(data_samples[:, 0], data_samples[:, 1], alpha=0.6, s=10)
    plt.title('Original Data Samples')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])
    plt.grid(True, alpha=0.3)
    
    # Plot 2: True mixture of Gaussians distribution
    plt.subplot(2, 2, 2)
    x = np.linspace(extent[0], extent[1], resolution)
    y = np.linspace(extent[2], extent[3], resolution)
    X, Y = np.meshgrid(x, y)
    grid_points = np.column_stack([X.ravel(), Y.ravel()])
    true_log_probs = true_gmm.score_samples(grid_points)
    true_probs = np.exp(true_log_probs).reshape(X.shape)
    
    contour1 = plt.contourf(X, Y, true_probs, levels=20, cmap='viridis')
    plt.title('True Distribution (Mixture of Gaussians)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar(contour1)
    
    # Plot 3: RBM learned distribution
    plt.subplot(2, 2, 3)
    rbm_probs = np.zeros_like(X)
    print("Computing RBM probabilities...")
    with torch.no_grad():
        for i in range(resolution):
            for j in range(resolution):
                point = torch.tensor([float(X[i, j]), float(Y[i, j])], dtype=torch.float32)
                try:
                    prob_val = trained_rbm.unnorm_prob(point)
                    rbm_probs[i, j] = float(prob_val.item())
                except:
                    rbm_probs[i, j] = 0.0
    
    # Normalize and handle any NaN/inf values
    rbm_probs = np.nan_to_num(rbm_probs)
    if np.max(rbm_probs) > 0:
        rbm_probs = rbm_probs / np.max(rbm_probs)
    
    contour2 = plt.contourf(X, Y, rbm_probs, levels=20, cmap='viridis')
    plt.title('RBM Learned Distribution')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar(contour2)
    
    # Plot 4: RBM generated samples
    plt.subplot(2, 2, 4)
    print("Generating RBM samples...")
    with torch.no_grad():
        # Generate samples from the RBM using Gibbs sampling
        n_samples = 500
        # Start with samples from the training data
        sample_indices = torch.randperm(len(data_samples))[:n_samples]
        init_samples = torch.tensor(data_samples[sample_indices], dtype=torch.float32)
        
        # Run Gibbs sampling for a few steps
        current_samples = init_samples
        for _ in range(10):  # Run 10 Gibbs steps
            h_probs = trained_rbm.P_z_x(current_samples)
            h_samples = trained_rbm.sample(h_probs)
            v_probs = trained_rbm.P_x_z(h_samples)
            current_samples = trained_rbm.sample(v_probs)
        
        generated_samples = current_samples.detach().numpy()
    
    plt.scatter(generated_samples[:, 0], generated_samples[:, 1], alpha=0.6, s=10, color='red')
    plt.title('RBM Generated Samples')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('rbm_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()  # Close figure instead of showing
    print("Saved comparison plot to 'rbm_comparison.png'")


def plot_training_curve(errors):
    plt.figure(figsize=(10, 6))
    plt.plot(errors)
    plt.title('RBM Training: Reconstruction Error over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Reconstruction Error')
    plt.grid(True)
    plt.savefig('rbm_training_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved training curve to 'rbm_training_curve.png'")


if __name__ == "__main__":
    # Generate mixture of Gaussians dataset
    print("Generating mixture of Gaussians dataset...")
    data, true_gmm = create_mixture_of_gaussians_dataset(n_samples=2000)
    
    # Initialize and train RBM
    print("Initializing RBM...")
    model = RBM(x_dim=2, z_dim=50, k=1)
    
    print("Training RBM...")
    errors = model.train_rbm(data, epochs=200, batch_size=64, lr=0.01)
    
    # Plot training curve
    plot_training_curve(errors)
    
    # Compare distributions
    print("Plotting distribution comparison...")
    plot_distributions(true_gmm, model, data.detach().numpy())
    
    print("Training complete! Check the plots to see how well the RBM learned the distribution.")
