title: Lights Out — in pure CSS
date: 2024-10-14 07:41
tags: web

One of several CSS crimes I made for Cohost during its heyday: a version of Lights Out that functions using only CSS.  Here it is, reproduced with classes instead of inline CSS.  I've added a minor hover effect (which wasn't possible on Cohost), but otherwise, this is identical to the original, right down to the starting state of the board.

Each button toggles itself, but also the orthogonally adjacent lights.  The goal, as the name of the puzzle suggests, is to turn every light off.

<!-- more -->

<style>
.local-lights-out {
    position: relative;
    width: 80%;
    margin: 1em auto;
    overflow: hidden;  /* hides the extra bits of open lights near the edges */

    &.--buttons-demo {
        max-width: 24em;
    }

    > .-lights {
        display: grid;
        grid: repeat(5, 1fr) / repeat(5, 1fr);
        gap: 1em;
        isolation: isolate;
        margin: 4px;  /* enough space for the highlight ring */

        details {
            position: relative;
            padding-bottom: 100%;

            > summary {
                position: absolute;
                inset: 0;
                list-style: none;
                cursor: pointer;
                background: black;
                border-radius: 1em;
            }
            &:hover > summary {
                box-shadow: 0 0 0 4px orange;
            }

            > .-on {
                position: absolute;
                inset: 0;
                z-index: 3;
                display: grid;
                place-items: center;
                margin-bottom: 1em;  /* match button underlay so it's centered on the "top" */
                font-weight: bold;
                pointer-events: none;
                mix-blend-mode: difference;
                color: white;
            }

            > .-light {
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 1em;
                background: gold;
                pointer-events: none;

                &.--center {
                    inset: 0;
                    z-index: 1;
                }

                &.--north, &.--south, &.--east, &.--west {
                    mix-blend-mode: difference;
                    z-index: 2;
                }

                &.--north {
                    bottom: calc(-100% - 1em);
                }
                &.--south {
                    top: calc(-100% - 1em);
                }
                &.--east {
                    right: calc(-100% - 1em);
                }
                &.--west {
                    left: calc(-100% - 1em);
                }
            }
        }
    }

    > .-buttons {
        display: grid;
        grid: repeat(5, 1fr) / repeat(5, 1fr);
        gap: 1em;
        isolation: isolate;
        position: absolute;
        inset: 0;
        margin: 4px;
        pointer-events: none;
        opacity: 0.5;

        > div {
            padding-bottom: 100%;
            background: radial-gradient(#ffcc, transparent);
            box-shadow: inset 0 0 0 2px black, inset 0 calc(-1em - 2px) 2px 0 gray, inset 0 0 2px 0.25em white, inset 0 -1em 2px 0.25em white;
            border-radius: 1em;
        }
    }
}

button#local-lights-out-scramble {
    font-size: 1.5em;
    display: block;
    margin: 1em auto;
    padding: 0.5em 2em;
}

.local-lights-out-example {
    display: grid;
    grid: auto-flow / repeat(5, auto);
    gap: 0.5em;
    width: max-content;
    margin: 1em auto;

    > div {
        display: grid;
        place-items: center;
        height: 2em;
        width: 2em;
        line-height: 1;
        border-radius: 0.25em;

        background: #666;
        color: white;

        &.-a {
            background: hsl(345deg 100% 60%);
        }
        &.-b {
            background: hsl(225deg 100% 60%);
        }
        &.-ab {
            background: repeating-linear-gradient(to bottom right, hsl(345deg 100% 60%) 0 0.71em, hsl(225deg 100% 60%) 0.71em 1.414em);
        }
    }
}
</style>

<div class="local-lights-out" id="local-lights-out-main-puzzle">
    <div class="-lights">
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details>      <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details open> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    </div>
    <div class="-buttons">
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
    </div>
</div>

Naturally, pure CSS can't create a random setup, and this is a static page, so the initial state of the board is always the same.  At the price of a droplet of JavaScript, you may use the following button:

<button type="button" id="local-lights-out-scramble">Scramble the board</button>

