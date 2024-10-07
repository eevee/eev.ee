title: Converting a Git repo from tabs to spaces
date: 2016-06-04 22:40
category: blog
tags: tech, git, python

This post is about the thing in the title.

I used to work for Yelp.  For historical reasons — probably "the initial developers preferred it" — their mostly-Python codebase had always been indented with tabs.  That's in stark contrast to the vast majority of the Python ecosystem, which generally uses the [standard library's style guide][PEP8] recommendation of four spaces.  The presence of tabs caused occasional minor headaches and grumbles among the Python developers, who now numbered in the dozens and were generally used to spaces.

At the end of 2013, I bestowed Yelp with a Christmas gift: I converted their _entire primary codebase_ from tabs to four spaces.  On the off chance anyone else ever wants to do the same, here's how I did it.  Probably.  I mean, it's been two and a half years, but I wrote most of this at the time, so it should be correct.

**Please note: I _do not care_ what you think about tabs versus spaces.**  That's for a _different_ post!  I no longer work for Yelp, anyway — so as compelling as your argument may be, I can no longer undo what I have done.

<!-- more -->


## Prerequisites

First, **be absolutely sure you're never going to change your mind**.  If you as an organization are ambivalent about your whitespace needs, or if you have influential coworkers who will use this post for evil to switch everything back to tabs as soon as you leave, you may wish to reconsider.

### Fix mixed indentation

If you're using a whitespace-sensitive language, you _must_ fix any inconsistent indentation.  (You might want to do this anyway, or your code will look like nonsense.)  By "inconsistent", I mean any code that will change relative indentation levels if the width of a tab changes.  Consider:

    :::text
    ....if foo:
    ------->print("true")

If a tab is considered to be eight cells wide, as the good Lord intended, this is fine.  But if you're about to replace all your tabs with four spaces, the extra indentation level vanishes, and suddenly this is invalid Python.

You would not _believe_ how many cases of this I found.  I most fondly remember the file that was for some reason indented with `n` tabs _plus_ a single space, except where it wasn't.  I have no idea how that happened.  (Incidentally, the need to micromanage variable-width invisible characters is one of the reasons I wanted to get rid of tabs.)  (Please don't leave comments about this.)  (Also consider `set shiftround` if you use vim, which pretty well eliminates this problem but is tragically under-used.)

On the other hand, if you are some kind of monster and want to replace every tab with _eight_ spaces, then you don't need to worry about this.

You could just scan your codebase for leading spaces, but if you have a mix of tabbed files and spaced files, you'll get a ton of false positives and it'll be a huge pain in the ass.  A somewhat more robust approach for Python specifically is:

    :::zsh
    python -tt -m compileall . | grep Sorry

`-tt` tells the interpreter to treat inconsistent indentation as a `SyntaxError`.  The `compileall` module searches recursively for `.py` files and produces `.pyc` bytecode, which requires parsing each file, which will trigger the `SyntaxError`.  And any errors encountered while compiling modules produce a line starting with `Sorry`, along with the filename, line number, and column number.

Now you can spend an afternoon fixing those all by hand and trying to figure out why this one file seems to have been written with a tabstop of 3.

### Distribute a Git filter definition

The actual process uses a [Git filter](https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes) to enforce that no new tabs find their way into the repository and fix any tabs on in-flight branches.  The configuration for which filters to run on which files is stored as part of the repository, but unfortunately, the configuration for what each filter _does_ is not.

One way or another, you **must** get this block in your devs' Git configuration — anyone doing regular development who doesn't have the filter definition will be _utterly_ confused.  This is probably the hardest part of the process.  Thankfully, Yelp mostly does work on beefy shared dev machines, so I only had to bug an ops person to stick this incantation in `/etc/gitconfig` and wait for Puppet.  YMMV.

    :::text
    [filter "spabs"]
        clean = expand --initial -t 4
        smudge = expand --initial -t 4
        required
    [merge]
        renormalize = true

I'll explain what this all actually does later.  Oh, and it might help to actually have `expand` installed.  Most Unix-likes should have it already; if you have developers using Windows, `expand` is one of the utilities in the [unixutils][] project.  Also, BSD (i.e. OS X) `expand` apparently doesn't have the `--initial` argument, but unless you're in the habit of sprinkling tab characters inside string literals, you can safely leave it off.


## Doing it

Here's the good part.

If at all possible, get all your collaborators to stop doing work for a day while you get this sorted.  Christmas works pretty well!  I did this on December 26, when we were so short-staffed that there weren't even any deploys scheduled.

### Invoking Git's nuclear option

First, create or amend `.gitattributes` in the root of your repository with the following:

    :::text
    *.py    filter=spabs

You can add as many source-like filetypes as you want by adding more lines with different extensions.  I converted everything I could find that we'd used in any repository, including but not limited to: `.css`, `.scss`, `.js`, `.html`, `.xml`, `.xsl`, `.txt`, `.md`, `.sh`, etc.  (I left `.c` and `.h` alone.  It seemed somehow inappropriate to change tabbed C code.)

