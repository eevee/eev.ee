title: Digital painter rundown
date: 2017-06-17 00:58
category: articles
tags: tech, patreon

Another [patron](https://www.patreon.com/eevee) post!  [IndustrialRobot](https://www.patreon.com/user?u=199476) asks:

> You should totally write about drawing/image manipulation programs! (Inspired by [https://eev.ee/blog/2015/05/31/text-editor-rundown/]({filename}/2015-05-31-text-editor-rundown.markdown))

This is a little trickier than a text editor comparison — while most text editors are cross-platform, quite a few digital art programs are _not_.  So I'm effectively unable to even try a decent chunk of the offerings.  I'm also still a _relatively_ new artist, and image editors are much harder to briefly compare than text editors...

Right, now that your expectations have been suitably lowered:

<!-- more -->


## Krita

I do all of my digital art in [Krita](https://krita.org/en/).  It's pretty alright.

...

Okay so Krita grew out of [Calligra](https://www.calligra.org/), which used to be KOffice, which was an office suite designed for KDE (a Linux desktop environment).  I bring this up because KDE has a certain...  reputation.  With KDE, there are at least three completely different ways to do _anything_, each of those ways has ludicrous amounts of customization and settings, and somehow it still can't do what you want.

Krita inherits this aesthetic by attempting to do _literally everything_.  It has 17 different brush engines, more than 70 layer blending modes, seven color picker dockers, and an ungodly number of colorspaces.  It's clearly intended primarily for drawing, but it also supports animation and vector layers and a pretty decent spread of raster editing tools.  I _just right now_ discovered that it has Photoshop-like "layer styles" (e.g. drop shadow), after a year and a half of using it.

In fairness, Krita manages all of this stuff well enough, and (apparently!) it manages to stay out of your way if you're not using it.  In less fairness, they managed to break erasing with a Wacom tablet pen for three months?

I don't want to rag on it too hard; it's an impressive piece of work, and I enjoy using it!  The emotion it evokes isn't so much frustration as...  mystified bewilderment.

I once filed a ticket suggesting the addition of a brush size palette — a panel showing a grid of fixed brush sizes that makes it easy to switch between known sizes with a tablet pen (and increases the chances that you'll be able to get a brush back to the right size again).  It's a prominent feature of Paint Tool SAI and Clip Studio Paint, and while I've never used either of those myself, I've seen a good few artists swear by it.

The developer response was that I could emulate the behavior by creating brush presets.  But that's flat-out wrong: getting the same effect would require creating a ton of brush presets _for every brush I have_, plus giving them all distinct icons so the size is obvious at a glance.  Even then, it would be much more tedious to use and fill my presets with junk.

And that sort of response is what's so mysterious to me.  I've never even been able to use this feature myself, but a year of amateur painting with Krita has convinced me that it would be pretty useful.  But a developer didn't see the use _and_ suggested an incredibly tedious alternative that only half-solves the problem and creates new ones.  Meanwhile, of the 28 existing dockable panels, _a quarter_ of them are different ways to choose colors.

What is Krita trying to be, then?  What does Krita think it is?  Who precisely is the target audience?  I have no idea.

----

Anyway, I enjoy drawing in Krita well enough.  It ships with a respectable set of brushes, and there are [plenty more](https://docs.krita.org/Resources) floating around.  It has canvas rotation, canvas mirroring, perspective guide tools, and other art goodies.  It doesn't colordrop on right click by default, which is arguably a grave sin (it shows a customizable radial menu instead), but that's easy to rebind.  It understands having a background color _beneath_ a bottom transparent layer, which is very nice.  You can also toggle _any_ brush between painting and erasing with the press of a button, and that turns out to be very useful.

It doesn't support infinite canvases, though it does offer a one-click button to extend the canvas in a given direction.  I've never used it (and didn't even know what it did until just now), but would totally use an infinite canvas.

I haven't used the animation support too much, but it's pretty nice to have.  Granted, the only other animation software I've used is Aseprite, so I don't have many points of reference here.  It's a relatively new addition, too, so I assume it'll improve over time.

The one annoyance I remember with animation was really an interaction with a larger annoyance, which is: working with selections kind of sucks.  You can't drag a selection around with the selection tool; you have to switch to the move tool.  That would be fine if you could at least drag the selection _ring_ around with the selection tool, but you can't do that either; dragging just creates a new selection.

If you want to _copy_ a selection, you have to explicitly copy it to the clipboard and paste it, which _creates a new layer_.  Ctrl-drag with the move tool doesn't work.  So then you have to merge that layer down, which I think is where the problem with animation comes in: a new layer is non-animated by default, meaning it effectively appears in any frame, so simply merging it down with merge it onto _every single frame_ of the layer below.  And you won't even notice until you switch frames or play back the animation.  Not ideal.

This is another thing that makes me wonder about Krita's sense of identity.  It has a lot of fancy general-purpose raster editing features that even GIMP is still struggling to implement, like high color depth support and non-destructive filters, yet something as basic as working with selections is clumsy.  (In fairness, GIMP is a bit clumsy here too, but it has a consistent notion of "floating selection" that's easy enough to work with.)

I don't know how well Krita would work _as_ a general-purpose raster editor; I've never tried to use it that way.  I can't think of anything obvious that's missing.  The only real gotcha is that some things you might expect to be tools, like smudge or clone, are just types of brush in Krita.


## GIMP

Ah, [GIMP](https://www.gimp.org/) — open source's answer to Photoshop.

It's very obviously intended for raster editing, and I'm pretty familiar with it after half a lifetime of only using Linux.  I even wrote a little Scheme script for it _ages_ ago to automate some simple edits to a couple hundred files, back before I was aware of ImageMagick.  I don't know what to say about it, specifically; it's fairly powerful and does a wide variety of things.

In fact I'd say it's almost _frustratingly_ intended for raster editing.  I used GIMP in my first attempts at digital painting, before I'd heard of Krita.  It was _okay_, but so much of it felt clunky and awkward.  Painting is split between a pencil tool, a paintbrush tool, and an airbrush tool; I don't really know why.  The default brushes are largely uninteresting.  Instead of brush presets, there are _tool_ presets that can be saved for any tool; it's a neat idea, but doesn't feel like a real substitute for brush presets.

Much of the same functionality as Krita is there, but it's all somehow more clunky.  I'm sure it's possible to fiddle with the interface to get something friendlier for painting, but I never really figured out how.

And then there's the surprising stuff that's _missing_.  There's no canvas rotation, for example.  There's only one type of brush, and it just stamps the same pattern along a path.  I don't think it's possible to smear or blend or pick up color while painting.  The only way to change the brush size is via the very sensitive slider on the tool options panel, which I remember being a little annoying with a tablet pen.  Also, you have to specifically _enable_ tablet support?  It's not difficult or anything, but I have no idea why the default is to _ignore_ tablet pressure and treat it like a regular mouse cursor.

As I mentioned above, there's also no support for high color depth or non-destructive editing, which is honestly a little embarrassing.  Those are the major things Serious Professionals™ have been asking for for ages, and GIMP has been trying to provide them, but it's taking a very long time.  The first signs of GEGL, a new library intended to provide these features, appeared in GIMP 2.6...  in 2008.  The last major release was in 2012.  GIMP has been working on this new plumbing for almost as long as Krita's _entire development history_.  (To be fair, Krita has also raised almost €90,000 from three Kickstarters to fund its development; I don't know that GIMP is funded at all.)

I don't know what's up with GIMP nowadays.  It's still under active development, but the exact status and roadmap are a little unclear.  I still use it for some general-purpose editing, but I don't see any reason to use it to draw.

I do know that canvas rotation will be in the next release, and there was some experimentation with embedding MyPaint's brush engine (though when I tried it it was basically unusable), so maybe GIMP _is_ interested in wooing artists?  I guess we'll see.


## MyPaint

Ah, [MyPaint](http://mypaint.org/).  I gave it a try once.  Once.

It's a shame, really.  It _sounds_ pretty great: specifically built for drawing, has very powerful brushes, supports an infinite canvas, supports canvas rotation, has a simple UI that gets out of your way.  Perfect.

Or so it seems.  But in MyPaint's eagerness to shed unnecessary raster editing tools, it forgot a few of the more useful ones.  Like selections.

MyPaint has no notion of a selection, nor of copy/paste.  If you want to move a head to align better to a body, for example, the sanctioned approach is to duplicate the layer, erase the head from the old layer, erase everything _but_ the head from the new layer, then move the new layer.

I can't find anything that resembles HSL adjustment, either.  I guess the workaround for that is to create H/S/L layers and floodfill them with different colors until you get what you want.

I can't work seriously without these basic editing tools.  I could see myself doodling in MyPaint, but Krita works just as well for doodling as for serious painting, so I've never gone back to it.


## Drawpile

[Drawpile](https://drawpile.net/) is the modern equivalent to OpenCanvas, I suppose?  It lets multiple people draw on the same canvas simultaneously.  (I would not recommend it as a general-purpose raster editor.)

It's a _little_ clunky in places — I sometimes have bugs where keyboard focus gets stuck in the chat, or my tablet cursor becomes invisible — but the collaborative part works surprisingly well.  It's not a brush powerhouse or anything, and I don't think it allows textured brushes, but it supports tablet pressure and canvas rotation and locked alpha and _selections_ and whatnot.

I've used it a couple times, and it's worked well enough that...  well, other people made pretty decent drawings with it?  I'm not sure I've managed yet.  And I wouldn't use it single-player.  Still, it's fun.


## Aseprite

[Aseprite](https://www.aseprite.org/) is for pixel art so it doesn't really belong here at all.  But it's very good at that and I like it a lot.


## That's all

I can't name any other serious contender that exists for Linux.

I'm dimly aware of a thing called "Photo Shop" that's more intended for photos but functions as a passable painter.  More artists seem to swear by Paint Tool SAI and Clip Studio Paint.  Also there's Paint.NET, but I have no idea how well it's actually suited for painting.

And that's it!  That's all I've got.  Krita for drawing, GIMP for editing, Drawpile for collaborative doodling.
