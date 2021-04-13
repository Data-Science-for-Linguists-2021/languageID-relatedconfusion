Progress report
===============

## First progress Report

### Current state

Originally I wanted to use two datasets: the JHU Bible Corpus and Wikipedia dumps. I have tried to obtain the JHU Bible Corpus dataset by filling out a form to request it nearly a month ago, and even emailed the first author on the paper announcing this data set a couple weeks ago. I never got a response, so I have instead focused more on the Wikipedia data.

For the Wikipedia data, I have written the script [datagather/get-data-wiki.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/data-explanation.ipynb) that automates much of the pipeline. For each language, it downloads the raw dump file, ensures that the file is large enough to be useable, removes the Wikipedia formatting so I can get just plain article texts and does some cleaning like removing punctuation. Then, it splits all the text for a language into 500-character lines (I call "chunks") and writes each language's chunks to its own .txt file. Each chunk is one line. Example output files are in [data_samples/](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/data_samples) and a walkthrough of this data gathering process is in data-explanation.ipynb. I did the chunking in anticipation that I will want to create a file that contains random samples of texts from all the languages together, with two columns: one for the language sample and the other for the language's abbreviation/code. Altogether, the script creates three directories: datagather/dumps/ for raw dump files, datagather/texts/ for texts that are extracted and cleaned but not chunked and datagather/extracted/ for texts that are chunked and shuffled.

The script takes about 1.5 days to run in its entirety, which I did manage to do in order to ensure it doesn't crash on any language and my computer doesn't run out of storage. However, there were some issues in the ways the data was being cleaned and processed, so I deleted that data. I've fixed some of the issues, then ran the script again. However, I was running out of time to meet this progress report deadline, so I decided to artificially only process the first 100000 characters' worth of articles for each language this go-around. This is *not* the full amount of data, but I wanted to have something as I wrote the report.

### Next steps

Next, I plan to run the entire script again to process the full amount of data and write another script to mix the samples from different languages together. I can also get started with feature extraction. I'll probably take a moment to look at how prior language identification systems have been done and think more about what type of model/architecture I want.

I also do have some ideas for how I will separate a language from its writing system automatically, so the classifier doesn't just pay attention to that (I imagine this isn't too common a concern for most language ID systems, but I have the added linguistic goal of trying to model language relatedness, so I want the model to go off more than just writing system. I might pass writing system, or some similar feature, to the model but want the text to exist somehow free from the writing system too). For each language's extracted text file (or more precisely a portion I have chosen for the train dataset), I would compute how common each character is. The most common character corresponds to 0, second most common to 1 and so on. Then, I could replace the characters with their number correspondances. I would want to store the text converted/mapped to these numbers on disk as integers but don't know if Python will give me that much control over how things are written to disk. Python might store as string which is less efficient. I could do it in C if need be, but would like to stick to Python where possible since it's what we use in this class.

### Data sharing ideas

The raw dump files sitting on my computer take up about 76GB, so I am expecting the full size of the complete extracted and cleaned dataset to also be pretty large. I do not think Github wants you uploading such large amounts of data there, but I am probably going to put up samples. For now, I will pick some random languages and upload the entirety of their extracted, chunked and shuffled files. Later, when I have files of all languages shuffled together, I will probably include one or some of those.

Also, my data gathering script automatically fetches files from the web and cleans them to become exactly the way I plan to use them, so anybody who wants to replicate my process can certainly run that script. The only difference would be that they would recieve an updated version of Wikipedia if they run the script at a later date.

---

## Second progress report

### Current state

[Here](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/data-explanation.ipynb) is the walkthrough of the dataset and how it was gathered (continuing from the notebook used in progress report 1) and [here](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/data_chunked) is the chunked dataset of all 248 languages. Since the first progress report, I have gathered and cleaned the full dataset. To do so, I learned how to use Pitt's Computing Resource Center (CRC). I probably could have rewritten the program so it didn't exceed the memory on my computer during cleaning and then done everything locally, but for the largest Wikipedias like English it way easier to do it this way. If everything had gone seamlessly, it might have taken about two days to run in entirety on CRC, but I needed to learn some lessons first about networking, storage and enterprise VPNs.

