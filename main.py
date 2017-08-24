# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT

import sys
#from urllib import urlencode
from urlparse import parse_qsl
#import xbmcgui
#import xbmcplugin
import urllib, urllib2, cookielib
import json

username = ''
password = ''

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
opener.open('https://streama.example.net/login/authenticate', login_data)

shows = opener.open('https://streama.example.net/dash/listShows.json')
movies = opener.open('https://streama.example.net/dash/listMovies.json')
genericmovies = opener.open('https://streama.example.net/dash/listGenericVideos.json')
genres = opener.open('https://streama.example.net/dash/listGenres.json')

# https://streama.example.net/tvShow/episodesForTvShow.json?id=35
# https://streama.example.net/video/show.json?id=130
# https://streama.example.net/dash/searchMedia.json?query=crowd 

print shows.read()
print movies.read()
print genericmovies.read()
print genres.read()
