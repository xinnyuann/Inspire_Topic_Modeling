# Community Posts Topic Modeling 

## Project Overview

The project aims to identify and inspect latent topics across all community posts (from 2017 to 2019) to help Inspire's Data Science Team better understand the hidden patterns and monitor topic drifting through an interactive interface. A topic in this context is a set of words that can be used to represent a document. 

## End Product
The output is a well defined set of topics that describe each document in the collections. A specific visualization technique is adpoted for assessing textual LDA topic model - Termite. "Termite is a visualization tool for inspecting the output of statistical topic models such as Latent Dirichlet allocation (LDA) using an interactive interface as shown above. Termite is an alternative to lists of per-topic words, the standard practice: Users can drill down to examine a specific topic by clicking on a circle or topic label in the matrix, revealing the word-frequency view. The order of the terms presented in this view also uses seriation, which accounts for co-occurrence and collocation likelihood between all pairs of words. Term probabilities are encoded in circles."[2] For more details, see Chuang et al [1].

## Future Work
- Refine evaluation methodologies for the topic quality 

## Reference
[1][Termite: Visualization Techniques for Assessing Textual Topic Models. Jason Chuang, Christopher D. Manning, Jeffrey Heer. Computer Science Dept, Stanford University.](http://vis.stanford.edu/papers/termite)

[2]Revised Version of Termite: https://github.com/sailuh/termite
