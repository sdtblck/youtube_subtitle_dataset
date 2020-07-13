import os
from tqdm import tqdm
import webvtt, glob
from multiprocessing import Pool, cpu_count


def get_cc(vid, outpath="vtt_out", lang="en", verbosity=0):
    base_url = 'https://www.youtube.com/watch?v='
    url = base_url + vid
    if verbosity:
        cmd = ["youtube-dl", "--skip-download", "-o", f"{outpath}/{vid}", "--write-sub",
               "--sub-lang", lang, url]
    else:
        cmd = ["youtube-dl", "--skip-download","-q", "-o", f"{outpath}/{vid}", "--write-sub",
               "--sub-lang", lang, url]
    os.system(" ".join(cmd))


def get_all_ccs(vids, outpath="vtt_out"):
    os.makedirs(outpath, exist_ok=True)
    for vid in vids:
        get_cc(vid)


def get_all_ccs_mp(yt_ids):
    cpu_no = cpu_count() - 1
    os.makedirs(f"vtt_out", exist_ok=True)
    with Pool(cpu_no) as p:
        r = list(tqdm(p.imap(get_cc, yt_ids), total=len(yt_ids), desc="Downloading subtitles"))


def convert_vtt(path_to_file, out_folder="txt_out", delete_vtt=True):
    fn = os.path.split(path_to_file)[1]
    captions = webvtt.read(path_to_file)
    text = [caption.text for caption in captions]
    fn = fn.replace('.en', "")
    with open(f'{out_folder}/{fn[:-4]}.txt', 'w') as f:
        for item in text:
            item = item.replace('\n', ' ')
            item = item.replace('\t', ' ').strip().strip('-').strip('/')
            f.write(' "%s" ' % item)
    if delete_vtt:
        # remove files from local drive
        os.remove(path_to_file)


def convert_vtts(path_to_folder="vtt_out", out_folder="txt_out", delete_vtts=False):
    all_vtts = glob.glob(f"{path_to_folder}/*.vtt")
    os.makedirs('txt_out', exist_ok=True)
    #extract the text and times from the vtt file
    for file in all_vtts:
        convert_vtt(file, out_folder, delete_vtts)


def convert_vtts_mp(vtt_paths):
    cpu_no = cpu_count() - 1
    os.makedirs("txt_out", exist_ok=True)
    with Pool(cpu_no) as p:
        r = list(tqdm(p.imap(convert_vtt, vtt_paths), total=len(vtt_paths), desc="Converting vtts to txt"))