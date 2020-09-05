import csv
import math
import re
import random
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession, MaxRetries
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi


class Subtitles_downloader():

    def __init__(self, out_path="out", langs="all", save_links=True, scrolldown=10000):
        print('loading HTML session...')
        self.session = HTMLSession()
        self.sub_filter_code = "&sp=EgIoAQ%253D%253D"
        self.out_path = out_path
        self.langs = langs
        self.save_links = save_links
        self.scrolldown = scrolldown
        self.video_ids = []

    def search(self, queries):
        """
        returns a list of video ids for videos that match the search term, and have subtitles.
        :param queries: list of search queries
        :param scrolldown: number of times to page down
        """
        if isinstance(queries, list):
            for q in queries:
                search_url = "https://www.youtube.com/results?search_query={}{}".format(q, self.sub_filter_code)
                print('Fetching search results for "{}"...'.format(q))
                print('Fetching html content for "{}"...'.format(q))
                response = self.session.get(search_url)
                print('Executing JS...')
                try:
                    response.html.render(scrolldown=self.scrolldown, timeout=30.0)
                except MaxRetries as e:
                    print(e)
                    continue
                # create bs object to parse HTML
                soup = bs(response.html.html, "html.parser")
                # gets all video ids from soup
                query_ids = []
                for count, link in enumerate(
                        list(set(soup.findAll('a', attrs={'href': re.compile("^/watch\?v=.{8,12}")})))):
                    query_ids.append(link.get('href').split('v=')[1])
                self.video_ids.extend(query_ids)
                if self.save_links:
                    with open('links/{}_search_results.csv'.format(q), "w") as f:
                        writer = csv.writer(f)
                        writer.writerows([query_ids])
                print('{} unique links found for "{}"!'.format(count, q))
        else:
            raise TypeError("search queries must be list")

    def download_subs(self):
        for video_id in tqdm(list(set(self.video_ids)), desc="Downloading subtitles..."):
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            out = {}
            out_name = "{}/{}".format(self.out_path, video_id)
            total_minutes = -1
            n_langs = 0
            for t in transcript_list:
                if t.is_generated:
                    continue
                if self.langs != "all":
                    if t.language_code not in self.langs:
                        continue
                n_langs += 1
            for t in transcript_list:
                if t.is_generated:
                    continue
                if self.langs != "all":
                    if t.language_code not in self.langs:
                        continue
                transcript = t.fetch()
                out[t.language] = {}
                for i in transcript:
                    end = i["start"] + i["duration"]
                    minute = int(math.floor(end / 60.0))
                    if n_langs > 1:
                        header_txt = '\n{}: \n'.format(t.language)
                    else:
                        header_txt = ''
                    if minute > total_minutes:
                        total_minutes = minute
                    if minute in out[t.language]:
                        out[t.language][minute] += '{}\n'.format(i["text"])
                    else:
                        out[t.language][minute] = '{}{}\n'.format(header_txt, i["text"])

            with open("{}.txt".format(out_name), "w") as text_file:
                minutes = list(out.values())
                all_minutes = set(x for l in minutes for x in l)
                for m in all_minutes:
                    keys = list(out.keys())
                    random.shuffle(keys)
                    for l in keys:
                        try:
                            text_file.write(out[l][m])
                        except:
                            pass
