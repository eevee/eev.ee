title: Doom text generator
date: 2019-12-01 19:48
category: release
tags: doom

<div class="prose-full-illustration">
<img src="{filename}/media/release/doom-text-generator.png" alt="Screenshot of a generator with controls for the font, color, scale, and alignment">
</div>

🔗 [**Doom text generator**, locally hosted](https://c.eev.ee/doom-text-generator/)

I've been mad my _entire life_ that one of these didn't seem to exist.  ZDoom can print arbitrary text, of course, but only if you fuck around writing and compiling an ACS script or whatever!  There's no console command for it!  Outrageous!!!

So I finally made this.  It took like ten hours, which I have to say, is fucking incredible.

<!-- more -->

I don't want to make a whole blog post out of this (I mean it was only ten hours) but a few points of interest:

- Probably _most_ of the work was in getting stuff out of Doom and into a usable format.  The end result is a thorny combination of three different file format parsers (half of which I threw away), manual extraction from game files via SLADE, both PyPNG and ImageMagick for some reason, and way too much JSON.

- Did you know that the small Doom font's `|` (pipe) character is inexplicably assigned to lowercase `y`?  Neither did I!  It's the only lowercase letter in the font — it only supports uppercase.

- I fucking love CSS grid.

- The colors are done using ZDoom's font color translation.  I always thought those were palette remappings — which is what "translation" means elsewhere in ZDoom — but no!  They actually use the perceptual brightness of the font, stretched to the full range, and then mapped to a color gradient.  It's not at all what I expected (which led me to some dead ends early on), but it's kind of cool.

- Implementing undocumented RLE is fun because if you're off by even a byte somewhere you suddenly have either ten times more or ten times less data than you expected and it's all complete garbage.

- I haven't put the source code up yet but will eventually.  I want to put it on itch, too, but I have to put together a whole _page_ and _stuff_ and I'm very tired now.

Anyway now you can make your own cool [in-game textures](https://twitter.com/eevee/status/1200830161211363328) and other shenanigans, enjoy!
