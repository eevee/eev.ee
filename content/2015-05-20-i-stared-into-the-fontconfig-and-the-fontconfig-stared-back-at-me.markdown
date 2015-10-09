title: I stared into the fontconfig, and the fontconfig stared back at me
date: 2015-05-20 23:02
category: blog
tags: linux, typography, tech

Wow!  My [Patreon](https://www.patreon.com/eevee) experiment has been successful enough that I'm finally obliged to write one post per month, and this is the first such post.  Let us celebrate with a post about something near and dear to everyone's heart: _fonts_.  Or rather, about fontconfig.

[fontconfig][] is a pretty impressive piece of work.  If you're on Linux, it's probably the thing that picks default fonts, handles Unicode fallback, and magically notices when new fonts are installed without having to restart anything.  It's invisible and great.

And unfortunately once in a great while it's _wrong_.  There is no common GUI for configuring fontconfig, so you're stuck manually editing XML configuration files — for which [the documentation][fontconfig docs] is atrocious.

Lucky for you, and unlucky for me, I have _twice_ now had to delve down this rabbit hole.  Here is my story, that others may be saved from this madness.

<!-- more -->


## Trial the First: Monospace font falling back to proportional Unicode glyph

As I [explained](https://twitter.com/eevee/status/477954452226203648) almost a year ago, while live-tweeting my exploration of this problem:

> i typed "☺foo" and then took a screenshot.  i stress that my cursor is /actually/ positioned AFTER the second "o".
>
> ![](https://pbs.twimg.com/media/BqIJCmwCQAAdmJp.png)

Now, there's definitely a [Konsole bug](https://bugs.kde.org/show_bug.cgi?id=297390) here — terminal text should _never_ be allowed to escape the grid, and the cursor should absolutely not get out of sync with the text.

But this got me wondering.  I know for a _fact_ that I have a monospace font somewhere that contains the ☺ glyph.  I've seen it fit perfectly well in a terminal before.  So why is Konsole falling back to a proportional font?

The monospace font I was using at the time was [Source Code Pro](https://github.com/adobe-fonts/source-code-pro), a relative newcomer.  Could that have been related?  (Hint: _yes_.)

Here's a further hint.  If you use `fc-match -s <font>`, you get a sorted list of the fonts fontconfig will use for fallback.  Let's try it with Source Code Pro:

    ⚘ fc-match -s 'Source Code Pro'
    SourceCodePro-Regular.otf: "Source Code Pro" "Regular"
    PowerlineSymbols.otf: "PowerlineSymbols" "Medium"
    SourceSansPro-Regular.otf: "Source Sans Pro" "Regular"
    SourceHanSansJP-Normal.otf: "Source Han Sans JP" "Normal"
    DejaVuSans.ttf: "DejaVu Sans" "Book"
    DejaVuSans.ttf: "DejaVu Sans" "Book"
    DejaVuSansExtraLight.ttf: "DejaVu Sans" "ExtraLight"
    DejaVuSans-Bold.ttf: "DejaVu Sans" "Bold"
    ...

Something is distinctly wrong with this list.

I'll just jump to the payoff: unless it's told otherwise, _fontconfig assumes every font is sans-serif_.

It turns out there's nothing inherent to a particular font that makes it serif, sans-serif, monospace, cursive, or whathaveyou.  These are purely human categorizations.  _Manual_ human categorizations.  fontconfig actually ships with configuration files that assign generic family names to a hardcoded and ultimately arbitrary set of fonts.  Here's part of my `/etc/fonts/conf.d/45-latin.conf`:

    :::xml
    <fontconfig>
    <!--
    Mark common families with their generics so we'll get
    something reasonable
    -->

    <!--
    Serif faces
    -->
        <alias>
            <family>Bitstream Vera Serif</family>
            <default><family>serif</family></default>
        </alias>
        <alias>
            <family>DejaVu Serif</family>
            <default><family>serif</family></default>
        </alias>
        <alias>
            <family>Liberation Serif</family>
            <default><family>serif</family></default>
        </alias>
        <alias>
            <family>Times New Roman</family>
            <default><family>serif</family></default>
        </alias>
        ...

And `/etc/fonts/conf.d/49-sansserif.conf` contains the fallback for fonts not yet assigned a generic family:

    :::xml
    <fontconfig>
    <!--
    If the font still has no generic name, add sans-serif
    -->
        <match target="pattern">
            <test qual="all" name="family" compare="not_eq">
                <string>sans-serif</string>
            </test>
            <test qual="all" name="family" compare="not_eq">
                <string>serif</string>
            </test>
            <test qual="all" name="family" compare="not_eq">
                <string>monospace</string>
            </test>
            <edit name="family" mode="append_last">
                <string>sans-serif</string>
            </edit>
        </match>
    </fontconfig>

This is preposterous.  This is _unthinkable_.  And yet what might be even more incredible is that I'd never noticed before, because covering the most popular fonts _works well enough_.

Computers, right?

Anyway, so, all I have to do then is tell fontconfig that Source Code Pro is actually a monospace font.  I stuck this in my `~/.config/fontconfig/fonts.conf`:

    :::xml
    <alias>
        <family>Source Code Pro</family>
        <default>
            <family>monospace</family>
        </default>
    </alias>

I ran `fc-cache` and...  absolutely nothing was different.

Skipping past my pain and suffering again: it turns out that there's not actually anything special about the generic family names, and so fontconfig doesn't bat an eye if you give _two_ generic families to the same font.  User configuration applies just after that sans-serif fallback, so this naïve approach ended up with Source Code Pro falling back to _both_ sans-serif and monospace.

The solution, thankfully, is fairly simple:

    :::xml
    <!-- by default fontconfig assumes any unrecognized font is sans-serif, so -->
    <!-- the fonts above now have /both/ families.  fix this. -->
    <!-- note that "delete" applies to the first match -->
    <match>
        <test compare="eq" name="family">
            <string>sans-serif</string>
        </test>
        <test compare="eq" name="family">
            <string>monospace</string>
        </test>
        <edit mode="delete" name="family"/>
    </match>

fontconfig's XML-powered expression engine is a little weird, but this does pretty much what it looks like: if a font claims to be in both the sans-serif and monospace families, delete the sans-serif family.

With that, my ☺ rendering was fixed, and `fc-match` gave much more sensible output:

    SourceCodePro-Regular.otf: "Source Code Pro" "Regular"
    PowerlineSymbols.otf: "PowerlineSymbols" "Medium"
    SourceSansPro-Regular.otf: "Source Sans Pro" "Regular"
    SourceHanSansJP-Normal.otf: "Source Han Sans JP" "Normal"
    DejaVuSansMono.ttf: "DejaVu Sans Mono" "Book"
    DejaVuMonoSans.ttf: "DejaVu Sans Mono" "Book"
    DejaVuSansMono-Bold.ttf: "DejaVu Sans Mono" "Bold"
    ...

There's also a simpler solution here, which has only occurred to me now.  Like I said, Source Code Pro was my default monospace font, done with this simple incantation:

    :::xml
    <alias>
        <family>monospace</family>
        <prefer>
            <family>Source Code Pro</family>
        </prefer>
    </alias>

So I _could_ just...  only ever refer to it as "monospace" in applications.  Then when a glyph is missing, fontconfig would look for a fallback for monospace (the actual font I claim to want) rather than Source Code Pro (the first fallback fontconfig already selected).  Alas, at the time, my terminal was using Source Code Pro directly, and I never realized this might be a problem.

The above way is a wee bit more robust, though.


## Trial the Second: Kill Comic Sans

Between the fonts I happen to have installed and fontconfig's built-in defaults, my default "cursive" font ends up being...  Comic Sans.  I don't see it too often, but it tends to crop up if, say, a website tries to use some curly Windows-only font with only "cursive" as the fallback.

Enter [Comic Neue](http://comicneue.com/), a moderately successful attempt at bringing some respectability to Comic Sans.  Okay, neat.  I'll just set that as my default cursive font, then.

    :::xml
    <alias>
        <family>cursive</family>
        <prefer>
            <family>Comic Neue</family>
        </prefer>
    </alias>

And now cursive text is displaying in...  Comic Sans.

Hm.  Well.  That's interesting.

After _six hours_ of investigating this on and off, I finally discovered the problem.  Are you ready for this?  It's great.

Comic Neue doesn't have glyphs for caret or backtick.

Thus, fontconfig decided it didn't have a full set of English glyphs, and so wasn't appropriate to use for English text.

No, really.

Here's my grotesque solution:

    :::xml
    <!-- comic neue is missing a few glyphs and fontconfig thinks it's -->
    <!-- unsuitable for english text, oops!  fix this forcibly. -->
    <!-- once the font is fixed, the above rule is good enough -->
    <match>
        <test compare="contains" name="lang">
            <string>en</string>
        </test>
        <test name="family">
            <string>cursive</string>
        </test>
        <edit mode="delete_all" name="lang"/>
        <edit mode="prepend" name="family">
            <string>Comic Neue</string>
        </edit>
    </match>

i.e.: if we're looking for a font called "cursive" for English text, just drop the language requirement, and put Comic Neue at the beginning of the list.  Hacky, but it does work.

You may also want to do the same dance as with Source Code Pro: make Comic Neue fall back to other cursive fonts, then remove the extra sans-serif family.

As an aside: I distinctly remember testing this in Firefox, but now it doesn't work at all.  I don't know if I'm direly misremembering or was hallucinating or what, but there is a _fifteen year old_ [bug](https://bugzilla.mozilla.org/show_bug.cgi?id=47752) complaining that Firefox on Linux _doesn't specify cursive/fantasy CSS fonts at all_.  So they fall back to...  I don't know, something totally arbitrary?  Anyway I fixed _that_ by cracking open `about:config` and adding a `font.name.cursive.x-western` pref with a value of `cursive`.  Yes, apparently, Firefox doesn't even use fontconfig's cursive for CSS cursive out of the box.  But I swear it did a year ago when I was doing this.  I think.

I'm starting to doubt my perceptions of reality here.  That's how intense font configuration is.

But one more thing before we move on — let's really go out on a limb here, and ensure we _never see Comic Sans again_.  If anyone tries to use it _explicitly_, substitute Comic Neue instead!  But make it bold by default, since Comic Neue's regular weight is way lighter than Comic Sans.

    :::xml
    <!-- Replace Comic Sans with Comic Neue bold -->
    <match>
        <test name="family">
            <string>Comic Sans MS</string>
        </test>
        <edit binding="same" mode="assign" name="family">
            <string>Comic Neue</string>
        </edit>
        <edit binding="weak" mode="assign" name="style">
            <string>Bold</string>
        </edit>
    </match>

I thought using a "weak" binding here would mean that someone could explicitly ask for "light" Comic Sans and get light Comic Neue, but that doesn't seem to be working now that I'm actually trying it.  But fucking whatever, right?  It's Comic Sans, who cares.


## Trial the Third: Japanese fonts are junk for some reason

I was celebrating the addition of ruby (furigana) support to Firefox, and went to go show someone that the prior version did not in fact support it very well.  But then I noticed something else curious.  Compare these screenshots of the same page, in Firefox (left) versus Chrome (right):

![](https://pbs.twimg.com/media/CE1fCcBUgAAnI0j.png)
![](https://pbs.twimg.com/media/CE1fCb3UgAA9SQc.png)

Firefox's choice of font looks like total ass!  I wonder why.

Okay so it's because the surrounding font was a serif font, so naturally the CSS fallback was "serif", so Firefox was asking fontconfig for a serif Japanese font.  Lo and behold, in fontconfig's configuration spaghetti, I found `/etc/fonts/conf.d/65-nonlatin.conf`:

    ::xml
    <fontconfig>
        <alias>
            <family>serif</family>
            <prefer>
                ...
                <family>MS Mincho</family> <!-- han (ja) -->
                <family>SimSun</family> <!-- han (zh-cn,zh-tw) -->
                <family>PMingLiu</family> <!-- han (zh-tw) -->
                ...

The _first_ Japanese serif font that fontconfig prefers is MS Mincho, which I happen to have installed (it's in the Microsoft core fonts package, which we'll get back to shortly).  Firefox dev tools confirmed that this was the ugly font being used.

I did find a [bug on fontconfig](https://bugs.freedesktop.org/show_bug.cgi?id=20911) objecting to this ordering for a variety of reasons, but that doesn't help me too much.

Anyway, I went hunting for some really nice Japanese fonts, and I found two: [IPAMincho][] for serif, [Source Han Sans JP][] for sans-serif.  It was easy enough to force them to be preferred; I just stuck them below my preferred Western fonts.

    :::xml
    <alias>
        <family>serif</family>
        <prefer>
            <family>Source Serif Pro</family>
            <family>IPAMincho</family>
        </prefer>
    </alias>
    <alias>
        <family>sans-serif</family>
        <prefer>
            <family>Source Sans Pro</family>
            <family>Source Han Sans JP</family>
        </prefer>
    </alias>

Result:

![](https://pbs.twimg.com/media/CE1xg8BVAAAt6jM.png)

Gorgeous.


## Trial the Fourth: Fuck Helvetica

In the process of installing Source Han Sans, at one point I accidentally put it _first_, causing even Roman text to be rendered by that ostensibly Japanese font.

But it actually looked, uh, really nice.  _Really_ nice.  Like, I was blown away by how gorgeous some Python documentation (which used my default sans-serif font) [suddenly looked](https://pbs.twimg.com/media/CE2Ai9FUsAEXmgb.png:orig).  Wow!  Way nicer than I expected from some fallback glyphs in a Japanese font.  I looked into this and it turned out that the glyphs had been ported pretty directly from Adobe's Western font, Source Sans Pro.  I was already using Source Code Pro, so at this point I was strongly considering just drinking [all of Adobe's font Kool-Aid](https://github.com/adobe-fonts).  (The configuration above is from _after_ I did this.)

At this point I was suddenly struck by how _not_ gorgeous the Twitter web interface looked in comparison.  I had a peek, and the entire thing was, and always had been...

rendering...

in...

_Arial_.

This was caused by the perfect storm of font shenanigans.

1. I didn't have Helvetica installed, because this isn't a fucking Mac.
2. I _did_ have the Microsoft core fonts installed.  I want to say this is because Steam under Wine would either crash or just not render any text whatsoever if it couldn't find some particular Windows font.
3. fontconfig ships a `30-metric-aliases.conf` file that supplies some font fallback rules for fonts with very similar glyph shapes, such as...  having Helvetica fall back to Arial.  (Arial was deliberately designed to fill this role, because font licensing.)

Well, fuck your Helvetica, and _doublefuck_ your Arial.  I installed Source Sans Pro and Source Serif Pro, and set about fixing this posthaste.

    :::xml
    <!-- fuck helvetica -->
    <match>
        <test name="family">
            <string>Helvetica</string>
        </test>
        <edit binding="same" mode="assign" name="family">
            <string>Source Sans Pro</string>
        </edit>
    </match>

Here is Twitter Web, before and after.

![](https://pbs.twimg.com/media/CE2ITKVUIAA4XG-.png)
![](https://pbs.twimg.com/media/CE2ITJKVAAAcYa_.png)

_DAMN._


## Some hot parting tips

`fc-cache` will force fontconfig to pick up any changes.  There's a `-f`, but in all my fighting with fontconfig it never once made a difference.

As far as I can tell, there is no reason to _ever_ run `sudo fc-cache -vf`.  This has been floating around the Internet for years, but it seems to be apocryphal copy/paste.  You don't need to flush _root_'s fontconfig cache unless you're running GUI stuff _as root_.

`fc-match <font>` will tell you what font will be used in practice.  You might think that's what `fc-query` does, and you'd be wrong.  `fc-query`'s primary use is to produce bizarre error messages when you accidentally use it instead of `fc-match`.

It is _really fucking difficult_ to figure out what font will be used _for a specific glyph_.  There are two approaches:

1. Do it in a browser.  Make a URL like this:

        data:text/html,<meta charset="utf8"><p style="font-family: monospace;">☺</p>

    Then pop open your dev tools, and look for where it tells you the fonts that are _actually_ being used.  Firefox's Inspector has a dedicated "fonts" tab in the panel on the right; Chromium's Elements lists fonts at the bottom of the "computed" tab.

    Fair warning: this is one level removed from fontconfig, because CSS font rules may interfere.  This bit me above when I tried to confirm my new cursive font in Firefox!

    Another warning: while Firefox picks up fontconfig changes more or less instantly (after an `fc-cache`), Chromium _does not_.  Worse, Chromium seems to outright ignore fontconfig when it feels like it, such as when it used a sans serif Japanese font for text styled as serif.

2. You can also do this nonsense in a terminal:

        DISPLAY=:0 FC_DEBUG=4 pango-view --font=monospace -t ☺ | grep family:

    `pango-view` is a tiny program that just pops open a window containing some text in a particular font.  `FC_DEBUG` is an environment variable to make fontconfig spit out _mountains of fucking text_ on stdout.  The `grep` cuts it down to something a little more manageable.  Most likely the last family you see listed is the font actually being used to render your favorite glyph.

If you're _really_ curious how the `<match>` blocks work, good news: they are the one thing the [fontconfig docs][] actually kind of explain.  And of course your `/etc/fonts/conf.d` is probably full of real-world practical examples.

----

I haven't put my fontconfig font config (...) in my [rc.git](https://github.com/eevee/rc/); it seems pretty specific to my desktop's particular setup.  But here's [the whole thing in a gist](https://gist.github.com/eevee/ba231c1b9b64e6ced70d), if you're interested.



[IPAMincho]: http://ipafont.ipa.go.jp/
[Source Han Sans JP]: https://github.com/adobe-fonts/source-han-sans
[fontconfig]: http://www.freedesktop.org/wiki/Software/fontconfig/
[fontconfig docs]: http://www.freedesktop.org/software/fontconfig/fontconfig-user.html
