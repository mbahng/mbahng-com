[[2014sutskever_seq2seq.pdf]]
#deep-learning #natural-language-processing
[[2014cho_rnn-encoder-decoder-smt]], [[1997hochreiter_lstm]]

# Contribution 

   Basically used a ton of computation (at Google) to construct multilayer LSTM to translate better than before. Same encoder-decoder architecture, and turns out that reversing the inputs led to much better BLEU scores. 

   At this point I was wondering why BLEU cannot be optimized directly, but there are two problems. 
   1. It is not differentiable, though we can work around this. 
   2. Simply optimizing doesn't get noticeably better from a human's POV. There are papers that have done this. 
