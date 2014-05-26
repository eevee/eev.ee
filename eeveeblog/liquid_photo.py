"""Spiritual port of Devin Weaver's Jekyll {% photo %} tag."""

import os.path
import re
import sys

sys.path.insert(0, 'pelican-plugins.git')

from liquid_tags.mdx_liquid_tags import LiquidTags


@LiquidTags.register('photo')
def photo(preprocessor, tag, markup):
    # Syntax is: filename [thumbnail] [title]
    parts = markup.split(None, 2)
    if not markup or not parts or not parts[0]:
        raise ValueError("{% photo %} requires a filename")

    # Second part is a thumbnail if it contains a slash; otherwise it's part of
    # the title
    parts += ['', '']
    filename = parts[0]
    if '/' in parts[1]:
        thumbnail = parts[1]
        title = parts[2]
    else:
        # Add _m to the filename for now
        file_ext = os.path.splitext(filename)
        thumbnail = '_m'.join(file_ext)

        title = ' '.join(parts[1:3])


    return '<a href="{uri}" class="photo" title="{title}"><img src="{thumb_uri}" alt="{title}" /></a>'.format(
        uri=filename,
        thumb_uri=thumbnail,
        title=title,
    )


# this import makes pelican registration work
from liquid_tags import register
