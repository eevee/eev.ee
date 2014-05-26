#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eevee'
SITENAME = u'fuzzy notepad'
SITEURL = ''
#SITESUBTITLE = ...

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
# TODO lol these don't exist in my theme and i'm not sure whether i care??
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social cruft
# TODO theme doesn't support this, but i'd kinda like it for the main page
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)
TWITTER_USERNAME = 'eevee'
GITHUB_URL = 'https://github.com/eevee'

DEFAULT_PAGINATION = 17
DEFAULT_ORPHANS = 4
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

THEME = 'theme'

EXTRA_HEADER = """
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery.colorbox/1.4.33/jquery.colorbox-min.js"></script>
<script type="text/javascript">
    $(function() {
        $('article').each(function(index, article) {
            console.log(index, article);
            $(article).find('a.photo').colorbox({
                fixed: true,
                maxWidth: '100%',
                maxHeight: '100%',
                rel: 'colorbox' + String(index + 1)
            });
        });
    });
</script>
"""

# Smart quotes and other things
TYPOGRIFY = True

MD_EXTENSIONS = [
    'codehilite(css_class=highlight,linenums=True)',
    'extra',
    # GitHub-style fenced code blocks
    'fenced_code',
    # I don't actually care about a table of contents, but this turns headers
    # into self-links
    'toc(anchorlink=True)',
]

PATH = 'content/'
PAGE_DIR = '../pages/'
STATIC_PATHS = ['favicon.png', 'media']

# URL schema; compatible with Octopress, but i happen to like it anyway
ARCHIVES_URL = 'blog/archives/'  # doesn't officially exist but whatever
ARCHIVES_SAVE_AS = 'blog/archives/index.html'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
CATEGORIES_URL = 'blog/categories/'
CATEGORIES_SAVE_AS = 'blog/categories/index.html'
CATEGORY_URL = 'blog/categories/{slug}/'
CATEGORY_SAVE_AS = 'blog/categories/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'blog/tags/{slug}/'
TAG_SAVE_AS = 'blog/tags/{slug}/index.html'
TAGS_URL = 'blog/tags/'
TAGS_SAVE_AS = 'blog/tags/index.html'

# Octopress-compatible filename metadata parsing
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


### Plugins
# Some minor hackery to have multiple PLUGIN_PATHs, since I want both canonical
# plugins and one of my own...
import os.path
import sys
sys.path.insert(0, os.path.dirname(__file__))
import eeveeblog.liquid_photo

PLUGIN_PATH = "pelican-plugins.git"
PLUGINS = [
    eeveeblog.liquid_photo,
    'summary'
]

# Plugin config for summary
SUMMARY_BEGIN_MARKER = '<!-- just kidding i never use this -->'
SUMMARY_END_MARKER = '<!-- more -->'  # octopress compat
# This is actually a stock setting; I don't want an automatic summary if I
# don't use an explicit marker
SUMMARY_MAX_LENGTH = None
