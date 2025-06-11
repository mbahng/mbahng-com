[[2012krizhevsky_alexnet.pdf]]
#architecture
[[1998lecun_lenet]]

# Contributions 
   Implemented a large convnet (5 conv + 3 FC) to achieve SOTA accuracy on ImageNet-1K of top-1 62.5% and top-5 83%. 

# Background 


# Architecture and Training

   5 conv layers and 3 FC layers for a total of 60M parameters. 

   Even removing one of the conv layers (less than 1% of total weights) resulted in drop of 2% performance. 

   Takes 5-6 days with 2 3GB memory GPUs. 

   Apparently ReLUs train 6x faster compared to tanh activations, so used them. 

   Distribute across 2 GPUs, which gave them flexibility to limit communication between layers. 

   Used local (layer?) normalization, though ReLUs don't really need it for gradient saturation. 

   Did overlapping max pooling, i.e. max pooling windows overlap each other, which increased acc by about 0.4%. 

   Apparently weight decay is also important not as a regularizer, but also to reduce training error. 

   Equal learning rate for all layers. When error plateaued, reduce LR by 0.1.  

# Data Augmentation and Multiview Voting
   
   Generating image translations and horizontal reflections. Image is 256x256. Extract random 224x224 patches (and horizontal reflections) and use them to train. This increases training set by factor of 2048. We need to do data augmentation, otherwise the net overfits heavily, forcing us to use smaller network. At test time, network makes prediction by extracting 5 224x224 patches (4 corners and center) along with horizontal reflexctions (10 patches in total) and averages predictions. 

   Second way of augmenting is altering intensities of RGB channels in training images. Do PCA and scale the corresponding eigenvalue by random Gaussian. 
