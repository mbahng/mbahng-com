[[1985ku_dynamic-pca-time-lag.pdf]]
#dimensionality-reduction #dynamic-pca
[[2015vanhatalo_autocorrelation-impact-pca]]

# Contribution

   Introduced dynamic pca (pca of data with temporal dependencies) by taking the data matrix $X$ and horizontally stacking them with lags to make them independent. Doing this shows good results. Then they give a simple procedure to determine how far we should lag. 

# Background 

   **Static PCA limitation**: When applied to dynamic time series data, static PCA fails because:
   - Linear constraints that define the noise space remain static
   - Cannot capture temporal relationships between variables
   - The current values of variables depend on previous values, creating dynamic relationships that static PCA ignores

# Method

   **Core insight**: For dynamic systems, we need to identify linear relationships between:
   - **Current values**: $X(k)$ 
   - **Past values**: $X(k-1), X(k-2), ...$

   The method finds the "noise subspace" by solving:
   $$X_Λ(l)b = 0$$

   where $X_Λ(l)$ is a **Hankel matrix** constructed from time-shifted data:

   $$X_Λ(l) = \begin{bmatrix}
   X^T(1) & X^T(0) & \cdots & X^T(1-l) \\
   X^T(2) & X^T(1) & \cdots & X^T(2-l) \\
   \vdots & \vdots & \ddots & \vdots \\
   X^T(m) & X^T(m-1) & \cdots & X^T(m-l)
   \end{bmatrix}$$

   1. **Captures temporal structure**: Uses lagged versions of data to identify dynamic relationships
   2. **Single-step process**: Both data reduction and model extraction happen simultaneously
   3. **Handles AR/ARX models**: Can extract autoregressive models directly from the data
   4. **True statistical independence**: The extracted components from the noise subspace are truly independent

   The paper shows an AR(1) process example:
   - **Signal**: $z(k) = 0.8z(k-1) + u(k-1)$
   - **Colored noise**: $u(k) = 0.7u(k-1) + w(k-1)$

   DPCA successfully separates the 1-dimensional signal from the 2-dimensional colored noise, showing clear cross-correlation patterns that reveal the underlying dynamic structure. They do another real-life example on chemical processing in Tennessee Eastman process. 

