title: Maybe we could tone down the JavaScript
date: 2016-03-06 16:45
category: blog
tags: tech, web

I'm having a _really weird_ browser issue, where scripts on some pages just won't run until about 20 seconds have passed.

Whatever you're about to suggest, yes, I've thought of it, and no, it's not the problem.  I mention this not in the hope that someone will help me debug it, but because it's made me _acutely_ aware of a few...  quirks...  of frontend Web development.

(No, really, **do not** try to diagnose this problem from one sentence, I have heard and tried almost everything you could imagine.)

<!-- more -->


## Useless pages

See, here is a screenshot of a tweet, with all of the parts that _do not work without JavaScript_ highlighted in red.  I know this because I keep spending 20 seconds staring at a page that has not yet executed the bulk of its code.

<div class="illustration">
<img src="/media/2016-03-06-javascript/broken-twitter-areas.png" alt="Screenshot of a tweet, with almost everything except the tweet text and author name highlighted red">
</div>

Some of this I can understand.  The reply button, for example, focuses and expands the textbox below.  You can't do that without some scripting.  The … button opens a popup menu, which is _iffy_, since you could fake it with CSS too.  Similarly, the ♥ button does an action behind the scenes, which is _iffy_ since you could replicate it with a full page load.  But those are both non-trivial changes that would work significantly differently with script vs without.

On the other hand...

That × button at the top right, and all the empty surrounding space?  All they do is take you to my profile, which is shown in a skeletal form behind the tweet.  They could just as well be regular links, like the "previous" and "next" links on the sides.  But they're not, so they don't work without JavaScript.

That little graph button, for analytics?  All it does is load another page in a faux popup with an iframe.  It could just as well be a regular link that gets turned into a popup by script.  But it's not, so it doesn't work without JavaScript.

The text box?  Surely, that's just a text box.  But if you click in it before the JavaScript runs, the box is still awkwardly populated with "Reply to @eevee".  And when the script _does_ run, it erases anything you've typed and replaces it with "Reply to @eevee" again, except now the "@eevee" is blue instead of gray.

That happens on Twitter's search page, too, which is extra weird because there's no text in the search box!  If you start typing before scripts have finished running, they'll just erase whatever you typed.  Not even to replace it with homegrown `placeholder` text or apply custom styling.  For no apparent reason at all.

I also use NoScript, so I've seen some other bizarre decisions leak through on sites I've visited for the first time.  Blank white pages are common, of course.  For quite a while, articles on Time's site loaded perfectly fine without script, except that they wouldn't scroll — the entire page had a `overflow: hidden;` that was removed by script for reasons I can't begin to fathom.  Vox articles also load fine, except that every image is preceded by an entire screen height's worth of empty space.  Some particularly bad enterprise sites are a mess of overlapping blocks of text; I guess they gave up on CSS and implemented their layout in JavaScript.

There's no good reason for any of this.  These aren't cutting-edge interactive applications; they're pages with text on them.  We used to print those on paper, but as soon as we made the leap to computers, it became impossible to put words on a screen without executing several megabytes of custom junk?

I can almost hear the Hacker News comments now, about what a luddite I am for not thinking five paragraphs of static text need to be infested with a thousand lines of script.  Well, let me say proactively: fuck all y'all.  I think the Web is great, I think interactive dynamic stuff is great, and I think the progress we've made in the last decade is great.  I also think it's great that the Web is and always has been inherently customizable by users, and that I can use an extension that lets me decide ahead of time what an arbitrary site can run on my computer.

What's _less_ great is a team of highly-paid and highly-skilled people all using Chrome on a recent Mac Pro, developing in an office half a mile from almost every server they hit, then turning around and scoffing at people who don't have exactly the same setup.  Consider that any of the following might cause your JavaScript to not work:

* Someone is on a slow computer.
* Someone is on a slow connection.
* Someone is on a phone, i.e. a slow computer with a slow connection.
* Someone is stuck with an old browser on a computer they don't control — at work, at school, in a library, etc.
* Someone is trying to write a small program that interacts with your site, which doesn't have an API.
* Someone is trying to download a copy of your site to read while away from an Internet connection.
* Someone is Google's cache or the Internet Archive.
* Someone broke their graphical environment and is trying to figuring out how to fix it by reading your site from elinks in the Linux framebuffer.
* Someone has made a tweak to your site with a user script, and it interferes with your own code.
* Someone is using NoScript and visits your site, only to be greeted by a blank screen.  They're annoyed enough that they just leave instead of whitelisting you.
* Someone is using NoScript and whitelists you, but not one of the two dozen tracking gizmos you use.  Later, you inadvertently make your script rely on the presence of a tracker, and it mysteriously no longer works for them.
* You name a critical `.js` bundle something related to ads, and it doesn't load for the tens of millions of people using ad blockers.
* Your CDN goes down.
* Your CDN has an IPv6 address, but it doesn't actually work.  (Yes, I have seen this happen, from both billion-dollar companies and the federal government.)  Someone with IPv6 support visits, and the page loads, but the JS times out.
* Your deploy goes a little funny and the JavaScript is corrupted.
* You accidentally used a new feature that doesn't work in the second-most-recent release of a major browser.  It registers as a syntax error, and none of your script runs.
* You outright introduce a syntax error, and nobody notices until it hits production.

