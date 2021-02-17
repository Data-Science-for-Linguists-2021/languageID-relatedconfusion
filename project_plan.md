# Project plan

## Summary
Language identification is the problem of identifying the language of some sample of text, audio or other media. While this problem is considered solved for distinguishing between distant languages such as English and Japanese, it becomes much more challenging for closely related languages such as Czech and Slovak. As such, my hypothesis is that a text language identification tool, while useful on its own for its intended purpose, would also be a useful way of modeling the evolution of the world's languages. <br>


While language identification tools are already available (many people reading this may be familiar with Google Translate's "Detect Language" feature), most only work for a very small subset of the world's 6000+ languages. Both for usefulness of the language identification tool and for gaining a more complete picture of relations among languages, I also will strive to find datasets that include a high number of languages.

## Data
- What will your data look like? <br>
  Ultimately, I imagine that the source data will have two elements: a sample of text and a label that states the language of the text. For my purposes, I would likely split the samples of text to be 5-8 sentences each.
- What sorts of data sourcing and cleaning up effort will be involved? <br>
  At least to get started, I indend to begin with publicly available datasets. One dataset (Wikipedia) will need HTML junk removed but is ready for download now, while the other (JHU Bible Corpus) is clean but has some licensing restrictions on it that require me to fill out a form and wait to recieve it.
- Do you have a sense of the overall data size you should be aiming for? <br>
  I'll just try to get as much as I can. For some languages, huge datasets are not available so that could be the largest limiting factor in the project. I'll also likely need to take measures to balance the dataset (so each language has pretty much equal amount of representation in each of the train/dev/test sets) or make adjustments in the classifier to control for unbalanced data.
- Do you have an existing data source in mind that you can start with, and if so, what are the URLs or references? <br>
  - Wikipedia data: Wikipedia publicly releases its database backups, which includes 285 different languages. The download page is: [https://dumps.wikimedia.org/backup-index-bydb.html](https://dumps.wikimedia.org/backup-index-bydb.html)
  <br> I would probably use their HTML format, which means I will need to strip the HTML off. There are some publicly available tools for this on GitHub so I can hopefully start with those.
  - Bible data: McCarthy et al. (2020) created a clean corpus of translations of the Bible into 1600+ languages. While the Bible certainly has a very particular style compared to other texts, particularly modern texts, it still covers a great majority of any language's core vocabulary. For instance, as discussed in the paper announcing this corpus, prior works demonstrate a high overlap between the English Bible, the Longman Dictionary of Contemporary English and the Brown Corpus. More information and examples are proveded in that paper. As a result, I believe that this corpus will be useful for language identification for the large number of languages that it serves. The paper is [McCarthy et al. (2020): The Johns Hopkins University Bible Corpus: 1600+ Tongues for Typological Exploration](https://www.aclweb.org/anthology/2020.lrec-1.352.pdf). The data cannot simply be downloaded from the internet due to licensing restrictions, so I have filled out a form to recieve it.

## Analysis
- What is your end goal? <br>
  I have a technical goal and a linguistic goal. Technically, I want to create a language identification tool. Linguistically, I want to use this tool (and particularly the cases where it incorrectly classifies a text) as a way to study languages' similarities.
- What linguistic analysis do you have in mind? <br>
  After testing the classifier, I will compare its confusion matrix to data on language families, locations and writing systems. <br>
  I also am interested to see if a classifier trained on Bible data will perform well when tested on Wikipedia data, which would be a very good sign for low-resource languages that only have corpora like the Bible conveniently availible.
- Any hypothesis you will be testing? <br>
  Overall, my hypothesis is that languages that are more closely related to each other will be confused more often by the classifier. However, "related" can mean many things - they could have evolved from a common ancestor, they could be unrelated but located near each other and have a lot of word borrowing and other influences, they could have the same writing system, etc. So, I will aim to see how different versions of "relatedness" influence how similar the languages are in the classifier's eyes.
- Are you planning to do any predictive analysis (machine learning, classification, etc.) and using what methods? <br>
  Yes, this project will involve a large amount of machine learning. I will want to read more about prior language identification projects and what architectures they used, but I will probably want to choose a model available with scikit-learn or that can be conveniently implemented in PyTorch. I imagine that a lot of my time spent on implementation might go towards feature extraction.

## Presentation
Probably a pretty typical setup with Github and JNB, maybe the oral presentation could feature a demo where a volunteer gives me a text sample in a language they know and we test it out on the classifier.
