title: On principle
date: 2012-03-24 20:44
category: blog
tags: culture, tech

Alice shows some code to Bob.  Something about it catches Bob's eye; he tells her that some mechanism is a bad idea and she should find another approach.  She asks _why_.

Bob, despite being absolutely correct, can't answer.

Or maybe he can, but is worse off nonetheless: for every pitfall or potential consequence he dreams up, Alice fires back with how she'll compensate or why it doesn't apply in this case.  Eventually Bob runs out of ideas, and Alice carries on with what she's doing, now feeling _more_ vindicated—she's fought for her work and won, after all.

Bob is arguing from principle, and Alice is scoffing at the idea of principle for its own sake.  Principles are for academics; out here in the real world, whatever gets the job done is good enough.

Right?

<!-- more -->

## `eval`

It seems everyone who gets into Python, at some point or another, decides to write an IRC bot.  One of the simplest capabilities to give such a bot is that of a calculator: feed it an arithmetic expression and get an answer.

Ah, but Python already knows how to do that, right?  So let's just use our old buddy `eval`, which executes a string as though it were code.

```python
def calculate(string):
    return eval(string)
```

Now someone can type `!calc 2+3` and the bot will respond with `5`.  _Ah, but wait,_ thinks our clever developer.  _This is why `eval` is bad: now someone can run any Python code they want!  I'd better fix this._

Off he goes to Google, where he looks for something like `python safe eval`, and he finds something like [this page][safe eval] (the first result I got, in fact).  It turns out you can tell the `eval()` function precisely what variables the given string should have access to.  So if you rewrite the function like this:

```python
def calculate(string):
    return eval(string, globals={'__builtins__': None}, locals={})
```

then the string can't use any variables at all, not even the built-in Python functions.  And `eval` refuses to execute statements, like `if` blocks or `import`s.  The bot is now safe, right?

Right?

### Wrong

Let's say the bot's developer comes into a technical IRC channel and asks for help with some tangential problem.  Along the way he lets slip that his bot uses `eval` to implement a calculator.  (Honestly, just saying his bot has a calculator is enough to make me suspicious now.  Writing a calculator from _scratch_ is a bit more involved and not the sort of thing you'd want to throw in as a simple command.)

"You shouldn't use `eval`," someone tells him.  "It's, y'know, bad."

"Aha!" proclaims the developer, having seen this coming.  He's thought of everything!  He knows `eval` is bad for a reason, and he's fixed that reason.  "I spent ten seconds on Google and blindly copied the first thing I read, so it's not an issue."

"You still shouldn't use it," another chimes in.  "It causes problems."

The developer scoffs aloud to himself.  "Like what?"  Perhaps he even brings the bot in, as if to dare anyone to try to take it down.  An uncomfortable silence descends upon the conversation.

Until an enterprising individual asks the bot to calculate the following:

```python
[t for t in (1).__class__.__bases__[-1].__subclasses__() if t.__name__ == 'file'][0]('/etc/passwd').read()
```

This code contains no statements.  It also contains no references to any external variables, not even any built-in functions.  The bot has no trouble `eval`ing it.

A critical and secret file from the developer's system is dutifully printed into the channel.  Both bot and owner quietly disconnect.

### The Problem

`eval` is a bad idea.

The problem, then, is that some people don't _believe_ this.  They've heard it, and they may even know it, but they don't truly feel it down to their bones.  When _I_ see `eval`, a dark cloud descends upon the surrounding code, and I eye the whole mess with suspicion and mistrust until I'm satisfied that its use is justified.

You see, I don't claim that `eval` is a bad idea for academic or even merely principled reasons.

`eval` is a bad idea because _nearly every time I have seen it used, it has caused unforeseen and unnecessary problems_.

The important bits are "unforeseen" and "unnecessary".  Unforeseen because `eval` has a _huge pile_ of caveats associated with it, a list that I can't even recall in its entirety without some thought.  Unnecessary because the alternatives to `eval` tend not to require much more work to implement, whereas the problems caused by `eval` are subtle and nefarious.

This isn't a mere philosophical dogma.  It's closer to a PTSD trigger, a thing that brings back vague haunting memories I don't really want to claw through but that left hard-earned lessons I urgently want to pass on to others.  (With apologies to those who have _actual_ triggers, which are rather more severe than this programming nonsense.)

But I can't pass it on to a certain type of developer, who sees all tools as equally viable and merely grabs the nearest one that can get the job done.  Frustrating.

Not to say that `eval` should _never_ be used, either.  Python's third-party `decorator` module, for example, is a great piece of software that hinges crucially on `eval`.  The difference is that the very problem `decorator` wishes to solve—making decorators that preserve the argspec of the original function—is _impossible_ due to limitations of Python itself.  And so it uses `eval` with great care, only on strings it constructs itself, in a small and confined place.  It tells me _I know `eval` is unfortunate, and I don't like this either, but there was no other way._

That's the real difference.  I'm left capable of believing that the author still agrees with me, because he's made his case that there was _no other way_ to do what he needed to do.  The `decorator` library would simply not exist if it weren't for `eval`.  Contrast this with the numerous IRC bot authors who don't defend their own code against a rule they agree with, but instead dispute the rule itself, feeling the need to upend commonly-accepted wisdom to feel justified in what they've done.

## Diversion

I'm reminded, of all things, of the abortion debate.  The common perception amongst the pro-life crowd is that anyone identifying as pro-choice _hates_ life, or is otherwise "anti-life".

Strangely, few in the pro-choice movement ever clarify that this is not the case.  I don't believe anyone really _supports_ abortion.  Every abortion is unfortunate.  The point is to support the _right_ to have an abortion, because sometimes there is _no other way_, and women should have the power to look themselves in the eye and say "I know this is a shame, but it _has to be this way_."

I feel similarly about neutering domesticated cats and dogs.  For all the arguments about potential health benefits for the animals and numbers of kittens in shelters, it really comes down to something much simpler: intact pets are inconvenient.  Massively so.  I can't deal with my house being scent-marked.  I can't deal with a sudden influx of kittens, whether born inside my house or out.  I'm just not willing to devote the necessary resources to handling the consequences of an adult, territorial, sexually-active animal.  And I have no way to explain this to my kitten, to either ask him to not do those things or ask him to make the choice himself or even ask his forgiveness; I can't communicate these ideas, and he lacks the faculties—lacks any _need_—to understand them.  Why would I care for trinkets over warding competitors away from the area I own?

But I am responsible for him, and he trusts me, so I'm going to do it anyway.  I feel guilty doing it, and I wish I had any other solution, but next week I'm having an inconvenient part of my pet removed because there's just _no other way_.

I rarely encounter anyone else who phrases things in such a way.  Most of us are either _for_ something or _against_ it.  Nobody wants to feel reluctant, I guess.  Perhaps part of a [culture that encourages certainty, victory][blog: american culture].

Back to programming, then.

## Why

I value my collection of principles (programming and otherwise).  They don't inspire that laundry list of consequences at the back of my mind; rather they match a sense of what is _right_.  Not right in a moral sense, but right in the intangible architectural sense of correctness and optimality, in the way that a hammer is the _right_ tool for a nail even though you could just as well whack it with the butt end of a screwdriver.

Some of them are more flexible than others; some of them aren't very important but resonate strongly anyway; some aren't even very well-defined.  It doesn't matter.  I stick to them because (and here I pause to wrap my mind around the thought I've just had) a craftsman is defined by his ability to tell bad from good, good from better.  If I had no basis on which to do that, I would be a poor craftsman indeed.  And if I didn't believe such an ability is important or even worth attempting to develop, I'd be a disgrace to the very act of creating.

