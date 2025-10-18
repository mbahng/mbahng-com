[[2014dinh_nice.pdf]]
#deep-learning
[[2013kingma_vae]], [[2015rezende_normalizing-flow]]  


In unsupervised learning, we have a random variable $x \in \mathbb{R}^D$ and want to find a good representation for it. One nice property to have is that we may want the distribution of $x$ to factorize into independent components. 
$$
   p(x) = \prod_{d=1}^D p_d (x_d)
$$

Therefore, we can take the data distribution $X$, and transform it into such a decomposable distribution through a differentiable function $f: \mathbb{R}^D \to \mathbb{R}^D, Z = f(X)$ such that 
$$
   p_Z (z) = \prod_{d=1}^D p_{Z_d} (x_{Z_d})
$$
So by the change of variable formula, we can calculate the pdf $p_X (x)$ 
$$
   p_X (x) = p_Z (f(x)) \cdot \bigg| \mathrm{det} \frac{\partial f}{\partial x} (x) \bigg| 
$$
the determinant may be nontrivial to calculate, so we restrict our scope to functions $f$ that have trivial determinants. However, we only have estimates of the density, so the best we can do is MCMC to sample from $X$. Therefore, we restrict our attention further by assuming $f$ is locally invertible everywhere. Therefore, the two properties 
1. easy determinant of Jacobian, and 
2. easy inverse 
allows us to have a lot of model capacity while easy to calculate. 
