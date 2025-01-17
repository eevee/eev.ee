#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False

SITEURL = 'https://eev.ee'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 20
FEED_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_RSS = 'feeds/rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'output-publish/'

# Following items are often useful when publishing

DISQUS_SITENAME = 'veekun'
#GOOGLE_ANALYTICS = 'UA-25539054-1'
