#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Eevee'
SITENAME = 'fuzzy notepad'
SITEURL = ''
#SITESUBTITLE = ...

TIMEZONE = 'America/Los_Angeles'
DEFAULT_DATE_FORMAT = '%a %b %d, %Y'

DEFAULT_LANG = 'en'

# Most of our time spent is on markdown parsing and Typogrify and whatnot, so, avoid redoing those
# constantly
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True
#CONTENT_CACHING_LAYER = 'generator'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Custom: Consistent delimiter in <title> tags
TITLE_DELIMITER = '/'

# Custom: Pretty names and descriptions for categories and series
CATEGORY_NAMES = {
    'articles': "Articles",
    'bleats': "Bleats",
    'corral': "Corral",
    'dev': "Dev log",
    'personal': "Personal",
    'process': "Process",
    'updates': "Updates",
}
CATEGORY_BLURBS = {
    'articles': "Longform stuff.  Effortposting.",
    'bleats': "Short, sweet, and slightly too long for Bluesky.",
    'corral': "Collections of recent links I saw and enjoyed.",
    'dev': "Brief, low-context updates on recent work.  Mostly deprecated.",
    'personal': "Very specific to me.",
    'process': "Deep dives into my own work, either a small project or a piece of a larger one.",
    'updates': "New releases or major updates of games, tools, the website, etc.",
}
SERIES_NAMES = {
    'birthday': "🎂 Eevee gained EXP",
    'cheezball rising': "🎑 Cheezball Rising",
    'game night': "🎲 Game night",
    'gamedev from scratch': "🔩 Gamedev from scratch",
    'make a doom level': "👺 You should make a Doom level",
    'monday night itch': "🦠 Monday night Itch",
    'python faq': "🐍 Python FAQ",
}
SERIES_BLURBS = {
    'birthday': "",
    'cheezball rising': "",
    'game night': "",
    'gamedev from scratch': "",
    'make a doom level': "",
    'monday night itch': "",
    'python faq': "",
}

# Custom: Links and social cruft
# NOTE: These aren't called just LINKS and SOCIAL because those are assumed by
# the default theme to be 2-tuples, but I need more info.
SOCIAL_EX = (
    ("email", '#9966cc', 'logo-email.png', 'mailto:eevee.fuzzynotepad@veekun.com'),
    ("Bluesky", '#1185fe', 'logo-bluesky.svg', 'https://bsky.app/profile/eev.ee'),
    ("Discord", '#5865F2', 'logo-discord.svg', 'https://discord.gg/W7aumDVTgE'),
    ("itch.io", '#fa5c5c', 'logo-itch.png', 'https://eevee.itch.io/'),
    ("GitHub", '#4183c4', 'logo-github.png', 'https://github.com/eevee'),
    ("Twitch", '#6441a4', 'logo-twitch.png', 'https://twitch.tv/lexyeevee'),
    ("YouTube", '#cc181e', 'logo-youtube.png', 'https://www.youtube.com/user/lexyeevee'),
    ("Patreon", '#ff5900', 'logo-patreon.png', 'https://www.patreon.com/eevee'),
    ("Square", '#29c501', 'logo-square-cash.png', 'https://cash.me/$eevee'),
    ("PayPal", '#009cde', 'logo-paypal.png', 'https://www.paypal.me/lexyeevee'),
)
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

def sort_by_article_count(tags):
    return sorted(tags, key=lambda pairs: len(pairs[1]), reverse=True)

JINJA_FILTERS = dict(
    sort_by_article_count=sort_by_article_count,
)

