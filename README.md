Language identification to map language relatedness
====================================================
Sonia Cromp, snc40@pitt.edu
---

Sonia's Data Science for Linguists term project: A classifier to detect the
language of a text sample, and an analysis of which languages are commonly
confused by the classifier and why

The data used is derived from [Wikipedia server dumps](https://dumps.wikimedia.org/backup-index-bydb.html). [Here](https://en.wikipedia.org/wiki/Category:Wikipedians_by_language) are all Wikipedia contributors.

### Directory

Administrivia
- [project_plan.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/project_plan.md) gives the ideas I had at the start of the project, which is pretty much what I adhered to
- [progress_report.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/progress_report.md) gives progress updates as I worked on the projects. I tried to make the reports fairly detailed and able to be followed
- [final_report.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/final_report.md) contains the final report
- [final_pres.pdf] is the slideshow I used for the final presentation
- [LICENSE.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/LICENSE.md) contains licensing information
- [README.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/README.md) is what you're reading right now
- [.gitignore](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/.gitignore) should be ignored

Code
- [1-data-explanation.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/1-data-explanation.ipynb) explains the data gathering process. Since GitHub mangles section links, [here's the same notebook through Jupyter's nbviewer](https://nbviewer.jupyter.org/github/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/1-data-explanation.ipynb).
- [2-dataAnonAndPrep.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/2-dataAnonAndPrep.ipynb) anonymizes all languages' writing systems, then reformats the anonymized and non-anonymized datasets to be all ready for machine learning. Since GitHub mangles section links, [here's the same notebook through Jupyter's nbviewer](https://nbviewer.jupyter.org/github/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/2-dataAnonAndPrep.ipynb).
- [3-naive_bayes.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/3-naivebayes.ipynb) does the language identification and relatedness mapping. Since GitHub mangles section links, [here's the same notebook through Jupyter's nbviewer](https://nbviewer.jupyter.org/github/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/3-naivebayes.ipynb).
- [4-clusterfun.ipynb](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/4-clusterfun.ipynb) does a bit more relatedness mapping and analysis. Since GitHub mangles section links, [here's the same notebook through Jupyter's nbviewer](https://nbviewer.jupyter.org/github/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/4-clusterfun.ipynb).
- [nbgrid.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/nbgrid.py) was used to perform grid search with the classifier on CRC
- [nbgrid.sh](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/nbgrid.sh) is the corresponding slurm script to run nbgrid.py

Subdirectories
- [data_chunked](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/data_chunked) contains the non-anonymized dataset (i.e. the final product of 1-data-explanation.ipynb)
- [data_samples](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/data_samples) contains intermediary examples of the data during the datagathering process, which are discussed in 1-data-explanation.ipynb
- [datagather](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/datagather) contains the actual scripts used to gather the data.
  - [get-data-wiki.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/get-data-wiki.py) is the main gathering script
  - [get-data-wiki.sh](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/get-data-wiki.sh) contains some utilities used by the Python script
  - [crc](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc) contains the files needed to run the data gathering process on Pitt's Computing Research Center (CRC) resources
    - [get-data-wiki.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc/get-data-wiki.py) and [get-data-wiki.sh](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc/get-data-wiki.sh) correspond with the same scripts in the parent directory, but with modifications for CRC
    - [guide.md](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc/guide.md) explains how to set up the script and all networking configurations on CRC, your personal computer, and a secondary storage computer
    - [paramiko-tuto.py](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc/paramiko-tuto.py) is a tutorial/test script to experiment with the networking setup used in the datagathering process
    - [ex.txt](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/blob/main/datagather/crc/ex.txt) is just a text file, sent across the network by paramiko-tuto.py
- [figs](https://github.com/Data-Science-for-Linguists-2021/languageID-relatedconfusion/tree/main/figs) contains figures, most of which are in the final report

The guestbook is [here](https://github.com/Data-Science-for-Linguists-2021/Class-Lounge/blob/main/guestbooks/guestbook_sonia.md).

### License

The data is licensed under the [Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/) policy and the [GNU Free Documentation License (GFDL)](https://en.wikipedia.org/wiki/Wikipedia:Copyrights). See the README.md in that directory for more information.

All other parts of this repository are licensed under the GNU General Public License v3.0.
