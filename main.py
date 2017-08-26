# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT

#                               #
# this file is just for testing #
#                               #

import sys
#from urllib import urlencode
from urlparse import parse_qsl
#import xbmcgui
#import xbmcplugin
import urllib, urllib2, cookielib
import json

#addon = xbmcaddon.Addon('plugin.video.streama')
#url = addon.getSetting('url')
username = '' #addon.getSetting('username')
password = '' #addon.getSetting('password')
streamaurl = 'https://streama.example.net'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
opener.open(streamaurl + '/login/authenticate', login_data)

# read 
shows = opener.open(streamaurl + '/dash/listShows.json')
movies = opener.open(streamaurl + '/dash/listMovies.json')
genericmovies = opener.open(streamaurl + '/dash/listGenericVideos.json')
genres = opener.open(streamaurl + '/dash/listGenres.json')

# https://streama.example.net/tvShow/episodesForTvShow.json?id=35
# https://streama.example.net/video/show.json?id=130
# https://streama.example.net/dash/searchMedia.json?query=crowd

# convert received json strings to python datastructure
movies_json = json.loads(movies.read())
shows_json = json.loads(shows.read())
genericmovies_json = json.loads(genericmovies.read())
genres_json = json.loads(genres.read())

# count the movies
print("There are " + str(len(movies_json)) + " Movies!")

# print title and src-url for every movie
for i in range(0, len(movies_json)):
    # read more data for the second movie (index 1) with API and movie ID
    movie = opener.open(streamaurl + '/video/show.json?id=' + str(movies_json[i]["id"]))

    # convert json string to python data structure
    movie_json = json.loads(movie.read())

    # print title
    print(movies_json[i]["title"])
    # print src-url
    print(movie_json["files"][0]["src"])

print

# Print shows
print("There are " + str(len(shows_json)) + " Shows!")

for i in range(0, len(shows_json)):
        show = opener.open(streamaurl + '/tvShow/episodesForTvShow.json?id=' + str(shows_json[i]["id"]))
        show_json = json.loads(show.read())

        print(shows_json[i]["name"])
        print("With " + str(len(show_json)) + " Episodes")

        for i in range(0, len(show_json)):
            print(show_json[i]["name"])
            episode = opener.open(streamaurl + '/video/show.json?id=' + str(show_json[i]["id"]))
            episode_json = json.loads(episode.read())

            # only print url, if there is a file available
            if str(episode_json["files"]) != '[]':
                print(episode_json["files"][0]["src"])
            else:
                print("No file!")
        print