EXTRA_HEADER = """
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery.colorbox/1.6.4/jquery.colorbox-min.js"></script>
<script>
    $(function() {
        $('article').each(function(index, article) {
            $(article).find('a.photo').colorbox({
                fixed: true,
                maxWidth: '100%',
                maxHeight: '100%',
                rel: 'colorbox' + String(index + 1),
                // Text
                previous: '←',
                next: '→',
                close: '×',
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

MARKDOWN = dict(
    extension_configs={
        'markdown.extensions.codehilite': dict(
            css_class='highlight',
            linenos='inline',
            guess_lang=False,
            # Tell the PHP lexer not to require <?php, so snippets work
            startinline=True,
        ),
        'markdown.extensions.extra': {},
        # GitHub-style fenced code blocks
        'markdown.extensions.fenced_code': {},
        # I don't actually care about a table of contents, but this turns headers
        # into self-links
        'markdown.extensions.toc': dict(anchorlink=True),
    },
)

PATH = 'content'
PAGE_PATHS = ['pages']
PATH_METADATA = 'pages/(?P<fullpath>.+)[.].+'
STATIC_PATHS = ['favicon.png', 'media/', 'dev/media/']

# Leave .html alone; I only use it for static attachments, not posts
READERS = dict(html=None)

# For the landing page
TEMPLATE_PAGES = {
    '../theme/templates/home.html': 'index.html',
}

# URL schema; compatible with Octopress, but i happen to like it anyway
ARCHIVES_URL = 'blog/archive/'
ARCHIVES_SAVE_AS = 'blog/archive/index.html'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
# Skipping these; they're at the top of the blog index
CATEGORIES_URL = ''
CATEGORIES_SAVE_AS = ''
CATEGORY_URL = 'blog/{slug}/'
CATEGORY_SAVE_AS = 'blog/{slug}/index.html'
INDEX_URL = 'blog/'
INDEX_SAVE_AS = 'blog/index.html'
PAGE_URL = '{fullpath}/'
PAGE_SAVE_AS = '{fullpath}/index.html'
TAG_URL = 'blog/tags/{slug}/'
TAG_SAVE_AS = 'blog/tags/{slug}/index.html'
TAGS_URL = 'blog/tags/'
TAGS_SAVE_AS = 'blog/tags/index.html'

# Octopress-compatible filename metadata parsing
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
# Slug fallback for pages
SLUGIFY_SOURCE = 'basename'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


### Plugins
# Some minor hackery to have multiple PLUGIN_PATHs, since I want both canonical
# plugins and one of my own...
import os.path
import sys
sys.path.insert(0, os.path.dirname(__file__))
import eeveeblog.liquid_gallery
import eeveeblog.liquid_illus
import eeveeblog.liquid_photo

# Add a Pygments lexer, which seems to require hacking Pygments guts.  It's also possible to do this
# with, like, package metadata, but I don't have a package lol
from eeveeblog.rgbasm_lexer import RGBASMLexer
import pygments.lexers._mapping
pygments.lexers._mapping.LEXERS['RGBASMLexer'] = (
    'eeveeblog.rgbasm_lexer',
    RGBASMLexer.name,
    tuple(RGBASMLexer.aliases),
    tuple(RGBASMLexer.filenames),
    tuple(RGBASMLexer.mimetypes))

PLUGIN_PATHS = ["pelican-plugins.git", "render-math.git"]
PLUGINS = [
    # Mine
    eeveeblog.liquid_gallery,
    eeveeblog.liquid_illus,
    eeveeblog.liquid_photo,

    # Old pelican-plugins repo
    'summary',                      # not ported
    # nb: there's a third-party version of this but the pelican-plugins one seems to override it
    'pelican.plugins.readtime',

    # New individual pelican plugins
    'pelican.plugins.photos',       # installed, but, i think i altered locally...
    'pelican.plugins.render_math',  # installed
    'pelican.plugins.series',       # installed
    'pelican.plugins.thumbnailer',  # installed
]

# Plugin config for summary
SUMMARY_BEGIN_MARKER = '<!-- just kidding i never use this -->'
SUMMARY_END_MARKER = '<!-- more -->'  # octopress compat
# This is actually a stock setting; I don't want an automatic summary if I
# don't use an explicit marker
SUMMARY_MAX_LENGTH = None

# Plugin config for photos
PHOTO_LIBRARY = 'content/galleries/'
PHOTO_GALLERY = (1280, 1280, 95)
PHOTO_ARTICLE = (320, 320, 95)
PHOTO_THUMB = (224, 224, 95)
# The dumb fucking thing uses multiprocessing and passes along the ENTIRE
# SETTINGS DICT, which includes everything in this file, which includes
# PLUGINS, which (necessarily) includes a module reference, which is
# unpickleable, which causes the who dang thing to silently fail.  This puts it
# in "debug" mode and does the processing in-process.
PHOTO_RESIZE_JOBS = -1

# Plugin config for thumbnailer
IMAGE_PATH = 'media'
THUMBNAIL_DIR = 'media'
THUMBNAIL_SIZES = dict(m='?x150')
THUMBNAIL_KEEP_NAME = False
THUMBNAIL_KEEP_TREE = True

# Plugin config for readtime
READTIME_WPM = 240
