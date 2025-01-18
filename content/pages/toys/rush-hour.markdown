title: Rush Hour — in pure CSS
date: 2024-10-14 07:41
tags: web

A CSS crime originally made for Cohost: the board game [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)), implemented using only CSS.  This version has been only slightly modified from the one on Cohost:

- It uses classes and some CSS variables, instead of gobs of inline CSS generated from a Python script, as Cohost required.
- The positioning is slightly simpler, which makes the implementation easier to explain.
- I've touched up the aesthetics very slightly, and made the arrows a bit bigger in the hopes it's easier to play on a small touchscreen.
- The extra puzzles (below) use a new set of colors.  The starting colors are as they appeared on Cohost.

The goal is to free the red car.  Pretend that they're cars.

<!-- more -->

<style>
.local-rush-hour {
    --local-grid-size: 6;
    --local-cell-size: 80px;
    --local-border: 30px;
    --local-car-border: 4px;
    --local-car-margin: 4px;
    --local-arrow-size: 20px;

    width: fit-content;
    margin: 1em auto;
    overflow: hidden;

    .-board-edge {
        width: fit-content;
        padding: calc(var(--local-cell-size) / 2 - var(--local-border));
        border: var(--local-border) solid #aaa;
        border-radius: calc(var(--local-cell-size) / 2);
        background: #ddd;
    }

    .-board {
        position: relative;
        isolation: isolate;
        width: calc(var(--local-cell-size) * var(--local-grid-size));
        height: calc(var(--local-cell-size) * var(--local-grid-size));
        margin: auto;

        .-exit-patch {
            position: absolute;
            top: calc(var(--local-cell-size) * 2);
            left: 100%;
            width: calc(var(--local-cell-size) / 2);
            height: var(--local-cell-size);
            background: #ddd;
        }

        .-dimples {
            position: absolute;
            inset: 0;
            display: grid;
            grid: repeat(6, 80px) / repeat(6, 80px);
            place-items: stretch;

            > div {
                margin: 12px;
                border: 3px solid #999;
                border-color: #eee #ccc #ccc #eee;
                border-radius: 12px;
            }
        }

        .-wall {
            position: absolute;
            box-sizing: border-box;
            z-index: 2;
            left: calc(var(--local-x) * var(--local-cell-size));
            top: calc(var(--local-y) * var(--local-cell-size));
            width: var(--local-cell-size);
            height: var(--local-cell-size);
            border: calc(var(--local-cell-size) / 8) outset #222;
            border-radius: var(--local-car-margin);
            background: #333;
        }

        .-piece {
            --local-piece-size: 1;
            --local-perp-offset: 0;
            --local-step: 0;
            position: absolute;
            display: flex;

            summary {
                list-style: none;
                font-size: 0;
                cursor: pointer;

                .-back, .-forth {
                    position: absolute;
                    z-index: 1;
                    border: var(--local-arrow-size) solid transparent;
                }
            }
            &.--horiz {
                flex-flow: row;
                top: calc(var(--local-cell-size) * var(--local-perp-offset));

                summary .-back {
                    border-right-color: black;
                    border-left: none;
                    left: calc(var(--local-cell-size) * (-0.1 + var(--local-step) * -9 - 9) - var(--local-arrow-size) + 1000%);
                    top: calc(var(--local-cell-size) * 0.5 - var(--local-arrow-size));
                }
                summary .-forth {
                    border-left-color: black;
                    border-right: none;
                    left: calc(var(--local-cell-size) * (0.1 + var(--local-step) * -9 + var(--local-piece-size)) + 1000%);
                    top: calc(var(--local-cell-size) * 0.5 - var(--local-arrow-size));
                }
            }
            &.--vert {
                flex-flow: column;
                left: calc(var(--local-cell-size) * var(--local-perp-offset));

                summary .-back {
                    border-bottom-color: black;
                    border-top: none;
                    top: calc(var(--local-cell-size) / -10 + var(--local-cell-size) * ((var(--local-step) + 1) * -9) - var(--local-arrow-size) + 1000%);
                    left: calc(var(--local-cell-size) * 0.5 - var(--local-arrow-size));
                }
                summary .-forth {
                    border-top-color: black;
                    border-bottom: none;
                    top: calc(var(--local-cell-size) / 10 + var(--local-cell-size) * (var(--local-step) * -9 + var(--local-piece-size)) + 1000%);
                    left: calc(var(--local-cell-size) * 0.5 - var(--local-arrow-size));
                }
            }

            .-space {
                width: var(--local-cell-size);
                height: var(--local-cell-size);
            }
            .-half-space {
                width: var(--local-border);
                height: var(--local-border);
            }

            .-car {
                box-sizing: border-box;
                position: absolute;
                z-index: 2;
                padding: var(--local-car-margin);
                border: var(--local-car-border) outset #2229;
                border-radius: calc(2 * var(--local-car-border));
                background: #f00;
                box-shadow: inset 0 0 calc(var(--local-cell-size) / 4) 4px hsl(300deg 50% 20% / 0.2), inset 0 0 1px #fff9, 0 1px 3px 1px #0006;
            }
            &.--horiz .-car {
                width: calc(var(--local-piece-size) * var(--local-cell-size) - 2 * var(--local-car-margin));
                height: calc(var(--local-cell-size) - 2 * var(--local-car-margin));
                left: calc(var(--local-car-margin) + 100%);
                top: calc(var(--local-car-margin));
            }
            &.--vert .-car {
                height: calc(var(--local-piece-size) * var(--local-cell-size) - 2 * var(--local-car-margin));
                width: calc(var(--local-cell-size) - 2 * var(--local-car-margin));
                top: calc(var(--local-car-margin) + 100%);
                left: calc(var(--local-car-margin));
            }

            .--car0 { background: hsl(  0deg  95%  50%); }  /* red */
            .--car1 { background: hsl( 20deg  30%  60%); }  /* brown */
            .--car2 { background: hsl( 30deg 100%  60%); }  /* orange */
            .--car3 { background: hsl( 40deg 100%  80%); }  /* cream */
            .--car4 { background: hsl( 55deg 100%  75%); }  /* lemon */
            .--car5 { background: hsl( 60deg  50%  50%); }  /* olive */
            .--car6 { background: hsl(160deg  40%  40%); }  /* teal */
            .--car7 { background: hsl(150deg  80%  80%); }  /* mint */
            .--car8 { background: hsl(195deg 100%  80%); }  /* azure */
            .--car9 { background: hsl(245deg  50%  75%); }  /* purple */
            .--car10 { background: hsl(340deg 100%  90%); }  /* pink */
            .--car11 { background: hsl(  0deg  10%  90%); }  /* gray */

            .--truck1 { background: hsl( 55deg 100%  50%); }  /* yellow */
            .--truck2 { background: hsl(170deg  75%  75%); }  /* cyan */
            .--truck3 { background: hsl(225deg  60%  50%); }  /* navy */
            .--truck4 { background: hsl(270deg  80%  90%); }  /* lavender */
        }
    }

    .-win {
        font-size: var(--local-cell-size);
        display: grid;
        place-items: center;
        position: absolute;
        z-index: 99;
        top: calc(-1 * var(--local-cell-size) * var(--local-perp-offset));
        left: 0;
        width: calc(var(--local-cell-size) * var(--local-grid-size));
        height: calc(var(--local-cell-size) * var(--local-grid-size));
        background: #dddc;
        text-shadow: 0 4px #0003;
    }
}

