"""Liquid-style tag for inserting a gallery of images."""

from html import escape
import os.path
import re
import sys

sys.path.insert(0, 'pelican-plugins.git')

from liquid_tags.mdx_liquid_tags import LiquidTags


@LiquidTags.register('gallery')
def gallery(preprocessor, tag, markup):
    # Syntax is a little complex and newline-sensitive:
    # {% gallery [root directory]
    #   (filename) [caption] [| alt text]
    #   ...
    # %}
    lines = markup.split('\n')

    # First line contains the root directory, optionally
    root_dir = lines[0].strip() or '/'

    # TODO warn on empty gallery?
    # TODO warn on files that don't exist?  don't seem to have that much access tho

    # Others contain filenames
    items = []
    for line in lines[1:]:
        if not line or line.isspace():
            continue

        m = re.fullmatch(r'\s* ([^| ]+) (?:\s+ ([^|]*))? (?:[|]\s* (.*\S))? \s*', line, re.VERBOSE)
        if not m:
            raise ValueError(f"{{% gallery %}} got bad line: {line!r}")

        filename, caption, alt = m.groups()

        if not caption and not alt:
            caption = alt = ''
        elif not caption:
            caption = ''
        elif not alt:
            alt = caption

        path = os.path.join(root_dir, filename)
        # Add _m to the filename for now
        thumbnail_path = '_m'.join(os.path.splitext(path))

        # TODO doesn't use site root, but that happens to be / for us
        items.append(f'<a href="{path}" class="photo" title="{escape(caption, True)}"><img src="{thumbnail_path}" alt="{escape(alt, True)}"></a>\n')

    return '<div class="gallery">\n' + ''.join(items) + '</div>'


# this import makes pelican registration work
from liquid_tags import register
