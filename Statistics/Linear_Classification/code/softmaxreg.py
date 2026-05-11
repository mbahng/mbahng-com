import numpy as np

n, d, K = 500, 5, 3  # n samples, d features, K classes
W_true = np.array([[1.0, 2.0, -1.5, 0.5, 3.0],
                  [-2.0, 1.0, 2.5, -1.0, 0.5],
                  [0.5, -1.5, 1.0, 2.0, -2.5]])
b_true = np.array([0.5, -1.0, 1.5])
X = np.random.randn(n, d)

def softmax(z):
  exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # numerical stability
  return exp_z / np.sum(exp_z, axis=1, keepdims=True)

logits = X @ W_true.T + b_true
probs = softmax(logits)
Y_labels = np.array([np.random.choice(K, p=prob) for prob in probs])

Y = np.zeros((n, K)) # Convert to one-hot encoding
Y[np.arange(n), Y_labels] = 1

W_hat, b_hat  = np.random.randn(K, d) * 0.1, np.random.randn(K) * 0.1
lr = 0.05
for epoch in range(10000):
  logits = X @ W_hat.T + b_hat
  predictions = softmax(logits)
  error = predictions - Y  # shape: (n, K)
  grad_W = error.T @ X / n  # shape: (K, d)
  grad_b = np.mean(error, axis=0)  # shape: (K,)
  W_hat -= lr * grad_W
  b_hat -= lr * grad_b

final_predictions = softmax(X @ W_hat.T + b_hat)
final_accuracy = np.mean(np.argmax(final_predictions, axis=1)==Y_labels)

print(W_hat)
print(b_hat)
print("Accuracy:", final_accuracy)
