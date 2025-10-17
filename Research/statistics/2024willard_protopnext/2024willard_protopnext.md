[[2024willard_protopnext.pdf]]
#deep-learning:interpretable:prototype
[[2021donnelly_deformable-protopnet]]

# Background

# Contribution

   Training ProtoPnets is hard since there is no systematic way to do it. 
     - It introduces a new framework for implementing and training descendant models of ProtoPnet. 
     - New sparsity metric as early stopping criterion
     - Bayesian hyperparameter tuning 
     - Angular prototype similarity metric. 
     - New objective based off of accuracy and prototype quality. 
   Achieves SOTA accuracy. 

# Interface

Every ProtoPnet can be divided into  
1. an embedding layer $f: \mathbb{R}^{C \times H \times W} \to \mathbb{R}^{D \times H^\prime \times W^\prime}$ mapping the image to a $D$-dimensional latent space of $HW$ patches, also called *perceptive fields*. 
2. a prototype later $g: \mathbb{R}^{D \times H^\prime \times W^\prime} \to \mathbb{R}^{P \times H^{\prime\prime} \times W^{\prime\prime}}$ which computes the similarity of each of the $P$ prototypes to the input at each of the $H^{\prime\prime}$ by $W^{\prime\prime}$ center locations. (?)
3. a class prediction head for the global classification logits $h: \mathbb{R}^{P \times H^{\prime\prime} \times W^{\prime\prime}} \to \mathbb{R}^K$. 
    
Remember that in almost (except for ProtoConcept) all variants, a projection/push step is performed during and at the end of training. 

# Prototype Metrics. 

   1. **Sparsity**. Quantifies amount of unique prototypes used by a model. 

   2. **Stability**. Measures the invariance of prototype activation to Gaussian noise added to the image. 

   3.  **Consistency**. Measures how frequently a prototype activates on the same semantic part of the image. 

   4. Just average all of these to optimize the prototype score. 

   $$
        v_{proto\_score} = \frac{v_{sparse} + v_{consist} + v_{stab}}{3}, \qquad objective = v_{acc} \cdot v_{proto\_score}
   $$

# Prototype-Aware Early Stopping 

   1. Patience is number of projection epochs without improvement. (?) 

# Results. 

   1. They just take original ProtoPnet (and DeformableProtoPnet) and replace L2 distance with cosine similarity, which improves accuracy. This is why DeformableProtoPnet and TesNet is superior, since they already use cosine similarity. 

   2. They do systematic Bayesian hyperparameter tuning. 

   3. Joint optimization (optimizing both accuracy and protoscore) substantially improves interpretability metrics without much cost to accuracy. 

# Citations
[[2019chen_protopnet]]
[[2021nauta_prototree]]