Here's a brief explanation.  [`.gitattributes`][gitattributes] is a magical file that tells Git how to handle the _contents_ of files.  The most common use is probably line-ending conversion behavior for projects edited on both Windows and Unix; I've also seen some use of it to define language-aware diffing for certain files (i.e. for each hunk, figure out what function it lives in, and put the function name in the hunk's header line).

What I've done here is add a custom _filter_, i.e. a program run on checkin and checkout.  The actual program, `expand`, was listed in the Git configuration you (hopefully) distributed to everyone.  When Git sticks a file in the repository (via `add`, `commit`, whatever), it runs the `clean` filter; when it updates a file on disk based on the repository, it runs the `smudge` filter.  In this case I want to be extra sure there are never any tabs anywhere, so I made both filters do the same thing: convert all leading tabs to four spaces.  (The `required` line from the config will cause Git to complain if `expand` doesn't exit with 0 — that means something has gone _really_ wrong.)

This isn't perfect, as we'll see later, but it's some gentle protection against letting tabs sneak into your codebase.  I hope we can all agree that mixing tabbed lines with spaced lines is far worse than either tabs or spaces.

If you like, you can commit `.gitattributes` separately.  If you do, **DO NOT PUSH YET**.

### Performing the conversion

I'm paranoid, and Yelp's codebase was colossal, so I wrote a whole script that inspected every single text-like file in the codebase and manually ran `expand` on it and very carefully and idempotently adjusted `.gitattributes`.  The nice thing about this was that anyone else could then run the script against one of Yelp's myriad smaller repositories, without having to understand any of this Git witchcraft.  (Gitchcraft?)  Unfortunately, I quit and don't have it any more.

The much faster way to do this is:

    :::zsh
    git checkout HEAD -- "$(git rev-parse --show-toplevel)"

This asks `git checkout` to re-checkout every single file in your whole repository.  As a side effect, the `smudge` command will be run, converting all your tabs to spaces.  You will end up with a whole lot of whitespace changes.

You may want to run your test suite right about now.

Then, commit!  As per Yelp tradition when rewriting every single file in the whole codebase, I attributed the commit to Yelp's lovable mascot [Darwin][].  It stands out better in `git blame`, _and_ it preserved the _extremely critical_ integrity of my commit stats.

Push to master and you're done.  More or less.


## Effects on Git

I think somewhere in the neighborhood of two million lines were affected, and Git handled it surprisingly well.  The commit was basically instant, and there weren't any noticeable performance problems going forward, save for a couple minor wrinkles explained later.

The impact on Git workflow is fairly minimal.  Most of the complications will happen to people who are performing casual wizardry anyway and thus probably know a little bit about what they're doing.  Developers who just commit and merge shouldn't have any problems.

* A fresh checkout of the repository (or master, at least) will contain spaces, of course, because the checked-in files contain spaces.

* Any inflight branches will contain tabs, because they haven't seen the `.gitattributes` file or the mass conversion commit.

* Merging an inflight branch with master (in either direction) will transparently convert all the tabs on the branch to spaces _before_ merging.  The developer shouldn't even notice that anything special happened at all.

    This is the magical thing the `merge.renormalize` setting does.  `renormalize` is an option for the default merge strategy (`recursive`) that applies filters before performing the merge; the `merge.renormalize` setting turns it on by default for `git merge`.  Since the merged `.gitattributes` contains the filter, it gets applied to both sides.  I think.

    Note: I don't know if `renormalize` works with more exotic merge strategies.  I also don't know what happens if there are merge conflicts within `.gitattributes` itself.

    Note 2: `renormalize` _does not apply_ to new files created in the branch — they only exist on one side, so there's no need to merge them.  See below.

* Rebasing an inflight branch **will not work**, or more precisely will produce a zillion merge conflicts.  `merge.renormalize` doesn't apply to `git rebase`, and there is no `rebase.renormalize` setting.

    Luckily, you can do the same thing manually with `-X`.  `git rebase -Xrenormalize origin/master` should work fine.

    `-X` is supported by all Git commands that do anything resembling a merge, so the same applies to e.g. `git cherry-pick` or `git pull --rebase`.  You can use it with `git merge`, as well, but the setting makes it unnecessary.

* Old stashes probably won't apply cleanly, and `git stash apply` tragically ignores `-X`.  I know of two workarounds:

    1. Convert the stash to a branch with `git stash branch`, then merge or rebase or whatever as above.

    2. Apply the stash _manually_ with, e.g., `git cherry-pick 'stash@{0}' -n -m 1 -Xrenormalize`.  You need the `-m 1` ("use diff against parent 1") because under the hood, a stash is a merge between several distinct commits that hold different parts of the stash, and cherry-pick needs to know which parent to diff against to create a patch.  `-n` just prevents committing, so your stash description of "wip: this doesn't fucking work" isn't automatically turned into a commit message.

