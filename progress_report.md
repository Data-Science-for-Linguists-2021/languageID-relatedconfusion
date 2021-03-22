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

I learned how to use Pitt's Computing Resource Center (CRC) and have put a lot of effort towards finally getting and cleaning the entire dataset. I probably could have rewritten the program so it didn't exceed the memory on my computer during cleaning and then done everything locally, but for the largest Wikipedias like English it was easier just to do it this way. If everything had gone seamlessly, it might have taken about two days to run in entirety on CRC, but I needed to learn some lessons first about networking, storage and enterprise VPNs.

When I first logged into the CRC, I saw that each user has by default 75GB of storage. There's an option to request more, but I didn't want to bother anybody and I wanted to keep my own copy of the data anyways. I looked for a way to automatically download data to my computer, but couldn't find a good way to do it. Even though I access CRC from my computer, CRC isn't aware of my computer just because I used it to get to CRC. So, I got to review the networking I learned in my systems software class. You know how you access the CRC by the command `ssh <username>@h2p.crc.pitt.edu`? The `ssh` part means "secure shell", meaning you want to extablish a connection to and run a shell (a terminal prompt) on CRC. The `username` just says which user/account you will sign into and `h2p.crc.pitt.edu` is the address for CRC. There are other commands beyond `ssh` that you can use for networking and remote access to computers. Since I want to transfer files, I was interested in file transfer commands like `scp` and `sftp`. The command `sftp` stands for "secure file transfer protocol" and opens a command line interface where you can transfer files between your "local" and "remote" computers. To do this with CRC, just type `sftp <username>@h2p.crc.pitt.edu`. I wanted to be able to run the `sftp` command from the CRC to access my laptop, i.e. have CRC be the local computer and my laptop be the remote computer. However, the remote computer needs to have an address like `h2p.crc.pitt.edu` to expose it to the entire internet. Normally, I can use `sftp` or `ssh` to get to another laptop on the same wifi network as me (technically, assuming the computer isn't set to deny all port 22 connections), but you need to do something special to use these commands for a laptop on another network. Your computer needs a web address of sorts (this is simplifying a little bit. Technically you need to publically expose port 22). The new thing I needed to learn was how to do so with the tool ngrok. Now, the setup is this: I use my laptop to connect to Pitt's VPN, whence I `ssh` to CRC and run the script. Periodically, as the script runs, it transfers intermediate data files for each language as well as the final cleaned and chunked data for that language. It does so by opening an `sftp` connection with my mom's old laptop on which I have configured ngrok, then sending the files. My mom's old laptop is acting sort of like a storage device and I now have the full clean dataset stored there.

I also started looking around for ideas on classifier models and architectures. I'll probably try a couple different models. Naive Bayes will probably be a quick and easy first step, and I'm curious how it would do with about 140 classes. I'll also try out a neural net. I found somebody's old project on GitHub where they used a neural net to classify between five languages, so I'll probably start from there as inspiration, move it from Keras to PyTorch and beef it up to deal with more languages. I might start working on these before anonymizing the languages' writing systems, then try again after doing so. I expect that performance will drop quite a bit, but I hope that it will reveal different patterns in which languages are most commonly confused. 

### Next steps

- Anonymize the writing systems using method described in progress report 1
- Finalize details of machine learning architecture
- Build architecture and try with toy dataset - with or without anonymized writing system

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
