import os
from internetarchive import get_item, upload
from datetime import datetime
import argparse
from filelock import FileLock
from slug import create_slug
from episodes_file import save_episodes, read_episodes
from feed import feed_items, feed_tree

parser = argparse.ArgumentParser(description="Nao Ouvo Internet Archive upload CLI")

parser.add_argument("imagesdir", type=str, help="Images directory path")
parser.add_argument("--lockfile", required=True, type=str, help="Episodes lock file")
parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")

args = parser.parse_args()

nao_ouvo_dir = args.imagesdir
lock_path = args.lockfile
episodes_path = args.episodesfile
# load secrets
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")

lock = FileLock(lock_path, timeout=5)

def upload_images():
    files = os.listdir(nao_ouvo_dir)
    for file_name in files:
        title = os.path.splitext(file_name)[0]
        slug = create_slug(title)

        lock.acquire()
        try:
            episodes = read_episodes(episodes_path)
        finally:
            lock.release()
       
        if slug not in episodes["uploaded"]:
            print("not found: " + slug)

        print("----- uploading -----")

        file = os.path.join(nao_ouvo_dir, file_name)

        print(slug + " " + file)

        if os.path.isfile(file) == False:
            print("missing: "+ file)
            exit(1)

        try:
            print(ia_upload(slug, file))
        except Exception as e:
            print(f"Failed to upload {slug}: {e}")

        print("----- uploaded ------")
    
    #     file = os.path.join(nao_ouvo_dir, title + ".mp3")
    #
    #
    #         lock.acquire()
    #         try:
    #             episodes = read_episodes(episodes_path)
    #             episodes["failed"].append(slug)
    #             save_episodes(episodes_path, episodes)
    #         finally:
    #             lock.release()
    #
    #     lock.acquire()
    #     try:
    #         episodes = read_episodes(episodes_path)
    #         episodes["uploaded"].append(slug)
    #         episodes["uploading"].remove(slug)
    #         print("uploaded: " + slug)
    #         save_episodes(episodes_path, episodes)
    #     finally:
    #         lock.release()
    #



def format_date(date):
    dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    formatted_date = dt.strftime("%Y-%m-%d")
    return formatted_date

def ia_upload(slug, upload_file):
    r = upload(slug, files=[upload_file], access_key = access_key, secret_key = secret_key)
    return r


upload_images()
