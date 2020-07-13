import pandas as pd
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from tqdm import tqdm
import glob, argparse
import parse_subs


def set_pandas_display_options(max_cols = 30, max_rows = 200):
    """
    Sets pandas display options.

    Parameters:

        max_cols: int, max number of cols to display

        max_rows: int, max number of rows to display

    """
    desired_width = 640
    pd.set_option('display.width', desired_width)
    # np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', max_cols)
    pd.set_option('display.max_rows', max_rows)


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def remove_empty_kwargs(**kwargs):
    # Remove keyword arguments that are not set
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def youtube_keyword(client, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.search().list(
        **kwargs
        ).execute()
    return response


def youtube_stats(video_id):
    # response = client.search()
    stats = client.videos().list(
        part='statistics, snippet',
        id=video_id).execute()
    return stats['items'][0]['statistics']['viewCount']


def youtube_search(criteria, max_res, res_per_page=50):
    # create lists and empty dataframe
    titles = []
    videoIds = []
    channelIds = []
    viewcounts = []
    resp_df = pd.DataFrame()
    pbar = tqdm(total=max_res + 1)
    while len(titles) < max_res:
        token = None
        response = youtube_keyword(client,
                                   part='id,snippet',
                                   maxResults=res_per_page,
                                   q=criteria,
                                   videoCaption='closedCaption',
                                   type='video',
                                   videoDuration='long',
                                   pageToken=token)

        for item in response['items']:
            titles.append(item['snippet']['title'])
            channelIds.append(item['snippet']['channelTitle'])
            videoIds.append(item['id']['videoId'])
            viewcount = youtube_stats(item['id']['videoId'])
            viewcounts.append(viewcount)

        token = response['nextPageToken']
        pbar.update(res_per_page)

    pbar.close()
    resp_df['title'] = titles
    resp_df['channelId'] = channelIds
    resp_df['videoId'] = videoIds
    resp_df['subject'] = criteria
    resp_df['viewcount'] = viewcounts
    return resp_df


def main(args):
    search_terms = args.search_terms.split(",")
    os.makedirs("links_out", exist_ok=True)  # make outdir
    for search_term in search_terms:
        search_term = search_term.strip(" ")
        inp = "[" + search_term.replace(" ", "+") + "]"  # reformat input
        results = youtube_search(inp, args.n_results)  # get search results

        # drop all videos with less than a certain viewcount
        # TODO: check viewcounts are in int form
        # remove_low_viewcounts = True
        # if remove_low_viewcounts:
        #     results = results.drop(results[results.viewcount < 1000].index)
        #TODO: filter videos less than a certain length

        print('Results:\n')
        print(results.head(20))
        results.to_csv(f"links_out/{search_term}.csv")
        ids = results["videoId"].tolist()

        # downloads subs for all videos into the current directory
        parse_subs.get_all_ccs_mp(ids)
        all_vtts = glob.glob(f"vtt_out/*.vtt")
        parse_subs.convert_vtts_mp(all_vtts)

if __name__ == "__main__":
    # TODO: YT's API quota is 10k requests a day, print custom error msg if it is exceeded
    parser = argparse.ArgumentParser(description='CLI for YT_subtitles - extracts subtitles from YouTube videos. ')
    parser.add_argument('search_terms',
                        help='A list of search terms separated by commas. (if you have spaces in the search terms, '
                             'the argument must be encapsulated in double quotes.)')
    parser.add_argument('-n', '--n_results', help="number of links to gather. default = 1000", required=False,
                        default=1000)
    parser.add_argument('--client_secret', help="Path to client secret file needed to access YouTube's API",
                        default="client_secret.json")
    args = parser.parse_args()

    CLIENT_SECRETS_FILE = args.client_secret
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    set_pandas_display_options()  # Set display options for printing pandas df
    client = get_authenticated_service()  # Authenticate w google API
    main(args)  # Run program