* Blame is not, in fact, permanently ruined.  `git blame -w` ignores whitespace-only changes.

* The total size of your repository will increase, but not by nearly as much as you'd think.  Git ultimately stores compressed binary patches, and a patch that contains mostly the same two characters compresses _really well_.  I want to say Yelp's repository only grew by 1% or so.  (The increase may be larger short-term, but `git gc` will eventually compress it all away.)


## Possible fallout

Relatively minor, considering the magnitude of the change.  Some short-term, some persisting for the life of your project, sorry.

### Old branches that introduced new tabbed files

About a week after the conversion, as developers trickled back from being on vacation, there was a sudden surge of confusion about a phantom file listed in `git status`.  It would be marked as modified, and no amount of `git checkout` or `git reset` would make it go away.  Everyone with this problem saw the same file marked as modified, but nobody had touched it.

It turned out that someone had had an inflight branch with a _newly-created_ file, indented with tabs.  This branch had been merged into master about a week after the conversion, and developers were seeing the new file show up as phantom-modified after their next interactions with master.

The problem was that git dutifully applied the `smudge` filter when checking this file out, converting it to spaces on-disk...  but the copy in the repository _still had tabs_, making it appear modified.  `git checkout` didn't fix this because it had caused the problem in the first place: a checkout would again run the filter and produce a modified file.  (I suspect this wouldn't have happened if our `clean` and `smudge` had actually been inverses and the repository had remained tabbed, but we explicitly didn't want that.)

Fixing this was simple enough: I told everyone to just commit the phantom changes in a separate commit whenever this happened.  (If the file had also been modified, `git diff -w` would show a "clean" diff.)  The whitespace change would happen in multiple commits, but they'd all merge cleanly as they hit master, since they all contained the same change.  Once the checked-in copy of the file contained spaces, the problem disappeared.

I saw a few instances of this over the first few weeks, but they all sorted themselves out as devs committed Git's whitespace change.  I think it could've been prevented with a clever git hook that applies filters to new files during a merge, but that would've been much more complicated.

### Intermittently slow `git status`

One or two developers saw `git status` be preposterously slow, taking a minute or more, rather than less than half a second.

Some `strace` revealed that `expand` was being run tens of thousands of times.  Whoops!

The developers who ran into this ended up making a fresh clone, which mysteriously resolved the issue.  My best guess is that we were accidentally hitting the slow path in `git status`—the solution to the ["racy Git" problem][racy git].  I had to do some guessing here, because the implications aren't fully described in that documentation, and very few people seem to have ever run into this.

Essentially, Git cheats a bit to keep "is this file changed?" fast: it compares only file _stats_, like size and mtime.  Git has a file called the "index", which contains, well, the index: it's a description of what the next commit will look like if you run a plain `git commit`.  The index also remembers which files on disk were modified, as of the last time it was written.  So if a file's mtime is older than the index's mtime, it's safe to assume the index is still correct.  But it's also possible that a file was changed in a way that kept its size the same _immediately after_ the index was last written — so quickly that the mtimes for both are identical.

To fix this, if Git sees a file that it thinks is unmodified, and the mtime is _exactly_ the same (or newer, of course) than the index's mtime, Git will compare the file's full contents to whatever's in the index.  Naturally, this takes much longer than just `stat`ing a bunch of files.

Now imagine someone switches from a very old branch to master.  A great many files are updated in the process, but the machine is fast enough that all the updated files _and_ Git's index end up with the same mtime.

I only discovered this explanation after all the affected developers had given up and recloned, so I never found out for sure whether it was the true case, and I never saw it happen again.  But that seems plausible.

If you find yourself with an index with a slow cache, you just need to do something that updates the index.  Read-only commands like `git status` or `git diff` won't do it, but `git add` will.  If you really don't have anything to add yet, you can force an update manually:

    :::zsh
    git update-index somefile

`somefile` can be any arbitrary file that's in the repository.  This command forces Git to examine it and write its modifiedness to the index—as a side effect, the index will now be updated.


## Final cleanup

Once everything has settled, you may want to remove all the filter stuff and just add a pre-commit hook that rejects tabs outright.

You can also tell your developers that they can _finally_ remove all their `.vimrc` hacks for switching to tabs specifically in your codebase.  (Maybe tell them they should've been using [vim-sleuth](https://github.com/tpope/vim-sleuth).)


[Darwin]: http://www.yelp.com/biz_photos/yelp-san-francisco?select=EkcG_DQeT9VWS0uRkHMAOg#EkcG_DQeT9VWS0uRkHMAOg
[PEP8]: http://www.python.org/dev/peps/pep-0008/
[unixutils]: http://unxutils.sourceforge.net/
[gitattributes]: http://git-scm.com/docs/gitattributes
[racy git]: https://github.com/git/git/blob/master/Documentation/technical/racy-git.txt#L123
