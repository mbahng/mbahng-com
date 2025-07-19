[[1933hotelling_pca.pdf]]
#dimensionality-reduction #pca
[[1901pearson_pca]]

# Contribution
Considered the limitations of underdetermined systems in factor analysis and fixed it by independently introducing PCA as an iterative method to maximize variance. Showed that this coincides with axes of ellipsoid and showed how to compute the principal axes via eigen-decomposition of the covariance or correlation matrix. Also provided the first iterative algorithm for computing principal components and developed statistical tests for determining the number of significant components.

# Background 
Motivation is if we have $n$-covariates $x_1, \ldots, x_n$ called a *complex*, it may be modeled by a simpler system of *components* $\gamma$ such that $x_i = f(\gamma_1, \ldots, \gamma_k)$. These components are called mental factor in psychology. 

Hotelling starts with $n$ variables $x_1, x_2, \ldots, x_n$ for each individual in a population. He wants to find a smaller set of fundamental components $\gamma_1, \gamma_2, \ldots$ that determine the $x$'s through linear relations (also called *mental factors* in psychology from Pearson). 
$$
   x_i = f_i(\gamma_1, \gamma_2, \ldots) \quad \text{for } i = 1, 2, \ldots, n
$$

The components $\gamma_j$ are assumed to be:
1. *Normally distributed*
2. *Uncorrelated* with each other: $E\gamma_i\gamma_j = \delta_{ij}$ (Kronecker delta)
3. *Zero mean*: $E\gamma_j = 0$
4. *Unit variance*: $E\gamma_j^2 = 1$

The variables are converted to "standard measures" by subtracting means and dividing by standard deviations, giving standardized variables $z_1, z_2, \ldots, z_n$. For linear relationships, this becomes. 
$$
   z_i = \sum_j a_{ij}\gamma_j \quad \text{(equation 3)}
$$
where there is no bias term since everything is $0$-mean anyways. 

Let $r_{ik}$ be the correlation between $z_i$ and $z_k$. Substituting the linear expressions:
$$
\begin{align}
   r_{ik} &= Ez_iz_k \\
   &= E\left(\sum_j a_{ij}\gamma_j\right)\left(\sum_l a_{kl}\gamma_l\right) \\
   &= \sum_j \sum_l a_{ij}a_{kl}E\gamma_j\gamma_l
\end{align}
$$

Using the orthogonality condition $E\gamma_j\gamma_l = \delta_{jl}$:
$$
   r_{ik} = \sum_j a_{ij}a_{kj} \quad \text{(equation 6)}
$$

This is the core issue: Since $r_{ik} = r_{ki}$, the number of equations (6) is only $\frac{1}{2}n(n+1)$. They are therefore insufficient for determining the $n^2$ quantities $a_{ij}$ when the correlations between the tests are known.

The system is underdetermined, i.e. there are infinitely many ways to choose components consistent with the observed correlations.

# Method 

## Variance Maximization Approach
These analogies suggest that, in choosing among the infinity of possible modes of resolution of our variables into components, we begin with a component $\gamma_1$ whose contributions to the variances of the $x_i$ have as great a total as possible; that we next take a component $\gamma_2$, independent of $\gamma_1$, whose contribution to the residual variance is as great as possible; and that we proceed in this way to determine the components.

This leads to the **method of principal components** - finding components that sequentially maximize the variance they explain.

The contribution of $\gamma_1$ to the total variance is:
$$
   S = \sum_i a_{i1}^2 = a_{i1}a_{i1} \quad \text{(using tensor notation)}
$$

The problem becomes: Maximize $S$ subject to the constraint $r_{ik} = a_{ij}a_{kj}$. To solve this constrained optimization, Hotelling uses Lagrange multipliers:
$$
   2T = S - \lambda_{ik}a_{ij}a_{kj}
$$

Taking partial derivatives and setting to zero:
$$
\frac{\partial T}{\partial a_{11}} = a_{11} - \lambda_{ik}a_{k1} = 0
$$
$$
\frac{\partial T}{\partial a_{ij}} = -\lambda_{ik}a_{kj} = 0 \quad (j \neq 1)
$$

Through algebraic manipulation, this leads to $\lambda_{ik} = \epsilon a_i a_k$, which when substituted back gives:
$$
r_{km}a_{m1} - ka_{m1} = 0 \quad \text{for } m = 1,2,\ldots,n
$$

Writing this system explicitly:
$$
\begin{align}
   (1-k)a_1 + r_{12}a_2 + \cdots + r_{1n}a_n &= 0\\
   r_{21}a_1 + (1-k)a_2 + \cdots + r_{2n}a_n &= 0\\
   &\vdots\\
   r_{n1}a_1 + r_{n2}a_2 + \cdots + (1-k)a_n &= 0
\end{align}
$$

For non-trivial solutions, the determinant must be zero:
$$
f(k) = \begin{vmatrix}
1-k & r_{12} & r_{13} & \cdots & r_{1n}\\
r_{21} & 1-k & r_{23} & \cdots & r_{2n}\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
r_{n1} & r_{n2} & r_{n3} & \cdots & 1-k
\end{vmatrix} = 0
$$

This is the **characteristic equation**. The largest root $k_1$ gives the maximum variance $S = k_1$, and the corresponding eigenvector gives the coefficients $a_{i1}$.

## Geometric Interpretation
Hotelling shows this procedure is equivalent to finding the principal axes of ellipsoids of constant density in the $n$-dimensional space. The method of principal components, we shall see, is equivalent to choosing a set of coordinate axes coinciding with the principal axes of these ellipsoids.

## Iterative Algorithm
Hotelling provides a practical iterative method:

1. Start with arbitrary trial values $a_1, a_2, \ldots, a_n$
2. Compute $a_i' = \sum_j r_{ij}a_j$ 
3. Normalize: divide by a fixed coefficient to get comparable values
4. Repeat until convergence

The process fails only in the infinitely improbable case of the initial values being linearly dependent upon principal components other than the first; the greatest of these components is then approached.

## Statistical Tests
Hotelling develops methods to determine the number of significant components by:

1. **Comparing eigenvalues**: Using the distribution of correlation coefficients to test if $k_i$ is significantly different from $k_j$
2. **Reliability coefficients**: Comparing computed variances with those expected from measurement error to determine which components are genuine vs. artifacts

For reliability coefficient $r_i$ of test $i$, the error variance is $\sigma_i^2 = \frac{1-r_i}{1+r_i}$. Components with variances not significantly exceeding error expectations may be discarded.

# Results
Applied to 4 educational tests (reading speed, reading power, arithmetic speed, arithmetic power) with 140 seventh-grade children. Found:
- First component (46% variance): general ability
- Second component (37% variance): arithmetic vs. verbal ability  
- Third component (13% variance): speed vs. deliberation
- Fourth component (4% variance): likely measurement error

Statistical tests confirmed only the first two components were significantly above measurement error levels.
