import numpy as np 

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

n, d = 200, 5
beta_true = np.array([1, 2, 3, 1, -2])
X = np.random.randn(n, d)
logits = X.dot(beta_true)
probs = sigmoid(logits)
Y = np.random.binomial(1, probs, n)

lr = 0.5
beta_hat = np.random.randn(5) * 0.1
for _ in range(1000): 
    Y_hat = sigmoid(X.dot(beta_hat))
    grad = (1/n) * X.T.dot(Y_hat - Y)
    beta_hat -= lr * grad  

print(beta_hat)
