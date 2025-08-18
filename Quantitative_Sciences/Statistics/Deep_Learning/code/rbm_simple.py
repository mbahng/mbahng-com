import torch
import torch.nn as nn 
import torch.nn.functional as F
import numpy as np 
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
    return torch.exp(-self.free_energy(x))
    
  def forward(self, x): 
    x_sample = x

    for _ in range(self.k): 
      pzx = self.P_z_x(x_sample)  
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


def evaluate_distributions(true_gmm, trained_rbm, data_samples, extent=[-5, 5, -5, 5], resolution=20):
    """Evaluate and compare distributions without plotting"""
    print("\n" + "="*60)
    print("DISTRIBUTION COMPARISON RESULTS")
    print("="*60)
    
    # Create grid for evaluation
    x = np.linspace(extent[0], extent[1], resolution)
    y = np.linspace(extent[2], extent[3], resolution)
    X, Y = np.meshgrid(x, y)
    grid_points = np.column_stack([X.ravel(), Y.ravel()])
    
    # Evaluate true distribution
    true_log_probs = true_gmm.score_samples(grid_points)
    true_probs = np.exp(true_log_probs)
    
    print(f"True GMM Statistics:")
    print(f"  - Log likelihood range: [{true_log_probs.min():.3f}, {true_log_probs.max():.3f}]")
    print(f"  - Probability range: [{true_probs.min():.6f}, {true_probs.max():.6f}]")
    
    # Evaluate RBM distribution
    rbm_probs = []
    with torch.no_grad():
        for point in grid_points:
            point_tensor = torch.tensor(point, dtype=torch.float32)
            prob_val = trained_rbm.unnorm_prob(point_tensor)
            rbm_probs.append(float(prob_val.item()))
    
    rbm_probs = np.array(rbm_probs)
    rbm_probs = np.nan_to_num(rbm_probs)
    
    print(f"\nRBM Distribution Statistics:")
    print(f"  - Unnormalized probability range: [{rbm_probs.min():.6f}, {rbm_probs.max():.6f}]")
    
    # Generate samples from RBM
    print(f"\nGenerating samples from trained RBM...")
    with torch.no_grad():
        n_samples = 500
        # Start with samples from the training data
        sample_indices = torch.randperm(len(data_samples))[:n_samples]
        init_samples = torch.tensor(data_samples[sample_indices], dtype=torch.float32)
        
        # Run Gibbs sampling
        current_samples = init_samples
        for step in range(10):
            h_probs = trained_rbm.P_z_x(current_samples)
            h_samples = trained_rbm.sample(h_probs)
            v_probs = trained_rbm.P_x_z(h_samples)
            current_samples = trained_rbm.sample(v_probs)
        
        generated_samples = current_samples.detach().numpy()
    
    # Compare sample statistics
    print(f"\nSample Statistics Comparison:")
    print(f"Original data:")
    print(f"  - Mean: [{data_samples[:, 0].mean():.3f}, {data_samples[:, 1].mean():.3f}]")
    print(f"  - Std:  [{data_samples[:, 0].std():.3f}, {data_samples[:, 1].std():.3f}]")
    print(f"  - Range X: [{data_samples[:, 0].min():.3f}, {data_samples[:, 0].max():.3f}]")
    print(f"  - Range Y: [{data_samples[:, 1].min():.3f}, {data_samples[:, 1].max():.3f}]")
    
    print(f"\nRBM generated samples:")
    print(f"  - Mean: [{generated_samples[:, 0].mean():.3f}, {generated_samples[:, 1].mean():.3f}]")
    print(f"  - Std:  [{generated_samples[:, 0].std():.3f}, {generated_samples[:, 1].std():.3f}]")
    print(f"  - Range X: [{generated_samples[:, 0].min():.3f}, {generated_samples[:, 0].max():.3f}]")
    print(f"  - Range Y: [{generated_samples[:, 1].min():.3f}, {generated_samples[:, 1].max():.3f}]")
    
    print("\n" + "="*60)
    return generated_samples


if __name__ == "__main__":
    print("="*60)
    print("RBM TRAINING ON MIXTURE OF GAUSSIANS")
    print("="*60)
    
    # Generate mixture of Gaussians dataset
    print("Generating mixture of Gaussians dataset...")
    data, true_gmm = create_mixture_of_gaussians_dataset(n_samples=2000)
    print(f"Generated {len(data)} samples from 3-component Gaussian mixture")
    
    # Initialize and train RBM
    print(f"\nInitializing RBM with 50 hidden units...")
    model = RBM(x_dim=2, z_dim=50, k=1)
    
    print(f"Training RBM for 200 epochs...")
    print("-" * 40)
    errors = model.train_rbm(data, epochs=200, batch_size=64, lr=0.01)
    print("-" * 40)
    print(f"Training complete! Final reconstruction error: {errors[-1]:.4f}")
    
    # Evaluate and compare distributions
    generated_samples = evaluate_distributions(true_gmm, model, data.detach().numpy())
    
    print(f"\nTo visualize results, you can plot the data using any plotting tool:")
    print(f"- Original data shape: {data.shape}")
    print(f"- Generated samples shape: {generated_samples.shape}")
    print(f"- Training errors available for plotting: {len(errors)} points")