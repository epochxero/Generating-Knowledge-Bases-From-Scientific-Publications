## Specifications
**Deep Learning Framework**: [Pytorch](https://shiftlab.github.io/pytorch/)
**Seed Knowledge Base**: [PropNet](https://github.com/materialsintelligence/propnet)
**Language Model**: [BERT or XLNet](https://github.com/huggingface/pytorch-transformers)

## Roadmap

### Develop Pipeline for Experimentation
* [ ] Investigate necessary kb, matsci and nlp libraries
* [ ] Discuss and establish what is unlikely to change about the experiment to determine modular requirements
* [ ] Construct flexible modules for the preliminary experimental pipeline
* [ ] Test pipeline using the current version of the experiment

### Gather Data
* [x] Write scraper for Elsevier
* [ ] Write scraper for Springer
* [ ] Distribute scrapers across numerous machines (4 - 10 ideally)
* [ ] Determine which knowledge bases are best suits our needs for MatSci. Download and analyze them
* [ ] Collect other potentially fruitful literature for further testing
* [ ] Find knowledge bases from the domains of this additional literature

### Literature Review
* [ ] Make sure everyone has read up on and roughly understands the latest NLP breakthroughs such as BERT, Transformers, etc.
* [ ] Review the NLP for MatSci discovery literature
* [ ] Review the strengths, weaknesses and uses of knowledge bases within MatSci 
* [ ] Review the broader AI for MatSci literature for context

### Outline Experiment
* [ ] Utilize domain knowledge to better understand what advances are most useful for those in the field of MatSci
* [ ] Using the knowledge gained, synthesize the final experimental design, ideally remaining compatible with the preliminary pipeline
* [ ] Set benchmarks and measures of success for the experiences

### Conduct Experiments
* [ ] Process data as informed by the literature, including cleaning, PoS tagging, NER or other necessary steps
* [ ] Construct and train the necessary models using the Epoch Zero TPUs
* [ ] Analyze results, tune and adjust as needed
* [ ] Attempt to expand results to other domains

### Write Paper
* [ ] Use notes and results from previous steps to create outline
* [ ] Write first draft 
* [ ] Circulate among Epoch Zero members
* [ ] TBD
