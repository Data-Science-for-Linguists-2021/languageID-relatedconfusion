Progress report
===============

## First progress Report

### Current state

Originally I wanted to use two datasets: the JHU Bible Corpus and Wikipedia dumps. I have tried to obtain the JHU Bible Corpus dataset by filling out a form to request it nearly a month ago, and even emailed the first author on the paper announcing this data set a couple weeks ago. I never got a response, so I have instead focused more on the Wikipedia data.

For the Wikipedia data, I have written the script [datagather/get-data-wiki.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/data-explanation.ipynb) that automates much of the pipeline. For each language, it downloads the raw dump file, ensures that the file is large enough to be useable, removes the Wikipedia formatting so I can get just plain article texts and does some cleaning like removing punctuation. Then, it splits all the text for a language into 500-character lines (I call "chunks") and writes each language's chunks to its own .txt file. Each chunk is one line. Example output files are in [data_samples/](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/data_samples) and a walkthrough of this data gathering process is in data-explanation.ipynb. I did the chunking in anticipation that I will want to create a file that contains random samples of texts from all the languages together, with two columns: one for the language sample and the other for the language's abbreviation/code. Altogether, the script creates three directories: datagather/dumps/ for raw dump files, datagather/texts/ for texts that are extracted and cleaned but not chunked and datagather/extracted/ for texts that are chunked and shuffled.

The script takes about 1.5 days to run in its entirety, which I did manage to do in order to ensure it doesn't crash on any language and my computer doesn't run out of storage. However, there were some issues in the ways the data was being cleaned and processed, so I deleted that data. I've fixed some of the issues, then ran the script again. However, I was running out of time to meet this progress report deadline, so I decided to artificially only process the first 100000 characters' worth of articles for each language this go-around. This is *not* the full amount of data, but I wanted to have something as I wrote the report.

### Next steps

Next, I plan to run the entire script again to process the full amount of data and write another script to mix the samples from different languages together. I can also get started with feature extraction. I'll probably take a moment to look at how prior language identification systems have been done and think more about what type of model/architecture I want.

I also do have some ideas for how I will separate a language from its writing system automatically, so the classifier doesn't just pay attention to that (I imagine this isn't too common a concern for most language ID systems, but I have the added linguistic goal of trying to model language relatedness, so I want the model to go off more than just writing system. I might pass writing system, or some similar feature, to the model but want the text to exist somehow free from the writing system too). For each language's extracted text file (or more precisely a portion I have chosen for the train dataset), I would compute how common each character is. The most common character corresponds to 0, second most common to 1 and so on. Then, I could replace the characters with their number correspondances. I would want to store these numbers on disk as integers but don't know if Python will give me that much control over how things are written to disk. Python might store as string which is less efficient. I could do it in C if need be, but would like to stick to Python where possible since it's what we use in this class.

### Data sharing ideas

The raw dump files sitting on my computer take up about 76GB, so I am expecting the full size of the complete extracted and cleaned dataset to also be pretty large. I do not think Github wants you uploading such large amounts of data there, but I am probably going to put up samples. For now, I will pick some random languages and upload the entirety of their extracted, chunked and shuffled files. Later, when I have files of all languages shuffled together, I will probably include one or some of those.

Also, my data gathering script automatically fetches files from the web and cleans them to become exactly the way I plan to use them, so anybody who wants to replicate my process can certainly run that script. The only difference would be that they would recieve an updated version of Wikipedia if they run the script at a later date.

---

2021
---

### February

-   15: Created repo, added/minorly updated plan

-   21: Learned how to clean wikipedia raw dump data

-   23: Learned about wikipedia API for automatically getting language codes

-   24: Started draft of simple script to gather, clean wiki data

-   27/28: Ran script, first time successfully gathering data for all languages

### March

-   1: Started summary notebook of data processing pipeline, cleaned some code

-   2: Regathered small data samples

-   3: Finished draft of data pipeline notebook

-   4: Drafter first progress report

-   5: Finishing first progress report, data pipeline notebook
