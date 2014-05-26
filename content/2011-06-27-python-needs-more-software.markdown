title: Python needs more software
date: 2011-06-27 03:21
tags: python
category: essay

Consider this a companion article.

I love Python.  It's healthy and thriving and attracts a lot of clever people.  It has its warts, but they're mostly manageable.

Unfortunately, it still strikes me as a bit invisible.  I haven't really been able to articulate _why_, but after reading a bunch of those Perl blogs that bring up CPAN, I think it might actually be the software.

For example: there's no good Python forum software.  I'm sure there are some bits and pieces here and there, but nothing that's attractive, feature-rich, and _easy to deploy_.  That last one is a bitch, I know, but it's important.  Right now, if I want to throw up a forum, my viable options are really phpBB, vBulletin, and some other crappy PHP things.  I think MyBB might be Perl, but who even uses that?

<!-- more -->

Likewise, there's little blog software, little wiki software, no fleshed-out equivalent to phpmyadmin, and so on.  Despite all the cool Python Web frameworks, the Python Web ecosystem really kinda sucks.  Most of those frameworks go towards building one-off custom applications; we have very few that are ready to go out of the box, like cake mix.

This is sort of an illusion, yes, but I feel it's one that makes Python look less obvious a choice for Web development.  If you ask me what PHP is used for, I can just say "phpBB"; it may be a single application, but it's all over the damned place.  Telling you that my blog is written in Python doesn't have the same effect, really.

The other problem is that a lot of the general-purpose libraries are kind of stagnant and have no decent alternatives.  PIL is the worst offender by far, here; it's barely been updated in years, has crappy documentation, can't open interlaced PNGs, and is vastly underpowered.  There's nothing better to use for image manipulation, so a whole section of potential applications are just quietly ignored.  We direly need some Pythonic GraphicsMagick bindings, or _something_.

Other niches are already filled, but by somewhat outdated software; urwid and Twisted come to mind.  Both are very solid projects, but they were written against ancient versions of Python, and don't play too well with what we've got now.  They could seriously use some better documentation, too.  Supybot is just awful and shall not be mentioned further.

I'm not sure what I can do about this, besides attempt to fill all these niches myself (ho ho, fat chance).  I'd actually be interested in getting some other developers together and starting a suite of tools to fill these gaps; if we can get a little critical mass and attract some outside attention, maybe we can shine some more light on Python.
