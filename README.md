# YT_subtitles
YT_subtitles - extracts subtitles from YouTube videos to raw text for Language Model training.

# Usage
To run this script you need to have a google account and access to the Youtube API enabled with a client_secret file. Follow these instructions to get set up: https://developers.google.com/youtube/v3/quickstart/python . Once you're done, place your client secret in the same directory as the python script and name it client_secret.json, or point to it with the --client_secret CL arg.

the Youtube API limits requests to 10k per day.

YT_subs.py [-h] [-n N_RESULTS] [--client_secret CLIENT_SECRET]
                  search_terms

CLI for YT_subtitles - extracts subtitles from YouTube videos.

positional arguments:
  search_terms          A list of search terms separated by commas. (if you
                        have spaces in the search terms, the argument must be
                        encapsulated in double quotes.)

optional arguments:
  -n N_RESULTS, --n_results N_RESULTS
                        number of links to gather. default = 1000
  --client_secret CLIENT_SECRET
                        Path to client secret file needed to access YouTube's
                        API

