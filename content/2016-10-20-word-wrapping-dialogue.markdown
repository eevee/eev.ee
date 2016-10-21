title: Word-wrapping dialogue
date: 2016-10-20 22:50
category: blog
tags: tech, gamedev

I have a teeny tiny pet peeve with dialogue boxes.  Er, not _dialog_ boxes — dialogue boxes, the ones in video games with scrolling lines of dialogue.

<div class="prose-full-illustration">
<img src="{filename}/media/2016-10-20-dialogue/dialogue-bad.gif" alt="A fake dialogue box, with scrolling text that jumps when it wraps">
</div>

I recently wrote a dialogue box, and I saw a game that made this mistake, so here's a post about it.

<!-- more -->


## Obvious, simple, but wrong

Here's a live example of the above animation.  (You can double-click on any of these to restart them.)

<div class="prose-full-illustration">
<iframe src="{filename}/media/2016-10-20-dialogue/dialogue-bad.html" width="600" height="200"></iframe>
</div>

And the code responsible.  I wrote this in the form of a fairly generic `update()` function, rather than in terms of `requestAnimationFrame`, to minimize the DOM-specific stuff.  All the JS in this post is vanilla DOM.

```javascript
"use strict";
var TEXT = "Demonstrating inadequate word-wrapping functionality necessitates conspicuously verbose representative scripture.";
var SPEED = 8;  // characters per second

// Number of characters currently visible
var cursor = 0;
// Elapsed time * SPEED, so every time this value increases by
// 1, one more character should be displayed
var timer = 0;
function update(dt) {
    timer += dt * SPEED;
    while (timer >= 1 && cursor < TEXT.length) {
        // Don't count spaces as characters
        if (TEXT.charAt(cursor) != " ") {
            timer -= 1;
        }

        cursor += 1;
    }

    var el = document.getElementById('target');
    el.textContent = TEXT.substr(0, cursor);

    // Stop updating once we run out of text
    if (cursor >= TEXT.length) {
        return false;
    }
}
```

If you've ever written dialogue handling code, this shouldn't be too surprising.  Multiplying `dt` (seconds) by `SPEED` (characters per second) produces a number of characters, so whenever `timer` is at least 1, another character should be displayed.  Spaces are counted as "free"; otherwise, the scrolling would seem to pause between words.

(The above code has a bug, as does most "string" manipulation code in JavaScript: it cuts astral plane characters in half, briefly displaying garbage.  Fixing this is left as an exercise.)

The problem, of course, is that the resulting text looks like this on successive frames, where the `|`s mark the edges of the box:

1. `|Demonstrating inadequate word-wra |`
2. `|Demonstrating inadequate word-wrap|`
3. `|Demonstrating inadequate          |`  
    `|word-wrapp                        |`

And so on.  The renderer has no way of knowing that "word-wrap" is only part of a longer word, so it merrily puts everything on one line.  The player then sees half a word abruptly jump to a new line, and judges you harshly for it.

Depending on your environment, you can solve this one of two ways, or not-solve it a third way.


## Render everything, but only draw some of it

This works well in browser-based games, where you have a comically powerful text rendering engine at your fingertips.  In graphics-oriented engines that don't offer any text rendering beyond "print this text to the screen somewhere", this approach may not be practical.

The idea is to always "draw" the entire phrase, but implement scrolling by making it partially invisible.  Consider this HTML:

```html
<span class="visible">Demonstra</span><span class="invisible">ting</span>
```

Even though the word is split across two tags, the browser must still treat it as a single word, because there's no space anywhere.  So the phrase will be word-wrapped correctly from the beginning, and the problem is solved.

You could implement this with _only_ two `<span>`s, as above, but that forces the browser to reflow the text every single frame.  It probably doesn't make a visible difference, but I prefer to wrap _each character_ in its own `<span>` and simply make them visible one at a time.  As a minor bonus, you can put whitespace in the same `<span>` as the preceding letter, and you won't have to worry about it within your update loop.

Also, if your text contains formatting — i.e., more HTML — then one `<span>` per character is _much_ simpler to deal with.  (Dealing with it is left as an exercise.)

Here it is live:

<div class="prose-full-illustration">
<iframe src="{filename}/media/2016-10-20-dialogue/dialogue-html.html" width="600" height="200"></iframe>
</div>

