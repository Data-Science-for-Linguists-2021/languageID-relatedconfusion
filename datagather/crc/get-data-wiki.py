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


def sftp(address, port, usr, pwd, fname):
    try:
        print("sftp port " + port + " of " + usr + "@" + address + ", transferring : " +
                     fname)
        client = paramiko.client.SSHClient()
        client.load_system_host_keys() # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, port=port, username=usr, password=pwd)
        sftp = client.open_sftp() # type SFTPClient
        print(sftp.put(fname, fname)) #src, dest path/filename
        client.close()
    except IOError:
        print(".. host " + address + " is not up or some other error occured")
        return "host not up", "host not up"


if __name__ == '__main__':
    statmsgs = True # whether or not to output mid-language status updates
    outpath = './'
    langs = wikipedia.languages() #dictionary where key is code, value is language name in that language

    # authenticate to storage device
    authenticated = False
    pwd = ''
    while not authenticated:
        pwd = getpass.getpass(prompt='sftp password: ')
        authenticated = check_pwd("8.tcp.ngrok.io", "17387", "snc", pwd)
        if not authenticated:
            print('authentication failed. try again')
        else:
            print('authenticated.')

    # create dumps, extracted dirs
    if 'dumps' not in os.listdir():
        os.mkdir('dumps')
    if 'extracted' not in os.listdir():
        os.mkdir('extracted')
    if 'texts' not in os.listdir():
        os.mkdir('texts')

    # skip = True

    print('status\t\tcode\tlanguage name')
    print('------------------------------------')
    for lang in langs.keys():
        # if lang =='hr': ## useful for debugging
        #     skip = False
        # elif skip:
        #     continue
        # else:
        #     break

        try:
            # don't download dump if already have it from previous run:
            if lang + '-raw.xml.bz2' not in os.listdir('./dumps/'):
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
        if statmsgs: print('\tremove XML')
        subprocess.call(['sh', './get-data-wiki.sh', './dumps/'+lang+'-raw.xml.bz2', lang])

        fname = './extracted/' + lang + '.txt' #temp file created by the shell script
        f = open(fname, 'r')
        l = f.readlines()
        f.close()
        # TODO: send to device

        if statmsgs: print('\tclean 1')
        #fix encoding
        if lang != 'en':   #en corpus too big; crases on this step but doesn't need it anyways
            l = [ w.encode('utf-8').decode('raw_unicode_escape') for w in l]

        # parse jsons, do some cleaning of remaining XML junk
        pat = re.compile('\\n|\d|https?://.*|&lt.*;|__.*__')
        texts = ''
        for line in l:
            if len(texts) > 100000:
                break
            try:
                article = rapidjson.loads(line)
                text = article['text']
                text = re.sub(pat, ' ', text)
                if len(text) > 0:
                    texts = texts + ' ' + text
            except:
                continue

        # # tokenize
        # if statmsgs: print('\ttokenize')
        # f = open(fname, 'w')
        # f.writelines(texts)
        # f.close()
        # subprocess.call(['sh', './tokenize.sh', lang, fname, './extracted/tokenized-'+lang+'.txt'])
        # f = open('./extracted/tokenized-'+lang+'.txt', 'r')
        # texts = f.read()
        # f.close()

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
        # TODO: send to device

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
        f = open('./extracted/' + lang + '.txt', 'w')
        f.writelines([c+'\n' for c in chunks])
        f.close()
        # TODO: send to device

        #TODO: delete this language's local files
