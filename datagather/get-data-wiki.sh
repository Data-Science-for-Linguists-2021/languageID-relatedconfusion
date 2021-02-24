#1 fname, 2 lang
TOKENIZE=~/Documents/skola/dl/proj/XLM/tools/tokenize.sh
python -m wikiextractor.WikiExtractor $1 --processes 8 --no-templates -q -o - \
| sed "/^\s*\$/d" \
| grep -v "^<doc id=" \
| grep -v "</doc>\$" \
 > ~/Documents/skola/ds/languageID-relatedconfusion/datagather/extracted/$2.txt
# | $TOKENIZE $2 \
# | python $LOWER_REMOVE_ACCENT \
