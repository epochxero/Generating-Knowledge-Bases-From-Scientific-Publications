# NLP Review

#### By: Tyler

### Overview
NLP is a core technology for this project, and while there is a long and rich history from which to draw upon, only the last decade or so will be covered. The reason for this is that this review is meant to quickly get those who are unfamiliar with the current state of the art up to speed. While it will attempt to get across the main ideas and roughly describe the algorithms themselves, those seeking a deeper understanding may wish to consult the cited literature directly, or discuss points of confusion with other project members.   

### Past Work (Greater detail forthcoming)
In 2017 NLP began to have its “ImageNet Moment” (Ruder, 2018). A series of breakthroughs in model architectures and methodologies has allowed for not just better results, but faster training and easier adaptation to a variety of tasks (Child, Gray, Radford, & Sutskever, 2019; Devlin, Chang, Lee, & Toutanova, 2018; Vaswani et al., 2017). 

Earlier work (Collobert & Weston, 2008.; Mikolov, Chen, Corrado, & Dean, 2013; Pennington, Socher, & Manning, 2014) focused on adopting feature-based approaches to transform words into distributed representations. Pre-trained word representations capture syntactic and semantic information in the textual corpora, they are often used as input embeddings and initialization parameters for various NLP models, and offer significant improvements over random initialization parameters (Turian, Ratinov, & Bengio, 2010). Since these word-level models often suffer from the word polysemy, Peters et al. (2018) further adopted the sequence-level model to  capture complex word features across different linguistic contexts and generate context-aware word embeddings (ELMo). 

Different from the above-mentioned feature-based language approaches only using the pretrained language representations as input features, (A. M. Dai & Le, 2015) trained auto-encoders on unlabeled text, and then used the pre-trained model architecture and parameters as a starting point for other specific NLP models. Inspired by Dai and Le, more pre-trained language representation models for fine-tuning were proposed, resulting in Howard and Ruder's (2018) universal language model (ULM-Fit), which allowed for effective and efficient tuning for downstream tasks.

Radford, Narasimhan, Salimans, and Sutskever (2018) created the OpenAI Transformer, GPT, which implemented a generative pre-trained Transformer (Vaswani et al., 2017) to learn language representations. This was a unidirectional language model that effectively combined the pretraining of ULM-Fit with the long range capabilities of transformers. Devlin et al. (2018) proposed a masking training task for the language model that allowed for a bidirectional model with multiple layer Transformers (BERT), which achieves the state-of-the-art results for various NLP tasks. 

Recently, the transformer has been further improved by Transformer-XL (extra long), which uses recurrent hidden states between segments to allow for longer term dependencies then the context length of the transformer (Dai et al., 2019). This was combined with much of the work done on BERT, along with reformulating the pretraining task to prevent predicted tokens from assuming they’re independent of each other given unmasked tokens, achieving the SOTA as of June 2019 (Yang et al., 2019). Of the recent advances made in NLP, UNILM is also of particular note, as it shows a marked improvement in question answering and summarization tasks while remaining competitive on other benchmarks (Dong et al., 2019). 

These advances not only set new SOTA which can be built on, but fundamentally changed how NLP is approached. It is no longer necessary to train individual models for each subtask, and it is far less problematic if the target problem only has a limited number of samples. This has resulted in a plethora of opportunities for researchers focusing on relatively narrow but important problems.

### Avenues For Inclusion
While there may be alterations and true contributions that can be made to NLP through this project, since developing NLP models is not the focus, BERT or XLNET, the most recent language models developed will likely be used. A possible alternative is ERNIE, which uses knowledge graphs in the construction of the language model, which may make the knowledge graph generation task easier and more accurate. 

### References
TBD
