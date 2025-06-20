[[2014weston_memory-nets.pdf]]
#memory # qa
[[2015bahdanau_neural-machine-translation]] 

# Contribution 

   Introduced a new neural net architecture for storing memory and retrieving it based on context. It can learn from both general information and from specific stories inputted sequentially. Closely related to QA (question-answer). 

# Background 

   RNNs are bad at storing memory as hidden states gets deteriorated over time. The embeddings are also dense, and compression is most likely lossy. Therefore, we want to have some sort of non-degrading memory units. Even better, if it has some organizational structure (like wikipedia). 

# Architecture 

   We consider 4 parts: IGOR. Let the input be called $x$ and the memory units be $\mathbf{m}_i$. 

   1. Input: takes the input and converts it into feature representations. We can do standard preprocessing, feature extraction, or learned embeddings: 
   $$
      x \mapsto I(x)
   $$

   2. Generalization: Updates old memories given the new input. 
   $$
      \mathbf{m}_i = G(\mathbf{m}_i, I(x), \mathbf{m})
   $$
   The $i$ represents which memory address $I(x)$ is stored in. 

   3. Output: Takes entire memory to compute output: 
   $$
      o = O(I(x), \mathbf{m})
   $$ 

   4. Response: Converts output to response format desired: 
   $$
      r = R(o)
   $$

   They talk specifically about implementations of each module, in the context of text generation, but it is generalizable. 

## Input 

   There isn't much to talk about input. 

## Generalization

   For generalization, the simplest form is to simply store $I(x)$ into a slot of memory. 
   
   $$ 
      \mathbf{m}_{H(x)} = I(x)
   $$

   More sophisticated variants could update previous memory slots. Also, we can also simulating "forgetting" by overriding stuff. For efficiency, $G$ and $O$ need not operate on all memories. All this is case by case. 

   Doing simple storing scales linearly, which is not good (e.g. Wikipedia). Therefore, they suggest a hashing mechanism where you hash $I(x)$ into one or more buckets and then only score memories $\mathbf{m}_i$ that are in the same buckets. Two ways. 
   1. Hashing words. Construct as many buckets as there are words in the dictionary. For a given sentence, hash it into all the buckets corresponding to its words. The problem is that memory $\mathbf{m}_i$ will only be considered if it shares words with $x$, which may not always be the case. 
   2. Clustering word embeddings. After training embedding matrix $U_O$, we run $K$-means to cluster the word vectors $(U_O)_i$, giving $K$ buckets. We then hash a given sentence into all the buckets that its individual words fall into. This is intuitive, since similar words tend to be close to each other, and so similarity scores will be similar as well. Choosing $K$ controls the speed-accuracy trade-off. 

## Output 

   The output module produces output features by finding $k$ supporting memories given $I(x)$. For $k = 1$, we have the following, though it is generalizable to higher $k$. 

   $$
      o_1 = O_1(x, m) = \arg\max_{i=1,\ldots,N} s_O(x, m_i)
   $$ 
   where $s_O$ is a scoring function that determines the similarity of $x$ with memory $m$. They implement it as simply matrix multiplication. 

   $$
      s(x, y) = \Phi_x(x)^T U^T U \Phi_y(y), \qquad U \in \mathbb{R}^{n \times D}
   $$

   where $D$ is the number of features and $n$ is the embedding dimension. The role of $\Phi_x$ and $\Phi_y$ is to map the original text to the $D$-dimensional feature space. The simplest feature space to choose is a bag of words representation, we choose $D = 3|W|$ for $s_O$, i.e., every word in the dictionary has three different representations: one for $\Phi_y(\cdot)$ and two for $\Phi_x(\cdot)$ depending on whether the words of the input arguments are from the actual input $x$ or from the supporting memories so that they can be modeled differently. Similarly, we used $D = 3|W|$ for $s_R$ as well. $s_O$ and $s_R$ use different weight matrices $U_O$ and $U_R$.

   For general $k$, the final output is $[x, \mathbf{m}_{o_1}, \ldots, \mathbf{m}_{o_k}]$, which is the input to the response module $R$. 
   
## Response

   Finally, the output needs to generate a word. In the simplest case, we can look at all the words in our dictionary $w \in W$ and output the best matching word given our context memory. 

   $$
      r = \argmax_{w \in W} s_R([x, m_{o_1}, m_{o_2}], w)
   $$

   where $s_R$ is some score function determines similarity of $x$ to memory $m$. It is implemented in the same way as $s_O$. The simplest feature space is to choose a bag-of-words representation, so $D = 3 |W|$. So every word in the dictionary has 3 representations. 

   In other cases, we can use a RNN to generate the output. 

# Training 

   Fully supervised, with desired inputs (with labeled supporting sentences) and outputs. That is, we know the choice of the argmax $o_1, \ldots$ above. Specifically, for a given question $x$ with true response $r$ and supporting sentences $\mathbf{m}_{o_1}$ and $\mathbf{m}_{o_2}$ (when $k = 2$), we minimize over model parameters $U_O$ and $U_R$. This loss is 

   $$
      \sum_{\tilde{f} \neq m_{o_1}} \max(0, \gamma - s_O(x, \mathbf{m}_{o_1}) + s_O(x, \tilde{f})) + \\ 
      \sum_{\tilde{f}' \neq m_{o_2}} \max(0, \gamma - s_O([x, m_{o_1}], m_{o_2}) + s_O([x, \mathbf{m}_{o_1}], \tilde{f}')) \\ 
      \sum_{\tilde{r} \neq r} \max(0, \gamma - s_R([x, m_{o_1}, m_{o_2}], r) + s_R([x, m_{o_1}, m_{o_2}], \tilde{r})) 
   $$

   where $\tilde{f}$, $\tilde{f}'$ and $\tilde{r}$ are all other choices than the correct labels, and $\gamma$ is the margin. At every step of SGD we sample $\tilde{f}$, $\tilde{f}'$, $\tilde{r}$ rather than compute the whole sum for each training example. 

   To break down this loss, 

   1. Line 1: First supporting sentence selection

   - $s_O(x, m_{o_1})$ scores how well the correct first supporting sentence matches the question
   - $s_O(x, \tilde{f})$ scores how well an incorrect candidate sentence matches the question  
   - The loss ensures the correct sentence is ranked higher than incorrect ones by margin $\gamma$

   2. Line 2: Second supporting sentence selection

   - $s_O([x, m_{o_1}], m_{o_2})$ scores the correct second sentence given the question and first sentence
   - $s_O([x, m_{o_1}], \tilde{f}')$ scores an incorrect second sentence candidate in the same context
   - The loss ensures the correct second sentence is ranked higher than alternatives by margin $\gamma$

   3. Line 3: Response generation

   - $s_R([x, m_{o_1}, m_{o_2}], r)$ scores the correct response given question and both supporting sentences
   - $s_R([x, m_{o_1}, m_{o_2}], \tilde{r})$ scores an incorrect response candidate in the same context
   - The loss ensures the correct response is ranked higher than alternative responses by margin $\gamma$
