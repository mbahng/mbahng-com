[[2025dheur_conformal-scores-multi.pdf]]
#others
[[2024sun_sparsity-score]], [[2024willard_protopnext]] 

# Definition 

   Conformal prediction (CP) is an algorithm for uncertainty quantification that produces statistically valid prediction regions (multidimensional prediction intervals) for any underlying point predictor. Consider a regression problem with a data distribution $p_{X \times Y}$ over $\mathbb{R}^n \times \mathbb{R}^m$. Given a trained regressor $h: \mathcal{X} \subset \mathbb{R}^n \to \mathcal{Y} \subset \mathbb{R}^m$, on a train set, say that you have some new sample $x_0 \in \mathcal{X}$ that you want to predict. You might predict $\hat{y}_0 = \hat{h}(x_0)$, but another reasonable prediction might be $\hat{y}_0 + \epsilon$ for some small $\epsilon$. Therefore, we want to try and find a *region* $x \in \hat{R}(x) \subset \mathcal{Y}$ around that may consist of these valid predictions. 

   What's an intuitive way to do this? Well we can just define some sort of metric $d$ (called a **conformity score**) on $\mathcal{Y}$, and then set the region to be the open $r$-ball with respect to $d$
   $$
      \hat{R}(x) = B_d (x, r)
   $$
   If we don't assume homoscedacity, we can't even assume that $r$ is fixed, and so we should really be writing 
   $$
      B_d (x, r(x))
   $$

   There are two questions: how do we choose a metric $d$, and what should $r$ be? 

## Split Conformal Predictions

   Let's focus on choosing $r$. **Split-conformal predictions (SCP)** basically hold out a calibration dataset $\mathcal{D}_{cal}$. Once $d$ is chosen, for some fixed $x$, we basically compute the set of all distances 
   $$
      \{s(x, y) \mid (x, y) \in \mathcal{D}_{cal} \}
   $$
   and compute the empirical $\alpha$-percentile, denoted $\hat{q} = \hat{q}_\alpha$. If the data generating process is homoskedactic, then we have an unbiased estimator of the probability of landing in the region. This is called **marginal coverage**. 
   $$
      \mathbb{P}_{X, Y, \mathcal{D}_{cal}} (Y \in \hat{R}(X)) = \mathbb{P}(s(X, Y) \leq \hat{q}) \geq 1 - \alpha
   $$

   But there is bias in here due if there is heteroskedacity, so ideally, we should be conditioning this on $x$, i.e. achieving **conditional coverage**, where the LHS is the probability over the conditional distribution $Y \mid X = x$, and the calibration dataset. 
   $$
      \mathbb{P}(Y \in \hat{R}(X) \mid X = x) \geq 1 - \alpha 
   $$
   Apparently, achieving conditional coverage is generally impossible without making additional assumptions. 

## Density Conformal Metrics

   Now let's talk about how to choose a metric within the context of SPD. There are two
   1. DR-CP: Assuming that we have a probabilistic model that can model the conditional distribution $f(y \mid x)$, we can define 
   $$
      s(x, y) = -f(y \mid x) 
   $$
   which basically sets the region around $y$ to be some higher probability. The weakness is that in the SPD scheme, the quantile threshold $\hat{q}$ doesn't depend on $x$. 

   2. C-HDR. This is a based on the *highest predictive density (HPD)*, defined 
   $$
      HPD_f (y \mid x) = \mathbb{P}_{\hat{Y} \sim \hat{f}( \cdot \mid X)}\big[ \hat{f}(\hat{Y} \mid x) \geq \hat{f}(y \mid x) \mid X = x\big]
   $$
   and then they define the threshold. 

   3. PCP. Let $\tilde{Y}^{(l)}$ denote $L$ samples from the estimated conditional distribution $\hat{f}(Y \mid x)$. Then, *probabilistic conformal prediction*  defines the conformity score as the distance to the closest point. 
   $$ 
      s(x, y) = \min_{l \in [L]} \| y - \tilde{Y}^{(l)} \|, \qquad \tilde{Y}^{(l)} \sim \hat{f}(Y \mid x) 
   $$
   So the region $\hat{R}(x)$ is just the union of $L$ open balls centered at each sample, with radius $\hat{q}$. 


# CDF-Based Conformity Scores

   Now let's get to the actual contributions. Given a method already with a conformal score 
   $$
      s_W (x, y)
   $$
   we define a *new* score. Consider the random variable $W = s_W (X, Y)$, which is the distribution of all possible scores. 
   $$
      s_{CDF} (x, y) = \mathbb{P}_{W \mid X = x}\big[ W \leq s_W (x, y) \mid X = x\big]
   $$
   What does this mean? Our inputs $(x, y)$ are fixed. We already know $s_W (x, y)$, which is also fixed. Now look at the conditional distribution $W \mid X = x$, which is really just random in $Y$. It is the distributions of scores of $y$ with respect to fixed $x$. If $s_W (x, y)$ is large, then $x$ and $y$ aren't very similar, and we have a higher threshold compared to if $s_W (x, y)$ is small. 

   Apparently, it has the nice property that this distribution is independent of $x$, and so this achieves conditional coverage! But in practice, $s_{CDF}$ is approximated using monte carlo. 
   $$
      s_{CDF} (x, y) \approx \frac{1}{K} \sum_{k \in [K]} 1 [ s_W (x, \hat{Y}^{(k)}) \leq s_W (x, y) ], \qquad \hat{Y}^{(k)} \sim \hat{f}_{Y \mid X = x}
   $$

   1. This method applied to DR-CP gives us C-HDR, so it's a method to "HPD-ify" an existing conformal score.
   2. If we apply this to PCP, then we get C-PCP, with a new conformal score of 
   $$
      s_{C-PCP}(x, y) = \frac{1}{K} \sum_{k \in [K]} 1 \bigg[ \min_{l \in [L]} \| \hat{Y}^{(k)} - \tilde{Y}^{(l)} \| \leq \min_{l \in [L]} \| y - \tilde{Y}^{(l)} \| \bigg]
   $$
   This has the advantage of not requiring the estimation of a predictive density $\hat{f}$, replying instead on samples from the conditional distribution. So, this can be applied to with any generative model, even if it doesn't give an explicit density. 

## Latent-Based Conformity Scores 

   Latent-based conformity scores are probably the most powerful, but it only applies for the most restrictive class of models: generative and invertible (e.g. normalizing flows). Let $\hat{Q}: \mathcal{Z} \times \mathcal{X} \to \mathcal{Y}$ denote such a model, which maps latent variable $Z \in \mathcal{Z}$ to output space $\mathcal{Y}$ conditional on input $X \in \mathcal{X}$. 

   Since it is invertible, we have 
   $$
      \hat{Q} ( \hat{Q}^{-1} (y ; x); x)
   $$
   for all $x \in \mathcal{X}, y \in \mathcal{Y}$. Note that $\hat{Q}^{-1} (y ; x)$ takes input $y$ and outputs the corresponding $z$ in the Gaussian latent space that maps to $y$. Therefore, a natural measure would just be to look at the pdf. If the $z = \hat{Q}^{-1} (y ; x)$ ends up being close to $0$, then the likelihood of $y$ is high, and so $s(x, y)$ should be similar. This motivates the following 
   $$
      s_{L-CP} (x, y) = \| \hat{Q}^{-1} (y ; x) \|
   $$



