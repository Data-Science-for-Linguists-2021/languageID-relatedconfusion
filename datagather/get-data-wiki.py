import wikipedia
import requests
import subprocess
import re
import json

if __name__ == '__main__':
    outpath = './'
    langs = wikipedia.languages() #dictionary where key is code, value is language name in that language
    i = 0
    for lang in langs.keys():
        if i > 5:
            break
        i += 1
        print(lang, langs[lang])

        try:
            # download the dump, save raw to file
            dumpname = lang + 'wiki-latest-pages-articles.xml.bz2'
            dumplink = 'https://dumps.wikimedia.org/' + lang + 'wiki/latest/' + dumpname
            r = requests.get(dumplink, allow_redirects=True)

            fsz = int(r.headers['Content-length'])
            print(fsz)
            if fsz < 2**20: #filesize less than 1 MB
                print('wiki too small')
                continue

        except:
            print('empty wiki')
            continue

        #remove XML
        print('remove XML')
        open('./dumps/'+lang+'-raw.xml.bz2', 'wb').write(r.content)
        subprocess.call(['sh', './get-data-wiki.sh', './dumps/'+lang+'-raw.xml.bz2', lang])

        fname = './extracted/' + lang + '.txt' #temp file created by the shell script
        f = open(fname, 'r')
        l = f.readlines()
        f.close()

        print('fix encoding')
        #fix encoding
        l = [ w.encode('utf-8').decode('raw_unicode_escape') for w in l]

        # parse jsons, do some cleaning of remaining XML junk
        print('parse jsons')
        texts = ''
        for line in l:
            try:
                article = json.loads(line)
                text = re.sub('\n|&lt.*;|http://.*|__.*__', ' ', article['text'])
                text = re.sub('&amp;', '&', text)
                if len(text) > 0:
                    texts = texts + ' ' + text
            except:
                continue

        # tokenize
        f = open(fname, 'w')
        f.writelines(texts)
        f.close()
        subprocess.call(['sh', './tokenize.sh', lang, fname, './extracted/tokenized-'+lang+'.txt'])
        f = open('./extracted/tokenized-'+lang+'.txt', 'r')
        texts = f.read()
        f.close()

        # remove punctuation

        # split to 500-char chunks
        print('chunking')
        chunks = []
        n = 500
        print(len(texts))
        while len(texts) > 500:
            chunk = texts[:500] # remove 1st and last "word" since it could be cut in middle
            chunks.append(chunk)
            texts = texts[500:]
        if len(texts) > 350:
            chunks.append(texts)

        # todo: shuffle chunks, then limit to 10000 chunks per language?

        # write to file
        print('writing')
        out = '\n'.join(chunks)
        f = open('./extracted/' + lang + '.txt', 'w')
        f.writelines(out)
        f.close()
