# Description

YT_subtitles is a tool for building a dataset from youtube subtitles. It extracts the (non machine-generated) subtitles
from all the videos returned by a list of search terms.

The resulting files contain a string of text per language, per minute of subtitles, with the name of the language appended
as a header. The dataset is designed to improve the multilingual performance of language models trained on it.
If only a single language is available, the output is just a text version of the subtitles, with no metadata.

# Setup

`pip install -r requirements.txt`

# Usage

```
CLI for YT_subtitles - extracts Youtube subtitles from a list of search terms

positional arguments:
  search_terms         A comma separated list of search terms, alternatively,
                       pass path to a csv with the -c argument

optional arguments:
  -h, --help           show this help message and exit
  --out_path OUT_PATH  Output location for final .txt files (default "output")
  -s, --save_links     whether to save links to a .csv file (default True)
  -c, --csv            if true, positional arg should be a path to a .csv file
                       containing search terms (default False)
  --scroll SCROLL      how far to scroll down in the youtube search (default 1000)
```

e.g

`python get_subs.py -c examples.csv`

or

`python get_subs.py movie review,GPT-3,true crime documentary`