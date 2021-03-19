import sys
import os
import wikipedia
import requests
import subprocess
import re
import rapidjson
from unicodedata import category as cat # for punctuation removal
import random
import shutil
from itertools import zip_longest
import paramiko
import getpass

def check_pwd(address, port, usr, pwd):
    try:
        client = paramiko.client.SSHClient()
        client.load_system_host_keys() # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, port=port, username=usr, password=pwd)
        client.close()
        return True
    except:
        return False


def sftp(address, port, usr, pwd, remworkdir, fname):
    # try:
        # print("sftp port " + str(port) + " of " + usr + "@" + address + ", transferring : " +
        #              remworkdir+fname)
        client = paramiko.client.SSHClient()
        client.load_system_host_keys() # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, port=port, username=usr, password=pwd)
        sftp = client.open_sftp() # type SFTPClient
        sftp.put('.'+fname, remworkdir+fname) #src, dest path/filename
        print('\ttransferred', fname)
        client.close()
    # except IOError:
    #     print(".. host " + address + " is not up or some other error occured")
    #     return "host not up", "host not up"


if __name__ == '__main__':
    #TODO: commandlineargs address, port, usr, statmsgs
    address = ''
    port = ''
    username = ''
    remworkdir = ''
    statmsgs = True # whether or not to output mid-language status updates
    print(sys.argv)
    if(len(sys.argv) != 6):
        print('USAGE: python3 get-data-wiki.py <sftp address> <sftp port> <sftp username> <remote workdir> <verbose (0/1)>')
        exit()
    else:
        address = sys.argv[1]
        port = int(sys.argv[2])
        username = sys.argv[3]
        remworkdir = sys.argv[4]
        statmsgs = bool(int(sys.argv[5]))

    outpath = './'
    langs = wikipedia.languages() #dictionary where key is code, value is language name in that language

    # authenticate to storage device
    authenticated = False
    pwd = ''
    while not authenticated:
        pwd = getpass.getpass(prompt='sftp password: ')
        authenticated = check_pwd(address, port, username, pwd)
        if not authenticated:
            print('authentication failed. try again.')
        else:
            print('authenticated.')

    # create dumps, extracted dirs
    if 'dumps' not in os.listdir():
        os.mkdir('dumps')
    if 'extracted' not in os.listdir():
        os.mkdir('extracted')
    if 'texts' not in os.listdir():
        os.mkdir('texts')
    if 'chunked' not in os.listdir():
        os.mkdir('chunked')

    skip = True

    print('status\t\tcode\tlanguage name')
    print('------------------------------------')
    for lang in langs.keys():
        if lang =='en': ## useful for debugging
            skip = False
        elif skip:
            continue
        else:
            break

        try:
            # don't download dump if already have it from previous run:
            if lang + '-raw.xml.bz2' not in os.listdir('./dumps/') and './extracted/' + lang + '.txt' not in os.listdir('./extracted/'):
                # download the dump, save raw to file
                dumpname = lang + 'wiki-latest-pages-articles.xml.bz2'
                dumplink = 'https://dumps.wikimedia.org/' + lang + 'wiki/latest/' + dumpname
                r = requests.get(dumplink, allow_redirects=True)

                fsz = int(r.headers['Content-length'])
                # print(fsz)
                if fsz < 2**20: #filesize less than 1 MB, can't do much with it so skip
                    print('wiki too small', lang, langs[lang], sep='\t')
                    continue
                open('./dumps/'+lang+'-raw.xml.bz2', 'wb').write(r.content)
        except: #closed wikipedias throw an error when you try to download
            print('empty wiki', lang, langs[lang], sep='\t')
            continue

        print('proceeding...', lang, langs[lang], sep='\t') # means this language
        #will be included in the corpus

        #remove XML
        if './extracted/' + lang + '.txt' not in os.listdir('./extracted/'):
            if statmsgs: print('\tremove XML')
            subprocess.call(['sh', './get-data-wiki.sh', './dumps/'+lang+'-raw.xml.bz2', lang])
        elif statmsgs: print('reading from backup extracted')

        fname = './extracted/' + lang + '.txt' #temp file created by the shell script
        f = open(fname, 'r')
        l = f.readlines()
        f.close()
        # send to device then delete locally
        sftp(address, port, username, pwd, remworkdir, '/extracted/' + lang + '.txt')
        # os.remove('./extracted/' + lang + '.txt')
        # os.remove('./dumps/'+lang+'-raw.xml.bz2') #delete the raw dump too


        if statmsgs: print('\tclean 1')
        pat = re.compile('\\n|\d|https?://.*|&lt.*;|__.*__')
        textsarr = []
        for line in l:
            textsarr.append(re.sub(pat, ' ', line))
        texts = ' '.join(textsarr)

        # final clean: remove punctuation, sequences of multiple spaces
        if statmsgs: print('\tclean 2')
        texts2 = ''
        for char in texts:
            #                   punctuation             pipeline            newline        numbers, ², fractions, etc
            if (not cat(char).startswith('P')) and (char != '|') and (char !='\n') and (not cat(char).startswith('N')):
                texts2 += char
        texts = texts2
        pattern = re.compile(r'  +')
        texts = re.sub(pattern, ' ', texts) #replace multiple spaces with just one

        # write non-chunked text to file
        f = open('./texts/' + lang + '.txt', 'w')
        f.writelines(texts + '\n')
        f.close()
        # send to device then delete locally
        sftp(address, port, username, pwd, remworkdir, '/texts/' + lang + '.txt')
        # os.remove('./texts/' + lang + '.txt')

        # split to 500-char chunks
        if statmsgs: print('\tchunking')
        n = 500 # size of a chunk/line
        # Group function using zip_longest to split
        def group(n, iterable, fillvalue=None):
            args = [iter(iterable)] * n
            return zip_longest(fillvalue=fillvalue, *args)
        chunks = [''.join(lis) for lis in group(n, texts, '')]

        # shuffle chunks, then limit to 10000 chunks per language
        if statmsgs: print('\tshuffling')
        random.seed(5)
        chunklimit = 10000
        if len(chunks) > chunklimit:
            chunks = random.sample(chunks, chunklimit) # choose chunklimit chunks at random
        random.shuffle(chunks)

        # write to file
        if statmsgs: print('\twriting to file')
        f = open('./chunked/' + lang + '.txt', 'w')
        f.writelines([c+'\n' for c in chunks])
        f.close()
        # send to device then delete locally
        sftp(address, port, username, pwd, remworkdir, '/chunked/' + lang + '.txt')
        os.remove('./chunked/' + lang + '.txt')
