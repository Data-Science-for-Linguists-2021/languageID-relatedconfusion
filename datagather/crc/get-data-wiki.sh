#1 fname, 2 lang
python3 -m wikiextractor.WikiExtractor $1 --processes 8 --no-templates -q -o - \
| gsed "/^\s*\$/d" \
| grep -v "^<doc id=" \
| grep -v "</doc>\$" \
 > ./extracted/$2.txt
 # | gsed 's%\\n\|http://.*\|&lt.*;\|__.*__%%g' \
 # | gsed 's%\&amp%\&%g' \
