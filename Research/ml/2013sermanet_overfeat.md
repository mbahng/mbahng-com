[[2013sermanet_overfeat.pdf]] 

[[2012krizhevsky_alexnet.md]]

# Contribution

   Introduced new CNN architecture that got 1st on ImageNet 2013 competition. 14.18% error rate for accurate model, and ensemble of 7 accurate models gives 13.6% error. 

# Background 

   At this point, classification is getting significantly easier. Most pictures in datasets are centered objects that fills up much of the image, but this is not always the case in practice. There are two generalizations/levels of this problem, with each task being a subtask of the next (there is also the problem of semantic segmentation, which is also relevant). 

   1. *Classification*. 
   2. *Localization*. 
   3. *Detection*. 

# Classification Architecture and Training 

   They have two models. The specific architecture is in the tables in the paper. Both totaling about 145M parameters compared to AlexNet of 60M, but num of connections are significantly different.  
   1. *Fast model* has 5 conv layers plus 3 FC layers. 2810M connections. 
   2. *Accurate model* has 6 conv layers plus 3 FC layers. 5369M connections. 

   Employ multiscale classification by extending multiview voting from AlexNet (224x224 patches from 256x256). Densely run the network at each location and at multiple scales for more flexibility. 

   Usually our subsampling leads to a ratio of say 36x, i.e. every 36x36 pixels, we have a scalar classifying. But our goal is to get the object as filled and in the center as possible, so we subsample with offset/overlap (so that we are not partitioning the image in the end), leading to a smaller ratio of say 12x. 
   1. For single image, start with unpooled layer 5 feature maps. 
   2. Each unpooled maps undergoes 3x3 max pooling operation (non-overlapping regions), repeated 3x3 times for $(\Delta_x, \Delta_y)$ pixel offsets of $\{0, 1, 2\}$. 
   3. This produces a set of pooled feature maps, replicated $3 \times 3$ times for different $(\Delta_x, \Delta_y)$ combinations. 
   4. The classifier has a fixed input size of $5 \times 5$ and produces a $C$-dimensional output vector for each location within pooled maps. The classifier is applied in sliding window fashion to the pooled maps, yielding $C$-dimensional output maps for a given $(\Delta_x, \Delta_y)$ combination. 
   5. The output maps for different $(\Delta_x, \Delta_y)$ combinations are reshaped into a single 3D output map (two spatial dimensions and $C$ classes). 

   ![image](ml/img/overfeat_arch.png)

   This is computationally fine since we're working with convnets, and by including the padding we aren't really adding too much computation. 

   ![image](ml/img/overfeat_conv_fine.png)

