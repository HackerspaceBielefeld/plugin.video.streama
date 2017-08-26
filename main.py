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

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
opener.open('https://streama.example.net/login/authenticate', login_data)

# read 
shows = opener.open('https://streama.example.net/dash/listShows.json')
movies = opener.open('https://streama.example.net/dash/listMovies.json')
genericmovies = opener.open('https://streama.example.net/dash/listGenericVideos.json')
genres = opener.open('https://streama.example.net/dash/listGenres.json')

# https://streama.example.net/tvShow/episodesForTvShow.json?id=35
# https://streama.example.net/video/show.json?id=130
# https://streama.example.net/dash/searchMedia.json?query=crowd

# convert received json string to python datastructure
movies_json = json.loads(movies.read())

# read more data for the second movie (index 1) with API and movie ID
movie = opener.open('https://streama.example.net/video/show.json?id=' + str(movies_json[1]["id"]))

# convert json string to python data structure
movie_json = json.loads(movie.read())

# print title
print(movie_json[1]["title"])
# print src-url
print(movie_json["files"][0]["src"])
