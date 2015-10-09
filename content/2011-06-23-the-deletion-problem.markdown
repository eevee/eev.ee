title: The deletion problem
date: 2011-06-23 18:15:00
modified: 2011-06-23 19:28:00
tags: squiggle, tech, making things
category: blog

[floof][] does not, as of yet, support deleting artwork.  It's not exactly a high priority for getting an art site off the ground; we need to facilitate _creating_ content before _removing_ it is even a thing to be done.

Recently, I keep returning to the question of whether deletion should even be supported at all.

I hear complaints about this all the time on FA: people move accounts, people "clean up" their old art (what?), people just up and decide to leave and [remove all traces of themselves][damnatio] in the process.  Suddenly, a lot of people have tons of gaps in their favorites, with no trace of what used to be there or why.

Now, obviously part of this is purely technical: it's easy enough to let favoriters know what's been removed, and those gaps [shouldn't really exist][database integrity] in the first place.

But then, my whole philosophy so far has been about _compromise_.  There are sites where producers have all the power, and sites where consumers have all the power, but not really anywhere that tries to appeal to both sides, and that's the niche I'm either inventing or filling.

Consider a wiki: when you write an article, you're _creating_ something.  The article is your prose, created by you, copyright to you.   Yet nobody leaving a wiki project would think to delete all the articles they'd written in the process; the very idea is absurd, because we hardly even acknowledge that the individual writing itself is an individual creation.  The project is _the wiki itself_, created by everybody and owned by nobody.

So can an art site do this?  Can the site itself function as that kind of singular project, with individual artwork acting as mere contributions to the whole?  I've always had the inkling that public art sites are for _sharing the art_, and features like disabling comments or restricting viewing ability run contrary to that goal; this is the same kind of idea taken to a further extreme.

I'm still not sold on this myself; I feel like there's some obvious use case I'm missing that would drive many artists away.  But most of the problems I think of aren't actually solved by deletion from a single art site, since most art ends up mirrored in untold dozens of archives and imageboards.  The only real difference is that the artist doesn't directly see that it's going on.

The biggest hurdle won't be with discouraging artists from deleting art they upload.  It'll be discouraging artists from uploading art they might want to delete in the first place.  If you don't well and truly want to share it, then you probably just shouldn't.  This is a tricky problem; if the site resembles deviantArt-style sites, it'll be easy to assume that it works the same way.  Big scary warnings are helpful, but "no deletion" sounds more like lazy development than a nod to the subtle philosophy I'm gradually figuring out here.

I don't know.  Are you interested?  Are you an artist?  Am I crazy?

**Addenda**: Some things that were mentioned to me:

1. Wikis tend to require that you (often passively) license your contribution under a free documentation license or similar.  I doubt that would be amenable to everyone, but at the very least we'd need something granting permission to display the work indefinitely.

2. One comment implied allowing an artist to remove art from his/her gallery without actually deleting it from the site.  This is actually kind of interesting, and hints at another problem I haven't much thought about: some artists let commissioners upload purchased work, but don't bother to upload the works themselves.  If "your gallery" is just all the art tagged as being created by you, how can we handle that?


[damnatio]: http://en.wikipedia.org/wiki/Damnatio_memoriae
[database integrity]: http://en.wikipedia.org/wiki/Database_integrity
[floof]: http://floof.us/
