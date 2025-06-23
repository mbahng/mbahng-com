[[2015luong_addressing-rare-word-prob-nmt.pdf]] 
#language
[[2015jean_large-vocab-for-nmt]]

# Contribution 

   Train and NMT system on data that is augmented by the output of word alignment algorithms, allowing the NMT to emit, for each OOV word in the target sentence, the corresponding word in the source sentence. At this point, we can just postprocess to translate every OOV word using a dictionary or identity map. 

# Background

   At this point, we use word-level tokenization, which may not be good since NMTs at this point must then have relatively small vocabularies with a single UNK symols that represents every possible out-of-vocabulary (OOV) word. Sentence translation with lots of UNK tokens are quite bad, so some improvement is needed. 

# Tokenization Model

   They introduce three ways to tokenize sentences with unknown vocab, with each being an improvement over the other. 
   1. *Copyable Model*. In the source sentence, label the words $unk_1, unk_2, \ldots$. Then in the target sentence, we label the unknown words that align with an unknown source word (and all copies of that target words) to the proper $unk_i$ token. If there are no source words that match a given target unknown token, then we label it with $unk_\emptyset$.
      - en: The $unk_1$ portico in $unk_2$ ...
      - fr: Le $unk_\emptyset$ $unk_1$ de $unk_2$ ...

   2. *Positional All Model*. The copyable model is limited in that it cannot translate unknown target words that are aligned to known words in the source, e.g. portico (en) and portique (fr). This often happens since source vocab is much larger than target vocab. Therefore, we go back to tokenizing unk universally for unknown source words, and for every target word, we add a positional token $p_d$ after every word, where $d$ indicates relative position ($d = -7, \ldots, 7$) to denote that target word at position $j$ is aligned to source word in position $i = j - d$. We limit to 7 since aligned words that are too far apart are considered unaligned. Unaligned words are annotated with null token $p_\emptyset$. 

      - en: The $unk$ portico in $unk$ ...
      - fr: Le $p_0$ $unk$ $p_{-1}$ $unk$ $p_1$ de $p_0$ $unk$ $p_{-1}$ ...

   3. *Positional Unknown Model*. However, the sentence length is doubled, which is not efficient. Therefore, we only want to focus on the unknown words. So we just replace positional tokens with just unknown tokens to simultaneously denote that a word is unknown and what its relative position $d$ w.r.t. its aligned source word is. 

      - en: The $unk$ portico in $unk$ ...
      - fr: Le $p_0$ $unk$ $p_{-1}$ $unk$ $p_1$ de $p_0$ $unk$ $p_{-1}$ ...

# Results 

   With this new tokenization schemes, they basically train a multilayer deep LSTM with 1000 cells and 1000 dim embeddings. Also reverse words in the source sentence which Sutskever found previously to improve performance. 

   Standard training on WMT12, 13 and test on 14. Surprised that they didn't use attention. 


   | System | Vocab | Corpus | BLEU |
   |--------|-------|--------|------|
   | **State of the art in WMT'14 (Durrani et al., 2014)** | All | 36M | 37.0 |
   | ***Standard MT + neural components*** | | | |
   | Schwenk (2014) – neural language model | All | 12M | 33.3 |
   | Cho et al. (2014)– phrase table neural features | All | 12M | 34.5 |
   | Sutskever et al. (2014) – 5 LSTMs, reranking 1000-best lists | All | 12M | 36.5 |
   | ***Existing end-to-end NMT systems*** | | | |
   | Bahdanau et al. (2015) – single gated RNN with search | 30K | 12M | 28.5 |
   | Sutskever et al. (2014) – 5 LSTMs | 80K | 12M | 34.8 |
   | Jean et al. (2015) – 8 gated RNNs with search + UNK replacement | 500K | 12M | 37.2 |
   | ***Our end-to-end NMT systems*** | | | |
   | Single LSTM with 4 layers | 40K | 12M | 29.5 |
   | Single LSTM with 4 layers + PosUnk | 40K | 12M | 31.8 (+2.3) |
   | Single LSTM with 6 layers | 40K | 12M | 30.4 |
   | Single LSTM with 6 layers + PosUnk | 40K | 12M | 32.7 (+2.3) |
   | Ensemble of 8 LSTMs | 40K | 12M | 34.1 |
   | Ensemble of 8 LSTMs + PosUnk | 40K | 12M | 36.9 (+2.8) |
   | Single LSTM with 6 layers | 80K | 36M | 31.5 |
   | Single LSTM with 6 layers + PosUnk | 80K | 36M | 33.1 (+1.6) |
   | Ensemble of 8 LSTMs | 80K | 36M | 35.6 |
   | Ensemble of 8 LSTMs + PosUnk | 80K | 36M | 37.5 (+1.9) |

