#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from functools import partial

AUTHOR = u'Eevee'
SITENAME = u'fuzzy notepad'
SITEURL = ''
#SITESUBTITLE = ...

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%a %b %d, %Y'

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Links and social cruft
# NOTE: These aren't called just LINKS and SOCIAL because those are assumed by
# the default theme to be 2-tuples, but I need more info.
LINKS_EX = ((
    'blog',
    'blog/',
    '#f6b441', 'category-blog.png',
    "detailed, thoughtful prose about why computers are the worst",
), (
    'dev',
    'dev/',
    '#ee7300', 'category-dev.png',
    "updates on cool things i make",
), (
#    'art',
#    '/art/',
#    '#41c518', 'category-art.png',
#    "i'm learning to draw, here are the results",
#), (
#    'cats',
#    'http://lexyeevee.tumblr.com/tagged/sphynx',
#    '#deb46a', 'category-cat-photos.png',
#    "our house is overrun with them and they are the best",
#), (
    'everything',
    'everything/',
    '#c57be6', 'category-everything.png',
    "why limit yourself when you can have it all",
))
SOCIAL_EX = ((
    'email',
    'mailto:eevee.fuzzynotepad@veekun.com',
    '#9966cc', 'logo-email.png',
    "i get so much spam because of this link; make it worth my while",
), (
    'twitter',
    'https://twitter.com/eevee',
    '#55acee', 'logo-twitter.png',
    "follow me for bad nerd jokes and yelling about computers",
), (
    'github',
    'https://github.com/eevee/',
    '#4183c4', 'logo-github.png',
    "a mausoleum for all the code i've ever written, then abandoned",
), (
    'patreon',
    'https://www.patreon.com/eevee',
    '#ff5900', 'logo-patreon.png',
    "force me to blog more often, with dollars",
), (
    'square cash',
    'https://cash.me/$eevee',
    '#29c501', 'logo-square-cash.png',
    "just plain give me money.  i don't know why you would do this",
))
TWITTER_USERNAME = 'eevee'
GITHUB_URL = 'https://github.com/eevee'
# i hate this stupid eyesore and i'm pretty sure my audience knows how to
# search a website with their favorite search engine
SEARCH_BOX = False

DEFAULT_PAGINATION = 17
DEFAULT_ORPHANS = 4
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

THEME = 'theme'

JINJA_FILTERS = dict(
    sort_by_article_count=partial(
        sorted,
        key=lambda pairs: len(pairs[1]),
        reverse=True,
    ),
)

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
# Stop putting &nbsp; in the fucking article titles
TYPOGRIFY_IGNORE_TAGS = [
    'pre', 'code', 'header', 'h1', 'h2', 'h3', 'aside',
]

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
PAGE_PATHS = ['../pages/']
PATH_METADATA = '../pages/(?P<fullpath>.+)[.].+'
STATIC_PATHS = ['favicon.png', 'media/', 'dev/media/']

# For the landing page
TEMPLATE_PAGES = {
    '../theme/templates/home.html': 'index.html',
}

# URL schema; compatible with Octopress, but i happen to like it anyway
ARCHIVES_URL = 'everything/archives/'
ARCHIVES_SAVE_AS = 'everything/archives/index.html'
ARTICLE_URL = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
CATEGORIES_URL = 'everything/categories/'
CATEGORIES_SAVE_AS = 'everything/categories/index.html'
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
# This is the /blog/ index specifically
INDEX_SAVE_AS = 'everything/index.html'
INDEX_URL = 'everything/'
PAGE_URL = '{fullpath}/'
PAGE_SAVE_AS = '{fullpath}/index.html'
TAG_URL = 'everything/tags/{slug}/'
TAG_SAVE_AS = 'everything/tags/{slug}/index.html'
TAGS_URL = 'everything/tags/'
TAGS_SAVE_AS = 'everything/tags/index.html'

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

PLUGIN_PATHS = ["pelican-plugins.git"]
PLUGINS = [
    eeveeblog.liquid_photo,
    'summary',
    'custom_article_urls',
    'photos',
    'thumbnailer',
    'optimize_images',
]

# Plugin config for summary
SUMMARY_BEGIN_MARKER = '<!-- just kidding i never use this -->'
SUMMARY_END_MARKER = '<!-- more -->'  # octopress compat
# This is actually a stock setting; I don't want an automatic summary if I
# don't use an explicit marker
SUMMARY_MAX_LENGTH = None

# Plugin config for custom article urls
# Preserve the old blog URL for blog stuff
CUSTOM_ARTICLE_URLS = {
    'blog': dict(
        URL='{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/',
        SAVE_AS='{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html',
    ),
}

# Plugin config for photos
PHOTO_LIBRARY = 'content/galleries/'
PHOTO_GALLERY = (1280, 1280, 95)
PHOTO_ARTICLE = (320, 320, 95)
PHOTO_THUMB = (224, 224, 95)

# Plugin config for thumbnailer
IMAGE_PATH = 'media'
THUMBNAIL_DIR = 'media'
THUMBNAIL_SIZES = dict(m='224x?')
THUMBNAIL_KEEP_NAME = False
THUMBNAIL_KEEP_TREE = True
