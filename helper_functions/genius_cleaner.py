"""
Functions to help get Genius data into a cleaner format
"""

import pandas as pd
import re


def get_song_info(album_json, album_directory, linebreak=True, artist=None):
    """
    Takes the bulk data from Genius and outputs a cleaner list

    Args:
        album_json: json file containing Genius data
        linebreak: boolean to include linebreaks in lyrics

    Returns:
        List of dictionaries containing relevant information
            for each song in an album
    """

    album_data = []

    headers = ["song_title", "artist", "album_title", "release_date", "lyrics"]

    album_df = pd.read_json(album_directory + album_json, orient="index")

    album_title = album_df.loc["name"][0]

    release_date = rel_date(album_df)

    for songs in album_df.loc["songs", :][0]:
        title = songs["title"]
        if artist == None:
            artist = songs["artist"]
        else:
            artist = artist
        lyrics = songs["lyrics"]
        lyrics = re.sub("\[.+?]", "", lyrics)
        if linebreak != True:
            lyrics = re.sub("(\\n)+", " ", lyrics)
        else:
            lyrics = re.sub("(\\n)+", "\n", lyrics)
        lyrics = re.sub("^ ", "", lyrics)
        lyrics = re.sub("^\\n", "", lyrics)
        data_list = [title, artist, album_title, release_date, lyrics]
        album_dict = dict(zip(headers, data_list))

        album_data.append(album_dict)

    return album_data


def rel_date(df):
    """
    Takes the broken up release date information and
        puts it into datetime format

    Args:
        df: Album dataframe from Genius

    Returns:
        Outputs release date in datetime format
    """

    release = df.loc["release_date_components"][0]
    year, month, day = (
        str(release["year"]),
        str(release["month"]),
        str(release["day"]),
    )
    date_st = year + month + day

    date_st = pd.to_datetime(date_st, format="%Y%m%d", errors="ignore")

    return date_st
