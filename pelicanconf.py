#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Adams Rosales'
SITENAME = 'Deciphering Big Data'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGIN_PATHS = ['/Users/adamsrosales/pelican-addon-clones/pelican-plugins']
PLUGINS = ['sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.5,
        'pages': 0.4
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}

# Static files to include with the site
STATIC_PATHS = ['static', "extra"]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/robots.txt': {'path': 'robots.txt'}
}

# Social widget
GITHUB_URL = 'https://github.com/adaros92'
LINKEDIN_URL = 'https://www.linkedin.com/in/adamsr09/'

# Homepage header cover
HEADER_COVER = 'static/masthead.jpg'

DEFAULT_PAGINATION = 8

THEME = "/Users/adamsrosales/pelican-addon-clones/pelican-themes/clean-blog"
