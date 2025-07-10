[[1936eckart_pca-with-svd.pdf]]
#dimensionality-reduction #pca
[[1933hotelling_pca]]

# Contribution 

   Introduces the SVD method of PCA, plus some other results. 
   1. Take SVD, take all diagonal entries past some rank and set to $0$. This is your best L2 approximation. 
   2. The original data matrix is known as the **score matrix**. 
   3. Given score matrix $A$ with best approximation $\alpha$, then $\alpha^T \alpha$ and $\alpha \alpha^T$ is the best approximation of $A^T A$ and $A A^T$. 
   Therefore, this problem reduces to having good eigensolvers. 
