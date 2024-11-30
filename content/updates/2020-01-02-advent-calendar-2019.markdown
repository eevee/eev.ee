title: Advent calendar 2019
date: 2019-12-01-19:48
category: updates
tags: tech

<div class="prose-full-illustration">
<img src="{static}/media/release/advent2019.png" alt="Calendar of things I made during December, with little screenshots">
</div>

🔗 [**Advent calendar**, with links to individual projects](https://c.eev.ee/advent-2019/)

Happy new year!

For December, I had the absolutely ludicrous idea to do an advent calendar, whereupon I would make and release a thing _every day_ until Christmas.

It didn't go quite as planned!  But some pretty good stuff still came out of it.

<!-- more -->

----

**Day 1**: I started out well enough with the [Doom text generator](https://c.eev.ee/doom-text-generator/) (and [accompanying release post]({filename}/release/2019-12-01-doom-text-generator.markdown)), which does something simple that I've wanted for a long time but never seen anywhere: generate text using the Doom font.  Most of the effort here was just in hunting down the fonts and figuring out how they worked; the rest was gluing them together with the canvas API.  It could be improved further, but it's pretty solid and useful as-is!

**Day 2**: I tried another thing I'd always wanted: making a [crossword](https://c.eev.ee/puzzles/the-nuclear-age.html)!  (Solve interactively on [squares.io](https://squares.io/info/3szq4vjmtk3e65j55uxp/info)!)  I didn't expect it to take _all day_, but it did, and _even then_ I found a typo that I didn't have time to fix, and I had to rush with the clues.  All in all, an entertaining but way too difficult first attempt.  I'd love to try doing this more, though.

**Day 3**: I've made a couple SVG visualizations before — most notably in my post on [Perlin noise]({filename}/2016-05-29-perlin-noise.markdown) — and decided to take another crack at it.  The result was a [visualization of all six modern trig functions](https://c.eev.ee/viz/trig-functions.html), showing the relationships between them in two different ways.  I'm pretty happy with how this turned out, and delighted that I learned some relationships I didn't know about before, either!  I do wish I'd drawn some of the similar triangles to make the relationships more explicit, but I ran out of time — just orienting the text correctly took _ages_, especially since a lot of it needed different placement in all four quadrants.  I vaguely intended to get around to doing a couple more of these, but it didn't end up happening.

**Days 4 and 7**: I love the [PICO-8](https://www.lexaloffle.com/pico-8.php)'s built-in tracker, which makes way more sense to me than any "real" tracker, and set out to replicate it for the web.  The result is [PICOtracker](https://c.eev.ee/picotracker/)!  Unfortunately, this one didn't get fully finished (yet) — it can play back sounds and music from the hardcoded [Under Construction](https://eevee.itch.io/under-construction) cart, but doesn't support editing yet.  Most of my time went to figuring out the Web Audio API, figuring out what the knobs in the PICO-8 tracker actually _do_ (and shoutout to [picolove](https://github.com/picolove/picolove/) for acting as source code reference), and figuring out how to weld the two together.  I definitely want to revisit this in the near future!

**Day 5**: I'd been recently streaming [Eternal Doom III](https://doomwiki.org/wiki/Eternal_Doom) and was _almost_ done, and I keep being really lazy about putting Doom streams on YouTube, so I finished up the game (which took far, far longer than I expected) and [posted the whole thing as a playlist](https://www.youtube.com/watch?v=9Y35ga7-ndw&list=PLe3hrqBmMcMI6M_Qqem9KflrSgR6An3jS).  It spans like 24 hours.  Good if you, uh, just want some Doom noise to listen to in the background.

**Day 6**: I'd expected Eternal Doom to be a quick day so I could have a break, and it was not.  So I took an explicit day off.

**Days 8 and 13**: I made [flathack](https://c.eev.ee/flathack/), a web roguelike with only one floor!  The idea came from having played NetHack a great many times, and having seen the first floor much more than any other part of the dungeon — so why not make that the whole game?  It needs a lot more work, but I'm happy to have finally published a roguelike, and I think it already serves its intended purpose at least a little bit: it's a cute little timewaster that doesn't keep killing you.

**Days 9–12**: I got food poisoning.  It sucked.  A lot.

**Days 14–20**: Fresh off of making flathack in only two days, I got a bit too big for my britches and decided to try writing an interactive fiction game.  In one day.  Spoilers: it took more than one day.  But I think the result is pretty charming: [Star Anise Chronicles: Escape from the Chamber of Despair](https://c.eev.ee/anise-escape-despair/), a game about being a cat and causing wanton destruction, and also the first Star Anise Chronicles game to actually be published.  A good chunk of the time was spent just drawing illustrations for it, which weren't strictly necessary, but they add a lot to the game and they _did_ get me back in an art mood.

**Day 21**: I feel like I've been scared of color for a long time, and that's no good, so I [drew and colored something](https://twitter.com/eevee/status/1208657658716143616).

**Day 22**: I drew some weird porn, and colored it too!  Porn is just a blast to draw, and it'd been a while.  I'll let you find the link on the calendar if you really want it.

**Day 23**: Did not exist, due to becoming nocturnal.

**Day 24–28**: I started a big reference of a bunch of my Flora characters way back in November 2018, but I tried to _paint_ it when I didn't know what I wanted in a painting style, and eventually I gave up.  Flat colors are better for references anyway, so I tried again, and this time I finished!  I'm really happy with how it came out — I feel like I'm finally starting to get the hang of art, maybe, just as I hit five years of trying.  Again, it's wildly NSFW, but the link is on the calendar.

----

All told, I didn't _quite_ end up with 25 distinct things, but I did make some interesting stuff — some of which I'd been thinking about for a long time — and I'll call that a success.

I'd love to get flathack to the point that it's worth playing repeatedly, make more crosswords, and finish PICOtracker — but those will have to wait, since my [GAMES MADE QUICK??? FOUR](https://itch.io/jam/games-made-quick-four) jam is coming up in a few days!

And speaking of which, I need to put a bunch of this stuff on [Itch](https://itch.io/jam/games-made-quick-four)!
