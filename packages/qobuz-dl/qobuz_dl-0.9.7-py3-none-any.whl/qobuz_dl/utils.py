#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import re
import string
from typing import Tuple

from qobuz_dl.color import RED, YELLOW

from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3


WEB_URL = "https://play.qobuz.com/"
ARTISTS_SELECTOR = "td.chartlist-artist > a"
TITLE_SELECTOR = "td.chartlist-name > a"
EXTENSIONS = (".mp3", ".flac")

# used in case of error
DEFAULT_FORMATS = {
    "MP3": [
        "{artist} - {album} ({year}) [MP3]",
        "{tracknumber}. {tracktitle}",
    ],
    "Unknown": [
        "{artist} - {album}",
        "{tracknumber}. {tracktitle}",
    ],
}

logger = logging.getLogger(__name__)


class PartialFormatter(string.Formatter):
    def __init__(self, missing="n/a", bad_fmt="n/a"):
        self.missing, self.bad_fmt = missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        try:
            val = super(PartialFormatter, self).get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            val = None, field_name
        return val

    def format_field(self, value, spec):
        if not value:
            return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt:
                return self.bad_fmt
            raise


def _clean_format_str(folder: str, track: str, file_format: str) -> Tuple[str, str]:
    """Cleans up the format strings, avoids errors
    with MP3 files.
    """
    final = []
    for i, fs in enumerate((folder, track)):
        if fs.endswith(".mp3"):
            fs = fs[:-4]
        elif fs.endswith(".flac"):
            fs = fs[:-5]
        fs = fs.strip()

        # default to pre-chosen string if format is invalid
        if (
            file_format in ("MP3", "Unknown")
            and "bit_depth" in file_format
            or "sampling_rate" in file_format
        ):
            default = DEFAULT_FORMATS[file_format][i]
            logger.error(
                f"{RED}invalid format string for format {file_format}"
                f". defaulting to {default}"
            )
            fs = default
        final.append(fs)

    return tuple(final)


def _safe_get(d: dict, *keys, default=None):
    """A replacement for chained `get()` statements on dicts:
    >>> d = {'foo': {'bar': 'baz'}}
    >>> _safe_get(d, 'baz')
    None
    >>> _safe_get(d, 'foo', 'bar')
    'baz'
    """
    curr = d
    res = default
    for key in keys:
        res = curr.get(key, default)
        if res == default or not hasattr(res, "__getitem__"):
            return res
        else:
            curr = res
    return res


def make_m3u(pl_directory):
    track_list = ["#EXTM3U"]
    rel_folder = os.path.basename(os.path.normpath(pl_directory))
    pl_name = rel_folder + ".m3u"
    for local, dirs, files in os.walk(pl_directory):
        dirs.sort()
        audio_rel_files = [
            # os.path.abspath(os.path.join(local, file_))
            # os.path.join(rel_folder,
            #              os.path.basename(os.path.normpath(local)),
            #              file_)
            os.path.join(os.path.basename(os.path.normpath(local)), file_)
            for file_ in files
            if os.path.splitext(file_)[-1] in EXTENSIONS
        ]
        audio_files = [
            os.path.abspath(os.path.join(local, file_))
            for file_ in files
            if os.path.splitext(file_)[-1] in EXTENSIONS
        ]
        if not audio_files or len(audio_files) != len(audio_rel_files):
            continue

        for audio_rel_file, audio_file in zip(audio_rel_files, audio_files):
            try:
                pl_item = (
                    EasyMP3(audio_file) if ".mp3" in audio_file else FLAC(audio_file)
                )
                title = pl_item["TITLE"][0]
                artist = pl_item["ARTIST"][0]
                length = int(pl_item.info.length)
                index = "#EXTINF:{}, {} - {}\n{}".format(
                    length, artist, title, audio_rel_file
                )
            except:  # noqa
                continue
            track_list.append(index)

    if len(track_list) > 1:
        with open(os.path.join(pl_directory, pl_name), "w") as pl:
            pl.write("\n\n".join(track_list))
            logger.info(f"{YELLOW}Playlist created: {pl_name}")


def format_duration(duration):
    return time.strftime("%H:%M:%S", time.gmtime(duration))


def create_clean_dir(directory=None):
    fix = os.path.normpath(directory)
    os.makedirs(fix, exist_ok=True)
    return fix


def get_id_from_url(url):
    return re.match(
        r"https?://(?:w{0,3}|play|open)\.qobuz\.com/(?:(?:album|track"
        r"|artist|playlist|label)/|[a-z]{2}-[a-z]{2}/album/-?\w+(?:-\w+)*"
        r"-?/|user/library/favorites/)(\w+)",
        url,
    ).group(1)


def get_url_type(url):
    if re.match(r"https?", url) is not None:
        url_type = url.split("/")[3]
        if url_type not in ["album", "artist", "playlist", "track", "label"]:
            if url_type == "user":
                url_type = url.split("/")[-1]
            else:
                # url is from Qobuz store
                # e.g. "https://www.qobuz.com/us-en/album/..."
                url_type = url.split("/")[4]
    else:
        # url missing base
        # e.g. "/us-en/album/{artist}/{id}"
        url_type = url.split("/")[2]
    return url_type