#local-rush-hour-buttons {
    display: grid;
    grid: auto-flow / repeat(auto-fill, minmax(2em, 1fr));
    gap: 0.5em;
    margin: 1em 10%;

    button {
        padding: 0.25em;
    }
}
</style>

<div class="local-rush-hour">
    <div class="-board-edge">
        <div class="-board">
            <div class="-exit-patch"></div>
            <div class="-dimples">
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
                <div></div> <div></div> <div></div> <div></div> <div></div> <div></div>
            </div>

            <div class="-piece --horiz" style="--local-piece-size: 2; --local-perp-offset: 2;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 4;">
                    <summary><div class="-forth"></div></summary> <div class="-half-space"></div>
                    <div class="-win">you win!!</div>
                </details>
                <div class="-car" style="background: #f00;"></div>
            </div>
            <div class="-piece --horiz" style="--local-piece-size: 2; --local-perp-offset: 0;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #53b689;"></div>
            </div>
            <div class="-piece --horiz" style="--local-piece-size: 3; --local-perp-offset: 3;">
                <details style="--local-step: 0;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #0567a9;"></div>
            </div>
            <div class="-piece --horiz" style="--local-piece-size: 2; --local-perp-offset: 4;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #344047;"></div>
            </div>
            <div class="-piece --horiz" style="--local-piece-size: 2; --local-perp-offset: 5;">
                <details style="--local-step: 0;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #ac9b8b;"></div>
            </div>
            <div class="-piece --horiz" style="--local-piece-size: 2; --local-perp-offset: 5;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #dce839;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 3; --local-perp-offset: 0;">
                <details style="--local-step: 0;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #fcdb00;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 2; --local-perp-offset: 1;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #00a7e6;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 2; --local-perp-offset: 2;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #e97895;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 2; --local-perp-offset: 2;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #008662;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 2; --local-perp-offset: 3;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #605495;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 2; --local-perp-offset: 4;">
                <details style="--local-step: 0;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 3;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #f93;"></div>
            </div>
            <div class="-piece --vert" style="--local-piece-size: 3; --local-perp-offset: 5;">
                <details style="--local-step: 0;" open> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 1;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <details style="--local-step: 2;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
                <div class="-car" style="background: #9571a7;"></div>
            </div>
        </div>
    </div>
