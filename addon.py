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

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
opener.open(streamaurl + '/login/authenticate', login_data)

VIDEOS = {'New': [],
            'Movies': [],
            'Shows': [],
            'Genres': []}

movies = opener.open(streamaurl + '/dash/listMovies.json')
VIDEOS['Movies'] = json.loads(movies.read())

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.

# STRVIDEOS = opener.open('https://streama.example.net/dash/listGenres.json')
# streama output genres
#[{"id":1,"apiId":28,"name":"Action"},{"id":2,"apiId":12,"name":"Adventure"},{"id":3,"apiId":16,"name":"Animation"},{"id":4,"apiId":35,"name":"Comedy"},{"id":5,"apiId":80,"name":"Crime"},{"id":6,"apiId":99,"name":"Documentary"},{"id":7,"apiId":18,"name":"Drama"},{"id":8,"apiId":10751,"name":"Family"},{"id":9,"apiId":14,"name":"Fantasy"},{"id":10,"apiId":36,"name":"History"},{"id":11,"apiId":27,"name":"Horror"},{"id":12,"apiId":10402,"name":"Music"},{"id":13,"apiId":9648,"name":"Mystery"},{"id":14,"apiId":10749,"name":"Romance"},{"id":15,"apiId":878,"name":"Science Fiction"},{"id":16,"apiId":10770,"name":"TV Movie"},{"id":17,"apiId":53,"name":"Thriller"},{"id":18,"apiId":10752,"name":"War"},{"id":19,"apiId":37,"name":"Western"},{"id":20,"apiId":10759,"name":"Action & Adventure"},{"id":21,"apiId":10762,"name":"Kids"},{"id":22,"apiId":10763,"name":"News"},{"id":23,"apiId":10764,"name":"Reality"},{"id":24,"apiId":10765,"name":"Sci-Fi & Fantasy"},{"id":25,"apiId":10766,"name":"Soap"},{"id":26,"apiId":10767,"name":"Talk"},{"id":27,"apiId":10768,"name":"War & Politics"}]


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    # return movies_json
    return VIDEOS.iterkeys()
    # return STRVIDEOS.iterkeys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        # list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
        #                  'icon': VIDEOS[category][0]['thumb'],
        #                  'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['title'], 'genre': 'Test'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': 'https://image.tmdb.org/t/p/w500//' + video['poster_path'], 'icon': 'https://image.tmdb.org/t/p/w500//' + video['poster_path'], 'fanart': 'https://image.tmdb.org/t/p/w1280//' + video['backdrop_path']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        videosrc = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c0/Big_Buck_Bunny_4K.webm/Big_Buck_Bunny_4K.webm.720p.webm'
        #movie = opener.open(streamaurl + '/video/show.json?id=' + str(video['id']))
        #movie_json = json.loads(movie.read())
        #videosrc = movie_json['files'][0]['src'])
        url = get_url(action='play', video=videosrc)
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
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
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])


# cj = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
# opener.open('https://streama.example.net/login/authenticate', login_data)

# shows = opener.open('https://streama.example.net/dash/listShows.json')
# movies = opener.open('https://streama.example.net/dash/listMovies.json')
# genericmovies = opener.open('https://streama.example.net/dash/listGenericVideos.json')
# genres = opener.open('https://streama.example.net/dash/listGenres.json')

# https://streama.example.net/tvShow/episodesForTvShow.json?id=35
# https://streama.example.net/video/show.json?id=130
# https://streama.example.net/dash/searchMedia.json?query=crowd

# print shows.read()
# print movies.read()
# print genericmovies.read()
# print genres.read()
