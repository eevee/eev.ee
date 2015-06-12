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

# Links and social cruft
# NOTE: These aren't called just LINKS and SOCIAL because those are assumed by
# the default theme to be 2-tuples, but I need more info.
LINKS_EX = ((
    'doodles',
    'http://lexyeevee.tumblr.com/tagged/my+art',
    '#41c518', 'logo-doodles.png',
    "i'm learning to draw, here are the results.  occasionally nsfw!",
), (
    'cats',
    'http://lexyeevee.tumblr.com/tagged/sphynx',
    '#deb46a', 'logo-cats.png',
    "our house is overrun with them and they are the best",
))
SOCIAL_EX = ((
    'email',
    'mailto:eevee.fuzzynotepad@veekun.com',
    '#9966cc', 'logo-email.png',
    "like sending a facebook message, but with less facebook",
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
SEARCH_BOX = True

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
PAGE_PATHS = ['../pages/']
STATIC_PATHS = ['favicon.png', 'media']

# For the landing page
TEMPLATE_PAGES = {
    '../theme/templates/home.html': 'index.html',
}

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
# This is the /blog/ index specifically
INDEX_SAVE_AS = 'blog/index.html'
INDEX_URL = 'blog/'
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

PLUGIN_PATHS = ["pelican-plugins.git"]
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
