title: Old CSS, new CSS
date: 2020-02-01 23:21
category: articles
tags: tech, web

I first got into web design/development in the late 90s, and only as I type this sentence do I realize how long ago that was.

And boy, it was horrendous.  I mean, being able to make stuff and put it online where other people could see it was pretty slick, but we did not have very much to work with.

I've been taking for granted that _most_ folks doing web stuff still remember those days, or at least the decade that followed, but I think that assumption might be a wee bit out of date.  Some time ago I encountered a [tweet](https://twitter.com/keinegurke_/status/1162309192855822339) marvelling at what we had to do without `border-radius`.  I still remember waiting with bated breath for it to be unprefixed!

But then, I suspect I also know a number of folks who only tried web design in the old days, and assume nothing about it has changed since.

I'm here to tell _all_ of you to get off my lawn.  Here's a history of CSS and web design, as I remember it.

<!-- more -->

----

(Please bear in mind that this post is a fine blend of memory and research, so I can't guarantee any of it is actually correct, _especially_ the bits about causality.  You may want to try the [W3C's history of CSS](https://www.w3.org/Style/CSS20/history.html), which is considerably shorter, has a better chance of matching reality, and contains significantly less swearing.)

(Also, this would benefit greatly from more diagrams, but it took long enough just to _write_.)

## The very early days

In the beginning, there was no CSS.

This was very bad.

My favorite artifact of this era is the book that taught me HTML: O'Reilly's [HTML: The Definitive Guide](https://isbnsearch.org/isbn/9781565924925), published in several editions in the mid to late 90s.  The book was indeed about _HTML_, with no mention of CSS at all.  I don't have it any more and can't readily find screenshots online, but here's a page from HTML & XHTML: The Definitive Guide, which seems to be a revision (I'll get to XHTML later) with much the same style.  Here, then, is the cutting-edge web design advice of 199X:

<div class="prose-full-illustration">
<img src="{static}/media/2020-02-css/html-definitive-guide.png" alt="Screenshot of a plain website in IE, with plain black text on a white background with a simple image">
</div>

"_Clearly delineate headers and footers with horizontal rules._"

No, that's not a `border-top`.  That's an `<hr>`.  The page title is almost certainly centered with, well, `<center>`.

The page uses the default text color, background, and font.  Partly because this is a guidebook introducing concepts one at a time; partly because the book was printed in black and white; and partly, I'm sure, because it reflected the reality that coloring anything was a huge pain in the ass.

Let's say you wanted all your `<h1>`s to be red, across your entire site.  You had to do this:

```html
<H1><FONT COLOR=red>...</FONT></H1>
```

..._every single goddamn time_.  Hope you never decide to switch to blue!

Oh, and everyone wrote HTML tags in all caps.  I don't remember why we all thought that was a good idea.  Maybe this was before syntax highlighting in text editors was very common (read: I was 12 and using Notepad), and uppercase tags were easier to distinguish from body text.

Keeping your site consistent was thus something of a nightmare.  One solution was to simply not style anything, which a lot of folks did.  This was nice, in some ways, since browsers let you change those defaults, so you could read the Web how you wanted.

A clever alternate solution, which I remember showing up in a lot of Geocities sites, was to simply give every page a completely different visual style.  Fuck it, right?  Just do whatever you want on each new page.

That trend was quite possibly the height of web design.

Damn, I miss those days.  There were no big walled gardens, no Twitter or Facebook.  If you had anything to say to anyone, you had to put together your own website.  It was _amazing_.  No one knew what they were doing; I'd wager that the vast majority of web designers at the time were clueless hobbyist tweens (like me) all copying from other clueless hobbyist tweens.  Half the Web was fan portals about Animorphs, with inexplicable splash pages warning you that their site worked best if you had a 640×480 screen.  (Any 12-year-old with insufficient resolution should, presumably, buy a new monitor with their allowance.)  Everyone who was cool and in the know used Internet Explorer 3, the most advanced browser, but some losers still used Netscape Navigator so you had to put a "Best in IE" animated GIF on your splash page too.

This was also the era of "web-safe colors" — a palette of 216 colors, where every channel was one of `00`, `33`, `66`, `99`, `cc`, or `ff` — which existed because some people still had 256-color monitors!  The things we take for granted now, like 24-bit color.

In fact, a _lot_ of stuff we take for granted now was still a strange and untamed problem space.  You want to have the same navigation on every page on your website?  Okay, no problem: copy/paste it onto each page.  When you update it, be sure to update every page — but most likely you'll forget some, and your whole site will become an archaeological dig into itself, with strata of increasingly bitrotted pages.

Much easier was to use _frames_, meaning the browser window is split into a grid and a different page loads in each section...  but then people would get confused if they landed on an individual page without the frames, as was common when coming from a search engine like AltaVista.  (I can't believe I'm explaining frames, but no one has used them since like 2001.  You know iframes?  The "i" is for _inline_, to distinguish them from _regular_ frames, which take up the entire viewport.)

PHP wasn't even called that yet, and nobody had heard of it.  This weird "Perl" and "CGI" thing was really strange and hard to understand, and it didn't work on your own computer, and the errors were hard to find and diagnose, and anyway Geocities didn't support it.  If you were _really_ lucky and smart, your web host used Apache, and you could use its "server side include" syntax to do something like this:

```html
<BODY>
    <TABLE WIDTH=100% BORDER=0 CELLSPACING=8 CELLPADDING=0>
        <TR>
            <TD COLSPAN=2>
                <!--#include virtual="/header.html" --> 
            </TD>
        </TR>
        <TR>
            <TD WIDTH=20%>
                <!--#include virtual="/navigation.html" --> 
            </TD>
            <TD>
                (actual page content goes here)
            </TD>
        </TR>
    </TABLE>
</BODY>
```

_Mwah._  Beautiful.  Apache would see the special comments, paste in the contents of the referenced files, and you're off to the races.  The downside was that when you wanted to work on your site, all the navigation was missing, because you were doing it on your regular computer without Apache, and your web browser thought those were just regular HTML comments.  It was impossible to install Apache, of course, because you had a _computer_, not a _server_.

Sadly, that's all gone now — paved over by homogenous timelines where anything that wasn't made this week is old news and long forgotten.  The web was supposed to make information eternal, but instead, so much of it became ephemeral.  I miss when virtually everyone I knew had their own website.  Having a Twitter and an Instagram as your entire online presence is a poor substitute.

...

So, let's look at the Space Jam website.


## Case study: Space Jam

Space Jam, if you're not aware, is the greatest movie of all time.  It documents Bugs Bunny's extremely short-lived basketball career, playing alongside a live action Michael Jordan to save the planet from aliens for some reason.  It was followed by a series of very successful and critically acclaimed [RPG spinoffs](https://www.talesofgames.com/related_game/barkley-shut-up-jam-gaiden/), which describe the fallout of the Space Jam and are extremely canon.

And we are truly blessed, for 24 years after it came out, its website is [STILL UP](https://www.spacejam.com/1996/).  We can explore the pinnacle of 1996 web design, right here, right now.

First, notice that every page of this site is a static page.  Not only that, but it's a static page ending in `.htm` rather than `.html`, because people on Windows versions before 95 were still beholden to 8.3 filenames.  Not sure why that mattered in a URL, as if you were going to run Windows 3.11 on a Web server, but there you go.

The CSS for the splash page looks like this:

```html
<body bgcolor="#000000" background="img/bg_stars.gif" text="#ff0000" link="#ff4c4c" vlink="#ff4c4c" alink="#ff4c4c">
```

Haha, just kidding!  What the fuck is CSS?  Space Jam predates it by a month.  (I do see a single line in the page source, but I'm pretty sure that was added much later to style some legally obligatory policy links.)

Notice the extremely precise positioning of these navigation links.  This feat was accomplished the same way everyone did everything in 1996: with tables.

In fact, tables have one functional advantage over CSS for layout, which was very important in those days, and not only because CSS didn't exist yet.  You see, you can ctrl-click to select a table _cell_ and even drag around to select all of them, which shows you how the cells are arranged and functions as a super retro layout debugger.  This was great because the first meaningful web debug tool, [Firebug](https://en.wikipedia.org/wiki/Firebug_%28software%29), wasn't released until 2006 — a whole decade later!

<div class="prose-full-illustration">
<img src="{static}/media/2020-02-css/space-jam-landing-table-cells.png" alt="Screenshot of the Space Jam website with the navigation table's cells selected, showing how the layout works">
</div>

The markup for this table is overflowing with inexplicable blank lines, but with those removed, it looks like this:

```html
<table width=500 border=0>
<TR>
<TD colspan=5 align=right valign=top>
</td></tr>
<tr>
<td colspan=2 align=right valign=middle>
<br>
<br>
<br>
<a href="cmp/pressbox/pressboxframes.html"><img src="img/p-pressbox.gif" height=56 width=131 alt="Press Box Shuttle" border=0></a>
</td>
<td align=center valign=middle>
<a href="cmp/jamcentral/jamcentralframes.html"><img src="img/p-jamcentral.gif" height=67 width=55 alt="Jam Central" border=0></a>
</td>
<td align=center valign=top>
<a href="cmp/bball/bballframes.html"><img src="img/p-bball.gif" height=62 width=62 alt="Planet B-Ball" border=0></a>
</td>
<td align=center valign=bottom>
<br>
<br>
<a href="cmp/tunes/tunesframes.html"><img src="img/p-lunartunes.gif" height=77 width=95 alt="Lunar Tunes" border=0></a>
</td>
</tr>
<tr>
<td align=middle valign=top>
<br>
<br>
<a href="cmp/lineup/lineupframes.html"><img src="img/p-lineup.gif" height=52 width=63 alt="The Lineup" border=0></a>
</td>
<td colspan=3 rowspan=2 align=right valign=middle>
<img src="img/p-jamlogo.gif" height=165 width=272 alt="Space Jam" border=0>
</td>
<td align=right valign=bottom>
<a href="cmp/jump/jumpframes.html"><img src="img/p-jump.gif" height=52 width=58 alt="Jump Station" border=0></a>
</td>
</tr>
...
</table>
```

That's the first two rows, including the logo.  You get the idea.  Everything is laid out with `align` and `valign` on table cells; `rowspan`s and `colspan`s are used frequently; and there are some `<br>`s thrown in for good measure, to adjust vertical positioning by one line-height at a time.

Other fantastic artifacts to be found on this page include this header, which contains Apache SSI syntax!  This must've quietly broken when the site was moved over the years; it's currently hosted on Amazon S3.  You know, Amazon?  The bookstore?

```html
<table border=0 cellpadding=0 cellspacing=0 width=488 height=60>
<tr>
<td align="center"><!--#include virtual="html.ng/site=spacejam&type=movie&home=no&size=234&page.allowcompete=no"--></td>
<td align="center" width="20"></td>
<td align="center"><!--#include virtual="html.ng/site=spacejam&type=movie&home=no&size=234"--></td>
</tr>
</table>
```

Okay, let's check out [jam central](https://www.spacejam.com/1996/cmp/jamcentral/jamcentralframes.html).  I've used my browser dev tools to reduce the viewport to 640×480 for the authentic experience (although I'd also have lost some vertical space to the title bar, taskbar, and five or six IE toolbars).

Note the frames: the logo in the top left leads back to the landing page, cleverly saving screen space on repeating all that navigation, and the top right is a fucking ad banner which has been blocked like seven different ways.  All three parts are separate pages.

<div class="prose-full-illustration">
<img src="{static}/media/2020-02-css/space-jam-central.png" alt="Screenshot of the Space Jam website's 'Jam Central'">
</div>

Note also the utterly unreadable red text on a textured background, one of the truest hallmarks of 90s web design.  "Why not put that block of text on an easier-to-read background?" you might ask.  You imbecile.  How would I _possibly_ do that?  Only the `<body>` has a `background` attribute!  I could use a table, but tables only support solid background colors, and that would look so boring!

But wait, what is this new navigation widget?  How are the links all misaligned like that?  Is this yet another table?  Well, no, although filling a table with chunks of a sliced-up image wasn't uncommon.  But this is an _imagemap_, a long-forgotten HTML feature.  I'll just show you the source:

```html
<img src="img/m-central.jpg" height=301 width=438 border=0 alt="navigation map" usemap="#map"><br>

<map name="map">
<area shape="rect" coords="33,92,178,136" href="prodnotesframes.html" target="_top">
<area shape="rect" coords="244,111,416,152" href="photosframes.html" target="_top">
<area shape="rect" coords="104,138,229,181" href="filmmakersframes.html" target="_top">
<area shape="rect" coords="230,155,334,197" href="trailerframes.html" target="_top">
</map>
```

I assume this is more or less self-explanatory.  The `usemap` attribute attaches an image map, which is defined as a bunch of clickable areas, beautifully encoded as inscrutable lists of coordinates or something.

And this stuff still works!  This is in HTML!  You could use it right now!  Probably don't though!

### The thumbnail grid

Let's look at one more random page here.  I'd love to see some photos from the film.  (Wait, _photos_?  Did we not know what "screenshots" were yet?)

<div class="prose-full-illustration">
<img src="{static}/media/2020-02-css/space-jam-photos.png" alt="Screenshot of the Space Jam website's photos page">
</div>

Another frameset, but arranged differently this time.

```html
<body bgcolor="#7714bf" background="img/bg-jamcentral.gif" text="#ffffff" link="#edb2fc" vlink="#edb2fc" alink="#edb2fc">
```

They did an important thing here: since they specified a background image (which is opaque), they _also_ specified a background color.  Without it, if the background image failed to load, the page would be white text on the default white background, which would be unreadable.

(That's _still_ an important thing to keep in mind.  I feel like modern web development tends to assume everything will load, or sees loading as some sort of inconvenience to be worked around, but not everyone is working on a wired connection in a San Francisco office twenty feet away from a backbone.)

But about the page itself.  Thumbnail grids are a classic problem of web design, dating all the way back to...  er...  well, at least as far back as Space Jam.  The main issue is that you want to _put things next to each other_, whereas HTML defaults to stacking everything in one big column.  You could put all the thumbnails inline, in a single row of (wrapping) text, but that wouldn't be much of a grid — and you usually want each one to have some sort of caption.

Space Jam's approach was to use the only real tool anyone had in their toolbox at the time: a table.  It's structured like this:

```html
<table cellpadding=10>
<tr><td align=center><a href="..."><img src="..."></a></td>...</tr>
<tr>...</tr>
<tr>...</tr>
<table>
```

A 3×3 grid of thumbnails, left to the browser to arrange.  (The last image, on a row of its own, isn't actually part of the table.)  This can't scale to fit your screen, but everyone's screen was pretty tiny back then, so that was _slightly_ less of a concern.  They didn't add captions here, but since every thumbnail is wrapped in a table cell, they easily could have.

This was the state of the art in thumbnail grids in 1996.  We'll be revisiting this little UI puzzle a few times; you can see live examples (and view source for sample markup) on a [separate page]({static}/media/2020-02-css/thumbnail-grids.html#tables).

But let's take a moment to appreciate the size of the "full-size, full-color, internet-quality" movie screenshots on my current monitor.

<div class="prose-full-illustration">
<img src="{static}/media/2020-02-css/space-jam-photo-size.png" alt="Screenshot of one of the Space Jam website's full-size photos, fullscreened on my monitor">
</div>

Hey, though, they're less than 16 KB!  That'll only take nine seconds to download.

(I'm reminded of the problem of embedded _video_, which wasn't solved until HTML5's `<video>` tag some years later.  Until then, you had to use a binary plugin, and all of them were terrible.)

(Oh, by the way: images within links, by default, have a link-colored border around them.  Image links are _usually_ self-evident, so this was largely annoying, and until CSS you had to disable them for every single image with `<img border=0>`.)


## The regular early days

So that's where we started, and it sucked.  If you wanted _any_ kind of consistency on more than a handful of pages, your options were very limited, and they were pretty much limited to a whole lot of copying and pasting.  The Space Jam website opted to, for the most part, not bother at all — as did many others.

Then CSS came along, it was a _fucking miracle_.  All that inline repetition went away.  You want all your top-level headings to be a particular color?  No problem:

```css
H1 {
    color: #FF0000;
}
```

Bam!  You're done.  No matter how many `<h1>`s you have in your document, every single one of them will be eye-searing red, and you never have to think about it again.  Even better, you can put that snippet in its own file and have that questionable aesthetic choice applied to _every page of your whole site_ with almost no effort!  The same applied to your gorgeous tiling background image, the colors of your links, and the size of the font in your tables.

(Just remember to wrap the contents of your `<style>` tags in HTML comments, or old browsers without CSS support will display them as text.)

You weren't limited to styling tags en masse, either.  CSS introduced "classes" and "IDs" to target only specifically flagged elements.  A _selector_ like `P.important` would only affect `<P CLASS="important">`, and `#header` would only affect `<H1 ID="header">`.  (The difference is that IDs are intended to be unique in a document, whereas classes can be used any number of times.)  With these tools, you could effectively invent your own tags, giving you a customized version of HTML specific to your website!

This was a huge leap forward, but at the time, no one (probably?) was thinking of using CSS to actually _arrange_ the page.  When [CSS 1](https://www.w3.org/TR/2008/REC-CSS1-20080411/) was made a recommendation in December '96, it barely addressed layout at all.  All it did was divorce HTML's _existing_ abilities from the tags they were attached to.  We had font colors and backgrounds _because_ `<FONT COLOR>` and `<BODY BACKGROUND>` existed.  The only feature that even remotely affected where things were positioned was the `float` property, the equivalent to `<IMG ALIGN>`, which pulled an image to the side and let text flow around it, like in a magazine article.  Hardly whelming.

This wasn't too surprising.  HTML hadn't had any real answers for layout besides tables, and the table properties were too complicated to generalize in CSS and too entangled with the tag structure, so there was nothing for CSS 1 to inherit.  It merely reduced the repetition in what we were already doing with e.g. `<FONT>` tags — making Web design less tedious, less error-prone, less full of noise, and much more maintainable.  A pretty good step forward, and everyone happily adopted it for that, but tables remained king for arranging your page.

That was okay, though; all your blog really needed was a header and a sidebar, which tables could do just fine, and it wasn't like you were going to overhaul that basic structure very often.  Copy/pasting a few lines of `<TABLE BORDER=0>` and `<TD WIDTH=20%>` wasn't nearly as big a deal.

For some span of time — I want to say a couple years, but time passes more slowly when you're a kid — this was the state of the Web.  Tables for layout, CSS for...  well, _style_.  Colors, sizes, bold, underline.  There was even this sick trick you could do with links where they'd _only_ be underlined when the mouse was _pointing_ at them.  Tubular!

(Fun fact: HTML _email_ is still basically trapped in this era.)

(And here's about where I come in, at the ripe old age of 11, with no clue what I was doing and mostly learning from other 11-year-olds who also had no clue what they were doing.  But that was fine; a huge chunk of the Web was 11-year-olds making their own websites, and it was beautiful.  Why would you go to a _business_ website when you can take a peek into the very specific hobbies of someone on the other side of the planet?)


## The dark times

A year and a half later, in mid '98, we were gifted [CSS 2](https://www.w3.org/TR/2008/REC-CSS2-20080411/).  (I _love_ the background on this page, by the way.)  This was a modest upgrade that addressed a few deficiencies in various areas, but most interesting was the addition of a couple positioning primitives: the `position` property, which let you place elements at precise coordinates, and the `inline-block` display mode, which let you stick an element in a line of text like you could do with images.

Such tantalizing fruit, just out of reach!  Using `position` seemed nice, but pixel-perfect positioning was at serious odds with the fluid design of HTML, and it was difficult to make much of anything that didn't fall apart on other screen sizes or have other serious drawbacks.  This humble `inline-block` thing _seemed_ interesting enough; after all, it solved the core problem of HTML layout, which is _putting things next to each other_.  But at least for the moment, no browser implemented it, and it was largely ignored.

I can't say for sure if it was the introduction of positioning or some other factor, but _something_ around this time inspired folks to try doing layout in CSS.  Ideally, you would _completely_ divorce the structure of your page from its appearance.  A website even came along to take this principle to the extreme — [CSS Zen Garden](http://www.csszengarden.com/) is still around, and showcases the _same HTML_ being radically transformed into completely different designs by applying different stylesheets.

Trouble was, early CSS support was buggy as hell.  In retrospect, I suspect browser vendors merely plucked the behavior off of HTML tags and called it a day.  I'm delighted to say that RichInStyle still has [an extensive list of early browser CSS bugs](http://www.richinstyle.com/bugs/) up; here are some of my favorites:

- IE 3 would ignore all but the last `<style>` tag in a document.

- IE 3 ignored pseudo-classes, so `a:hover` would be treated as `a`.

- IE 3 and IE 4 treated `auto` margins as zero.  Actually, I think this one might've persisted all the way to IE 6.  But that was okay, because IE 6 also incorrectly applied `text-align: center` to block elements.

- If you set a background image to an absolute URL, IE 3 would try to open the image in a local program, as though you'd downloaded it.

- Netscape 4 understood an ID selector like `#id`, but ignored `h1#id` as invalid.

- Netscape 4 didn't inherit properties — including font and text color! — into table cells.

- Netscape 4 applied properties on `<li>` to the list _marker_, rather than the contents.

- If the same element has both `float` and `clear` (not unreasonable), Netscape 4 for Mac crashes.

This is what we had to work with.  And folks wanted to use CSS to _lay out_ an _entire page_?  Ha.

Yet the idea grew in popularity.  It even became a sort of elitist rallying cry, a best practice used to beat other folks over the head.  Tables for layout are just plain bad, you'd hear!  They confuse screenreaders, they're semantically incorrect, they interact poorly with CSS positioning!  All of which is true, but it was a much tougher pill to swallow when the alternative was—

Well, we'll get to that in a moment.  First, some background on the Web landscape circa 2000.

### The end of the browser wars and subsequent stagnation

The short version is: this company Netscape had been selling its Navigator browser (to businesses; it was free for personal use), and then Microsoft entered the market with its completely free Internet Explorer browser, and _then_ Microsoft had the audacity to bundle IE with Windows.  Can you imagine?  An operating system that _comes with_ a browser?  This was a whole big thing, [Microsoft was sued over it](https://en.wikipedia.org/wiki/United_States_v._Microsoft_Corp.), and they lost, and the consequence was basically nothing.

But it wouldn't have mattered either way, because they'd still _done it_, and it had worked.  IE pretty much annihilated Netscape's market share.  Both browsers were buggy as hell, and _differently_ buggy as hell, so a site built exclusively against one was likely to be a big mess when viewed in the other — this meant that when Netscape's market share dropped, web designers paid less and less attention to it, and less of the Web worked in it, and its market share dropped further.

Sucks for you if you don't use Windows, I guess.  Which is funny, because there was an IE for Mac 5.5, and it was generally _less_ buggy than IE 6.  (Incidentally, Bill Gates wasn't so much a brilliant nerd as an aggressive and ruthless businessman who made his fortune by deliberately striving to annihilate any competition standing in his way and making computing worse overall as a result, just saying.)

By the time Windows XP shipped in mid 2001, with Internet Explorer 6 built in, Netscape had gone from a juggernaut to a tiny niche player.

And then, having completely and utterly dominated, Microsoft stopped.  Internet Explorer had seen a release every year or so since its inception, but IE 6 was the last release for more than five years.  It was still buggy, but that was less noticeable when there was no competition, and it was _good enough_.  Windows XP, likewise, was good enough to take over the desktop, and there wouldn't be another Windows for just as long.

The W3C, the group who write the standards (not to be confused with W3Schools, who are shady SEO leeches), also stopped.  HTML had seen several revisions throughout the mid 90s, and then froze as HTML 4.  CSS had gotten an update in only a year and a half, and then no more; the minor update [CSS 2.1](https://www.w3.org/TR/CSS21/) wouldn't hit Candidate Recommendation status until early 2004, and took another seven years to be finalized.

With IE 6's dominance, it was as if the entire Web was frozen in time.  Standards didn't matter, because there was effectively only one browser, and whatever it did became the de facto standard.  As the Web grew in popularity, IE's stranglehold also made it difficult to use any platform other than Windows, since IE was Windows-only and it was a coin flip whether a website would actually work with any other browser.

(One begins to suspect that monopolies are bad.  There oughta be a law!)

In the meantime, Netscape had put themselves in an even worse position by deciding to do a massive rewrite of their browser engine, culminating in the vastly more standards-compliant Netscape 6 — at the cost of several years away from the market while IE was kicking their ass.  It never broke 10% market share, while IE's would peak at 96%.  On the other hand, the new engine was open sourced as the Mozilla Application Suite, which would be important in a few years.

Before we get to that, some other things were also happening.

### Quirks mode

All early CSS implementations were riddled with bugs, but one in particular is perhaps the most infamous CSS bug of all time: the _box model bug_.

You see, a box (the rectangular space taken up by an element) has several measurements: its own width and height, then surrounding whitespace called padding, then an optional border, then a margin separating it from neighboring boxes.  CSS specifies that these properties are all additive.  A box with these styles:

```css
    width: 100px;
    padding: 10px;
    border: 2px solid black;
```

...would thus be 124 pixels wide, from border to border.

IE 4 and Netscape 4, on the other hand, took a different approach: they treated `width` and `height` as measuring from border to border, and they _subtracted_ the border and padding to get the width of the element itself.  The same box in those browsers would be 100 pixels wide from border to border, with 76 pixels remaining for the content.

This conflict with the spec was not ideal, and IE 6 set out to fix it.  Unfortunately, simply making the change would mean completely breaking the design of a whole lot of websites that had previously worked in _both_ IE and Netscape.

So the IE team came up with a very strange compromise: they declared the old behavior (along with several other major bugs) as "quirks mode" and made it the _default_.  The new "strict mode" or "standards mode" had to be opted _into_, by placing a "doctype" at the beginning of your document, before the `<html>` tag.  It would look something like this:

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
```

Everyone had to paste this damn mess of a line at the top of every single HTML document for years.  (HTML5 would later simplify it to `<!DOCTYPE html>`.)  In retrospect, it's a really strange way to opt into correct CSS behavior; doctypes had been part of the HTML spec since way back when it was an [RFC](https://tools.ietf.org/html/rfc1866).  I'm guessing the idea was that, since _nobody_ bothered actually including one, it was a convenient way to allow opting in without requiring proprietary extensions just to avoid behavior that had been wrong in the first place.  Good for the IE team!

The funny thing is, quirks mode still exists _and is still the default_ in all browsers, twenty years later!  The exact quirks have varied over time, and in particular neither Chrome nor Firefox use the IE box model even in quirks mode, but there are still [quite a few other emulated bugs](https://developer.mozilla.org/en-US/docs/Mozilla/Mozilla_quirks_mode_behavior).

<aside class="aside--note-from-future" markdown="1">
Hello!  Eevee here, almost two years later.  You may notice the preceding link is broken.  Well, it seems Mozilla made the completely baffling decision to [nuke all Mozilla-specific information from MDN](https://groups.google.com/a/mozilla.org/g/dev-platform/c/HwRoRUOuyEw/m/ZfYG7oHZDQAJ?pli=1) on the grounds that it really belongs in Firefox documentation, then failed to add it to the Firefox documentation.  So some critical technical information that's also of deep historical interest, like exactly what quirks mode even _does_ in Firefox, is now lost, except for the unreadable [archived copy](https://github.com/mdn/archived-content/blob/main/files/en-us/mozilla/mozilla_quirks_mode_behavior/index.html).  This also reduces the only mention of quirks mode on MDN to [this lone article](https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode), which says very vaguely what it is but doesn't offer so much as a glimpse at what the differences actually are.  What a fucking circus.
</aside>

Modern browsers also have "almost standards" mode, which emulates only a single quirk, perhaps the second most infamous one: if a table cell contains only a single image, the space under the baseline is removed.  Under normal CSS rules, the image is sitting within a line of (otherwise empty) text, which requires some space reserved underneath for descenders — the tails on letters like y.  Early browsers didn't handle this correctly, and some otherwise strict-mode websites from circa 2000 rely on it — e.g., by cutting up a large image and arranging the chunks in table cells, expecting them to display flush against each other — hence the intermediate mode to keep them limping along.

But getting back to the past: while this was certainly a win for standards (and thus interop), it created a new problem.  Since IE 6 dominated, and doctypes were optional, there was little compelling reason to bother with strict mode.  Other browsers ended up _emulating_ it, and the non-standard behavior became its own de facto standard.  Web designers who cared about this sort of thing (and to our credit, there were a lot of us) made a rallying cry out of enabling strict mode, since it was the absolute barest minimum step towards ensuring compatibility with other browsers.

### The rise and fall of XHTML

Meanwhile, the W3C had lost interest in HTML in favor of developing XHTML, an attempt to redesign HTML with the syntax of XML rather than SGML.

(What on Earth is SGML, you ask?  I don't know.  Nobody knows.  It's the grammar HTML was built on, and that's the only reason anyone has heard of it.)

To their credit, there were some good reasons to do this at the time.  HTML was generally hand-written (as it still is now), and anything hand-written is likely to have the occasional bugs.  Browsers weren't in the habit of rejecting buggy HTML outright, so they had various error-correction techniques — and, as with everything else, different browsers handled errors differently.  Slightly malformed HTML might appear to work fine in IE 6 (where "work fine" means "does what you hoped for"), but turn into a horrible mess in anything else.

The W3C's solution was XML, because their solution to fucking everything in the early 2000s was XML.  If you're not aware, XML takes a much more explicit and aggressive approach to error handling — if your document contains a parse error, the _entire document_ is invalid.  That means if you bank on XHTML and make a single typo somewhere, **nothing at all** renders.  Just an error.

This sucked.  It sounds okay on the face of things, but consider: generic XML is usually assembled dynamically with _libraries_ that treat a document as a tree you manipulate, then turn it all into text when you're done.  That's great for the common use of XML as data serialization, where your data is already a tree and much of the XML structure is simple and repetitive and easy to squirrel away in functions.

HTML is not like that.  An HTML document has little reliable repeating structure; even this blog post, constructed _mostly_ from `<p>` tags, also contains surprise `<em>`s within body text and the occasional `<h2>` between paragraphs.  That's not fun to express as a tree.  And this is a big deal, because server-side rendering was becoming popular around the same time, and generated HTML was — still is! — put together with _templates_ that treat it as a text stream.

If HTML were only written as complete static documents, then XHTML might have worked out — you write a document, you see it in your browser, you know it works, no problem.  But generating it dynamically and risking that _particular edge cases_ might replace your entire site with an unintelligible browser error?  That sucks.

It certainly didn't help that we were just starting to hear about this newfangled Unicode thing around this time, and it was still not always clear how exactly to make that work, and one bad UTF-8 sequence is enough for an entire XML document to be considered malformed!

And so, after some dabbling, XHTML was largely forgotten.  Its legacy lives on in two ways:

- It got us all to stop using uppercase tag names!  So long `<BODY>`, hello `<body>`.  XML is case-sensitive, you see, and all the XHTML tags were defined in lowercase, so uppercase tags simply would not work.  (Fun fact: to this day, JavaScript APIs report HTML tag names in uppercase.)  The increased popularity of syntax highlighting probably also had something to do with this; we weren't all still using Notepad as we had been in 1997.

- A bunch of folks _still_ think self-closing tags are necessary.  You see, HTML has two kinds of tags: containers like `<p>...</p>` and markers like `<br>`.  Since a `<br>` can't possibly contain anything, there's no such thing as `</br>`.  XML, as a generic grammar, doesn't have this distinction; every tag _must_ be closed, but as a shortcut, you can write `<br/>` to mean `<br></br>`.

    XHTML has been dead for years, but for some reason, I still see folks write `<br/>` in regular HTML documents.  Outside of XML, that slash doesn't do anything; HTML5 has defined it for compatibility reasons, but it's silently ignored.  It's even actively harmful, since it might lead you to believe that `<script/>` is an empty `<script>` tag — but in HTML, it definitely is not!

I do miss one thing about XHTML.  You could combine it with XSLT, the XML templating meta-language, to do in-browser templating (i.e., slot page-specific contents into your overall site layout) with no scripting required.  It's the _only_ way that's ever been possible, and it was cool as all hell when it worked, but the drawbacks were too severe when it didn't.  Also, XSLT is totally fucking incomprehensible.

### The beginning of CSS layout

Back to CSS!

You're an aspiring web designer.  For whatever reason, you want to try using this CSS thing to lay out your whole page, even though it was _clearly_ intended just for colors and stuff.  What do you do?

As I mentioned before, your core problem is _putting things next to each other_.  Putting things on _top_ of each other is a non-problem — that's the normal behavior of HTML.  The whole reason everyone uses tables is that you can slop stuff into table cells and have it laid out side-by-side, in columns.

Well, tables seem to be out.  CSS 2 had added some element display modes that corresponded to the parts of a table, but to use them, you'd have to have the same three levels of nesting as real tables: the table itself, then a row, then a cell.  That doesn't seem like a huge step up, and anyway, IE won't support them until the distant future.

There's that `position` thing, but it seems to make things _overlap_ more often than not.  Hmm.

What does that leave?

Only one tool, really: `float`.

I said that `float` was intended for magazine-style "pull" images, which is true, but CSS had defined it fairly generically.  In _principle_, it could be applied to any element.  If you wanted a sidebar, you could tell it to float to the left and be 20% the width of the page, and you'd get something like this:

```text
+---------+
| sidebar | Hello, and welcome to my website!
|         |
+---------+
```

Alas!  Floating has the secondary behavior that text wraps around it.  If your page text was ever longer than your sidebar, it would wrap around _underneath_ the sidebar, and the illusion would shatter.  But hey, no problem.  CSS specified that floats don't wrap around each other, so all you needed to do was float the body as well!


```text
+---------+ +-----------------------------------+
| sidebar | | Hello, and welcome to my website! |
|         | |                                   |
+---------+ | Here's a longer paragraph to show |
            | that my galaxy brain CSS float    |
            | nonsense prevents text wrap.      |
            +-----------------------------------+
```

This approach worked, but its limitations were much more obvious than those of tables.  If you added a footer, for example, then it would try to fit to the _right_ of the body text — remember, all of that is "pull" floats, so as far as the browser is concerned, the "cursor" is still at the top.  So now you need to use `clear`, which bumps an element down below all floats, to fix that.  And if you made the sidebar 20% wide and the body 80% wide, then any margin between them would add to that 100%, making the page wider than the viewport, so now you have an ugly horizontal scrollbar, so you have to do some goofy math to fix that as well.  If you have borders or backgrounds on either part, then it was a little conspicuous that they were different heights, so now you have to do some _truly_ grotesque stuff to fix _that_.  And the more conscientious authors noticed that screenreaders would read the entire sidebar before getting to the body text, which is a pretty rude thing to subject blind visitors to, so they came up with yet _more_ elaborate setups to have a three-column layout with the middle column appearing first in the HTML.

The result was a design that looked nice and worked well and scaled correctly, but backed by a weird mess of CSS.  None of what you were _writing_ actually corresponded to what you _wanted_ — these are major parts of your design, not one-off pull quotes!  It was difficult to understand the relationship between the layout-related CSS and what appeared on the screen, and that would get much worse before it got better.

### Thumbnail grid 2

Armed with a new toy, we can improve that thumbnail grid.  The original table-based layout was, even if you don't care about tag semantics, incredibly tedious.  Now we can do better!

```html
<ul class="thumbnail-grid">
    <li><img src="..."><br>caption</li>
    <li><img src="..."><br>caption</li>
    <li><img src="..."><br>caption</li>
    ...
</ul>
```

This is the dream of CSS: your HTML contains the page data in some sensible form, and then CSS describes how it actually looks.

Unfortunately, with `float` as the only tool available to us, the results are a bit rough.  This [new version]({static}/media/2020-02-css/thumbnail-grids.html#floats) does adapt better to various screen sizes, but it requires some hacks: the cells have to be a fixed height, centering the whole grid is fairly complicated, and the grid effect falls apart entirely with wider elements.  It's becoming clear that what we wanted is something more like a table, but with a flexible number of columns.  This is just faking it.

You also need this weird "clearfix" thing, an incantation that would become infamous during this era.  Remember that a float doesn't move the "cursor" — a fake idea I'm using, but close enough.  That means that this `<ul>`, which is full _only_ of floated elements, has no height at all.  It ends exactly where it begins, with all the floated thumbnails spilling out below it.  Worse, because any subsequent elements don't have any floated _siblings_, they'll ignore the thumbnails entirely and render normally from just below the empty "grid" — producing an overlapping mess!

The solution is to add a dummy element at the _end_ of the list which takes up no space, but has the CSS `clear: both` — bumping it down below all floats.  That effectively pushes the bottom of the `<ul>` under all the individual thumbnails, so it fits snugly around them.

Browsers would later support the `::before` and `::after` "generated content" pseudo-elements, which let us avoid the dummy element entirely.  Stylesheets from the mid-00s were often littered with stuff like this:

```css
.thumbnail-grid::after {
    content: '';
    display: block;
    clear: both;
}
```

Still, it was better than tables.

### DHTML

As a quick aside into the world of JavaScript, the newfangled `position` property _did_ give us the ability to do some layout things dynamically.  I heartily oppose such heresy, not least because no one has ever actually done it right, but it was nice for some toys.

Thus began the era of "dynamic HTML" — i.e., HTML affected by JavaScript, a term that has fallen entirely out of favor because we can't even make a fucking static blog without JavaScript any more.  In the early days it was much more innocuous, with teenagers putting sparkles that trailed behind your mouse cursor or little analog clocks that ticked by in real time.

The most popular source of these things was [Dynamic Drive](http://www.dynamicdrive.com/), a site that miraculously still exists and probably has a bunch of toys not updated since the early 00s.

But if you don't like digging, here's an example: every year (except this year when I forgot oops), I like to add confetti and other nonsense to my blog on my birthday.  I'm very lazy so I started this tradition by using [this script I found somewhere](http://www.schillmania.com/projects/snowstormv12_20041121a/script/snowstorm.js), originally intended for snowflakes.  It works by placing a bunch of images on the page, giving them `position: absolute`, and meticulously altering their coordinates over and over.

Contrast this with [the version I wrote from scratch a couple years ago](https://c.eev.ee/PARTYMODE/), which has only a [tiny bit of JS](https://c.eev.ee/PARTYMODE/partymode.js) to set up the images, then lets the browser animate them with CSS.  It's slightly less featureful, but lets the browser do all the work, possibly even with hardware acceleration.  How far we've come.


## Web 2.0

Dark times can't last forever.  A combination of factors dragged us towards the light.

One of the biggest was [Firefox](https://www.mozilla.org/en-US/firefox/) — or, if you were cool, originally Phoenix and then Firebird — which hit 1.0 in Nov '04 and went on to take a serious bite out of IE.  That rewritten Netscape 6 browser core, the heart of the Mozilla Suite, had been extracted into a standalone browser.  It was quick, it was simple, it was much more standard-compliant, and absolutely none of that mattered.

No, Firefox really got a foothold because it had _tabs_.  IE 6 did not have tabs; if you wanted to open a second webpage, you opened another window.  It fucking sucked, man.  Firefox was a miracle.

Firefox wasn't the first tabbed browser, of course; the full Mozilla Suite's browser had them, and the obscure (but scrappy!) Opera had had them for ages.  But it was Firefox that took off, for various reasons, not least of which was that it didn't have a giant fucking ad bar at the top like Opera did.

Designers did push for Firefox on standards grounds, of course; it's just that that angle primarily appealed to other designers, not so much to their parents.  One of the most popular and spectacular demonstrations was the [Acid2 test](https://en.wikipedia.org/wiki/Acid2), intended to test a variety of features of then-modern Web standards.  It had the advantage of producing a cute smiley face when rendered correctly, and a [fucking nightmare hellscape](https://en.wikipedia.org/wiki/File:Ieacid2.png) in IE 6.  Early Firefox wasn't perfect, but it was certainly much closer, and you could _see_ it make progress until it fully passed with the release of Firefox 3.

It also helped that Firefox had a faster JavaScript engine, even before JIT caught on.  Much, much faster.  Like, as I recall, IE 6 implemented `getElementById` by iterating over the entire document, even though IDs are unique.  Glance at some [old jQuery release announcements](https://blog.jquery.com/2011/01/31/jquery-15-released/); they usually have some performance charts, and everything else absolutely _dwarfs_ IE 6 through 8.

Oh, and there was that whole thing where IE 6 was a giant walking security hole, especially with its native support for arbitrary binary components that only needed a "yes" click on an arcane dialog to get full and unrestricted access to your system.  Probably didn't help its reputation.

Anyway, with something other than IE taking over serious market share, even the most ornery designers couldn't just target IE 6 and call it a day any more.  Now there was a _reason_ to use strict mode, a reason to care about compatibility and standards — which Firefox was making a constant effort to follow better, while IE 6 remained stagnant.

(I'd argue that this effect opened the door for OS X to make some inroads, and also for the iPhone to exist at all.  I'm not kidding!  Think about it; if the iPhone browser hadn't actually worked with anything because everyone was still targeting IE 6, it'd basically have been a more expensive Palm.  Remember, at first Apple didn't even want native apps; it bet on the Web.)

(Speaking of which, Safari was released in Jan '03, based on a fork of the KHTML engine used in KDE's Konqueror browser.  I think I was using KDE at the time, so this was very exciting, but no one else really cared about OS X and its 2% market share.)

Another major factor appeared on April Fools' Day, 2004, when Google announced Gmail.  Ha, ha!  A funny joke.  Webmail that isn't terrible?  That's a good one, Google.

Oh.  Oh, fuck.  Oh they're not kidding.  _How the fuck does this even work_

The answer, as every web dev now knows, is XMLHttpRequest — named for the fact that nobody has ever once used it to request XML.  Apparently it was invented by Microsoft for use with Exchange, then cloned early on by Mozilla, but I'm just reading this from [Wikipedia](https://en.wikipedia.org/wiki/XMLHttpRequest) and you can do that yourself.

The important thing is, it lets you make an HTTP request from JavaScript.  You could now update only _part_ a page with new data, completely in the background, without reloading.  _Nobody_ had heard of this thing before, so when Google dropped an entire email client based on it, it was like fucking magic.

Arguably the whole thing was a mistake and has led to a hell future where static pages load three paragraphs of text in the background using XHR for no goddamn reason, but that's a [different post]({filename}/2016-03-06-maybe-we-could-tone-down-the-javascript.markdown).

Along similar lines, August 2006 saw the release of [jQuery](https://jquery.com/), a similar miracle.  Not only did it paper over the differences between IE's "JScript" APIs and the standard approaches taken by everyone else (which had been done before by other libraries), but it made it very easy to work with whole _groups_ of elements at a time, something that had historically been a huge pain in the ass.  Now you could fairly easily apply CSS all over the place from JavaScript!  Which is a bad idea!  But everything was so bad that we did it anyway!

Hold on, I hear you cry.  These things are about JavaScript!  Isn't this a post about CSS?

You're absolutely right!  I mention the rise of JavaScript because I think it led directly to the modern state of CSS, thanks to an increase in one big factor:

### Ambition

Firefox showed us that we could have browsers that actually, like, _improve_ — every new improvement on Acid2 was exciting.  Gmail showed us that the Web could do more than show plain text with snowflakes in front.

And folks started itching to get _fancy_.

The problem was, browsers hadn't really gotten any better yet.  Firefox was faster in some respects, and it adhered more closely to the CSS spec, but it didn't fundamentally do anything that browsers weren't supposed to be able to do already.  Only the _tooling_ had improved, and that mostly affected JavaScript.  CSS was a static language, so you couldn't write a library to make it better.  Generating CSS with JavaScript was a possibility, but boy oh boy is that ever a bad idea.

Another problem was that CSS 2 was only really good at styling rectangles.  That was fine in the 90s, when every OS had the aesthetic of rectangles containing more rectangles.  But now we were in the days of Windows XP and OS X, where everything was shiny and glossy and made of curvy plastic.  It was a little embarrassing to have rounded corners and neatly shaded swooshes in your _file browser_ and nowhere on the Web.

Thus began a new reign of darkness.

### The era of CSS hacks

Designers wanted a lot of things that CSS just could not offer.

- Round corners were a big one.  Square corners had fallen out of vogue, and now everyone wanted buttons with round corners, since they were The Future.  (Native buttons also went out of vogue, for some reason.)  Alas, CSS had no way to do this.  Your options were:

    1. Make a fixed-size background image of a rounded rectangle and put it on a fixed-size button.  Maybe drop the text altogether  and just make the whole thing an image.  Eugh.

    2. Make a _generic_ background image and scale it to fit.  More clever, but the corners might end up not round.

    3. Make the rounded rectangle, cut out the corner and edges, and put them in a 3×3 table with the button label in the middle.  Even better, use JavaScript to do this on the fly.

    4. Fuck it, make your entire website one big Flash app lol

    Another problem was that IE 6 didn't understand PNGs with 8-bit alpha; it could only correctly display PNGs with 1-bit alpha, i.e. every pixel is either fully opaque or fully transparent, like GIFs.  You had to settle for jagged edges, bake a solid background color into the image, or apply various fixes that centered around this fucking garbage nonsense:

        :::css
        filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src='bite-my-ass.png');

- Along similar lines: gradients and drop shadows!  You can't have fancy plastic buttons without those.  But here you were basically stuck with making images again.

- Translucency was a bit of a mess.  Most browsers supported the CSS 3 `opacity` property since very early on...  except IE, which needed another wacky Microsoft-specific `filter` thing.  And if you wanted _only_ the background translucent, you'd need a translucent PNG, which...  well, you know.

- Since the beginning, jQuery shipped with built-in animated effects like `fadeIn`, and they started popping up all over the place.  It was kind of like the Web equivalent of how every Linux user in the mid-00s (and I include myself in this) used that fucking [Compiz cube effect](https://youtu.be/4QokOwvPxrE?t=118).

    Obviously you need JavaScript to trigger an element's disappearance in most interesting cases, but using it to control the actual animation was a bit heavy-handed and put a strain on browsers.  Tabbed browsing compounded this, since browsers were largely single-threaded, and for various reasons, every open page ran in the same thread.

- Oh!  Alternating background colors on table rows.  This has since gone out of style, but I think that's a shame, because _man_ did it make tables easier to read.  But CSS had no answer for this, so you had to either give every other row a class like `<tr class="odd">` (hope the table's generated with code!) or do some jQuery nonsense.

- CSS 2 introduced the `>` child selector, so you could write stuff like `ul.foo > li` to style special lists without messing up nested lists, and IE 6!  Didn't!  Fucking!  Support!  It!

All those are merely aesthetic concerns, though.  If you were interested in layout, well, the rise of Firefox had made your life at once much easier and much harder.

Remember `inline-block`?  Firefox 2 actually supported it!  It was buggy and hidden behind a vendor prefix, but it more or less worked, which let designers start playing with it.  And then Firefox 3 supported it more or less fully, which felt miraculous.  Version 3 of our [thumbnail grid]({static}/media/2020-02-css/thumbnail-grids.html#inline-block) is as simple as a width and `inline-block`:

```css
.thumbnails li {
    display: inline-block;
    width: 250px;
    margin: 0.5em;
    vertical-align: top;
}
```

The general idea of `inline-block` is that the _inside_ acts like a block, but the block itself is placed in regular flowing text, like an image.  Each thumbnail is thus contained in a box, but the boxes all lie next to each other, and because of their equal widths, they flow into a grid.  And since it's functionally a line of text, you don't have to work around any weird impact on the rest of the page like you had to do with floats.

Sure, this had some drawbacks.  You couldn't do anything with the leftover space, for example, so there was a risk of a big empty void on the right with pathological screen sizes.  You still had the problem of breaking the grid with a wide cell.  But at least it's not floats.

One teeny problem: IE 6.  It did _technically_ support `inline-block`, but only on elements that were naturally `inline` — ones like `<b>` and `<i>`, not `<li>`.  So, not ones you'd actually want (or think) to use `inline-block` on.  Sigh.

Lucky for us, at some point an absolute genius discovered `hasLayout`, an internal optimization in IE that marks whether an element...  uh...  has...  layout.  Look, I don't know.  Basically it changes the rendering path for an element — making it _differently_ buggy, like quirks mode on a per-element basis!  The upshot is that the above works in IE 6 if you add a couple lines:

```css
.thumbnails li {
    display: inline-block;
    width: 250px;
    margin: 0.5em;
    vertical-align: top;
    *zoom: 1;
    *display: inline;
}
```

The leading asterisks make the property invalid, so browsers should ignore the whole line...  but for some reason I cannot begin to fathom, IE 6 ignores the asterisks and accepts the rest of the rule.  (Almost any punctuation worked, including a hyphen or — my personal favorite — an underscore.)  The `zoom` property is a Microsoft extension that scales stuff, with the side effect that it grants the mystical property of "layout" to the element as well.  And `display: inline` _should_ make each element spill its contents into one big line of text, but IE treats an `inline` element that has "layout" roughly like an `inline-block`.

And here we saw the true potential of CSS messes.  Browser-specific rules, with deliberate bad syntax that one browser would ignore, to replicate an effect that _still_ isn't clearly described by what you're writing.  [Entire tutorials](https://blog.mozilla.org/webdev/2009/02/20/cross-browser-inline-block/) written to explain how to accomplish something simple, like a _grid_, but have it actually work on most people's browsers.  You'd also see `* html`, `html > /**/ body`, and all kinds of other nonsense.  [Here's a full list!](http://browserhacks.com/)  And remember that "clearfix" hack from before?  The [full version](https://css-tricks.com/snippets/css/clear-fix/), compatible with _every_ browser, is a bit worse:

```css
.clearfix:after {
  visibility: hidden;
  display: block;
  font-size: 0;
  content: " ";
  clear: both;
  height: 0;
}
.clearfix { display: inline-block; }
/* start commented backslash hack \*/
* html .clearfix { height: 1%; }
.clearfix { display: block; }
/* close commented backslash hack */
```

Is it any wonder folks started groaning about CSS?

This was an era of blind copy/pasting in the frustrated hopes of making the damn thing work.  Case in point: someone (I dug the original source up once but can't find it now) had the bone-headed idea of always setting `body { font-size: 62.5% }` due to a combination of "relative units are good" and wanting to override the seemingly massive default browser font size of 16px (which, it turns out, [is correct](https://www.smashingmagazine.com/2011/10/16-pixels-body-copy-anything-less-costly-mistake/)) and dealing with IE bugs.  He walked it back a short time later, but the damage had been done, and now _thousands_ of websites start off that way as a "best practice".  Which means if you want to change your browser's default font size in either direction, you're screwed — scale it down and a bunch of the Web becomes microscopic, scale it up and everything will still be much smaller than you've asked for, scale it up more to compensate and everything that actually respects your decision will be ginormous.  At least we have better page zoom now, I guess.

Oh, and do remember: Stack Overflow didn't exist yet.  This stuff was passed around purely by word of mouth.  If you were lucky, you knew about some of the websites about websites, like [quirks mode](https://www.quirksmode.org/) and [Eric Meyer's website](https://meyerweb.com/).

In fact, check out Meyer's [css/edge](https://meyerweb.com/eric/css/edge/index.html) site for some wild examples of stuff folks were doing, even with just CSS 1, as far back as 2002.  I still think [complexspiral](https://meyerweb.com/eric/css/edge/complexspiral/demo.html) is pure genius, even though you could do it nowadays with `opacity` and just one image.  The approach in [raggedfloat](https://meyerweb.com/eric/css/edge/raggedfloat/demo.html) wouldn't get native support in CSS until a few years ago, with [`shape-outside`](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside)!  He also brought us [CSS reset](https://meyerweb.com/eric/tools/css/reset/), eliminating differences between browsers' default styles.

(I cannot understate how much of a CSS _pioneer_ Eric Meyer is.  When his young daughter Rebecca died six years ago, she was uniquely immortalized with her own CSS color name, [`rebeccapurple`](https://meyerweb.com/eric/thoughts/2014/06/19/rebeccapurple/).  That's how highly the Web community thinks of him.  Also I have to go cry a bit over that story now.)


## The future arrives, gradually

Designers and developers were pushing the bounds of what browsers were capable of.  Browsers were handling it all somewhat poorly.  All the fixes and workarounds and libraries were arcane, brittle, error-prone, and/or heavy.

Clearly, browsers needed some new functionality.  But just slopping something in wouldn't help; Microsoft had done plenty of that, and it had mostly made a mess.

Several struggling attempts began.  With the W3C's head still squarely up its own ass — even explicitly rejecting proposed enhancements to HTML, in favor of snorting XML — some folks from (active) browser vendors Apple, Mozilla, and Opera decided to make their own clubhouse.  WHATWG came into existence in June 2004, and they began work on HTML5.  (It would end up defining error-handling very explicitly, which completely obviated the need for XHTML and eliminated a number of security concerns when working with arbitrary HTML.  Also it gave us some new goodies, like native audio, video, and form controls for dates and colors and other stuff that had been clumsily handled by JavaScript-powered custom controls.  And, um, still often are.)

Then there was CSS 3.  I'm not sure when it started to exist.  It emerged slowly, struggling, like a chick hatching from an egg and taking its damn sweet fucking time to actually get implemented anywhere.

I'm having to do a lot of educated guessing here, but I _think_ it began with `border-radius`.  Specifically, with `-moz-border-radius`.  I don't know when it was first introduced, but the Mozilla bug tracker has mentions of it as far back as 1999.

See, Firefox's own UI is rendered _with CSS_.  If Mozilla wanted to do something that couldn't be done with CSS, they added a property of their own, prefixed with `-moz-` to indicate it was their own invention.  And when there's no real harm in doing so, they leave the property accessible to websites as well.

My guess, then, is that the push for CSS 3 really began when Firefox took off and designers discovered `-moz-border-radius`.  Suddenly, built-in rounded corners were available!  No more fucking around in Photoshop; you only needed to write a single line!  Practically overnight, everything everywhere had its corners filed down.

And from there, things snowballed.  Common problems were addressed one at a time by new CSS features, which were clustered together into a new CSS version: CSS 3.  The big ones were solutions to the design problems mentioned before:

- Rounded corners, provided by `border-radius`.
- Gradients, provided by `linear-gradient()` and friends.
- Multiple backgrounds, which weren't exactly a pressing concern, but which turned out to make some other stuff easier.
- Translucency, provided by `opacity` and colors with an alpha channel.
- Box shadows.
- Text shadows, which had been in CSS 2 but dropped in 2.1 and never implemented anyway.
- Border images, so you could do even fancier things than mere rounded borders.
- Transitions and animations, now doable with ease without needing jQuery (or any JS at all).
- `:nth-child()`, which solved the alternating rows problem with pure CSS.
- Transformations.  Wait, what?  This kinda leaked in from SVG, which browsers were also being expected to implement, and which is built heavily around transforms.  The code was already there, so, hey, now we can rotate stuff with CSS!  Couldn't do _that_ before.  Cool.
- Web fonts, which had been in CSS for some time but only ever implemented in IE and only with some goofy DRM-laden font format.  Now we weren't limited to the four bad fonts that ship with Windows and that no one else has!

These were pretty great!  They didn't solve any layout problems, but they _did_ address aesthetic issues that designers had been clumsily working around by using loads of images and/or JavaScript.  That meant less stuff to download and more text used instead of images, both of which were pretty good for the Web.

The grand irony is that all the stuff you could do with these features went out of style almost immediately, and now we're back to flat rectangles again.

### Browser prefixing hell

Alas!  All was still not right with the world.

Several of these new gizmos were, I believe, initially developed by browser vendors and prefixed.  Some later ones were designed by the CSS committee but implemented by browsers while the design was still in flux, and thus also prefixed.

So began _prefix hell_, which continues to this day.

Mozilla had `-moz-border-radius`, so when Safari implemented it, it was named `-webkit-border-radius` ("WebKit" being the name of Apple's KHTML fork).  Then the CSS 3 spec standardized it and called it just `border-radius`.  That meant that if you wanted to use rounded borders, you actually needed to give _three_ rules:

```css
element {
    -moz-border-radius: 1em;
    -webkit-border-radius: 1em;
    border-radius: 1em;
}
```

The first two made the effect actually work in current browsers, and the last one was future-proofing: when browsers implemented the real rule and dropped the prefixed ones, it would take over.

You had to do this _every fucking time_, since CSS isn't a programming language and has no macros or functions or the like.  Sometimes Opera and IE would have their own implementations with `-o-` and `-ms-` prefixes, bringing the total to five copies.  It got much worse with gradients; the syntax went through a number of major incompatible revisions, so you couldn't even rely on copy/pasting and changing the property name!

And plenty of folks, well, fucked it up.  I can't blame them too much; I mean, this sucks.  But enough pages used _only_ the prefixed forms, and not the final form, that browsers had to keep supporting the prefixed form for longer than they would've liked to avoid breaking stuff.  And if the prefixed form still works and it's what you're used to writing, then maybe you still won't bother with the unprefixed one.

Worse, _some_ people would _only_ use the form that worked in their pet choice of browser.  This got especially bad with the rise of mobile web browsers.  The built-in browsers on iOS and Android are Safari (WebKit) and Chrome (originally WebKit, now a fork), so you only "needed" to use the `-webkit-` properties.  Which made things difficult for Mozilla when it released [Firefox for Android](https://www.mozilla.org/en-US/firefox/mobile/).

Hey, remember that whole debacle with IE 6?  Here we are again!  It was bad enough that Mozilla eventually decided to [implement](https://developer.mozilla.org/en-US/docs/Web/CSS/WebKit_Extensions#Supported_in_Firefox_with_-webkit-_prefix) a number of `-webkit-` properties, which remain supported even in desktop Firefox to this day.  The situation is goofy enough that Firefox now supports some effects _only_ via these properties, like [`-webkit-text-stroke`](https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-text-stroke), which isn't being standardized.

Even better, Chrome's current forked engine is called Blink, so _technically_ it shouldn't be using `-webkit-` properties either.  And yet, here we are.  At least it's not as bad as the [user agent string mess](https://webaim.org/blog/user-agent-string-history/).

Browser vendors have pretty much abandoned prefixing, now; instead they hide experimental features behind flags (so they'll only work on the developer's machine), and new features are theoretically designed to be smaller and easier to stabilize.

This mess was probably a huge motivating factor for the development of [Sass](https://sass-lang.com/) and [LESS](http://lesscss.org/), two languages that produce CSS.  Or...  two CSS preprocessors, maybe.  They have very similar goals: both add variables, functions, and some form of macros to CSS, allowing you to eliminate a lot of the repetition and browser hacks and other nonsense from your stylesheets.  Hell, this blog [still uses SCSS](https://github.com/eevee/eev.ee/tree/988fc2b4547ee41388f29c4bad622c492c4c6f77/theme/static/sass), though its use has gradually decreased over time.

### Flexbox

But then, like an angel descending from heaven...  [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout).

Flexbox has been around for a _long_ time — [allegedly](https://www.caniuse.com/#feat=flexbox) it had partial support in Firefox 2, back in 2006!  It went through several incompatible revisions and took ages to stabilize.  Then IE took ages to implement it, and you don't really want to rely on layout tools that only work for half your audience.  It's only relatively recently (2015?  Later?) that flexbox has had sufficiently broad support to use safely.  And I could swear I still run into folks whose current Safari doesn't recognize it at all without prefixing, even though Safari supposedly dropped the prefixes five years ago...

Anyway, flexbox is a CSS implementation of a pretty common GUI layout tool: you have a parent with some children, and the parent has some amount of space available, and it gets divided automatically between the children.  You know, it _puts things next to each other_.

The general idea is that the browser computes how much space the parent has available and the "initial size" of each child, figures out how much extra space there is, and distributes it according to the flexibleness of each child.  Think of a toolbar: you might want each button to have a fixed size (a flex of 0), but want to add spacers that share any leftover space equally, so you'd give them a flex of 1.

Once that's done, you have a number of quality-of-life options at your disposal, too: you can distribute the extra space _between_ the children instead, you can tell the children to stretch to the same height or align them in various ways, and you can even have them wrap into multiple rows if they won't all fit!

With this, we can take yet another crack at that [thumbnail grid]({static}/media/2020-02-css/thumbnail-grids.html#flexbox):

```css
.thumbnail-grid {
    display: flex;
    flex-wrap: wrap;
}
.thumbnail-grid li {
    flex: 1 0 250px;
}
```

This is miraculous.  I forgot all about `inline-block` overnight and mostly salivated over this until it was universally supported.  It even expresses very clearly what I want.

...almost.  It still has the problem that too-wide cells will break the grid, since it's _still_ a horizontal row wrapped onto several independent lines.  It's pretty damn cool, though, and solves a number of other layout problems.  Surely this is good enough.  Unless...?

I'd say mass adoption of flexbox marked the beginning of the modern era of CSS.  But there was one lingering problem...

### The slow, agonizing death of IE

IE 6 took a long, long, _long_ time to go away.  It didn't drop below 10% market share (still a huge chunk) until early 2010 or so.

Firefox hit 1.0 at the end of 2004.  IE 7 wasn't released until two years later, it offered only modest improvements, it suffered from compatibility problems with stuff built for IE 6, and the IE 6 holdouts (many of whom were not Computer People) generally saw no reason to upgrade.  Vista shipped with IE 7, but Vista was kind of a flop — I don't believe it ever came close to overtaking XP, not in its entire lifetime.

Other factors included corporate IT policies, which often take the form of "never upgrade anything ever" — and often for good reason, as I heard endless tales of internal apps that only worked in IE 6 for all manner of horrifying reasons.  Then there was the _entirety of South Korea_, which was _legally required_ to use IE 6 because they'd enshrined in law some [security requirements](https://www.washingtonpost.com/world/asia_pacific/due-to-security-law-south-korea-is-stuck-with-internet-explorer-for-online-shopping/2013/11/03/ffd2528a-3eff-11e3-b028-de922d7a3f47_story.html) that could only be implemented with an IE 6 ActiveX control.

So if you maintained a website that was used — or worse, _required_ — by people who worked for businesses or lived in other countries, you were pretty much stuck supporting IE 6.  Folks making little personal tools and websites abandoned IE 6 compatibility early on and plastered their sites with increasingly obnoxious banners taunting anyone who dared show up using it...  but if you were someone's boss, why would you tell them it's okay to drop 20% of your potential audience?  Just work harder!

The tension grew over the years, as CSS became more capable and IE 6 remained an anchor.  It still didn't even understand _PNG alpha_ without workarounds, and meanwhile we were starting to get more critical features like native video in HTML5.  The workarounds grew messier, and the list of features you basically just couldn't use grew longer.  (I'd show you what my blog looks like in IE 6, but I don't think it can even connect — the TLS stuff it supports is so ancient and broken that it's been disabled on most servers!)

Shoutouts, by the way, to some folks on the YouTube team, who in July 2009 [added a warning banner](https://www.theverge.com/2019/5/4/18529381/google-youtube-internet-explorer-6-kill-plot-engineer) imploring IE 6 users to switch to _anything_ else — without asking anyone for approval.  "Within one month...  over 10 percent of global IE6 traffic had dropped off."  Not all heroes wear capes.

I'd mark the beginning of the end as the day YouTube _actually_ dropped IE 6 support — March 13, 2010, almost nine years after its release.  I don't know how much of a _direct_ impact YouTube has on corporate users or the South Korean government, but a massive web company dropping an entire browser sends a pretty strong message.

There were other versions of IE, of course, and many of them were messy headaches in their own right.  But each subsequent one became less of a pain, and nowadays you don't even have to think too much about testing in IE (now Edge).  Just in time for Microsoft to scrap their own rendering engine and turn their browser into a Chrome clone.


## Now

CSS is pretty great now.  You don't need weird fucking hacks just to put things next to each other.  Browser dev tools are built in, now, and are fucking amazing — Firefox has started specifically warning you when some CSS properties won't take effect because of the values of others!  Obscure implicit side effects like "stacking contexts" (whatever those are) can now be set explicitly, with properties like `isolation: isolate`.

In fact, let me just list everything that I can think of that you can do in CSS now.  This isn't a guide to all possible uses of styling, but if your CSS knowledge hasn't been updated since 2008, I hope this whets your appetite.  And this stuff is just CSS!  So many things that used to be impossible or painful or require clumsy plugins are now natively supported — audio, video, custom drawing, 3D rendering...  not to mention the vast ergonomic improvements to JavaScript.

### Layout

A [grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout) container can do pretty much anything tables can do, and more, including automatically determining how many columns will fit.  It's fucking amazing.  More on that below.

A [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout) container lays out its children in a row or column, allowing each child to declare its "default" size and what proportion of leftover space it wants to consume.  Flexboxes can wrap, rearrange children without changing source order, and align children in a number of ways.

[Columns](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Columns) will pour text into, well, multiple columns.

The [`box-sizing`](https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing) property lets you opt into the IE box model on a per-element basis, for when you need an entire element to take up a fixed amount of space and need padding/borders to _subtract_ from that.

[`display: contents`](https://developer.mozilla.org/en-US/docs/Web/CSS/display) dumps an element's contents out into its parent, as if it weren't there at all.  `display: flow-root` is basically an automatic clearfix, only a decade too late.

[`width`](https://developer.mozilla.org/en-US/docs/Web/CSS/width) can now be set to `min-content`, `max-content`, or the `fit-content()` function for more flexible behavior.

[`white-space: pre-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space) preserves whitespace, but breaks lines where necessary to avoid overflow.  Also useful is `pre-line`, which collapses sequences of spaces down to a single space, but preserves literal newlines.

[`text-overflow`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-overflow) cuts off overflowing text with an ellipsis (or custom character) when it would overflow, rather than simply truncating it.  Also specced is the ability to fade out the text, but this is as yet unimplemented.

[`shape-outside`](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside) alters the shape used when wrapping text around a float.  It can even use the alpha channel of an image as the shape.

[`resize`](https://developer.mozilla.org/en-US/docs/Web/CSS/resize) gives an arbitrary element a resize handle (as long as it has `overflow`).

[`writing-mode`](https://developer.mozilla.org/en-US/docs/Web/CSS/writing-mode) sets the direction that text flows.  If your design needs to work for multiple writing modes, a number of CSS properties that mention left/right/top/bottom have alternatives that describe directions in terms of the writing mode: [`inset-block`](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-block) and [`inset-inline`](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-inline) for position, [`block-size`](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size) and [`inline-size`](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size) for width/height, [`border-block`](https://developer.mozilla.org/en-US/docs/Web/CSS/border-block) and [`border-inline`](https://developer.mozilla.org/en-US/docs/Web/CSS/border-inline) for borders, and similar for padding and margins.

### Aesthetics

[Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions) smoothly interpolate a value whenever it changes, whether due to an effect like `:hover` or e.g. a class being added from JavaScript.  [Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations) are similar, but play a predefined animation automatically.  Both can use a number of different [easing functions](https://easings.net/en).

[`border-radius`](https://developer.mozilla.org/en-US/docs/Web/CSS/border-radius) rounds off the corners of a box.  The corners can all be different sizes, and can be circular or elliptical.  The curve also applies to the border, background, and any box shadows.

[Box shadows](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow) can be used for the obvious effect of casting a drop shadow.  You can also use multiple shadows and `inset` shadows for a variety of clever effects.

[`text-shadow`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow) does what it says on the tin, though you can also stack several of them for a rough approximation of a text outline.

[`transform`](https://developer.mozilla.org/en-US/docs/Web/CSS/transform) lets you apply an arbitrary matrix transformation to an element — that is, you can scale, rotate, skew, translate, and/or do perspective transform, all without affecting layout.

[`filter`](https://developer.mozilla.org/en-US/docs/Web/CSS/filter) (distinct from the IE 6 one) offers a handful of specific visual filters you can apply to an element.  Most of them affect color, but there's also a `blur()` and a `drop-shadow()` (which, unlike `box-shadow`, applies to an element's appearance rather than its containing box).

[`linear-gradient()`](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient), [`radial-gradient()`](https://developer.mozilla.org/en-US/docs/Web/CSS/radial-gradient), the new and less-supported [`conic-gradient()`](https://developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient), and their `repeating-*` variants all produce gradient images and can be used anywhere in CSS that an image is expected, most commonly as a `background-image`.

[`scrollbar-color`](https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-color) changes the scrollbar color, with the downside of reducing the scrollbar to a very simple thumb-and-track in current browsers.

[`background-size: cover` and `contain`](https://developer.mozilla.org/en-US/docs/Web/CSS/background-size) will scale a background image proportionally, either big enough to completely cover the element (even if cropped) or small enough to exactly fit inside it (even if it doesn't cover the entire background).

[`object-fit`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) is a similar idea but for non-background media, like `<img>`s.  The related [`object-position`](https://developer.mozilla.org/en-US/docs/Web/CSS/object-position) is like `background-position`.

Multiple backgrounds are possible, which is especially useful with gradients — you can stack multiple gradients, other background images, and a solid color on the bottom.

[`text-decoration`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration) is fancier than it used to be; you can now set the color of the line and use several different kinds of lines, including dashed, dotted, and wavy.

[CSS counters](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Lists_and_Counters/Using_CSS_counters) can be used to number arbitrary elements in an arbitrary way, exposing the counting ability of `<ol>` to any set of elements you want.  

The [`::marker`](https://developer.mozilla.org/en-US/docs/Web/CSS/::marker) pseudo-element allows you to style a list item's marker box, or even replace it outright with a custom counter.  Browser support is spotty, but improving.  Similarly, the [`@counter-style`](https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style) at-rule implements an entirely new counter style (like 1 2 3, i ii iii, A B C, etc.) which you can then use anywhere, though only Firefox supports it so far.

[`image-set()`](https://developer.mozilla.org/en-US/docs/Web/CSS/image-set) provides a list of candidate images and lets the browser choose the most appropriate one based on the pixel density of the user's screen.

[`@font-face`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face) defines a font that can be downloaded, though you can avoid figuring out how to use it correctly by using [Google Fonts](https://developers.google.com/fonts/).

[`pointer-events: none`](https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events) makes an element ignore the mouse entirely; it can't be hovered, and clicks will go straight through it to the element below.

[`image-rendering`](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering) can force an image to be resized nearest-neighbor rather than interpolated, though browser support is still spotty and you may need to also include some vendor-specific properties.

[`clip-path`](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path) crops an element to an arbitrary shape.  There's also [`mask`](https://developer.mozilla.org/en-US/docs/Web/CSS/mask) for arbitrary alpha masking, but browser support is spotty and hoo boy is this one complicated.

### Syntax and misc

[`@supports`](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports) lets you explicitly write different CSS depending on what the browser supports, though it's nowhere near as useful nowadays as it would've been in 2004.

`A > B` selects immediate children.  `A ~ B` selects siblings.  `A + B` selects immediate (element) siblings.  Square brackets can do a [bunch of stuff](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to select based on attributes; most obvious is `input[type=checkbox]`, though you can also do interesting things with matching parts of `<a href>`.

There are a whole bunch of pseudo-classes now.  Many of them are for form elements: [`:enabled`](https://developer.mozilla.org/en-US/docs/Web/CSS/:enabled) and [`:disabled`](https://developer.mozilla.org/en-US/docs/Web/CSS/:disabled); [`:checked`](https://developer.mozilla.org/en-US/docs/Web/CSS/:checked) and [`:indeterminate`](https://developer.mozilla.org/en-US/docs/Web/CSS/:indeterminate) (also apply to radio and `<option>`); [`:required`](https://developer.mozilla.org/en-US/docs/Web/CSS/:required) and [`:optional`](https://developer.mozilla.org/en-US/docs/Web/CSS/:optional); [`:read-write`](https://developer.mozilla.org/en-US/docs/Web/CSS/:read-write) and [`:read-only`](https://developer.mozilla.org/en-US/docs/Web/CSS/:read-only); [`:in-range`](https://developer.mozilla.org/en-US/docs/Web/CSS/:in-range)/[`:out-of-range`](https://developer.mozilla.org/en-US/docs/Web/CSS/:out-of-range) and [`:valid`](https://developer.mozilla.org/en-US/docs/Web/CSS/:valid)/[`:invalid`](https://developer.mozilla.org/en-US/docs/Web/CSS/:invalid) (for use with HTML5 client-side form validation); [`:focus`](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus) and [`:focus-within`](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-within); and [`:default`](https://developer.mozilla.org/en-US/docs/Web/CSS/:default) (which selects the default form button and any pre-selected checkboxes, radio buttons, and `<option>`s).

For targeting specific elements within a set of siblings, we have: [`:first-child`](https://developer.mozilla.org/en-US/docs/Web/CSS/:first-child), [`:last-child`](https://developer.mozilla.org/en-US/docs/Web/CSS/:last-child), and [`:only-child`](https://developer.mozilla.org/en-US/docs/Web/CSS/:only-child); [`:first-of-type`](https://developer.mozilla.org/en-US/docs/Web/CSS/:first-of-type), [`:last-of-type`](https://developer.mozilla.org/en-US/docs/Web/CSS/:last-of-type), and [`:only-of-type`](https://developer.mozilla.org/en-US/docs/Web/CSS/:only-of-type) (where "type" means tag name); and [`:nth-child()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child), [`:nth-last-child()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-child), [`:nth-of-type()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type), and [`:nth-last-of-type()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-of-type) (to select every second, third, etc. element).

[`:not()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:not) inverts a selector.  [`:empty`](https://developer.mozilla.org/en-US/docs/Web/CSS/:empty) selects elements with no children and no text.  [`:target`](https://developer.mozilla.org/en-US/docs/Web/CSS/:target) selects the element jumped to with a URL fragment (e.g. if the address bar shows `index.html#foo`, this selects the element whose ID is `foo`).

[`::before`](https://developer.mozilla.org/en-US/docs/Web/CSS/::before) and [`::after`](https://developer.mozilla.org/en-US/docs/Web/CSS/::after) should have two colons now, to indicate that they create pseudo-elements rather than merely scoping the selector they're attached to.  [`::selection`](https://developer.mozilla.org/en-US/docs/Web/CSS/::selection) customizes how selected text appears; [`::placeholder`](https://developer.mozilla.org/en-US/docs/Web/CSS/::placeholder) customizes how placeholder text (in text fields) appears.

[Media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/@media) do just a whole bunch of stuff so your page can adapt based on how it's being viewed.  The [`prefers-color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) media query tells you if the user's system is set to a light or dark theme, so you can adjust accordingly without having to ask.

You can write translucent [colors](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) as `#rrggbbaa` or `#rgba`, as well as using the `rgba()` and `hsla()` functions.

[Angles](https://developer.mozilla.org/en-US/docs/Web/CSS/angle) can be described as fractions of a full circle with the `turn` unit.  Of course, `deg` and `rad` (and `grad`) are also available.

[CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) (officially, "custom properties") let you specify arbitrary named values that can be used anywhere a value would appear.  You can use this to reduce the amount of CSS fiddling needs doing in JavaScript (e.g., recolor a complex part of a page by setting a CSS variable instead of manually adjusting a number of properties), or have a generic component that reacts to variables set by an ancestor.

[`calc()`](https://developer.mozilla.org/en-US/docs/Web/CSS/calc) computes an arbitrary expression and updates automatically (though it's somewhat obviated by `box-sizing`).

The [`vw`, `vh`, `vmin`, and `vmax` units](https://developer.mozilla.org/en-US/docs/Web/CSS/length) let you specify lengths as a fraction of the viewport's width or height, or whichever of the two is bigger/smaller.

----

Phew!  I'm sure I'm forgetting plenty and folks will have even longer lists of interesting tidbits in the comments.  Thanks for saving me some effort!  Now I can stop browsing MDN and do this final fun part.

### State of the art thumbnail grid

At long last, we arrive at the final and objectively correct way to construct a thumbnail grid: using [CSS grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout).  You can tell this is the right thing to use because it has "grid" in the name.  Modern CSS features are pretty great about letting you say the thing you want and having it happen, rather than trying to coax it into happening implicitly via voodoo.

And it is oh so simple:

```css
.thumbnail-grid {
    display: grid;
    grid: auto-flow / repeat(auto-fit, minmax(250px, 1fr));
}
```

Done!  That [gives you a grid]({static}/media/2020-02-css/thumbnail-grids.html#grid).  You have myriad other twiddles to play with, just as with flexbox, but that's the basic idea.  You don't even need to style the elements themselves; most of the layout work is done in the container.

The [`grid` shorthand property](https://developer.mozilla.org/en-US/docs/Web/CSS/grid) looks a little intimidating, but only because it's so flexible.  It's saying: fill the grid one row at a time, generating as many rows as necessary; make as many 250px columns as will fit, and share any leftover space between them equally.

CSS grids are also handy for laying out `<dl>`s, something that's historically been a massive pain to make work — a `<dl>` contains any number of `<dt>`s followed by any number of `<dd>`s (including zero), and the only way to style this until grid was to float the `<dt>`s, which meant they had to have a fixed width.  Now you can just tell the `<dt>`s to go in the first column and `<dd>`s to go in the second, and grid will take care of the rest.

And laying out your page?  That whole sidebar thing?  Check out how easy that is:

```css
body {
    display: grid;
    grid-template:
        "header         header          header"
        "left-sidebar   main-content    right-sidebar"
        "footer         footer          footer"
        / 1fr           6fr             1fr
    ;
}
body > header {
    grid-area: header;
}
#left-sidebar {
    grid-area: left-sidebar;
}
/* ... etc ... */
```

Done.  Easy.  It doesn't matter what order the parts appear in the markup, either.

### On the other hand

The web is still a _little bit_ of a disaster.  A lot of folks don't even know that flexbox and grid are supported [almost universally](https://www.caniuse.com/#feat=css-grid) now; but given how long it took to get from early spec work to broad implementation, I can't really blame them.  I saw a brand new little site just yesterday that consisted mostly of a huge list of "thumbnails" of various widths, and it used floats!  Not even `inline-block`!  I don't know how we managed to teach everyone about all the hacks required to make that work, but somehow haven't gotten the word out about flexbox.

But far worse than that: I still regularly encounter sites that do their entire page layout with _JavaScript_.  If you use [uMatrix](https://addons.mozilla.org/en-US/firefox/addon/umatrix/), your first experience is with a pile of text overlapping a pile of other text.  Surely this is a step backwards?  What are you possibly doing that your header and sidebar can only be laid out correctly by executing code?  It's not like the page loads with _no_ CSS — nothing in plain HTML will overlap by default!  You have to tell it to do that!

And then there's the mobile web, which despite everyone's good intentions, has kind of turned out to be a failure.  The idea was that you could use CSS media queries to fit your normal site on a phone screen, but instead, most major sites have entirely separate mobile versions.  Which means that either the mobile site is missing a bunch of important features and I'll have to awkwardly navigate that on my phone anyway, or the desktop site is full of crap that nobody actually needs.

(Meanwhile, Google's own Android versions of Docs/Sheets/etc. have, like, 5% of the features of the Web versions?  Not sure what to make of that.)

Hmm.  Strongly considering writing something that goes more into detail about improvements to CSS since the Firefox 3 era, similar to [the one I wrote for JavaScript]({filename}/2017-10-07-javascript-got-better-while-i-wasnt-looking.markdown).  But this post is long enough.


## Some futures that never were

I don't know what's coming next in CSS, especially now that flexbox and grid have solved all our problems.  I'm vaguely aware of some work being done on more extensive math support, and possibly some functions for altering colors like in Sass.  There's a [painting API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Painting_API) that lets you generate backgrounds on the fly with JavaScript using the canvas API, which is...  quite something.  Apparently it's now in spec that you can use [`attr()`](https://developer.mozilla.org/en-US/docs/Web/CSS/attr) (which evaluates to the value of an HTML attribute) as the value for any property, which seems cool and might even let you implement HTML tables entirely in CSS, but you could do the same thing with variables.  I mean, um, custom properties.  I'm more excited about [`:is()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:is), which matches any of a list of selectors, and [subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Subgrid), which lets you add some nesting to a grid but keep grandchildren still aligned to it.

Much easier is to list some things that _were_ the future, but fizzled out.

- [`display: run-in`](https://developer.mozilla.org/en-US/docs/Web/CSS/display) has been part of CSS since version 2 (way back in '98), but it's basically unsupported.  The idea is that a "run-in" box is inserted, inline, into the next block, so this:

        :::html
        <h2 style="display: run-in;">Title</h2>
        <p>Paragraph</p>
        <p>Paragraph</p>

    displays like this:

    > **Title** Paragraph
    >
    > Paragraph

    And, ah, hm, I'm starting to see why it's unsupported.  It _used_ to exist in WebKit, but was apparently so unworkable as to be removed six years ago.

- "Alternate stylesheets" were popular in the early 00s, at least on a few of my friends' websites.  The idea was that you could list _more than one_ stylesheet for your site (presumably for different themes), and the browser would give the user a list of them.  Alas, that list was always squirrelled away in a menu with no obvious indication of when it was actually populated, so in the end, everyone who wanted multiple themes just implemented an in-page theme switcher themselves.

    This feature is [still supported](https://developer.mozilla.org/en-US/docs/Web/CSS/Alternative_style_sheets), but apparently Chrome never bothered implementing it, so it's effectively dead.

- More generally, the original CSS spec clearly expects users to be able to write their own CSS for a website — right in paragraph 2 it says

    > ...the reader may have a personal style sheet to adjust for human or technological handicaps.

    Hey, that sounds cool.  But it never materialized as a browser feature.  Firefox has [`userContent.css`](http://kb.mozillazine.org/UserContent.css) and some URL selectors for writing per-site rules, but that's relatively obscure.

    Still, there's clearly demand for the concept, as evidenced by the popularity of the Stylish extension — which does just this.  (Too bad it was [bought by some chucklefucks who started using it to suck up browser data to sell to advertisers](https://robertheaton.com/2018/07/02/stylish-browser-extension-steals-your-internet-history/).  Use [Stylus](https://addons.mozilla.org/en-US/firefox/addon/styl-us/) instead.)

- A common problem (well, for me) is that of styling the _label_ for a checkbox, depending on its state.  Styling the checkbox itself is easy enough with the `:checked` pseudo-selector.  But if you arrange a checkbox and its label in the obvious way:

        :::html
        <label><input type="checkbox"> Description of what this does</label>

    ...then CSS has no way to target either the `<label>` element or the text node.  jQuery's (originally custom) selector engine offered a custom `:has()` pseudo-class, which could be used to express this:

        :::css
        /* checkbox label turns bold when checked */
        label:has(input:checked) {
            font-weight: bold;
        }

    Early CSS 3 selector discussions seemingly wanted to avoid this, I guess for performance reasons?  The somewhat novel alternative was to write out the entire selector, but be able to alter which part of it the rules affected with a "subject" indicator.  At first this was a pseudo-class:

        :::css
        label:subject input:checked {
            font-weight: bold;
        }

    Then later, they introduced a `!` prefix instead:

        :::css
        !label input:checked {
            font-weight: bold;
        }

    Thankfully, this was decided to be a bad idea, so the current specced way to do this is...  [`:has()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)!  Unfortunately, it's only allowed when querying from JavaScript, not in a live stylesheet, and nothing implements it anyway.  20 years and I'm still waiting for a way to style checkbox labels.

- `<style scoped>` was an attribute that would've made a `<style>` element's CSS rules only apply to other elements within its immediate parent, meaning you could drop in arbitrary (possibly user-written) CSS without any risk of affecting the rest of the page.  Alas, this was quietly dropped some time ago, with shadow DOM suggested as a wildly inappropriate replacement.

- I seem to recall that when I first heard about [Web components](https://developer.mozilla.org/en-US/docs/Web/Web_Components), they were templates you could use to reduce duplication in pure HTML?  But I can't find any trace of that concept now, and the current implementations require JavaScript to define them, so there's nothing declarative linking a new tag to its implementation.  Which makes them completely unusable for anything that doesn't have a compelling reason to rely on JS.  Alas.

- `<blink>` and `<marquee>`.  RIP.  Though both can be easily replicated with CSS animations.


## That's it

You're still here?  It's over.  Go home.

And maybe push back against Blink monoculture and use [Firefox](https://www.mozilla.org/en-US/firefox/), including [on your phone](https://www.mozilla.org/en-US/firefox/mobile/), unless for some reason you use an iPhone, which forbids other browser engines, which is far worse than anything Microsoft ever did, but we just kinda accept it for some reason.