When I first logged into the CRC, I saw that each user has by default 75GB of storage. There's an option to request more, but I didn't want to bother anybody and I wanted to keep my own copy of the data anyways. I looked for a way to automatically download data to my computer, but couldn't find a good way to do it. Even though I access CRC from my computer, CRC isn't aware of my computer just because I used it to get to CRC. So, I got to review the networking I learned in my systems software class. You know how you access the CRC by the command `ssh <username>@h2p.crc.pitt.edu`? The `ssh` part means "secure shell", meaning you want to extablish a connection to and run a shell (a terminal prompt) on CRC. The `username` just says which user/account you will sign into and `h2p.crc.pitt.edu` is the address for CRC. There are other commands beyond `ssh` that you can use for networking and remote access to computers. Since I want to transfer files, I was interested in file transfer commands like `scp` and `sftp`. The command `sftp` stands for "secure file transfer protocol" and opens a command line interface where you can transfer files between your "local" and "remote" computers. To do this with CRC, just type `sftp <username>@h2p.crc.pitt.edu`. I wanted to be able to run the `sftp` command from the CRC to access my laptop, i.e. have CRC be the local computer and my laptop be the remote computer. However, the remote computer needs to have an address like `h2p.crc.pitt.edu` to expose it to the entire internet. Normally, I can use `sftp` or `ssh` to get to another laptop on the same wifi network as me (technically, assuming the computer isn't set to deny all port 22 connections), but you need to do something special to use these commands to access a laptop on another network. That laptop needs a web address of sorts (this is simplifying a little bit. Technically you need to publically expose port 22). The new thing I needed to learn was how to do so with the tool ngrok. Now, the setup is this: I use my laptop to connect to Pitt's VPN, whence I `ssh` to CRC and run the script. Periodically, as the script runs, it transfers intermediate data files for each language as well as the final cleaned and chunked data for that language. It does so by opening an `sftp` connection with my mom's old laptop on which I have configured ngrok, then sending the files. My mom's old laptop is acting sort of like a storage device and I now have the full clean dataset stored there.

I also started looking around for ideas on classifier models and architectures. I'll probably try a couple different models. Naive Bayes will probably be a quick and easy first step, and I'm curious how it would do with about 248 classes. I'll also try out a neural net. I found [somebody's old repository](https://github.com/Pankti99/Language_Identifier) on GitHub where they used a small neural net to classify between five languages, so I think I could design something beefier for more languages (not reusing their work at all, just realizing that somebody has done this before with a CNN). I learned about PyTorch in my deep learning class, so I'll probably use that. I might start working on these before anonymizing the languages' writing systems, then try again after doing so. I expect that performance will drop quite a bit, but I hope that it will reveal different patterns in which languages are most commonly confused. I could then use that information in my linguistic analysis.

### Next steps

- Anonymize the writing systems using method described in progress report 1
- Finalize details of machine learning architecture
- Build architecture and try with toy dataset - with and without anonymized writing system

### Licensing plan, for everything but the data

I don't really care what others do with my code/work; I would be a little surprised but glad if it's helpful to anyone. However, it would be nice to get credit for it and would prefer people cited this repository or my name if they're going to reuse anything. According to [this site](https://choosealicense.com/licenses/gpl-3.0/) run by GitHub, GNU General Public License v3.0 lets people reuse my work, but they're required to cite me as the source.

### Data sharing plan

As far as the data, it took so much work to gather that I really wish I could share it publicly for all to use. Unfortunately, the full dataset (excluding the raw dump files straight from Wikipedia) is about 175GB so I don't know where I could do that. However, the chunked files are pretty small so I'll try putting those on GitHub. I also wasn't quite sure how to attribute the authors of the wikipedia pages since I am no longer distributing the articles as "articles" but rather as random 500-character segments drawn at random (as in, even I don't know) from the entirety of each language's wikipedia's server backup. However, I found [this page](https://en.wikipedia.org/wiki/Category:Wikipedians_by_language) that lists the all the authors to Wikipedia by their language, so I will be sure to include a copy of this link in order to credit everybody. I will also include a link to the dump website and information on the wikipedia license.

Wikipedia data is distributed under the [Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/) policy and the [GNU Free Documentation License (GFDL)](https://en.wikipedia.org/wiki/Wikipedia:Copyrights) and wants people reusing the data to share it under similar licenses. So I will reuse these licenses for the data.

---

## Third progress report

At a glance, what I did since last project report: I trained a naive bayes (NB) model on the data (without and without writing systems anonymized) and subsequently used a clustering method to form groups of similar or commonly-confused languages. The model for the non-anonymized (NA) writing system was completed a couple weeks ago, so I was able to spend some time thinking about analysis or final conclusions to draw from that subset of results. I just trained the model for the anonymized (A) writing system today, but it achieved such good accuracy (over 99% accuracy on 5 fold crossval) that I'm having trouble getting much analysis of how languages are confused with each other - I guess it's sort of a good problem to have? I've never had to purposefully try to make a model perform *worse* before, but I might do that so I can see better which languages are more likely to get confused. I also do find it slightly suspicious that performance would be so good, so I'll try to spend a little more time making sure that really is correct.

Going into a little more details, I'll walk through chronologically. I got the results for NA NB just after progress report 2 was due, achieving about 90% accuracy. I quickly noticed that a confusion matrix for 248 classes isn't really readable and I needed a better way to distill the model outputs for analysis. I remembered that a [student](https://github.com/Data-Science-for-Linguists/Document_Clustering/blob/master/clustering.ipynb) from a previous year did clustering of some texts, so I followed that method with my model output. When the model makes predictions for a 248-class variable, you get a 248x248 confusion matrix where each datapoint/predicted input is assigned some index in this matrix. For some chunk at some position, its row index corresponds to its true language and its column index corresponds to the language predicted by the model. So, I used this confusion matrix directly as input to a clustering algorithm (k-means). Each datapoint is a vector that represents a "true" language, drawn from the rows of the confusion matrix. Each feature of the vector is the "predicted" languages of any chunk that had this true language. So, if the language at row index 2 has 10,000 chunks and 9,500 are classified correctly while 500 are mistaken for the language at index 8, then the vector representing true language 2 will have 248 (number of languages) elements, with all elements as 0 except at the second position, which will be 9,500, and the eighth position, which will be 500 (technically I normalize the matrix row-wise too but don't feel getting into this now). These 248 vectors are fed to the k-means algorithm which spits out k groups/clusters of the vectors. When I re-associate these vectors with their ground-truth language name, I see which languages have been placed in groups together. Real examples of these groups are "Bosnian, Croatian and Serbo-Croatian" or "Modern Standard Arabic and Moroccan Arabic". Looking at these groups my preliminary conclusion has reached that geographical relatedness trumps ancestral relatedness, but I'll elaborate in my presentation Thursday (oh gosh..).

Then I started working on the anonymized writing systems. In progress report 1, I mentioned an algorithm where one computes how common each character is, then substitutes each character in the text with indices where 0 is most common, 1 is second most common and so on. I applied this algorithm and, after some technical difficulties of how to actually represent these numbers to sklearn, I was able to use an equivalent feature (character bigrams) extraction and NB setup to the NA NB version. As mentioned earlier, it achieved very high performance and so clustering came out a little odd. I'll mess with this more next.

Earlier I was talking about and found resources to implement a CNN as well, but I'm looking at how the end of semester and undergrad is going and also seeing that the results for NB give a lot to discuss. So, I'd still like to do the CNN if I have time but I'm thinking the project could still stand on its feet without that and focusing more quality to the NB and the analysis. I purposefully kept model ideas pretty loose in the project proposal, since I would want to see the results of some things before trying others. We'll see I suppose.

As far as the structure of the repository, it's structured the way it is because both my computer and I tend to get overwhelmed if any Jupyter notebook is too big. Last progress report I directed you to the "existing" data gathering notebook [data-exploration.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/data-explanation.ipynb) but, as I no longer am gathering data, I have created a few new notebooks that handle different parts of the pipeline. Each of these are "new continuing": [anon-writingsys.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/anon-writingsys.ipynb) is for the algorithm that anonymizes the writing systems and [naive-bayes.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/naivebayes.ipynb) contains both NA NB and A NB, along with clustering for each. A NB has both unigram and bigram versions - unigrams performed poorly (accuracy about 35%) but has slightly more meaningful clustering if not still strange results compared to A NB bigrams. I used the file [MLdataprep.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/MLdataprep.ipynb) to prepare the data for use in the NB notebook but I'm intending to move the contents of this notebook into the NB notebook soon and delete this notebook.


### Data

The raw data files and non-anonymized chunks themselves haven't changed at all since the last report. Of course, I did do the anonymization (which got stored in separate files, which are just local to my computer) but I would maybe put that more in the analysis than in the data portion of the project. It's not really a clear line though between data and analysis though.

### Next steps
- Make A NB perform worse and redo clustering
- Look into remaining issues with anonymization system if there's time
- Clean repository
- Do presentation

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

-   14: Learned (some) how to use CRC, set up remote storage device in prep to gather full data

-   16: Starting to adapt my setup onto CRC, getting file transfer protocols set up

-   17: Pilot run of script on CRC after tinkering, installation. Some cleaning

-   18: Gathered languages starting with 'a' up until 'en'

-   19: Gathered full English data!

-   20: Gathering 'eo' through .. and .. through 'z' (simultaneously running one script forwards through alphabet and one script backwards)

-   21: It's official: 248 languages' Wikipedias gathered and cleaned!

-   22: Progress report 2 finished

-   25: First attempt of ML (NB), plus clustering on confusion matrix results - much tweaking to do but promising

-   26: Wrote code to anonymize writing systems, some tweaking of storage format still to do

-   28: Looked up information about the languages in the clusters

### April

-  10: Working on anonymized writing systems file format

-  11: Trying to do NB with anonymous writing systems

-  12: Successfully did anonymized NB, progress report 3
