import logging
import os
import re
import shutil
import time
from datetime import datetime as dt
from os.path import expanduser

import eyed3
import feedparser
import requests
from feedparser.util import FeedParserDict
from termcolor import cprint
from tqdm import tqdm

from . import ui
from .db import *

TEMPDIR = "/tmp/podpuller"
BADFNCHARS = re.compile(r"[^\w]+")


def hash_episode(episode, rss):
    episode.hash = episode_hash(episode)
    episode.pub_date = dt.fromtimestamp(time.mktime(episode.published_parsed))
    episode.podcast = rss.feed.title
    episode.publisher = rss.feed.author
    if hasattr(episode, 'image'):
        episode.imagelink = episode.image.href
    else:
        episode.imagelink = rss.feed.image.href



def get_episode(show, episode, dl_dir):

    dl_loc = expanduser(dl_dir) + os.sep + show + os.sep + generate_filename(episode)

    # Do we have this file?
    if os.path.exists(dl_loc):
        cprint(f"Already have: {episode.title}", "cyan")
        return True
    else:
        # We not have this file
        e = seen(episode)

        # We might have played and deleted it in the past, don't download again
        if e and e.played:
            cprint(f"Already listened: {episode.title}", "magenta")
            return False

    # If we are here, we want another episode, we don't have this one, and haven't played
    if download_episode(episode, dl_loc):
        markDownloaded(episode)
        return True

    return False


def download_episode(episode, dl_loc):
    """Performs downloading of specified file. Returns success boolean"""

    # Find and download first MPEG audio enclosure
    download_loc = download_enclosure(episode)
    if not download_loc:
        return False

    if download_loc == "dontwant":
        # Just mark as played but don't count
        cprint(f"Marked listened: {episode.title}", "magenta")
        markDownloaded(episode)
        return False

    # Updat ID3 tags
    tag_mp3file(download_loc, episode)

    # Move downloaded file to its final destination
    logging.debug(f"Moving {download_loc} to {dl_loc}")

    # Create show directory if necessary and move
    if not os.path.exists(os.path.dirname(dl_loc)):
        os.makedirs(os.path.dirname(dl_loc))
    shutil.move(download_loc, dl_loc)

    return True

def tag_mp3file(filepath, episode):

    f = eyed3.load(filepath)
    t = f.tag

    # Adjust version
    if t.isV1():
        t.version = eyed3.id3.ID3_V2_4

    t.title = episode.title
    t.artist = episode.publisher
    t.album = episode.podcast

    # Add album art
    type = eyed3.id3.frames.ImageFrame.FRONT_COVER
    r = requests.get(episode.imagelink)
    t.images.set(type, r.content, r.headers['Content-Type'])

    # Save ID3 tag
    t.save()


def download_enclosure(episode):
    """Downloads URL to file, returns file name of download (from URL or Content-Disposition)"""

    # Temp DL destination
    downloadto = TEMPDIR + os.sep + episode.hash
    if not os.path.exists(os.path.dirname(downloadto)):
        os.makedirs(os.path.dirname(downloadto))

    # Get link from first mpeg enclosure
    first_mp3 = list(filter(lambda x: x["type"] == "audio/mpeg", episode.enclosures))[0]
    url = first_mp3.href

    try:
        cprint(f"Downloading {episode.title}", "yellow")
        r = requests.get(url, stream=True, timeout=15)

        # Download with progress bar in 2k chunks
        with open(downloadto, "wb") as f:
            total_length = int(r.headers["content-length"])
            with tqdm(total=total_length, unit="B", unit_scale=True, ncols=90) as pbar:
                for chunk in r.iter_content(2048):
                    f.write(chunk)
                    if chunk:
                        pbar.update(len(chunk))

    except KeyboardInterrupt:
        if ui.interrupt_dl():
            # Mark as played
            return "dontwant"
        else:
            return None

    # TODO: Add MP3 metadata if it doesn't exist

    return downloadto


def generate_filename(episode):
    """Generates file name for this enclosure based on episode title."""
    entry_title = sanitize(episode.title)
    return f"{entry_title}.mp3"


def sanitize(str):
    return re.sub(BADFNCHARS, "_", str).strip("_")


def episode_location(dl_dir, show, episode):
    return expanduser(dl_dir) + os.sep + show + os.sep + generate_filename(episode)


def delete_episode(show, episode, dl_dir, manual=False):

    episode_loc = episode_location(dl_dir, show, episode)

    # Remove episode
    if os.path.exists(episode_loc):
        cprint(f"Removing: {episode.title}", "red")
        os.remove(episode_loc)
        return True

    return False


def parse_date(date_str):
    if not date_str:
        return None
    elif date_str == "now":
        return dt.now()
    else:
        try:
            d = dt.strptime(date_str, "%Y-%m-%d")
        except Exception:
            msg = "Date should be in YYYY-MM-DD format"
            raise AttributeError(msg)
        return d


def check_feederrors(rss):
    """Checks if the parsed RSS is actually a valid podcast feed"""

    # Not all bozo errors cause total failure
    if rss.bozo and isinstance(
        rss.bozo_exception,
        (
            type(FeedParserDict.NonXMLContentType),
            type(feedparser.CharacterEncodingOverride),
        ),
    ):
        raise rss.bozo_exception

    # When parsing a website or error message, title is missing.
    if "title" not in rss.feed:
        raise Exception("Not RSS Feed")
