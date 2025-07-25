[[2009wright_robust-pca.pdf]]
#dimensionality-reduction #pca #pca-robust
[[2003torre_robust-pca-framework]]

# Contribution

   Defines RCPA as decomposition of $n \times p$ matrix C into a sum of two $n \times p$ matrices, a low rank component $L$ and sparse component $S$. More precisely, a convex optimization problem was defined as identifying the matrix components of $X = L + S$ that minimize a linear combination of two different norms of the components. 

   $$
      \min_{L, S}\|L\|_\ast + \lambda \|S\|_1
   $$

   where $\|L\|_\ast$ is the sum of the singular values of $L$ and $\|S\|_1$ is the $L_1$ norm. The motivation for such a decomposition is that in many applications, low-rank matrices are associated with a general pattern (e.g. the correct data in a corrupted dataset, a face in facial recognition), whereas a sparse matrix is associated with disturbances (corrupted data values, light/shading in faces). Sparse components are also called noise. 

