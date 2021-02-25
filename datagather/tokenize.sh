# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

# Tokenize text data in various languages
# Usage: e.g.   tokenize.sh ar file.txt
# WARNING: OVERWRITES THE FILE WITH ITS OUTPUT

set -e

N_THREADS=8

lg=$1
file=$2
outfile=$3
TOOLS_PATH=~/Documents/skola/dl/proj/XLM/tools #$PWD/tools

# moses
MOSES=$TOOLS_PATH/mosesdecoder
REPLACE_UNICODE_PUNCT=$MOSES/scripts/tokenizer/replace-unicode-punctuation.perl
NORM_PUNC=$MOSES/scripts/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$MOSES/scripts/tokenizer/remove-non-printing-char.perl
TOKENIZER=$MOSES/scripts/tokenizer/tokenizer.perl

# Chinese
if [ "$lg" = "zh" ]; then
  $TOOLS_PATH/stanford-segmenter-*/segment.sh pku /dev/stdin UTF-8 0 | $REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $lg | $REM_NON_PRINT_CHAR
# Thai
elif [ "$lg" = "th" ]; then
  cat $file | $REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $lg | $REM_NON_PRINT_CHAR | python $TOOLS_PATH/segment_th.py > $file
# Japanese
elif [ "$lg" = "ja" ]; then
  cat $file | $REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $lg | $REM_NON_PRINT_CHAR | kytea -notags > $file
# other languages
else
  cat $file | $REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $lg | $REM_NON_PRINT_CHAR | $TOKENIZER -no-escape -threads $N_THREADS -l $lg > $outfile
fi