```javascript
"use strict";
var TEXT = "Demonstrating inadequate word-wrapping functionality necessitates conspicuously verbose representative scripture.";
var SPEED = 8;  // characters per second

// The first invisible letter <span>
var next_letter = null;

function init() {
    var el = document.getElementById('target');

    // Setup: populate the element with the entire phrase,
    // split into characters, each wrapped in a <span>
    var i = 0;
    while (i < TEXT.length) {
        var span = document.createElement('span');
        span.classList.add('js-invisible');
        span.textContent = TEXT.charAt(i);
        el.appendChild(span);
        i += 1;

        // Also include any following whitespace
        var ch;
        while ((ch = TEXT.charAt(i)) == " ") {
            span.textContent += ch;
            i += 1;
        }
    }

    next_letter = el.firstChild;
}

// Elapsed time * SPEED, so every time this value increases by
// 1, one more character should be displayed
var timer = 0;
function update(dt) {
    timer += dt * SPEED;
    while (timer >= 1) {
        timer -= 1;
        next_letter.classList.remove('js-invisible');
        next_letter = next_letter.nextSibling;

        // Stop updating once we run out of text
        if (next_letter == null) {
            return false;
        }
    }
}
```

I added an `init()` function (called from a `load` handler, not shown here) to do the setup and split the string into a series of `<span>`s.  (If you wanted to be especially clever, you could use the [`DocumentFragment`](https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment) API here, but I'm not sure it'd make a real difference.)  The main loop becomes much simpler: rather than counting characters, it can use the DOM tree API and hop from one `<span>` to the next with `.nextSibling`.  Once you hit `null`, you've run out of characters, so you're done.

The CSS is merely:

```css
.js-invisible {
    visibility: hidden;
}
```

Be sure to use `visibility: hidden;` here and **NOT** `display: none;`!  The latter tells the browser to _ignore_ the hidden characters while rendering, which defeats the whole purpose of having them.


## Hard wrap ahead of time

The other fix is to keep drawing one character at a time, but split the phrase into lines _once_ ahead of time.

**DO NOT** use your programming language's standard library to do this.  **DO NOT** just Google for code that does this.  You will get something that word wraps based on _number of characters_ without taking the _font_ into account, and the results will be wrong.

**DO NOT** fudge it by guessing the width of the "average" character.  You will hit edge cases, and they will look ridiculous.

Find something in your _graphics library_ to do this for you.  For example, LÖVE has the poorly-named [`Font:getWrap`](https://love2d.org/wiki/Font:getWrap): it takes a string of text and a width, and it returns a set of wrapped strings, one per line.

(Of course, if your font is monospace and will always be monospace, feel free to do naïve word-wrap.)

Font-aware word-wrapping is surprisingly difficult in JavaScript, even though it's sitting on top of a glorified text renderer, so in the following example I've totally fudged it.  It may not work the same way on your screen that it does on mine, which is why you shouldn't be fudging it.

<div class="prose-full-illustration">
<iframe src="{filename}/media/2016-10-20-dialogue/dialogue-love.html" width="600" height="200"></iframe>
</div>

```javascript
"use strict";
var TEXT = "Demonstrating inadequate word-wrapping functionality necessitates conspicuously verbose representative scripture.";
var SPEED = 8;  // characters per second

function init() {
    // This is hard in JavaScript, so just pretend there's
    // an API to do it for us
    //var lines = magical_word_wrap_api(TEXT);
    var lines = [
        "Demonstrating inadequate",
        "word-wrapping functionality",
        "necessitates conspicuously verbose",
        "representative scripture."
    ];
    TEXT = lines.join('\n');
}

// Number of characters currently visible
var cursor = 0;
// Elapsed time * SPEED, so every time this value increases by
// 1, one more character should be displayed
var timer = 0;
function update(dt) {
    timer += dt * SPEED;
    while (timer >= 1 && cursor < TEXT.length) {
        // Don't count spaces as characters
        if (TEXT.charAt(cursor).match(/\S/)) {
            timer -= 1;
        }

        cursor += 1;
    }

    var el = document.getElementById('target');
    el.textContent = TEXT.substr(0, cursor);

    // Stop updating once we run out of text
    if (cursor >= TEXT.length) {
        return false;
    }
}
```

This code is fairly similar to the original, since the basic idea is the same.  All I did was add the `init()` step and change the space code to also skip over newlines.

And, hm, that's all there is to it, really.


## The desperate approach

Maybe you don't have a fancy text rendering engine, _and_ you don't have any way to correctly break the text, _and_ you're dead set on using a proportional font.

At this point I would be questioning some of the decisions that had brought me to this point in my life, but you do still have one final recourse.  The classic solution, dating back decades.  Pokémon did it.  Come to think of it, Pokémon might still do it.

What you do is: manually include line breaks in your dialogue.  All of it.  Everywhere.

That is, instead of this:

```javacript
var TEXT = "Demonstrating inadequate word-wrapping functionality necessitates conspicuously verbose representative scripture.";
```

You will need to literally have this:

```javacript
var TEXT = "Demonstrating inadequate\nword-wrapping functionality\nnecessitates conspicuously verbose\nrepresentative scripture.";
```

Have fun.


## Yeah

I hope at least one person reads this and goes to fix the word-wrapping in their scrolling dialogue.  I'll have made the world a slightly better place.  🌈
