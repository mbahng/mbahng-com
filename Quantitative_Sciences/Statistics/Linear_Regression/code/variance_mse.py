import numpy as np 

n, d = 200, 10
beta_true = np.array([1, 2, 3, 1, -2, -3, 1, -2, 3, -1])
X = np.random.randn(n, d)

def run(): 
  Y = X.dot(beta_true) + 0.1 * np.random.randn(n)
  beta_hat = np.linalg.inv(X.T @ X) @ X.T @ Y 
  return beta_hat

true_cov = 0.1 * np.linalg.inv(X.T.dot(X)) 
print(true_cov[:3, :3]) # True covariance according to our theorem

betas = np.stack([run() for _ in range(10000)], axis=0)
print(np.cov(betas.T)[:3, :3]) # estimated sample covariance


