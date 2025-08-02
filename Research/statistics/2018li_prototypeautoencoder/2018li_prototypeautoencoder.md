[[2018li_prototypeautoencoder.pdf]]
#deep-learning:interpretable:prototype
[[2013zeiler_understandingcnns]]

# Background. 

   Lots of post-hoc interpretations on neural nets. Want another source of interpretability. Activation maps (AM) are too prone to confirmation bias since we are doing post hoc interpretation. We want the architecture itself to be interpretable. 

# Contribution

   Introduces an autoencoder based prototype network with a new prototype layer where each unit of that layer stores a weight vector that resembles an encoded training input. 

# Model Inference. 

   1. Take image $x \in \mathbb{R}^p$. Encoder $f: \mathbb{R}^p \to \mathbb{R}^q$ maps $x \mapsto z$ into latent space.  

   2. Decoder $g: \mathbb{R}^q \to \mathbb{R}^p$ maps $z \mapsto x$ back into image space, like a saliency map. 

   3. Prototype layer $h: \mathbb{R}^q \to \mathbb{R}^K$ is consisted of three parts. 

      i) A prototype layer $p: \mathbb{R}^q \to \mathbb{R}^m$ mapping latent encoding $z$ to a vector of similarity scores $p(z)$, paramaterized by $m$ prototype vectors $p_1, \ldots, p_m \in \mathbb{R}^q$, where the $i$th element of the output is the distance between $z$ and $i$th prototype. 
      $$
         p(z)_i = \| z - p_i \|^2 
      $$

      ii) A fully connected layer $w: \mathbb{R}^m \to \mathbb{R}^K$, where $K$ is number of classes. This is just a linear map to convert these distances into logits. 

      iii) A softmax layer $s: \mathbb{R}^K \to \mathbb{R}^K$.

# Training. 

   1. Training is straightforward through backpropagation, but we want to optimize for both CE and interpretability. 

   2. Standard CE optimizes $h \circ f$, denoted as $E$ in paper. 

   3. Reconstruction loss optimizes $g \circ f$, denoted as $R$. 

   4. Interpretability loss consists of $R_1, R_2$, which optimizes for the $p_1, \ldots, p_m$ in $h$ as 

   $$
      R_1 = \frac{1}{m} \sum{j = 1}^m \min_{i \in [n]} \| p_j - f(x_i) \|^2, \qquad 
      R_2 = \frac{1}{n} \sum{i = 1}^n \min_{j \in [m]} \| f(x_i) - p_j \|^2,
   $$

   $R_1$ encourages each prototype vector to be as close to at least one of training examples in latent space. $R_2$ requires every encoded training example to be as close to one of the prototype vectors. Sort of like a dual optimization problem. 

# Results. 

   1. Done on MNIST, some reconstruction of cars (not Stanford Cars), and FashionMNIST. 

   2. In three cases the decoded prototypes become very uninterpretable when removing $R_1, R_2$. Accuracy is comparable, losing approx 4%.
   