I'm not saying that genuine web apps like Google Maps shouldn't exist — although even Google Maps had a script-free fallback for many years, until the current WebGL version!  I'm saying that something has gone very wrong when basic features that _already work in plain HTML_ suddenly no longer work without JavaScript.  40MB of JavaScript, in fact, according to `about:memory` — that's live data, not download size.  That might not sound like a lot (for a page dedicated to showing a 140-character message?), but it's not uncommon for me to accumulate a dozen open Twitter tabs, and now I have _half a gig_ dedicated solely to, at worst, 6KB of text.


## Reinventing the square wheel

You really have to go _out of your way_ to do this.  I mean, if you want a link, you just do `<a href="somewhere">label</a>` and you are done.  If you go reinvent that with JavaScript, you need a click handler, and you need it to run at the right time so you know the link actually exists, and maybe you have to do some work to add click handlers to new faux links added by ajax.  Right?

Wrong!  That will get you a pale, shoddy imitation of a link.  Consider all these features that native links have:

- I can tab to a link.
- I can open a link in a new tab or window with some combination of ctrl, shift, and middle-clicking.
- I can copy a link's address and paste it somewhere, or open it in another browser, or whatever.
- I can use `'` in Firefox to search only for links.
- Some browsers — I want to say Opera, Konqueror, uzbl, Firefox with vimperator? — have a hotkey that shows a number or letter next to every link on the page, so you can very quickly "click" a link visually without ever touching the mouse.
- I believe screenreaders treat links specially.
- Simple crawlers rely on links to discover the rest of the site.
- Browsers are starting to experiment with prefetching prominent links, so that the next page load is instant if the user actually clicks a prefetched link.

The common thread here is that `<a href=...>` _means something_.  It says "this is a place you can go".  Tons of tools that want to know what places you can go rely on that information.  If you replace it with a `<div onclick>`, then yes, clicking on the div will do something, but all the _meaning_ has been completely lost.  Conversely, if you use `<a href="javascript:void(0);">`, then you're effectively lying to those tools; you're invoking meaning but providing meaningless information.

This is what people mean when they harp on about "semantics" — that there's useful information to be gleaned.  Figuring out what "counts" as a link when you've reinvented it yourself would require either speculatively executing a lot of arbitrary code, writing an _extremely_ clever static analyzer, or just being a trained human programmer.  Declaring your intentions is much more powerful and flexible than just doing the work, because generic tools can do useful things with the former almost trivially.

Another good example is dropdown boxes — `<select>` — which I sometimes see reimplemented entirely out of non-native widgets.  I guess to make them prettier?  A noble goal.  But did you know that in native dropdowns, you can start typing to jump to the first choice with a matching label?  Apparently most of the people who make these reimplementation didn't, and then they use them for long lists like states and countries.  The end result looks better (or, well, different) but is functionally much worse.

Twitter's custom text box is not a text box at all, but a `contenteditable` `<div>`.  At least `contenteditable` means most native controls work fairly well, but it still has some bizarre behavior at times, like moving the cursor to the start of the text when I tab away.  Or sometimes the script will have trouble keeping up with my typing for whatever reason, and <span style="letter-spacing: 0.5em;">it will visibly lag</span>.  The only reason to have this at all instead of a regular `<textarea>` seems to be to turn `@handles` and links blue?  The custom textbox doesn't truncate links or substitute Twitter's emoji font, so it's not really a preview of how your tweet will look.

You know how some sites have keyboard shortcuts?  Cute, right?  Well, `/` is actually a built-in Firefox shortcut key — it opens a quick-find bar.  Apparently nobody at Twitter or GitHub or BitBucket or Tumblr or half a dozen other places are aware of this, because they all bound it to move the focus to their whole-site search bar.  Which is completely different from searching the current page.  (To GitHub's credit, they fixed this after I complained about it on Twitter.)  For the longest time, Google+ disabled spacebar to scroll down.  How did _no one_ at these huge companies stop and say "hey, wait, this is already a thing and we're breaking it"?  Do web developers actually use web browsers?

Which reminds me: every Twitter page silently consumes all keyboard events and mouse clicks until all its script has finished running.  That means that I can't even tab away while waiting those 20 seconds for a page to load; ctrl-t, ctrl-w, ctrl-tab, ctrl-pgup, and ctrl-pgdn are all keyboard events and all swallowed indiscriminately.  The gizmo responsible is called the "swift action queue", which makes it sound like it's supposed to replay the events once the page is ready, but (a) you can't replay a browser shortcut and (b) it doesn't seem to do that anyway.  I had to write a user script to block a script tag with a specific id to fix this.  I think it's still a problem even now.

I don't think I'm complaining about anything wildly unreasonable here.  This is basic browser stuff, and you're breaking it, often for no good reason.  I don't expect you to make Google Docs work without JavaScript.  I just expect you to not break my goddamn keyboard.


## If I may offer some advice

Accept that sometimes, or for some people, your JavaScript will not work.  Put some thought into what that means.  Err on the side of basing your work on existing HTML mechanisms whenever you can.  Maybe one day a year, get your whole dev team to disable JavaScript and try using your site.  Commence weeping.

If you're going to override or reimplement something that already exists, do some research on what the existing thing does first.  You cannot possibly craft a good replacement without understanding the original.  Ask around.  Hell, just try pressing `/` before deciding to make it a shortcut.

Remember that for all the power the web affords you, the control is still ultimately in end user's hands.  The web is not a video game console; act accordingly.  Keep your stuff modular.  Design proactively around likely or common customizations.  Maybe scale it down a bit once you hit 40MB of loaded script per page.

Thanks.  ♥
