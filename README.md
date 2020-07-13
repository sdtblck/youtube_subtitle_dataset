# YT_subtitles
YT_subtitles - extracts subtitles from YouTube videos to raw text for Language Model training.

# Usage
YT_subs.py [-h] [-n N_RESULTS] [--client_secret CLIENT_SECRET]
                  search_terms

CLI for YT_subtitles - extracts subtitles from YouTube videos.

positional arguments:
  search_terms          A list of search terms separated by commas. (if you
                        have spaces in the search terms, the argument must be
                        encapsulated in double quotes.)

optional arguments:
  -h, --help            show this help message and exit
  -n N_RESULTS, --n_results N_RESULTS
                        number of links to gather. default = 1000
  --client_secret CLIENT_SECRET
                        Path to client secret file needed to access YouTube's
                        API

