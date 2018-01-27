# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT

from __future__ import print_function

import json
import operator
import routing
import sys
import urllib
from urllib import urlencode
import urllib2
import urlparse
from urlparse import parse_qsl
import cookielib
import xbmcgui
import xbmcplugin
import xbmcaddon

addon = xbmcaddon.Addon('plugin.video.streama')
streamaurl = addon.getSetting('url')
username = addon.getSetting('username')
password = addon.getSetting('password')
maxval = addon.getSetting('maxval')

# Initialize the authentication
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
# Authenticate
opener.open(streamaurl + '/login/authenticate', login_data)

cookiestring = str(cj).split(" ")
sessionid = cookiestring[1].split("JSESSIONID=")
remember_me = cookiestring[5].split("streama_remember_me=")

VIDEOS = {'Search': [],
            'Shows': [],
            'Movies': [],
            'Generic Videos': [],
            'Genres': [],
            'New Releases': []}


# Get the list of Movies from Streama
# movies = opener.open(streamaurl + '/dash/listMovies.json')
# Put the list of movies into the category list
# VIDEOS['Movies'] = json.loads(movies.read())

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Initialize the authentication
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
# Authenticate
opener.open(streamaurl + '/login/authenticate', login_data)

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    # return the list of categories
    return VIDEOS.iterkeys()


def get_videos(category, showid):
    if category == 'Shows':
        items = opener.open(streamaurl + '/dash/listShows.json?max=' + maxval)
        videolist = json.loads(items.read())
        return videolist["list"]
    elif category == 'Episodes':
        items = opener.open(streamaurl + '/tvShow/EpisodesForTvShow.json?id=' + showid)
        videolist = json.loads(items.read())
        return videolist["list"]
    elif category == 'Movies':
        items = opener.open(streamaurl + '/dash/listMovies.json?max=' + maxval)
        videolist = json.loads(items.read())
        return videolist["list"]
    elif category == 'Generic Videos':
        items = opener.open(streamaurl + '/dash/listGenericVideos.json')
        videolist = json.loads(items.read())
        return videolist["list"]
    elif category == 'Genres':
        items = opener.open(streamaurl + '/dash/listGenres.json')
        videolist = json.loads(items.read())
        return videolist
    elif category == 'New Releases':
        items = opener.open(streamaurl + '/dash/listNewReleases.json')
        videolist = json.loads(items.read())
        return videolist
    elif category == 'Search':
        dialog = xbmcgui.Dialog()
        searchstring = dialog.input('Search:', type=xbmcgui.INPUT_ALPHANUM)
        searchstring = urllib.quote_plus(searchstring)
        items = opener.open(streamaurl + '/dash/searchMedia.json?query=' + searchstring)
        videolist = json.loads(items.read())
        return videolist
    else:
        items = []
        videolist = json.loads(items.read())
        return videolist


def list_categories():
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        url = get_url(action='listing', category=category, showid=0)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category, showid):
    # Get the list of videos in the category.
    videos = get_videos(category, showid)

    if category == 'Shows':
        for video in videos:
            list_item = xbmcgui.ListItem(label=video['name'])
            try:
                list_item.setArt({'thumb': 'https://image.tmdb.org/t/p/w500//' + video['poster_path'], 'icon': 'https://image.tmdb.org/t/p/w500//' + video['poster_path']})
            except:
                foo = 23
            id = video['id']
            url = get_url(action='listing', category='Episodes', showid=id)
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    elif category == 'Episodes':
        for video in videos:
            if video['hasFile'] == 1:
                list_item = xbmcgui.ListItem(label='S'+str(video['season_number'])+'E'+str(video['episode_number'])+' '+video['name'])
                list_item.setInfo('video', {'title': 'S'+str(video['season_number'])+'E'+str(video['episode_number'])+' '+video['name'], 'genre': 'Test'})
                list_item.setArt({'thumb': 'https://image.tmdb.org/t/p/w300//' + video['still_path'], 'icon': 'https://image.tmdb.org/t/p/w300//' + video['still_path'], 'fanart': 'https://image.tmdb.org/t/p/w300//' + video['still_path']})
                list_item.setProperty('IsPlayable', 'true')
                id = video['id']
                url = get_url(action='play', video=id)
                is_folder = False
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    elif category == 'Movies':
        # Iterate through videos.
        for video in videos:
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=video['title'])
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': video['title'], 'genre': 'Test'})
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # Here we use the same image for all items for simplicity's sake.
            # In a real-life plugin you need to set each image accordingly.
            try:
                list_item.setArt({'thumb': 'https://image.tmdb.org/t/p/w500//' + video['poster_path'], 'icon': 'https://image.tmdb.org/t/p/w500//' + video['poster_path'], 'fanart': 'https://image.tmdb.org/t/p/w1280//' + video['backdrop_path']})
            except:
                    foo = 23
            # Set 'IsPlayable' property to 'true'.
            list_item.setProperty('IsPlayable', 'true')
            # Create a URL for a plugin recursive call.
            id = video['id']

            url = get_url(action='play', video=id)

            # Add the list item to a virtual Kodi folder.
            is_folder = False
            # Add our item to the Kodi virtual folder listing.
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    elif category == 'Generic Videos':
        for video in videos:
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=video['title'])
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': video['title'], 'genre': 'Test'})
            list_item.setProperty('IsPlayable', 'true')
            id = video['id']

            url = get_url(action='play', video=id)
            is_folder = False
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    elif category == 'Genres':
        for video in videos:
            list_item = xbmcgui.ListItem(label=video['name'])
            id = video['id']
            url = get_url(action='play', video=id)
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    elif category == 'New Releases':
        for video in videos:
            try:
                list_item = xbmcgui.ListItem(label=video['movie']['title'])
                id = video['movie']['id']
                url = get_url(action='play', video=id)
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
            except:
                foo = 23
            try:
                list_item = xbmcgui.ListItem(label=video['tvShow']['name'])
                id = video['tvShow']['id']
                url = get_url(action='listing', category='Episodes', showid=id)
                is_folder = True
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
            except:
                foo = 42

    elif category == 'Search':
        if len(videos['shows']) != 0:
            for i in range (0, len(videos['shows'])):
                list_item = xbmcgui.ListItem(label=videos['shows'][i]['name'])
                id = videos['shows'][i]['id']
                url = get_url(action='listing', category='Episodes', showid=id)
                is_folder = True
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        if len(videos['movies']) !=0:
            for i in range (0, len(videos['movies'])):
                list_item = xbmcgui.ListItem(label=videos['movies'][i]['title'])
                id = videos['movies'][i]['id']
                url = get_url(action='play', video=id)
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(id):
    # Get the JSON for the corresponding video from Streama
    movie = opener.open(streamaurl + '/video/show.json?id=' + id)
    # Create the path from resulting info
    movie_json = json.loads(movie.read())
    path = streamaurl + movie_json['files'][0]['src']

    # if path contains streamaurl, append sessionid-cookie and remember_me-cookie for auth
    if path.find(streamaurl) != -1:
        path = path + '|Cookie=JSESSIONID%3D' + sessionid[1] + '%3Bstreama_remember_me%3D' + remember_me[1] + '%3B'
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'], params['showid'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    router(sys.argv[2][1:])
