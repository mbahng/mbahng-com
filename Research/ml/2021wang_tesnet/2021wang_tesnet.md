[[2021wang_tesnet.pdf]]
#interpretable #prototype
[[2019chen_protopnet]]

# Background
Protopnet may have entangled prototypes in the latent space due to minimization of the L2 distance. Ideally, we would like the prototypes within a class to be orthogonal. 

# Contribution
Present a plug-in architecture of transparent embedding space spanned by transparent basis concepts. The prototypes are both: 
1. category-aware, i.e. know which class they represent, and 
2. within-category prototypes are orthogonal to each other. 

# Inference 
Let the train dataset be denoted $\mathbf{X}$, with $X^{(c)} \subset X$ representing the subset belonging to class $c$ (from $c = 1, \ldots, C$)$.  Given input image $x$, we first feed it through a conv backbone (resnet, vgg, densenet) as a feature extractor. 
$$
x \xrightarrow{f} Z \in \mathbb{R}^{D \times W \times H}
$$
The next layer is the transparent subspace layer $s_b (\cdot)$, which is parameterized by $M$ $D$-dimensional basis concepts (aka the prototypes) for each class. So there are a total of $MC$ basis concepts, denoted as $\mathbf{B} = \{\{b_j^{(1)}\}_{j=1}^{M}, \dots, \{b_{j}^{(C)}\}_{j=1}^{M} \}$, denoted as $\mathbf{B} = \{b_{j}\}_{j=1}^{MC}$ for convenience. Note that the $j$ indexes the prototypes. For every prototype $j$ , we dot it with the $WH$ patches in $Z$ and max pool. 
$$
s_{b_{j}} (Z) = \max_{p \in \mathrm{patches}(Z)} p^T b_j
$$
Doing this over all $j =  1, \ldots MC$	 gives us a $MC$-vector of activations of the image with each prototype. Then, the final step is to input through a linear layer $G: \mathbb{R}^{MC} \to \mathbb{R}^{C}$, so a simple matrix, giving us the logits. 

# Training
We want to impose some constraints in building our loss. 
1. The basis concepts should be orthogonal within each class. Letting $B^{(c)} \in \mathbb{R}^{M \times D}$ denote the basis vectors for each class, we can impose orthogonality by minimizing 
$$
\mathcal{L}_{\mathrm{orth}} = \sum_{c=1}^C \| B^{(c)} (B^{(c)})^T - \mathbb{I}_{M} \|_{F}^2
$$
2. To separate the class aware subspaces, we want to minimize this metric. 
$$
\mathcal{L}_{ss} = -\frac{1}{\sqrt{ 2 } } \sum_{c_1 = 1}^{C - 1}  \sum_{c_2 = c_{1} + 1}^{C} \| B^{(c_{1}) T} B^{(c_{1})} - B^{(c_{2}) T} B^{(c_{2})} \|_{F}
$$
	Apparently there is some Grasmann manifold stuff here. We model the latent space not simply as Euclidean space, but as the set of all $M$-dimensional subspaces of $\mathbb{R}^D$, which turns out to be compact smooth manifold. Apparently there exists one unique projection matrix for each point on the manifold, and from this we can build a metric on this manifold to distinguish the distance between points, i.e. subspaces. 
3.  Projecting the patches to the embedding subspaces should preserve essential information. Therefore, we should encourage patches to be close to at least one basis vector of ground truth class (compactness) and stay away from basis vectors of other classes (separation).  Given basis vectors $B = \{b_j\}_{j=1}^{MC}$ with $\|b_j\| = 1$, and patches of the feature map $\{Z_i\}_{i=1}^{n}$, where $i$ indexes the sample, the compatness-separation loss is 
$$
\begin{align}
\mathcal{L}_{\mathrm{compactness}} & = \frac{1}{n} \sum_{i=1}^n \min_{j : b_{j} \in B^{(y_{i})}} \min_{p \in \mathrm{patches}(Z_{i})} -\frac{p^T b_{j}}{\|p\|} \\
\mathcal{L}_{\mathrm{separation}} & = \sum_{i=1}^n \min_{j : b_{j} \not\in B^{(y_{i})}} \min_{p \in \mathrm{patches}(Z_{i})} \frac{p^T b_{j}}{\|p\|} 
\end{align} 
$$
	and $\mathcal{L}_{cs} = \mathcal{L}_{\mathrm{compactness}} + \mu \mathcal{L}_{\mathrm{separation}}$. 
4. The identification loss is simply cross entropy. Letting $\phi_c$ denote the $c$th element of the entire network $\phi$, it is 
$$
\mathcal{L}_{\mathrm{id}} = -\frac{1}{n} \sum_{i=1}^n \sum_{c=1}^C y_{ic} \log \phi_c (x_i)
$$

We therefore minimize with backprop the following 
$$
\mathcal{L}_{\mathrm{total}} + \lambda_1  \mathcal{L}_{\mathrm{id}} + \lambda_2 \mathcal{L}_{\mathrm{orth}} + \lambda_3  \mathcal{L}_{\mathrm{ss}} + \lambda_4 \mathcal{L}_{\mathrm{cs}}
$$
## Transparency Projection 
Like ProtoPnet, you want to make sure each basis concept is mapped directly to each prototype. So, we can update the $j$th prototype of class $c$ to be 
$$
b_j \leftarrow \arg\max_{p \in \mathcal{P}_c} p^T b_j
$$
where $\mathcal{P}_c = \{ \tilde{p} \mid \tilde{p} \in \mathrm{patches}(Z_i) \forall i \text{ s.t. } y_i = c \}$ . Then we initialize the matrix $G$ by initializing $G_{(c, j)} \approx 0$ if $j$th unit doesn't belong to $c$th class, and we initialize it at $-0.5$. 
