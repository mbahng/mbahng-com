[[2021nauta_prototree.pdf]]
#interpretable
Cites: [[2019chen_protopnet]]
## Contribution. 

   Extends the original ProtoPnet model by using a soft decision tree to classify rather than minimum distance. Outperforms original with only 10% of the number of prototypes. 

## Model Inference. 

   1. Take image $x$ with label $y$ and forward it through the CNN backabone $f(x) = z$. The latent embedding with the CNN is the same of output shape $(D, H, W)$ consisting of $HW$ patches of shape $(D, 1, 1)$. 

   2. This now gets inputted into a soft binary tree (it must be soft to allow backpropagation). Tree consists of set of internal nodes $\mathcal{N}$, leaf nodes $\mathcal{L}$, and edges $\mathcal{E}$. Each internal node $n \in \mathcal{N}$ has 2 child nodes $n.left$ and $n.right$ connected by $e(n, n.left), e(n, n.right) \in \mathcal{E}$. Each internal node $n \in \mathcal{N}$ corresponds to trainable prototype $p_n \in P$, where $p_n$ is of size $(D, 1, 1)$. Each leaf node $\ell \in \mathcal{L}$ does *not* correspond to a class! It is just a representation of a sample in terms of which prototypes it has and does not have. 

   3. With $p_n$, we compute the minimum distance between $p_n$ and all patches in $z$, and this distance determines to what extent the prototype $P$ is present anywhere in the image. This score influences the routing f the sample either right or left (but in a soft way so that it routes through both probabilistically). The probability of routing $z$ to right edge is defined 

   $$
        p_{e(n, n.right)} (\tilde{z}) \coloneqq \exp(- \| z^\ast - p_n \| ), \qquad \tilde{z}^\ast \coloneqq \arg \min_{\tilde{z} \in patches(z)} \| \tilde{z} - p_n \|
   $$   
   with of course $p_{e(n, n.left)} (\tilde{z}) \coloneqq 1 - p_{e(n, n.right)} (\tilde{z})$ 

   4. The path to leaf node $\ell \in \mathcal{L}$ is denoted as $P_\ell$ and the total probability of classification is simply the product of probabilities of edges in path $P_\ell$ 
   $$
        \pi_\ell (z) = \prod_{e \in P_\ell} p_e (z) 
   $$

   Each leaf node also carries trainable parameter $c_\ell \in \mathbb{R}^K$ (where $K$ is the number of classes), denoting the logits of the classes. The softmax is therefore $\sigma(c_\ell)$. 

   5. Therefore, once a sample is taken, we take a weighted sum of the probability distribution to get our global prediction. 

   $$
        \hat{y}(x) = \sum_{\ell \in \mathcal{L}} \sigma(c_\ell) \cdot \pi_\ell (f(x))
   $$

## Training. 

   1. The backpropagation process is straightforward since we have closed forms of the equation. Both the internal node prototypes $p$ and the backbone weights are trained according to CE.  

   2. The leaf nodes $c$ are updated iteratively with a non-gradient strategy since apparently it is a convex problem. 

   3. Leaf nodes with uniform distributions are pruned. 

## Results. 

    1. CUB-200-2011. ProtoPnet (79.2), Triplet Model (87.5), 5-Ensemble ProtoTree (87.2)

    2. Stanford Cars. ProtoPnet (86.1), RAU (93.8), 5-Ensemble ProtoTree (91.5)
