"Functions related to the episode info DB"

import hashlib
import os
from os.path import expanduser

from sqlobject import SQLObject, col, sqlite, SQLObjectNotFound


class Episode(SQLObject):
    "A DB entry of things we want to remember about an episode"
    hash = col.UnicodeCol(unique=True, alternateID=True)
    pubdate = col.DateTimeCol()
    played = col.BoolCol(default=False)


def init_db(data_dir):
    Episode._connection = sqlite.builder()(
        expanduser(data_dir + os.sep + "episodes.db"), debug=False
    )
    Episode.createTable(ifNotExists=True)


def episode_hash(episode):
    return hashlib.sha1(episode["title"].encode("ascii", "ignore")).hexdigest()


def markDownloaded(episode):
    if not seen(episode):
        Episode(hash=episode.hash, pubdate=episode.pub_date)


def markPlayed(episode):
    e = seen(episode)
    e.played = True


def seen(episode):
    try:
        return Episode.byHash(episode.hash)

    except SQLObjectNotFound:
        return None
