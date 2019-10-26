"""Liquid-style tag for inserting an illustration."""

import os.path
import re
import sys

sys.path.insert(0, 'pelican-plugins.git')

from liquid_tags.mdx_liquid_tags import LiquidTags


@LiquidTags.register('illus')
def photo(preprocessor, tag, markup):
    # Syntax: {% illus [float] (filename) [alt text] %}
    m = re.fullmatch(r'\s* (float \s+)? (\S+) (?:\s+ (.+))? \s*', markup, re.VERBOSE)
    if not m:
        raise ValueError(f"{{% illus %}} syntax error, somewhere: {markup!r}")

    is_float, path, alt = m.groups()

    if not alt.strip():
        alt = ''

    if is_float:
        cls = 'prose-illustration'
    else:
        cls = 'prose-full-illustration'

    # TODO escaping??
    # TODO doesn't use site root, but that happens to be / for us
    return f'<div class="{cls}"><img src="{path}" alt="{alt}"></div>'


# this import makes pelican registration work
from liquid_tags import register
