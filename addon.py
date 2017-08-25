# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT

from __future__ import print_function
import operator
import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl, getSetting, setContent
import resources.lib.http as http
from resources.lib.helpers import maybe_json, calc_aspect, json_date_to_info
import sys
from urlparse import parse_qsl
import urllib, urllib2, cookielib
import json

plugin = routing.Plugin()
addon = xbmcaddon.Addon('plugin.video.streama')
url = addon.getSetting('url')
username = addon.getSetting('username')
password = addon.getSetting('password')

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

# print shows.read()
# print movies.read()
# print genericmovies.read()
 #print genres.read()
