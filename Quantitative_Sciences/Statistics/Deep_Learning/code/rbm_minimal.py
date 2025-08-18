import torch
import torch.nn as nn 
import torch.nn.functional as F


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


def create_mixture_of_gaussians_dataset(n_samples=1000, random_state=42):
    """Create mixture of Gaussians dataset using pure PyTorch"""
    torch.manual_seed(random_state)
    
    # Define 3 Gaussian components
    means = torch.tensor([[-2.0, -2.0], [2.0, 2.0], [0.0, 3.0]])
    
    # Define covariance matrices (using Cholesky decomposition for sampling)
    covs = torch.tensor([
        [[0.7, 0.0], [0.0, 0.7]],    # Component 1
        [[0.9, -0.3], [-0.3, 0.9]],  # Component 2  
        [[0.5, 0.0], [0.0, 1.1]]     # Component 3
    ])
    
    # Component weights
    weights = torch.tensor([0.4, 0.35, 0.25])
    
    # Sample from each component
    samples_list = []
    n_per_component = (n_samples * weights).long()
    n_per_component[-1] = n_samples - n_per_component[:-1].sum()  # Ensure exact total
    
    for i in range(3):
        # Generate samples for component i
        n_comp = n_per_component[i]
        # Sample from standard normal then transform
        std_samples = torch.randn(n_comp, 2)
        # Apply covariance and mean
        L = torch.linalg.cholesky(covs[i])  # Cholesky decomposition
        transformed = std_samples @ L.T + means[i]
        samples_list.append(transformed)
    
    # Combine and shuffle
    all_samples = torch.cat(samples_list, dim=0)
    shuffle_idx = torch.randperm(len(all_samples))
    data = all_samples[shuffle_idx]
    
    return data, means, covs, weights


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
        # For a single point x (1D tensor)
        if x.dim() == 1:
            bias_term = torch.dot(x, self.b)
            hidden_term = torch.sum(torch.log(1 + torch.exp(F.linear(x, self.W.t(), self.c))))
        # For batch of points x (2D tensor)
        else:
            bias_term = torch.mv(x, self.b)
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
            
            avg_error = sum(epoch_errors) / len(epoch_errors)  # Avoid numpy
            errors.append(avg_error)
            
            if (epoch + 1) % 20 == 0:
                print(f'Epoch {epoch+1}/{epochs}, Reconstruction Error: {avg_error:.4f}')
        
        return errors


def evaluate_rbm_vs_true(data, rbm_model, true_means, true_covs, true_weights):
    """Compare RBM performance against true mixture parameters"""
    print("\n" + "="*60)
    print("RBM EVALUATION RESULTS")
    print("="*60)
    
    # Original data statistics
    data_mean = torch.mean(data, dim=0)
    data_std = torch.std(data, dim=0)
    data_min = torch.min(data, dim=0)[0]
    data_max = torch.max(data, dim=0)[0]
    
    print(f"Original Data Statistics:")
    print(f"  Mean: [{data_mean[0]:.3f}, {data_mean[1]:.3f}]")
    print(f"  Std:  [{data_std[0]:.3f}, {data_std[1]:.3f}]")
    print(f"  Range X: [{data_min[0]:.3f}, {data_max[0]:.3f}]")
    print(f"  Range Y: [{data_min[1]:.3f}, {data_max[1]:.3f}]")
    
    # Generate samples from trained RBM
    print(f"\nGenerating samples from trained RBM...")
    with torch.no_grad():
        n_samples = 1000
        # Initialize with random samples from data
        init_idx = torch.randperm(len(data))[:n_samples]
        current_samples = data[init_idx].clone()
        
        # Run Gibbs sampling
        for step in range(20):
            h_probs = rbm_model.P_z_x(current_samples)
            h_samples = rbm_model.sample(h_probs)
            v_probs = rbm_model.P_x_z(h_samples)
            current_samples = rbm_model.sample(v_probs)
            
            if (step + 1) % 5 == 0:
                print(f"  Gibbs step {step + 1}/20 completed")
    
    # Generated samples statistics
    gen_mean = torch.mean(current_samples, dim=0)
    gen_std = torch.std(current_samples, dim=0)
    gen_min = torch.min(current_samples, dim=0)[0]
    gen_max = torch.max(current_samples, dim=0)[0]
    
    print(f"\nRBM Generated Samples Statistics:")
    print(f"  Mean: [{gen_mean[0]:.3f}, {gen_mean[1]:.3f}]")
    print(f"  Std:  [{gen_std[0]:.3f}, {gen_std[1]:.3f}]")
    print(f"  Range X: [{gen_min[0]:.3f}, {gen_max[0]:.3f}]")
    print(f"  Range Y: [{gen_min[1]:.3f}, {gen_max[1]:.3f}]")
    
    # Compare means (simple similarity metric)
    mean_diff = torch.norm(data_mean - gen_mean)
    print(f"\nSimilarity Metrics:")
    print(f"  Mean difference (L2 norm): {mean_diff:.3f}")
    print(f"  Std difference X: {abs(data_std[0] - gen_std[0]):.3f}")
    print(f"  Std difference Y: {abs(data_std[1] - gen_std[1]):.3f}")
    
    # Evaluate probability on some test points
    print(f"\nRBM Probability Evaluation (unnormalized):")
    test_points = torch.tensor([
        [0.0, 0.0],   # Center
        [-2.0, -2.0], # Near component 1
        [2.0, 2.0],   # Near component 2
        [0.0, 3.0]    # Near component 3
    ])
    
    with torch.no_grad():
        for i, point in enumerate(test_points):
            prob = rbm_model.unnorm_prob(point)
            print(f"  Point {point.tolist()}: {prob.item():.6f}")
    
    print("\n" + "="*60)
    return current_samples


if __name__ == "__main__":
    print("="*60)
    print("MINIMAL RBM TRAINING ON MIXTURE OF GAUSSIANS")
    print("(No numpy/sklearn dependencies)")
    print("="*60)
    
    # Generate mixture of Gaussians dataset
    print("Generating mixture of Gaussians dataset with PyTorch...")
    data, true_means, true_covs, true_weights = create_mixture_of_gaussians_dataset(n_samples=2000)
    print(f"Generated {len(data)} samples from 3-component Gaussian mixture")
    print(f"True component means:")
    for i, mean in enumerate(true_means):
        print(f"  Component {i+1}: [{mean[0]:.1f}, {mean[1]:.1f}]")
    
    # Initialize and train RBM
    print(f"\nInitializing RBM with 50 hidden units...")
    model = RBM(x_dim=2, z_dim=50, k=1)
    
    print(f"Training RBM for 200 epochs...")
    print("-" * 40)
    errors = model.train_rbm(data, epochs=200, batch_size=64, lr=0.01)
    print("-" * 40)
    print(f"Training complete! Final reconstruction error: {errors[-1]:.4f}")
    
    # Evaluate results
    generated_samples = evaluate_rbm_vs_true(data, model, true_means, true_covs, true_weights)
    
    print(f"\nSUCCESS! Your RBM has been trained and evaluated.")
    print(f"Key data available for further analysis:")
    print(f"  - Original data: torch.Tensor of shape {data.shape}")
    print(f"  - Generated samples: torch.Tensor of shape {generated_samples.shape}")
    print(f"  - Training errors: list of {len(errors)} values")
    print(f"  - Trained RBM model ready for further sampling")