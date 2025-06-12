[[1998lecun_lenet.pdf]]
#architecture 
[[1958rosenblatt_perceptron]]


# Contributions 

   Introduces both MNIST handwritten digits datasets and CNNs. Very nice historical summary of the field. 

# Background

## Alternative Bias Variance Decomposition 

   States that much theoretical and experimental work shows that gap between expected error on train and test decreases as 
   $$
      E_{\mathrm{test}} - E_{\mathrm{train}} = k (h/P)^\alpha 
   $$
   where $P$ is number of training samples, $h$ is a measure of effective capacity/complexity of machine, $\alpha$ is a number between $0.5$ and $1$, and $k$ is a constant. Gap decreases when number of training samples increases. Furthermore, as capacity $h$ increases, $E_{\mathrm{train}}$ decreases while increasing the gap, with some optimal value $h$ achieving lowest generalization error.  

## Motivation 

   Machines usually consists of manual feature extractor and trainable classifier. What if we try to train the feature extractor? There is an explosion of complexity for images, requiring as above much larger training sets. If we did learn it, we would probably have multiple units with similar weight patterns that depends only on location in the input. We want invariance. 

   Images have strong 2D local structure. Variables (pixels) that are spatially/temporally nearby are highly correlated. This is why it is easy to extract local features. CNNs force extraction of local features by restricting receptive fields. 

# Architecture 

   Generic architecture is LeNet, with conv into 6 planes (channels), subsampling, conv, subsampling, 2 FC layers, and 1 gaussian connections (?). 

   Once feature is detected, exact location becomes less relevant.

# MNIST 

   Constructed database from NIST's special database 3 and 1. Originally split was 50 50, and worked with 20x20, 28x28, and 32x32 sizes. 

# Traing 

   Convergence after 10-12 epochs, with 99%+ accuracy on both train and test sets. 

   Usually overfitting happens, but they didn't observe this. Concluded because the learning rate was quite large, so it bounces around a lot and never settles down on local minimum. In a way, SGD has similar effect on regularization that favors broader minima. 

