[[2019chen_protopnet.pdf]]
#deep-learning:interpretable:prototype
[[2018li_prototypeautoencoder]]
# Background. 

# Contribution. 

This is the first implementation of the protopnet, which provides an interpretable alternative to black box neural nets. 

## Model Inference. 

A convolutional backbone that maps the original image to a latent space $f: \mathbb{R}^{224 \times 224 \times 3} \to \mathbb{R}^{D \times 7 \times 7}$. We can think of each image as being embedded as a set of $7 \times 7 = 49$ vectors in a $D$-dimensional space, called patches.

Assuming that there are $K$ classes. The network is built so that for every class, there are $P$ prototypes of shape $D \times 1 \times 1$. So during inference, it takes the image, embeds it to shape $(D, 7, 7)$ and for each of the $KP$ total prototypes, we compare each prototype to each patch (a total of $49KP$ comparisons) and find the prototype that has maximum similarity (either negative L2 distance or cosine similarity). 

With this collection of all similarity scores, we use a fully connected layer to predict. the logits of the proper class. 

## Training. 

You are essentially training the backbone, prototype, and FC weights. 

There is a warm, joint, last (FC) layer training epoch. 

There is also a projection/push epoch where the prototypes are projected onto the nearest patch of a given class. This is so that we can absolutely match a prototype with a patch in the latent space, which will correspond to a heatmap of the original image, giving us the diagrams in the paper. 

Dataset is CUB only. 

Loss is custom, with CE loss for the classifier along with ones for prototypes. Cluster loss tries to minimize the distances between each prototype and its nearest patch (for high confidence). Separation loss tries to maximize distances between a prototype of one class and all other prototypes of different classes, since different birds will have different features. 

## Results