`eval` is bad because it introduces a lot of subtle security and translation issues, it defeats bytecode caching, it hides syntax and other errors until runtime, it causes action at a distance that's hard to follow, it defeats syntax highlighting.  It just makes your code _worse_.

Plenty of similar "rules" have numerous subtle consequences.  Creating a Web site that requires JavaScript isn't just a problem because 0.1% of the population is using elinks.  It hinders search engines, it breaks history and bookmarks, it breaks tabbed browsing, it prevents users from sharing links, it confuses accessibility technology, it introduces strange UI problems while your JS loads, it makes writing third-party scrapers and tests and other tools far more difficult, it makes your site unfriendly and useless if your JS happens to break, it eats more RAM on visitors' machines, it increases the time people have to wait before seeing anything useful, it drives away the growing handful of people running NoScript for security or annoyance reasons, it breaks your site for millions of people if you happen to miss a browser-specific bug in an ill-specified language that runs on at least four different implementations.  It just makes your site _worse_.

And just like `eval`, sometimes there's _no other way_: Google Docs, for example, couldn't exist in any usable form without JavaScript.  But GMail and Google Maps _could_, and they _do_, and the results are that the massive bulk of GMail can fall back to something on old machines and Google Maps has a much less resource-hungry static map API.  The results are _better_.

You can scoff at that 0.1% of people using elinks, and build your site that requires JavaScript just to click links or see text.  You can run into each of these problems and wonder whether to ignore it or stop everything to fix it.  Or you can put in slightly more effort up-front.  I've found that, surprisingly, forcing everything I make to work without JavaScript also forces me to remember to validate forms server-side, forces me to include information in the page and fetch it with JS rather than trying to hokily generate JS code, forces me to think about my UI as a whole instead of focusing on how to cram a particular step into a modal dialog.  Following the principle for its own sake, rather than arguing with the particulars that led me to value it in the first place, rather than looking for any excuse to just do it the easy hacky way "this time", ends up making my code _better_.  And that's not something I know how to easily impart on anyone else.

Separate style from content.  Make different things look different.  Don't run stuff as root.  Use good passwords.  Keep localization in mind from the start.  Use version control.  Write tests.  Make functions only do one thing at a time.  Smile.  Be creative.  Live longer.

And if you haven't filled your quota of nerd ire today, [read this blog post][rofl] and all the comments by Bryan S. Katz.  It makes for a good, er, alternative perspective to what I've written here.


[blog: american culture]: /blog/2011/06/27/something-is-wrong-with-american-culture/
[rofl]: http://perlhacks.com/2012/03/you-must-hate-version-control-systems/
[safe eval]: http://lybniz2.sourceforge.net/safeeval.html
