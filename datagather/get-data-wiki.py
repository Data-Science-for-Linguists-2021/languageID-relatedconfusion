import wikipedia
import requests
import subprocess

if __name__ == '__main__':
    outpath = './'
    langs = wikipedia.languages() #dictionary where key is code, value is language name in that language
    i = 0
    for lang in langs.keys():
        if i > 2:
            break
        i += 1
        print(lang, langs[lang])

        try:
            # download the dump, save to file
            dumpname = lang + 'wiki-latest-pages-articles.xml.bz2'
            dumplink = 'https://dumps.wikimedia.org/' + lang + 'wiki/latest/' + dumpname
            r = requests.get(dumplink, allow_redirects=True)

            fsz = int(r.headers['Content-length'])
            print(fsz)
            if fsz < 2**20: #filesize less than 1 MB
                print('wiki too small')
                continue

            open('./dumps/'+lang+'-raw.xml.bz2', 'wb').write(r.content)
            subprocess.call(['sh', './get-data-wiki.sh', './dumps/'+lang+'-raw.xml.bz2', lang])
            f = open('./extracted/' + lang + '.txt', 'r')
            l = f.readlines()
            f.close()
            l = [w.encode('utf-8').decode('raw_unicode_escape') for w in l]
            print(l[:10])

        except:
            print('empty wiki')
