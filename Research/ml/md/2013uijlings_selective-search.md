[[2013uijlings_selective-search.pdf]] 

[[2004lowe_sift]], [[2004felzenszwalb-graph-image-seg]] 

# Contribution 

   Implements a bottom-up approach to do efficient image segmentation. 

# Background 
   
   Object recognition usually is done by randomly sampling or exhaustive search (with coarse grids if too computationally heavy). This is inefficient and may not have different scales. Furthermore, there are many different ways to compare,e.g. texture or color, so there are too many edge cases. Therefore, we want a data driven approach. 

# Implementation 

   First use graph-based image segmentation to get a good initialization of a bunch of chunks $c$ in the image. Then for every pairwise chunks that touch $(c_i, c_j)$, we compute the similarity between the two $s(c_i, c_j)$ with the following component functions. 
   1. color. Similar color means they're probably part of the same object. Use color histograms for this. 
   2. texture. Similar texture means they're probably part of the same object. Use SIFT for this. 
   3. size. Small regions should merge early. 
   4. fill. Regions that fit into each other well should be merged early. 
   So the total similarity is the combination of the four. 

   $$
      s(r_i, r_j) = a_1 s_colour(r_i, r_j) + a_2 s_texture(r_i, r_j) + a_3 s_size(r_i, r_j) + a_4 s_fill(r_i, r_j)
   $$

   Then these are greedily merged starting with the pairs that have the highest similarity, and we continue on until we hit a threshold. 
