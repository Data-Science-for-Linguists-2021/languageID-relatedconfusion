#1 fname, 2 lang
python -m wikiextractor.WikiExtractor $1 --processes 8 --no_templates -q -o - \
| sed "/^\s*\$/d" \
| grep -v "^<doc id=" \
| grep -v "</doc>\$" \
 > ./extracted/$2.txt
 # | sed 's%\\n\|http://.*\|&lt.*;\|__.*__%%g' \
 # | sed 's%\&amp%\&%g' \