</div>

This starting arrangement was borrowed from the final card in the original Rush Hour, #40, which turns out to be the hardest possible game — in the sense that it requires the most moves to solve.

If you'd like to play some others, here's a selection of the "hardest" puzzles from [Michael Fogleman's database](https://www.michaelfogleman.com/rush/) of every nontrivial Rush Hour, in ascending order by difficulty.  (He does also have his own [Rush Hour player](https://www.michaelfogleman.com/static/rush/), with the more natural dragging controls you might expect.)

The original puzzle above is number 34.  Many of these use wall tiles, not part of the board game, which is how they manage to be even more difficult.

<div id="local-rush-hour-buttons"></div>

<template id="local-rush-hour-piece-step">
    <details style="--local-step: 0;"> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
</template>
<template id="local-rush-hour-red-step">
    <details style="--local-step: 4;">
        <summary><div class="-forth"></div></summary> <div class="-half-space"></div>
        <div class="-win">you win!!</div>
    </details>
</template>
<script>
{
let patterns = [
    'oooIBBoCCIKoAAHJKoDDHJEEGFFFoLGooooL',
    'ooooxoCCCJLoAAIJLoooIDDoHEEKooHFFKox',
    'BBJCCoDDJoLMIAAoLMIEEELMIooKFFGGoKHH',
    'ooxooKCCoJoKHAAJooHoIJDDEEIooLFFFGGL',
    'GBBJLxGooJLoHAAKooHoIKDDHoIEEMFFFooM',
    'HxoCCoHDDDLMAAIJLMEEIJLMoooKFFoGGKoo',
    'BBKCCoJoKDDoJAALooEEoLFFGGGLoMoxIIoM',
    'xCCoKLooIoKLAAIoKMGHDDDMGHoJEExooJoo',
    'BBCCLoooJoLMIoJAAMIDDEEMoFFKooGGGKHH',
    'BBCCCoDDoKoxIAAKoLIoJFFLGGJoooooJHHH',

    'xCCMooooLMDDKoLAANKEEooNKFFGGOxIIJJO',
    'xooJCCGHoJKMGHAAKMDDIoLNooIxLNFFFoLN',
    'xCCLooooKLDDJoKAAMJEEooMJFFGGNHHHIIN',
    'oooooxCCCJooAAIJoLooIDDLHEEKooHFFKGG',
    'ooHBBBooHJooAAIJoKCCIDDKFGEEoKFGoooo',
    'xCCKooooJKDDIoJAALIEEooLIFFGGMoHHHoM',
    'GooBBBGCCJoKAAHJoKooHDDKooIEEoooIFFF',
    'xCCLMNooKLMNAAKooOIJDDxOIJFFooGGHHHo',
    'BBBKLMHCCKLMHoAALoDDJooooIJEEooIFFGG',
    'HIoxLxHIDDLoHAAKoooooKEEooJFFMGGJooM',

    'ooHBBBooHJooAAIJoKCCIDDKoGEEoKoGFFoo',
    'oxCCMoDDDKMoAAJKooooJEEoIFFLooIGGLxo',
    'oooJBBoCCJLoAAIKLoDDIKEEHFFFoMHGGGoM',
    'oxCCMoDDDKMoAAJKooooJLEEIFFLooIGGHHo',
    'GBBoLoGHIoLMGHIAAMCCCKoMooJKDDEEJoxo',
    'oxCCoMDDDKoMAAJKooooJEEoIFFLooIGGLox',
    'oooJBBoCCJLoAAIKLoDDIKEEHFFFoMHoGGoM',
    'BBBKLMHCCKLMHoAALMDDJooooIJEEooIFFGG',
    'BBBJCCHooJoKHAAJoKooIDDLEEIooLooxoGG',
    'ooxCCLDDoKoLIAAKooIoJKEEFFJooMGGGHHM',

    'ooooLxCCCJLoAAIJoMooIDDMHEEKooHFFKGG',
    'ooIBBBooIKooAAJKoLCCJDDLGHEEoLGHFFoo',
    'BBIooMGHIoLMGHAALNGCCKoNooJKDDooJEEx',
    'GBBoLoGHIoLMGHIAAMCCCKoMooJKDDEEJFFo',  // starting arrangement
    'xCCoLMooJoLMAAJoLNHIDDDNHIoKEExooKGG',
    'oxCCMNDDDKMNAAJKooooJLEEIFFLooIGGHHo',
    'BBBCCNDDoxMNJAAoMOJoKFFOGGKLooxIILoo',
    'oooJLxCCCJLoHAAKooHoIKDDooIEEMoFFoxM',
    'ooBBMxDDDKMoAAJKoNooJEENIFFLooIGGLHH',
    'IBBxooIooLDDJAALooJoKEEMFFKooMGGHHHM',
];
let car_colors = ['--car1', '--car2', '--car3', '--car4', '--car5', '--car6', '--car7', '--car8', '--car9', '--car10', '--car11'];
let truck_colors = ['--truck1', '--truck2', '--truck3', '--truck4'];
function shuffle(list) {
    // Knuth–Fisher–Yates, of course
    for (let i = list.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [list[i], list[j]] = [list[j], list[i]];
    }
}

let step_template = document.getElementById('local-rush-hour-piece-step');
let red_template = document.getElementById('local-rush-hour-red-step');

let button_container = document.getElementById('local-rush-hour-buttons');
for (let [i, pattern] of patterns.entries()) {
    let button = document.createElement('button');
    button.setAttribute('type', 'button');
    button.textContent = String(i + 1);
    button_container.append(button);

    button.addEventListener('click', () => {
        shuffle(car_colors);
        shuffle(truck_colors);
        let car_color = 0;
        let truck_color = 0;

        // Snag pieces
        var seen = {};
        let chars = pattern.split('');
        let board = document.querySelector('.local-rush-hour .-board');
        for (let piece of board.querySelectorAll('.-piece, .-wall')) {
            piece.remove();
        }

        for (let [i, ch] of chars.entries()) {
            if (ch === 'o')
                continue;
            if (seen[ch])
                continue;

            let x = i % 6;
            let y = Math.floor(i / 6);
            if (ch === 'x') {
                let wall = document.createElement('div');
                wall.classList.add('-wall');
                wall.style.setProperty('--local-x', x);
                wall.style.setProperty('--local-y', y);
                board.append(wall);
                continue;
            }

            seen[ch] = true;
            let horiz = chars[i + 1] === ch;
            let size = chars.filter(x => x === ch).length;
            console.log(i, ch, horiz, size, chars.filter(x => x === ch));

            let color;
            if (ch === 'A')
                color = '--car0';
            else if (size === 3) {
                color = truck_colors[truck_color];
                truck_color += 1;
            }
            else {
                color = car_colors[car_color];
                car_color += 1;
            }

            let piece = document.createElement('div');
            piece.classList.add('-piece');
            let position;
            let offset;
            if (chars[i + 1] === ch) {
                piece.classList.add('--horiz');
                position = x;
                offset = y;
            }
            else {
                piece.classList.add('--vert');
                offset = x;
                position = y;
            }
            piece.style.setProperty('--local-piece-size', size);
            piece.style.setProperty('--local-perp-offset', offset);
            for (let i = 0; i < 6 - size; i++) {
                let step = step_template.content.cloneNode(true);
                let deets = step.querySelector('details');
                deets.style.setProperty('--local-step', i);
                if (i < position) {
                    deets.setAttribute('open', '');
                }
                piece.append(step);
            }
            if (ch === 'A') {
                piece.append(red_template.content.cloneNode(true));
            }
            let car = document.createElement('div');
            car.classList.add('-car');
            car.classList.add(color);
            piece.append(car);

            board.append(piece);
        }
    });
}
}
</script>


## How it works

Each piece is built from markup like this:

```html
<div class="-piece">
    <details> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
    <details> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
    <details> <summary><div class="-back"></div><div class="-forth"></div></summary> <div class="-space"></div> </details>
    ...
    <div class="-car"></div>
</div>
```

(For simplicity, I'll assume this is a horizontal piece.  All the same ideas apply for vertical pieces, just with the directions swapped.)

The basic idea is that the `div.-piece` container is a flexbox, everything in a `summary` is absolutely-positioned, and each `div.-space` is empty but exactly the size of a cell.  So the only in-flow contents of the `details` are those spacers, and ultimately the flexbox's width is equal to the number of _open_ `details` times the width of a cell.  The initial position of a piece is thus set by pre-opening some number of its `details` children.  (The total number of `details` is 6, the size of the board, minus the width of the car — that's the maximum number of cells it could move over from the left edge.)

The visual part of the car, the `div.-car`, is then absolutely positioned as follows:

```css
left: calc(var(--car-margin) + 100%);
top: calc(var(--car-margin));
```

The `--car-margin` is a few pixels to keep cars from butting up against the edges of their cells (and thus each other), so that's not very interesting.

The four edge-positioning properties treat percentages as relative to the size of the containing block.  So that `left` puts the car's left edge at the width of the container — which is the `div.-piece` flexbox, whose width is the number of open `details`, in cells.

So far, so good — now the car's horizontal position is controlled by the opening and closing of `details`, which is something a user can control interactively.

<aside markdown="1">
Why use absolute positioning on the car, rather than just add it to the flexbox?  Because I want to use percentages later to _measure_ where the car is, but if the car were in the flexbox, its width would also contribute the container width.  I could account for that, but at the time I found this easier to reason about.

The Cohost edition also shifted the _car_ downwards into its row, whereas this version shifts the entire container downwards into its row.  I think that was just an artifact of the very awkward process of generating inline CSS.  This is much simpler to explain, and easier to follow in your browser's inspector.
</aside>

The two elements in each `summary` are the two chevrons, one for moving the car left, one for moving it right.  The rules of the game (and, for the original board game, the rules of physical reality) say that you can't move a piece if it's up against another piece or the edge of the board.  That's not a huge problem, though, because these chevrons are the only controls the user has access to, so they don't need to be hidden or disabled, only _inaccessible_.  Giving the inner board element `overflow: hidden;` will chop off any arrows that peek over an edge, and giving the cars `z-index: 1;` to stack them on top of neighboring cars' arrows.

<aside class="aside--well-actually" markdown="1">
Alas!  A player could use keyboard navigation to activate a summary that's visually hidden.  Within the scope of Cohost CSS crimes, there's not much to be done about that.
</aside>

That just leaves the complicated part!

Clicking on a _left_ chevron should _always close_ a `details`, and clicking on a _right_ chevron should _always open_ one.  This is a fundamental rule for wiring the controls to the game model: revealing a spacer moves the car right, and hiding one moves the car left.  But this isn't how the `summary` element works; its contents act purely as a toggle.  Clicking the same left chevron will simply toggle its parent open or closed.

To fix this, the game needs to somehow _only_ show the left chevron for an _open_ `details`, and _only_ show the right chevron for a _closed_ `details`.  Under normal circumstances, this would be easy to do with a `details[open]` selector.  The result might be a bunch of chevrons stacked on top of each other, but they're identical and opaque so that's not a problem, and it doesn't really matter _which_ element is opened or closed.

Alas!  I originally wrote this for Cohost, where stylesheets (and thus selectors) weren't an option.  Instead, I engaged in some popular CSS crime shenanigans, known as _width hacking_.

Consider the red car from the initial puzzle.  It starts in the fourth column, so it has three `details` already open.  I'm going to add some additional requirements here and say that _only_ one of each chevron should be visible: the left chevron for the last open `details`, and the right chevron for the first closed `details`.  Here, that's the third and fourth, respectively.

First, each `details` is indexed from 0 with a `--step` property, so they can be distinguished with `calc()`.  Consider the right chevron from the fourth `details`, the one that should be visible.  It has `--step: 3;`, and it will _only_ be visible when the car is three cells over, so its position can be written as:

```css
left: calc(var(--cell-size) * (var(--step) + var(--piece-size) + 0.1));
```

That's 3 columns over to match the position of the car, 2 more columns to get to the right edge of the car, and then 0.1 to give the chevron a little breathing room.  (That's important because the cars aren't flush with the edges of the cells, so the chevrons can't be either, or the cars wouldn't fully cover them.)

Now here's the trick: to ensure this chevron is only visible when the car is actually in this position, add an expression that computes to zero when that's true, and _any large value_ when it's not.  As long as the large value exceeds the width of the board, the chevron will be shifted beyond its bounds and erased by the `overflow: hidden` that's already on the board.

This is possible because two related values are available: `--step` is where the car _should_ be, and `100%` is where the car _actually is_.  Therefore `100% - var(--step) * var(--cell-size)` gives the pixel distance between the car's actual position and its desired position, and when the car is in its correct position, that's zero.

When it's _not_ zero, that distance is at least one cell width (possibly negative).  To turn it into a "large value", just multiply the whole expression by at least 6, the width of the board.  I chose 10 because it stands out, giving:

```css
left: calc(var(--cell-size) * (var(--step) + var(--piece-size) + 0.1) + (100% - var(--step) * var(--cell-size)) * 10);
```

Rearranging a bit:

```css
left: calc(var(--cell-size) * (var(--step) + var(--piece-size) + 0.1) + 1000% - var(--cell-size) * 10 * var(--step));
left: calc(var(--cell-size) * (var(--step) + var(--piece-size) + 0.1 - 10 * var(--step)) + 1000%);
left: calc(var(--cell-size) * (var(--step) * -9 + var(--piece-size) + 0.1) + 1000%);
```

And that's pretty much what's in the stylesheet.

The only remaining detail is detecting a win, but that's pretty easy.  The red car gets one extra `details`, which also contains an element spanning the whole board, both congratulating the player and preventing them from making any further moves.  Its spacer is a little narrower, so it only makes the red car peek a little ways into the border.

And that's it!