<script>
document.querySelector('#local-lights-out-scramble').addEventListener('click', () => {
    for (let light of document.querySelectorAll('#local-lights-out-main-puzzle > .-lights > details')) {
        if (Math.random() < 0.5) {
            light.setAttribute('open', '');
        }
        else {
            light.removeAttribute('open');
        }
    }
});
</script>


## How it works

Before I get to the CSS, notice several properties of the game itself.  Since the buttons only toggle in a fixed pattern, it doesn't matter which order buttons are pressed in.  In this example, pressing A and then B will have exactly the same effect as pressing B and then A, even on the light between them: pressing one button will turn it on, and then pressing the other button will turn it back off.

<div class="local-lights-out-example">
    <div></div> <div class="-a"></div> <div></div> <div class="-b"></div> <div></div>
    <div class="-a"></div> <div class="-a">A</div> <div class="-ab"></div> <div class="-b">B</div> <div class="-b"></div>
    <div></div> <div class="-a"></div> <div></div> <div class="-b"></div> <div></div>
</div>

Similarly, pressing the same button twice will toggle the same set of lights twice, which ultimately does nothing.  So each button can be considered as either "on" (toggle lights) or "off" (do not toggle lights).  That doesn't help with solving the puzzle, since there's no way to tell which state any given button is in, but hold that thought.

In a sense, then, instead of thinking of the _buttons_ as altering the state of the _lights_, you might think of the _lights_ as reflecting something about the _buttons_ — specifically, a light is lit _if and only if_ an _odd number_ of relevant buttons (the ones that affect it, i.e., itself and its neighbors) are _on_.

This might sound strange, so by way of example, here's a version of the puzzle where each button clearly indicates whether it's on or not.  Feel free to play with it a bit.  Observe that it's impossible to guess whether a button is on just from the state of the puzzle, that the buttons toggle on or off when pressed, and that the lights really do act as a count of the buttons around them.

(As a bonus feature, you can always solve the puzzle by simply turning every button off.  For this basic Lights Out, that's the _only_ solution, but that's not necessarily true for this type of puzzle in general.)

<div class="local-lights-out --buttons-demo">
    <div class="-lights">
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>

        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
        <details> <summary></summary> <div class="-on">ON</div> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    </div>
    <div class="-buttons">
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
        <div></div> <div></div> <div></div> <div></div> <div></div>
    </div>
</div>

Parity is cool!

Given these properties, only two web features are necessary to create the puzzle.  First, something that can _toggle_, so the puzzle can remember the state of each button (and also so the player can actually click on something).  The classic way to do this is to use an invisible checkbox, and you could very well use that here — _except_ that on Cohost, I could only write inline CSS, and you need a real stylesheet to detect a checkbox's state (with `:checked`).  Thankfully, Cohost launched shortly after the introduction of the `<details>` element, which allows toggling the existence of arbitrary child elements.

The other requirement is something that can _count_.  Bear in mind, again, that I could only use inline styles, so selector trickery was right out.

Hmm.

The answer is actually what inspired me to make this in the first place.  Enter `mix-blend-mode`, which allows for applying image-editor-esque layer modes to arbitrary elements (or backgrounds, with the similar `background-blend-mode` property).  There are some familiar faces available, such as `multiply` and `screen`, but what caught my eye was `difference`.

One of the most telling properties of a blend mode is what happens when you blend a color with white, black, or itself.  Difference blending just produces, well, the difference of two colors, so blending a color with itself produces black (because anything minus itself is zero), and blending a color with black leaves it unchanged (because anything minus zero is unchanged).

And with this, I can count!  Or at least I can count mod 2, which is exactly what I want.

Here's how it actually works.  The game itself is a CSS grid.  Each button is a relatively-positioned `<details>` element whose `<summary>` is just an empty click zone, made to fill the cell with `position: absolute` and `inset: 0`.  Each button _also_ contains five other elements, arranged in the pattern of where the lights go.  They're absolutely positioned as well, sized to the cell with `width: 100%` and `height: 100%`, and then shifted over to exactly sit atop neighboring cells with, say, `left: calc(-100% - 1em)`.  That means align the left edge to the left edge of the parent, minus 100% of the width of the parent, minus 1em (the size of the gap) — which puts it in exactly the same position as the cell to the left.

