[[2010mikolov_rnn-language.pdf]]
#deep-learning #natural-language-processing
[[1985rumelhart_rnn]], [[2003bengion_neural-prob-language-model]] 

# Contributions 

   First major application of language modelling with RNNs since Bengio's feedforward LM wasn't good. 

# Implementation 
   
   A vanilla RNN architecture, called Elman networks. At time $t$, i.e. at the $t$ element of the sequence, 
   1. Words are one-hot encoded $w(t)$. 
   2. Inputs are simply concatentations $x(t) = s(t-1) + w(t)$, where $+$ is concatenation. 
   2. Hidden layer is just matrix multiplication followed by element-wise activation: $s(t) = f(U x(t))$, where $f$ is sigmoid activation. 
   3. Output is $y(t) = g(V s(t))$, where $g$ is softmax to output probabilities. 

   Regularization didn't impact much, despite fears of overfitting. 

   To optimize performance, they merged all words that occur less than some threshold into a special rare token. So, when it generates words, if we detect that the word is rare, we sample uniformly over the rare tokens. 

   $$
      P(w_i(t+1)|w(t), s(t-1)) = \begin{cases} 
      \frac{y_{rare}(t)}{C_{rare}} & \text{if } w_i(t+1) \text{ is rare,} \\
      y_i(t) & \text{otherwise}
      \end{cases}
   $$ 

   Also should be the case that this is *dynamic*, meaning that since there can always be new words (like names) in the test set, we have the model also do learning over test. Develop several models of the form "RNN H/C", where $H$ is the hidden layer size and $C$ is the threshold, e.g. RNN 90/2. 

   Trained on WSJ dataset of 34M words, but only used 6.4M. Compares it with n-gram models with perplexity (PPL) and word error rate (WER) scores. 

   ### Table 1: Performance of models on WSJ DEV set when increasing size of training data

   | Model | # words | PPL | WER |
   |-------|---------|-----|-----|
   | KN5 LM | 200K | 336 | 16.4 |
   | KN5 LM + RNN 90/2 | 200K | 271 | 15.4 |
   | KN5 LM | 1M | 287 | 15.1 |
   | KN5 LM + RNN 90/2 | 1M | 225 | 14.0 |
   | KN5 LM | 6.4M | 221 | 13.5 |
   | KN5 LM + RNN 250/5 | 6.4M | 156 | 11.7 |

   ### Table 2: Comparison of various configurations of RNN LMs and combinations with backoff models while using 6.4M words in training data (WSJ DEV)

   | Model | PPL |  | WER |  |
   |-------|-----|-----|-----|-----|
   |  | RNN | RNN+KN | RNN | RNN+KN |
   | KN5 - baseline | - | 221 | - | 13.5 |
   | RNN 60/20 | 229 | 186 | 13.2 | 12.6 |
   | RNN 90/10 | 202 | 173 | 12.8 | 12.2 |
   | RNN 250/5 | 173 | 155 | 12.3 | 11.7 |
   | RNN 250/2 | 176 | 156 | 12.0 | 11.9 |
   | RNN 400/10 | 171 | 152 | 12.5 | 12.1 |
   | 3xRNN static | 151 | 143 | 11.6 | 11.3 |
   | 3xRNN dynamic | 128 | 121 | 11.3 | 11.1 |

   ### Table 3: Comparison of WSJ results obtained with various models. Note that RNN models are trained just on 6.4M words

   | Model | DEV WER | EVAL WER |
   |-------|---------|----------|
   | Lattice 1 best | 12.9 | 18.4 |
   | Baseline - KN5 (37M) | 12.2 | 17.2 |
   | Discriminative LM [8] (37M) | 11.5 | 16.9 |
   | Joint LM [9] (70M) | - | 16.7 |
   | Static 3xRNN + KN5 (37M) | 11.0 | 15.5 |
   | Dynamic 3xRNN + KN5 (37M) | 10.7 | 16.3⁴ |

