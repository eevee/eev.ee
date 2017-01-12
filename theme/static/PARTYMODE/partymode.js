(function() {
    // Number of kilopixels dedicated to each snowflake
    var FLAKE_SPARSITY = 15;
    // Images
    var IMAGES = Array.apply(null, {length: 15}).map(function(_, index) { return String(index) + ".png"; });

    // Get the path to ourselves
    var cur = document.currentScript;
    var path;
    if (cur) {
        path = cur.src;
    }
    else {
        var scripts = document.getElementsByTagName('script');
        path = scripts[scripts.length - 1].src;
    }
    var lastslash = path.lastIndexOf('/');
    if (lastslash >= 0)
        path = path.substring(0, lastslash + 1);

    // Inject CSS we need
    var css = document.createElement('link');
    css.type = 'text/css';
    css.rel = 'stylesheet';
    css.href = path + 'partymode.css';
    document.head.appendChild(css);

    // Create the container and fill it with some elements
    var container = document.createElement('div');
    container.className = 'partymode--container';

    var num_flakes = (
        document.documentElement.clientWidth
        * document.documentElement.clientHeight
        / FLAKE_SPARSITY
        / 1000
    );
    for (var i = 0; i < num_flakes; i++) {
        var flake = document.createElement('img');
        flake.src = path + IMAGES[Math.floor(Math.random() * IMAGES.length)];
        flake.className = 'partymode--flake';
        // Randomize a bit
        flake.style.animationDelay = "-" + String(Math.random() * 4) + "s";
        flake.style.animationDuration = String(Math.random() * 3 + 4) + "s";
        flake.style.left = String(Math.random() * 120 - 10) + "%";

        container.appendChild(flake);
    }

    // And done!  No actual iavascript required to keep it running.
    document.documentElement.appendChild(container);
})();
