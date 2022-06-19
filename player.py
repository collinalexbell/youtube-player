# player.py
# This is a small python program that takes a list of YouTube URLs and plays the music
# It uses the YouTube API to know how long a video is and closes the video once the song has finished
# It then opens another YouTube video after the previous one has been finished and closed
# It loads the list of URLs from a file


import webbrowser
import time
import os
import sys
import urllib.request
import json
import random

# This function takes a YouTube URL and returns the length of the video in seconds
def get_video_length(url):
    # This is the API key for the YouTube API

    # Read api youtube key from file. Filename is "apikey"
    with open("apikey", "r") as f:
        api_key = f.read()
    # This is the URL for the YouTube API

    api_url = "https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id="
    # This is the ID of the video
    video_id = url.split("=")[1]
    # This is the full URL for the API
    full_url = api_url + video_id + "&key=" + api_key
    # This is the JSON data from the API
    json_data = urllib.request.urlopen(full_url).read()
    # This is the data in a dictionary
    data = json.loads(json_data)
    # This is the length of the video in ISO 8601 format
    duration = data["items"][0]["contentDetails"]["duration"]
    import re
    # This is the regex for the duration
    regex = re.compile(r'P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?')
    # This is the match for the regex
    match = regex.match(duration)
    if match is not None:
        video_length = int(match.group('days') or 0) * 86400 + int(match.group('hours') or 0) * 3600 + int(match.group('minutes') or 0) * 60 + int(match.group('seconds') or 0)
    else:
        video_length = 0
    return video_length

def play_music(urls):
    import threading
    for url in urls:
        threading.Thread(target=webbrowser.open_new_tab, args=(url,)).start()
        video_length = get_video_length(url)
        time.sleep(video_length)

def get_urls():
    urls = []
    with open('urls', 'r') as f:
        for line in f:
            urls.append(line.strip())
    return urls

play_music(get_urls())
