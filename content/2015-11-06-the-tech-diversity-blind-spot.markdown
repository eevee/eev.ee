title: The tech diversity blind spot
date: 2015-11-06 07:41
category: blog
tags: tech, culture

The only black engineer in a management role at Twitter [recently quit](https://medium.com/tech-diversity-files/thought-on-diversity-part-2-why-diversity-is-difficult-3dfd552fa1f7).

The top-voted comment about this story on Hacker News begins thusly (emphasis mine):

> I've been working for over 20 years in tech at 10+ different companies around the Valley, and I can count on 1 hand the number of direct coworkers that were black, and on 2 hands the number of coworkers that I indirectly worked with that were black.
>
> I don't believe this is due to any sort of racism, but rather due to the education system in general. Trying to solve the diversity issue at the hiring end, when the number of qualified candidates is so small, is not the right way to solve the problem. **The only way you will hit higher-than-normal diversity numbers is to reduce hiring standards, which is wrong.**

This is an interesting thing to say (and upvote) when the article itself said the exact opposite:

> In the course of the meeting, [the VP of Engineering] suggests that we begin tracking the ethnicity of potential candidates in the pipeline to understand better where candidates are falling out. I agreed that this is an important metric to track and conveyed that the current data we had indicated that the problem is not just the pipeline. While ethnic and gender data early in the pipeline is incomplete, we do know that in 2013, 4.5% of CS graduates from the top 25 schools were African-American, and 6.5% were Hispanic/Latino.

A chart in the article indicates that in 2014, Twitter's tech employee population was 1% black and 3% Hispanic.

<!-- more -->

----

Eric S. Raymond (who, according to himself, is an important tech figure) blogged a few days ago about a _terrifying feminist conspiracy_.  The Ada Initiative was allegedly plotting to get prominent men in tech alone with women, so the women could later make false claims about being assaulted, thus generating outrage, which would...  serve...  some kind of purpose.  This story comes from the most reliable of sources: an anonymized person on IRC.  Oh, and they've tried this multiple times with Linus Torvalds.

This is pretty clearly nonsense.  The usual suspects have eaten it up, of course, but that's to be expected.  Far more embarrassing is to see someone in tech of some inexplicable influence buy it and propagate it as fact.

Watch how easy this is to rebut: show me someone accusing Linus of sexual assault.

Oh.

----

There's a blind spot amongst tech people.  I think I understand it, because I remember a time when I had it as well.

It relies on a bit of speculation about how tech people think.  That's always a risky affair, since I can't _really_ claim to know what's going on inside someone else's head, let alone inside a whole group's.  But bear with me while I speculate a bit.

Tech people, almost by definition, believe in rules and rigor and measurements.  Computers are very stupid machines, after all: they do precisely what they're told to do, and no more.  It's hard to be a programmer without putting yourself into that kind of highly literal mindset.

If there's a bug in your code, you can binary search your function to find where it happens.  If your code is slow, you can profile it.  We're getting increasingly invasive about collecting any data we can think to collect, just so we can make lots of cool graphs that someday might even be useful.

Programming is about making everything obvious and quantifiable.

There are plenty of tech memes (in the straightforward "unit of culture" sense) that demonstrate this.  UI designed by programmers is usually clumsy nonsense laid out in a grid — because UI is more an artform, something you can't just measure or write unit tests for.  "Real" programming is done in C, not this high-level dynamically-typed nonsense — because a higher-level VM makes it harder to see and measure what the hardware is doing.  We're pretty sure you can't measure programmer productivity in net lines of code written — but the impulse to do so persists, because we want to measure it _somehow_.

----

If this is how you see the world, it's easy to think that skill, too, should be quantifiable.  We want to believe that whatever mechanism our company uses will rank candidates in order of Objective Programming Talent, and then we'll hire whoever's at the top of the list.

This, too, has some cultural evidence: consider how many tech shops still use whiteboarding to evaluate a candidate's ability to actually write code.  Even though whiteboard problems have no relation to 95% of the work you actually do.  Even though no one actually writes real code on a whiteboard.  Even though tech people seem to have a tendency to get anxious when put on the spot by a complete stranger.  Even though it doesn't at all test architecture or the ability to work on a team or the ability to adapt to changing requirements, which are all far more important than being able to come up with cutesy useless algorithms on the spot.

None of that matters, because it measures _something_, and we like measurements.  Measurements are concrete and reliable.

Right?

Oops.

----

There's a blog post I absolutely adore called [Page Weight Matters](http://blog.chriszacharias.com/page-weight-matters).  Here's the quick version: a YouTube developer experimented with getting the video page down from 1.2MB (!) to under 100KB.  They served the new lighter page to a fraction of all traffic.  Shockingly, the average page load time _increased_, even though the page was many times smaller and had many fewer requests!

It turns out that the old page had been _so_ big that some people in South America, Africa, and other places with not-too-great Internet speeds just weren't using YouTube at all, because that megabyte of crap took _twenty minutes_ to load.  The new leaner page loaded in only two minutes (!), so they could actually use the site — at the "cost" of increasing the average load time.

The author of the article thus concludes that page load times are important.  Which is a shame, because there's a much more important lesson in there that deserves to be triply-underlined.

**We [_suck_](http://zedshaw.com/archive/programmers-need-to-learn-statistics-or-i-will-kill-them-all/) at measuring.**

_Even if_ you're very very careful about assigning people to cohorts evenly and randomly, and you're sure you're measuring the right variable, and you only measure one thing at a time, and whatever else...  you can't adjust for problems like users _self-selecting_ themselves out of your website entirely.

Consider: what if those low-bandwidth users hadn't had as much of an impact?  What if they'd bumped up the average load time for the new page, but not so much that it exceeded the average load time of the old page?  The developer would've said "oh, it's 10% faster, nice", and that would be that.  No one would have ever realized the true impact of the change.  It wasn't the graph that revealed the insight — it was the fact that _the graph seemed to be wrong_ that led humans to dig deeper and discover the insight.

But we trust the graphs.  There's nothing in that story about how they updated the graphs to catch this kind of change in the future, and I'm willing to bet it didn't even occur to anyone.

----

I hope by now you accept my premise: tech people want everything to be sensible and measurable, and will assume this is the case even in the face of moderate evidence otherwise.  If not, I hope you'll suspend your disbelief for a few more minutes.

Now, pretend you're a white dude in tech.  (Or, if appropriate, just be a white dude in tech.)  You hear the occasional gripe that the subculture you love fiercely is _sexist_ and _racist_.  That people of color get turned down for no good reason.  That women get harassed at tech gatherings, or just proactively avoid them.

But _you've_ never seen this happen.  You know and trust the people doing the recruiting (maybe you're one of them!), and you know no one has ever turned someone down just for their race.  You've been to loads of tech conferences, and you've never seen any uncomfortable women.  You even know a woman, and she says everything is fine.  There are no _real_ studies about this, just a few people complaining.

There's a contradiction here.  This isn't about difference of opinion; this is about _reality_, which is concrete.  Someone has to be wrong.  Or in other words, there are only two possibilities:

1. Hiring decisions are made by the gut, not by an objective score, so [they might be influenced](http://blogs.scientificamerican.com/unofficial-prognosis/study-shows-gender-bias-in-science-is-real-heres-why-it-matters/) by [biases you don't even realize you have](http://curt-rice.com/2013/10/01/what-the-worlds-best-orchestras-can-teach-us-about-gender-discrimination/).  Race and gender and other axes actually _do_ influence how people are treated, just in little ways that are hard to notice from the outside.  But those little things build up over a [lifetime](http://www.nytimes.com/2015/02/07/upshot/how-elementary-school-teachers-biases-can-discourage-girls-from-math-and-science.html?_r=0) and become embedded in culture, which [deeply affects how we think and feel and act](http://mitadmissions.org/blogs/entry/picture-yourself-as-a-stereotypical-male).  Humans aren't fundamentally rational, you can't trust your own decisions to be objective, and the universe is catastrophically unfair.

2. For whatever reason, women and black people just aren't very good at tech stuff.

Which of these sounds [easier to believe](https://en.wikipedia.org/wiki/Cognitive_dissonance)?

If you believe that everything important can be quantified, if you believe that humans are fundamentally rational, if you believe you can be objective, if you live in a world where everything is factual and measurable and obeys clear immutable rules...

Then not only is the first choice repulsive, it may be _unthinkable_.  I might as well propose that the planet is made of waffles.  It's so ridiculous that it can't even come to mind as a serious possibility.

Which only leaves one explanation for the current state of affairs.

From there, a lot of other conclusions make an eerie kind of sense.  If people who aren't white and male just innately aren't good at computers, then _obviously_ hiring such people requires lowering our hiring standards, and _obviously_ anyone asking for diversity must have some ulterior motive, and _obviously_ organizations pushing for more women in tech are up to something, and so on.

Obviously.

----

I'm reminded of another article I really adore, by Graydon (of Rust fame), which [explores conservatism vs liberalism](http://graydon2.dreamwidth.org/193575.html) in a brilliant way I've never seen before.  It's definitely worth a read, but for me the climax is this explanation of reasoning:

> 1. I have many rewards in life, and this is probably due to my own merit and hard work.
> 2. But if someone else works hard and doesn't seem to be rewarded, there _has to be some reason_.
> 3. So I'm probably just inherently better, I can't help it if I wind up doing better.

Same sort of error, along a slightly different axis.  The world _must be_ this way; I see a contradiction; the only plausible explanation is that other people inherently suck, which isn't my problem.

----

I don't have any clever proposal for how to combat this problem, assuming I'm even right.

Rather, I think there's a mistake _all_ of us make: to write off the people we severely disagree with as idiots, or bigots, or crazy, or whathaveyou.

Which is really just cognitive dissonance all over again — we don't like the idea that another rational(ish) human being could see the same world and draw conclusions that are so _wrong_, so we cheerfully assume they're just incapable of thinking correctly.  (As if any of us are capable of thinking correctly.)

I think it's important, and interesting, to consider why people might believe what they do.  Especially people who believe the complete opposite of you.  Even the largest disagreements can boil down to a single low-level difference in perspective.  I like to think that we'd get a little further if we sat down and worked out those low-level differences.

After all, everything operates by a set of rules, and every problem can be understood with just a little binary searching...
