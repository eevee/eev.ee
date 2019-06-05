title: Weekly roundup: Exactly at the top
date: 2019-06-05 04:52
category: dev
tags: status

Hello!  I've been a little preoccupied with meatspace things again, but here is some digital stuff.

- **fox flux**: I have been a busy little beaver.  I consolidated 1D and 2D motion, made ground adherence more conservative about how far it tries to drop you, and totally overhauled climbing to not incredibly suck.  But who cares about any of that.

    What I _really_ did is spend like a solid week overhauling collision detection.  _Finally_, after years of wanting it, I have overlap resolution _and_ nearly zero-cost contact detection!  Which means that if objects overlap by some horrible twist of fate, instead of freely clipping through each other, they're now free to move _apart_ but not _closer together_.  It's god damn magic.  Also I now know [exactly where you're touching objects](https://twitter.com/eevee/status/1134270089547509761) which will probably come in handy for like, critters that walk back and forth on a platform without walking off it?  Or something?  I forget exactly why I wanted that but hey it's nice.

    As an added bonus, I can finally fix climbing off the top of ladders — instead of hopping off the top and then landing, you stop at _exactly_ the top, which is incredibly satisfying.

    I will almost certainly be wringing a blog post out of all this.

- **art**: I worked more on that animation and then kinda forgot about it.  Hm.  Also some doodling or whatever?

    I drew a little...  comic?  Series of panels?  I drew a _thing_ about a ground adherence bug I ran into, and also a general explanation of ground adherence.  It's [on Twitter](https://twitter.com/eevee/status/1133248372624613376), though it seems worth preserving elsewhere, once I figure out where that is.

- **gleam**: I finally made some kind of real start on an editor for the little Flora VNs I put together.  It doesn't do a lot yet, but it has some UI, which is backwards from how I usually make these things, so that's promising.

- **stream**: [Ash streamed](https://twitch.tv/glitchedpuppet) some Spyro while I commentated, and then [I streamed some Hat in Time](https://www.youtube.com/watch?v=5QcMzGPZ1Ms) while they commentated, and that was all great.

I am juggling too many things but I extremely want to get them all moving so I guess I'll get back to it!
