title: Fresh start
date: 2024-12-03 15:41
category: updates

I hit a point where I just didn't like this website any more.  It was too...  _stuffy_.  Posts kept getting longer, more elaborate, more time-consuming to write.  I didn't recognize the tone any more, and when I look back at older posts, those are way snarkier than they need to be.  I think I was trying to be taken seriously-but-not-too-seriously, and the voice that developed as a result was just really weird.

I kept looking at this blog and thinking...  who _is_ this?  Who wrote this?  And who is supposed to write more of this?

So I've changed _everything_.

<!-- more -->


## Design

The [previous design](https://c.eev.ee/eev.ee-2024/blog.html) was based around "keep looking like sort of like the default Octopress theme I used to have".  I don't think that was a great design philosophy, not least of all because I stopped using Octopress in 2012, and Octopress itself has been abandoned since 2015.  But it was also just...  beige.  I think I was hoping that brown-ish would be reminiscent of Eevee colors?

So I redid it from scratch, based on the _new_ design philosophy of "I like it".  And you know what?  I like it!  I hope you like it too.  But also, I don't care too much if you don't, because it's for me!

Also, hey, did you know CSS can do all kinds of crazy stuff now?  Like nesting blocks?  This blog used to use SCSS!  Now it doesn't need to!  And I barely had to change anything!  Maybe there's a post in there.

You might need a recent browser, but you should be using a recent browser anyway.


## Landing page

The [landing page](https://eev.ee/) is also completely different.  (I've preserved [the previous one](https://c.eev.ee/eev.ee-2024/), if you're interested.)

My time on Cohost, which allowed near-arbitrary inline HTML and CSS, has rekindled a joy in doing stupid tricks with CSS, and so I've glued together a mountain of stupid tricks to make something more playful and distinct.  Also I can draw better now than I could a decade ago, so I flexed those muscles a bit, too.

One thing I do slightly lament is that my games used to be above the fold (at least on my screen), and now they're not.  But I think this design actually rewards...  scrolling down?  So hopefully that helps.  Not like I'm collecting metrics or anything.


## Résumé

I've intended to do this for ages.  The old landing page contained an exhaustive list of...  _most_ things I've made or worked on, which made it kind of a cluttered mess.  Now that exhaustive list has a real home as [the landing page for c.eev.ee](https://c.eev.ee/).  I've been using this to host stuff (like [Lexy's Labyrinth](https://c.eev.ee/lexys-labyrinth/)) for ages, but the root page has been a 403 that whole time.  Now it's not!  Wow!

Also: [a list of my puzzles](https://c.eev.ee/puzzles/)!  There aren't too many yet, but maybe there will be??


## Pages

Pelican has both "articles", which are dated, and "pages", which are not.  I looked over a lot of my old posts in the course of this redesign, and a lot of them are either out of date w.r.t. technical information, about an event that was only interesting for a brief time, or just...  unmaintained?

Which all makes sense for something that has a _date_, right?  Like, Wikipedia articles don't have a date.  Those are assumed to be reasonably current.  And there's something a little sad about writing a very lengthy post with a lot of details about something, and then watching it sink into the ocean of time.  But keeping a post with "2015" in the URL up-to-date indefinitely doesn't seem quite right.

So I'm taking a crack at "pages".  I expect the presentation will change a bit as I accumulate more, but I've seeded the idea with a couple starter pages:

- Two pure-CSS toys/puzzles that were originally Cohost CSS crimes, now tidied up and with full
  explanations: [Lights Out]({filename}/pages/toys/lights-out.markdown) and [Rush Hour]({filename}/pages/toys/rush-hour.markdown).

- A lengthy list of [variant sudoku types]({filename}/pages/fyi/variant-sudoku.markdown) with full rules and examples, something that I hadn't seen anywhere else.

## I changed all the URLs sorry

At some point I put the category in the URL, so "normal" blog posts were at `/blog/foo`, whereas my [dev log posts]({category}dev) were at `/dev/foo`.  I don't know why I thought that was a good idea, and it makes it annoying to reshuffle the categories, so I've collapsed everything back into `/blog`.

There are redirects up the wazoo so this shouldn't matter to anyone.  But if you find a link to my site that 404s, I must've missed a redirect, so, please let me know.

The cool news is that instead of reverse-chrono categories, there's now a much better way to find a post you're looking for: I made a [full list of all my writing]({filename}/pages/site-index.markdown)!  Enjoy.  But don't read anything from before 2015.


## Pardon our dust

I probably forgot a lot of little things, and the layout is still a bit work-in-progress on very small screens.  I'm also not entirely sure how to convey the distinction between articles/pages at a glance, and I don't have a real name for the c.eev.ee page, so it's called something different everywhere it appears.

Feel free to send me your nitpicks; I'd like this design to be more actively maintained than the old one was.

Coming up next: Posts??  More posts??????  Remember when I wrote posts????????