So the basic pattern is this.  (You can click that central cell to toggle it.)

<style>
.local-lights-out-build {
    display: grid;
    grid: repeat(3, 4em) / repeat(3, 4em);
    gap: 1em;
    width: max-content;
    margin: 1em auto;
    isolation: isolate;

    > div {
        background: black;
        border-radius: 1em;
    }

    > details {
        position: relative;
        padding-bottom: 100%;

        > summary {
            position: absolute;
            inset: 0;
            list-style: none;
            cursor: pointer;
            background: black;
            border-radius: 1em;
            background: #666;
        }
        &:hover > summary {
            box-shadow: 0 0 0 4px orange;
        }

        > .-light {
            --position: calc(-100% - 1em);
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 1em;
            background: gold;
            pointer-events: none;

            &.--center {
                inset: 0;
                z-index: 1;
            }

            &.--north, &.--south, &.--east, &.--west {
                z-index: 2;
            }

            &.--north {
                bottom: var(--position);
            }
            &.--south {
                top: var(--position);
            }
            &.--east {
                right: var(--position);
            }
            &.--west {
                left: var(--position);
            }
        }
    }

    &.--offset > details > .-light {
        --position: calc(-100% - 0.25em);
        box-shadow: 0 0 0 2px gray;
        mix-blend-mode: difference;
    }
}
</style>

<div class="local-lights-out-build" style="grid: repeat(3, 4em) / repeat(3, 4em);">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <details> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
</div>

Of course, if two or more of these "light" regions appear in the same cell, then...  nothing happens.  They just draw on top of each other, and look like a single light.

That's where difference blending comes in.  With `mix-blend-mode: difference` on all of the lights, then the _first_ light in a cell (as long as the very bottom is black) appears lit.  But as soon as there's a _second_ one, because it's the same color, it'll combine with the one below it to become black again.  If a _third_ one appears, it'll combine with the black to become lit again.

Here's a full grid with only four working buttons, but with the lights offset so you can see the blending in action.  The lights on top of the gray cells also make a sort of murky pink color now, because the background is gray instead of black.

<div class="local-lights-out-build --offset" style="grid: repeat(5, 4em) / repeat(5, 4em);">
    <div></div> <div></div> <div></div> <div></div> <div></div>

    <div></div>
    <div></div>
    <details> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    <div></div>
    <div></div>

    <div></div>
    <details> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    <div></div>
    <details> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    <div></div>

    <div></div>
    <div></div>
    <details> <summary></summary> <div class="-light --center"></div> <div class="-light --north"></div> <div class="-light --south"></div> <div class="-light --east"></div> <div class="-light --west"></div> </details>
    <div></div>
    <div></div>

    <div></div> <div></div> <div></div> <div></div> <div></div>
</div>

That's pretty much the whole thing right there.  The only extra trickery is to use `isolation: isolate` to ensure that the lights only blend with each other and not with the page background underneath, and also apply `pointer-events: none` and `z-index` liberally to ensure none of the extra visual elements interfere with clicking on a cell's `<summary>`.

The extra regions at the edges are a bit of a problem, since they stick out of the puzzle, but you can either delete the outliers or be incredibly lazy (like me) and just slap `overflow: hidden` on the whole board.

The final detail is to add a little depth to the cells, so they look sort of like buttons.  Rather than fiddle further with the Jenga tower of elements within the board itself, I added a second board of exactly the same size (again, `position: absolute` and `inset: 0`, with the same grid configuration) and filled it with 25 empty divs and some fancy backgrounds and box shadows.  The colors and opacity are carefully chosen to work decently regardless of whether the light underneath is lit or not, but you could probably get fancier with blend modes and whatnot.  As a convenient bonus, the borders cover up any sub-pixel rounding errors or antialiasing artifacts from the stacked lights.

And that's it.  My favorite part of this scheme is that _nothing in the DOM_ actually remembers the state of the _lights_, only of the buttons!  The lights themselves are purely visual, a carefully choreographed artifact of the rendering.  As far as the DOM is aware, there's just a stack of boxes that happen to overlap.
