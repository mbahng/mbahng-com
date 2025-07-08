[[1956anderson_inference-factor-analysis.pdf]]
#factor-models
[[1941harman_modern-factor-analysis]]

# Contribution 

   The paper presents a unified mathematical framework for factor analysis, focusing on rigorous statistical inference rather than psychological interpretation. They analyze the factor model:
   $$
      X = \Lambda f + U + \mu
   $$
   where $X$ is the observed data, $\Lambda$ contains factor loadings, $f$ represents factors, $U$ is error, and $\mu$ is the mean.   

# Model 

   You can distinguish when $f$ is fixed or a random variable. 
   1. The elements of $U$ are uncorrelated. 
   2. $U$ is usually assumed to be Gaussian. 
   3. Every element of $f$ is a common factor. This is a simpler and more powerful representation than that mentioned in Spearman. 

   If $f$ is a random variable, then 
   1. We assume that $\mathbb{E}[f] = 0$. Otherwise, it can be absorbed in $\mu$. 
   2. We usually assume that $f$ is Gaussian. 
   3. Let $M = \mathrm{Var}[f] = \mathbb{E}[f f^T]$. 
   4. 

   If $f$ is fixed, then we have a fixed dataset $\{f_\alpha, X_\alpha\}_\alpha$ consisting of the observations $X_\alpha$ and the latent variables $f_\alpha$, and so it is more accurate to write the model as $X_\alpha = \Lambda f_\alpha + U + \mu$. 
   1. We assume that the sample mean $\frac{1}{N} \sum_\alpha f_\alpha = 0$. 
   2. We assume that the sample covariance $\frac{1}{N} \sum_\alpha f_\alpha f_\alpha^T = M$. 

   Geometrically, we have a $p$-dimensional space, and the columns of $\Lambda$ are $m$ vectors in the space that span some $m$-dimensional subspace. They are basically the coordiante axes, and $f$ can be considered as coordinates of a point that space with respect to this basis. This subspace is called the **factor space**. 

## Indeterminancy  

   Our job is to estimate $\mu, \Lambda, f$. Note that this model is overdetermined as follows. If we have some nonsingular matrix $A$ with $\Lambda^\ast = \Lambda A$, then $\mu, \Lambda^\ast, f^\ast = A^{-1} f$ is also just as good of a model. That is, by observing only $X$ we cannot distinguish between the two models. 

   Some of the indeterminancy can be eliminated by requiring that $\mathbb{E}[f f^T] = I$ (or that the sample covariance is $I$). In this case, the factors as said to be **orthogonal**, and if not, then it is called **oblique**. This means that $A A^T = I$, and so $A$ is really an orthogonal matrix. This can be both a problem and a strength, but in general this requires us that in the Gaussian case, the factors are independent. 

## Relation to PCA 

   There is another fundamental replacement assumption that we can make in that the factors should account for the maximum variance, but this is not elaborated here. 

## Positive Loadings 

   Sometimes the assumption that all loadings must be positive is enforced. 

# Solving the Model 

   Given the assumptions of $\mathbb{E}[f f^T] = I$, we can deduce that $X$ is normally distributed with mean $\mu$ and covariance matrix 
   $$
   \begin{align}
      \mathbb{E}[(X - \mu) (X - \mu)^T] & = \mathbb{E}[(\Lambda f + U) (\Lambda f + U)^T] \\ 
      & =  \mathbb{E}[\Lambda f f^T \Lambda^T + U f^T \Lambda^T + \Lambda f U^T + U U^T] \\ 
      & = \Lambda \mathbb{E}[f f^T] \Lambda^T + \mathbb{E}[U U^T] \\ 
      & = \Lambda \Lambda^T + \Sigma \\ 
      & = \Psi
   \end{align}
   $$

   and so the basic question is this: If we have a Gaussian population with mean $\mu^\ast$ and covariance matrix $\Psi^\ast$, is there a factor analysis model that can generate this population? The mean is trivial as the sample mean. The question is: what conditions must $\Psi^\ast$ satisfy so that $\Psi^\ast = \Lambda \Lambda^T + \Sigma$ can be solved? 

   Note that if $f$ is normally distributed with covariance $M$, then $\Psi = \Lambda M \Lambda^T + \Sigma$, but by the orthogonality problem, we can just restrict $M = I$. 

   So back to the question, and this has two components. First is the number of unknowns to the number of equations, and second is that if there is such a solution, does this give us a positive-definite matrix? We can expand out the matrix equation as a system of polynomials. 

   $$ 
      \psi_{ii} = \sigma_{ii} + \sum_{\alpha = 1}^m \lambda_{i \alpha}^2, \qquad \psi_{ij} = \sum_{\alpha = 1}^m \lambda_{i \alpha} \lambda_{j \alpha} \text{ for } i < j
   $$

   It turns out that the number of equations and conditions minus the number of unknowns is 
   $$
      C = \frac{p (p + 1)}{2} + \frac{m (m - 1)}{2} - p - pm 
   $$
   which we need to check if it is solvable, and if so, if it is solvable in the reals. 


