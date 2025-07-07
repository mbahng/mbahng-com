[[1901pearson_pca.pdf]]
#dimensionality-reduction

# Contribution
   
   First instance of PCA, formulated as the subspace that minimizes the $L^2$ distance. Gives a complete analytical solution for this best-fit hyperplane (of dimension $p-1$) through $n$ non-coplanar points in $\mathbb{R}^p$ by taking the derivative of the loss and setting it to $0$. Shows that it depends on the means, std-dev, and correlations of the variables. 

   Gives some geometric intuition with quadrics. 

# Background 

   In linear regression, we treat the independent variables $x$ and dependent variables $y$ differently. We wish to find the best estimate of $y$ given $x$, but this may not be the best estimate of $x$ given $y$. Therefore since we are often uncertain not only about $y$ but the observations $x$, to model the joint distribution, we should approach the modeling differently. We do not know $x$ and then proceed to find $y$, but both $x$ and $y$ are found by observation. 

# Derivation

   Clearly, a best fit line would be something that minimizes the squared distances. For simplicity, let us just denote the samples $\{x^{(i)}\}$ with $x$ and their covariates $x_1, \ldots, x_q$. We wish to minimize. 

   $$
      U = S(p^2) = \sum (x - x^\prime)^2
   $$

   where $x^\prime$ is our predicted variable, i.e. the projection onto our subspace. Note that $S$ represents summation notation. We first standardize across each covariate. 

   1. The sample mean is 
   $$
      \overline{x}_i = \frac{1}{n} \sum x_i = \frac{S(x_i)}{n}
   $$

   2. The sample standard deviation is 
   $$ 
   \begin{align} 
      \sigma_i^2 & = \frac{1}{n} \sum (x_i - \overline{x}_i)^2  \\ 
      & = \frac{1}{n} \sum x_i^2 - \frac{2}{n} \overline{x}_i \sum x_i + \overline{x}_i^2 \\ 
      & = \frac{S(x_i)}{n} - \overline{x}_i^2
   \end{align}
   $$
   
   3. The sample correlation for all pairs $i, j$ is 
   $$
   \begin{align} 
      r_{ij} = \frac{S(x_i x_j) - n \overline{x}_i \overline{x}_j}{n \sigma_i \sigma_j}
   \end{align}
   $$

   Now we can describe an affine hyperplane $P$ by its orthogonal distance from the origin $p$ and its unit orthogonal vector, denote it $l = (l_1, \ldots, l_p)$. Since it is unit, the perpendicular distance of a point $x$ from the hyperplane is $x \cdot l - p$. We therefore wish to minimize 
   $$
      U = S(x \cdot l - p) = S(l_1 x_1 + \ldots + l_q x_q - p)
   $$ 
   by variation of $l_i$ and $p$. Take the derivative w.r.t. $p$ and see that 
   $$ 
   \begin{align}
      \sum 2 (l_1 x_1 + \ldots + l_q x_q - p) = 0 & \implies l_1 S(x_1) + \ldots + l_q S(x_q) - S(p) = 0 \\ 
      & \implies l_1 \overline{x}_1 + \ldots + l_q \overline{x}_q = np
   \end{align}
   $$
   and so the hyperplane of best fit goes through the centroid. Now to solve for $l$, we use the method of Lagrange multipliers. We want to optimize $U = S(l_1 x_1 + \ldots + l_q x_q - p)^2$ subject to $l_1^2 + \ldots + l_q^2 = 1$. We take the lagrangian $\mathcal{L}(l) = U(l) + Q(l_1^2 + \ldots + l_2^2 - 1)$ and take the derivative of it to get 
   $$ 
   \begin{align}
      0 & = \frac{\partial \mathcal{L}(l)}{\partial l_i} = \frac{\partial U(l)}{\partial l_i} + \frac{\partial}{\partial l_i} Q(l_1^2 + \ldots + l_2^2 - 1) \\ 
      & = \sum 2(l_1 x_1 + \ldots + l_q x_q - p) x_i + 2 Q l_i \\
      0 & = l_1 S(x_1 x_i) + \ldots + l_q S(x_q x_i) - p S(x_i) + Q l_i
   \end{align}
   $$ 

   We can substitute to put this in terms of the correlation for each $l_i$. 
   $$
      l_1 \sigma_1 \sigma_i r_{1i} + \ldots + l_i \sigma_i^2 + \ldots + l_q \sigma_q \sigma_i r_{qi} + \frac{Q}{n} l_i = 0 
   $$ 
   which allows us to see that this is only dependent on the mean, variance, and covariance. This becomes a linear system of equations, and we can solve this for the $l_i$'s. 

# Intuition with Ellipsoids 

   They do a bit more derivation to show some intuition. In particular, let us take the quadric equation 
   $$
      \sum_{i, j} \sigma_i \sigma_j r_{ij} x_i x_j = \epsilon^4
   $$
   which defines an ellipsoid (since coefficients are all positive) of the data. It turns out that the axes of the ellipsoid are either on or are perpendicular to the hyperplane of best-fit.  

# Example 

   They do a tedious walkthrough of PCA with 10 points by hand. 
