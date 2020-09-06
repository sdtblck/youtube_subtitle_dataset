import traceback, argparse
from multiprocessing import Pool, cpu_count
from itertools import repeat
from downloader_class import Subtitles_downloader
import csv, os


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def download_subs_single(queries, out_path="out", save_links=True, scrolldown=1000):
    try:
        sub_downloader = Subtitles_downloader(out_path=out_path, save_links=save_links, scrolldown=scrolldown)
        sub_downloader.search(queries)
        sub_downloader.download_subs()
    except:
        traceback.print_exc()


def download_subs_mp(queries, out_path="out", save_links=True, scrolldown=1000):
    queries = chunks(queries, (len(queries) // cpu_count() - 1))
    with Pool(cpu_count() - 1) as p:
        p.starmap(download_subs_single, zip(queries, repeat(out_path), repeat(save_links), repeat(scrolldown)))
    print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI for YT_subtitles - extracts Youtube subtitles from a list of search terms')
    parser.add_argument('search_terms',
                        help='A comma separated list of search terms, alternatively, pass path to a csv with the -c '
                             'argument',
                        type=str)
    parser.add_argument('--out_path', help='Output location for final .txt files', type=str, required=False,
                        default='output')
    parser.add_argument('-s', '--save_links', help='whether to save links to a .csv file', action="store_false")
    parser.add_argument('-c', '--csv',
                        help='if true, positional arg should be a path to a .csv file containing search terms',
                        action="store_true")
    parser.add_argument('--scroll', help='how far to scroll down in the youtube search', type=int, required=False,
                        default=1000)
    args = parser.parse_args()
    os.makedirs(args.out_path, exist_ok=True)
    if args.save_links:
        os.makedirs("links", exist_ok=True)
    if not args.csv:
        search_terms = args.search_terms.split(',')
    else:
        search_terms = []
        with open(args.search_terms, newline='') as inputfile:
            for row in csv.reader(inputfile):
                search_terms.append(row)
        # flattens list of list into unique list of items that aren't empty
        search_terms = list(set([item for sublist in search_terms for item in sublist if item]))
    print('Searching Youtube for: \n {}'.format(search_terms))
    download_subs_mp(search_terms, args.out_path, args.save_links, args.scroll)
