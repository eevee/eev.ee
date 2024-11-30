title: The sad state of web app deployment
date: 2015-09-17 18:41
category: articles
tags: systems, web, tech, yelling, popular

I spent a good chunk of the last four days installing an Internet web forum, which claims it can be up and running in 30 minutes.

I like to think I'm pretty alright at computers.  So what went wrong here?  _Well let me tell you._

<!-- more -->


## My arduous tale

I don't want to name and shame here, because this is not my first such experience and the problem is larger than one individual product.  (Let's just say it rhymes with "piss horse".)

The 30-minute claim came because the software only officially supports being installed via Docker, the shiny new container gizmo that everyone loves because it's shiny and new, which already set off some red flags.  I managed to install an entire interoperating desktop environment without needing Docker for any of it, but a web forum is so complex that it needs its own quasivirtualized OS?  Hmm.

I tried installing the vendor Docker (I'm using Ubuntu 14.04, the current LTS release), but that's 1.0, and Docker has gotten up to 1.7 in the intervening year and a half, and this software needs at least Docker 1.2.  I stress that this web forum is so cutting-edge that it refuses to install without technology that did not exist two years ago.

So I tried installing current Docker via the officially condoned mechanism, which of course involves piping `curl` into your shell.  That's a fucking appalling idea, but [security is kind of a joke with Docker anyway](http://reventlov.com/advisories/using-the-docker-command-to-root-the-host).  It also didn't work, giving me the rather useless `E: Unable to locate package docker-engine` instead.  I'm sure glad Docker exists, to save me from all those package management nightmares!

Some digging revealed that Docker just doesn't exist for 32-bit, even though they say it _should_ work (as evidenced by the existence of a canonical 32-bit Ubuntu package), and they just don't bother mentioning this in their README or installation docs or shell script that runs as root.

At this point I was pretty sick of Docker, so I decided to try installing the damn thing manually.  It was just a Rails app, after all, and I've managed to install those before.  How hard could it possibly be?

Ha, ha!  After a `git clone` (because the app isn't in rubygems??), I then spent maybe _six hours_ fighting with RVM.  (I'm sure you have a suggestion for a different Ruby environment thing I should be using instead, and I don't care, shut up, I already had RVM installed and running something else.)

The problem was some extremely obtuse errors when running `bundle install`, which is supposed to install all of the app's dependencies.  Some library was complaining that a `.a` file in its own build directory didn't exist, which didn't make a lot of sense.  Also, I spotted `x86_64-linux` in the path, which made even less sense.

See, I actually have a 64-bit kernel, but a 32-bit userspace.  (There's a perfectly good reason for this.)  And the Ruby binary that RVM built was, of course, 32-bit — it wouldn't have worked otherwise, since libc and everything else are all 32-bit.  But those binaries _thought_ they were on a 64-bit system (which they were), and rubygems uses the _system_ architecture for building native extensions for some stupid fucking reason, so everything was built as 64-bit.  In a way I'm lucky that this _one_ particular package happened to fail, because all the others built just fine, and I only would've found the problem later when I actually tried to run the damn thing.

I tried all kinds of environment variables and hand-editing of files and whatnot to convince Ruby that it was actually 32-bit, to no avail.  Eventually I resorted to reading a bunch of RVM's source code, and then I discovered a `--32` flag that magically fixes everything.  It's not documented, but don't worry!  I found [a GitHub issue comment from three and a half years ago, saying the docs will be fixed with RVM 2.0](https://github.com/rvm/rvm/issues/623#issuecomment-5201721).

So now I had a working Ruby, and after some tedious rebuilding, I had a set of gems as well.  Super.

Now I just had to figure out how to configure the damn app, which is tricky when the README just says "use Docker".  It had a `config/app.conf.sample` file, but this turned out to be sample configuration for Upstart, the Ubuntu service manager.  I ended up discovering that there _are_ still docs for installing on Ubuntu, just not linked from anywhere.

The next step was to migrate the database from "doesn't exist" to "exists", which is usually a breeze in Rails, by which I mean I have never once had it actually work without descending into a hellish nightmare and this time was no exception.  The documentation claims the app needs to be superuser.  Let's see what PostgreSQL says about superusers.

> Superuser status is dangerous and should be used only when really needed.

Yes, this definitely seems like something a web forum needs.  I opted _not_ to give it root on my entire database, which of course broke the migrations because they use `CREATE EXTENSION` to load binary extensions into my server, a perfectly reasonable thing for _database migrations_ to be doing.  I didn't even have the required extension installed, and of course the documentation never once mentions needing it, so off I went to install it.

I installed `postgresql-contrib`, and then some funny things happened.  Long story short, I was running Postgres 9.1, and the current Ubuntu version is 9.3.  I'd originally installed the `postgresql` package, and using Arch Linux on my desktop has spoiled me into thinking that that will keep me on the latest version, but Ubuntu cares about trivialities like "not breaking your entire server" and had just kept me on 9.1 the whole time.  But `postgresql-contrib`, unqualified, meant the current version _now_ which was 9.3, and had also installed the full server.  Whoops!  So I just took a quick detour to upgrade to 9.3, which I've done before and which is _relatively_ painless.

Okay!  Now I have a database.

At this point the docs take a wild detour into installing some Ruby process management library called Bluepill and copying some massive pile of "configuration" (actually just Ruby code, of course) and using that to run the app and also adding Bluepill to the user's crontab as a `@reboot` and what the ever-loving fuck.

(I assumed this was some oblique Matrix reference, but someone later pointed out to me that it's called _bluepill_ and it _keeps things up_.  Charming, but [par for the course for Ruby](http://unethicalblogger.com/2011/11/13/ten-poorly-chosen-gem-names.html).)

Anyway, I opted to _not_ do all that, and just ran the thing directly with `rails server`.

Almost done.  Now I just need to proxy nginx to it.  The app helpfully provides some configuration for me, which is _two hundred lines long_ and consists mostly of convoluted rules for which URLs are static assets and which should be proxied.  I decided to hell with it and just proxied the whole thing and I'll fix it later if I feel like it.

Now we're up and running!  Except I never get any signup email, and it turns out _this_ is because I _also_ have to run "sidekiq", a job processor.  And with that, _now_ we're done.


## What horror have we created

I tell you this story to make the point that this is all **completely fucking ridiculous**.

Set aside the oddball tool breakage and consider that if you follow [the instructions](https://github.com/discourse/discourse/blob/master/docs/INSTALL-ubuntu.md) to the letter, this _web forum_ requires:

* Cloning (not installing!) the software's source code and modifying it in-place.
* Copy-pasting hundreds of lines of configuration into nginx, _as root_, and hoping it doesn't change when you upgrade.
* Copy-pasting hundreds of lines of Ruby for the sake of bluepill, and hoping it doesn't change when you upgrade.
* Installing non-default Postgres extensions, _as root_.
* Running someone else's arbitrary database commands _as a superuser_.
* Installing logrotate configuration, _as root_.

There's nothing revolutionary here.  It's an app that wants to accept HTTP connections, use a database, and send email.  Why is this so fucking complicated?

_I'll tell you why—_


### Rails sucks

My experience is admittedly limited here, but as far as I can tell, _installing a Rails app is impossible_.  It reads configuration from the source directory.  It logs to the source directory.  You have to manually precompile all the assets, which are of course also written to the source directory.

Rails is one of the most popular web frameworks in the world, championed by developers everywhere.  And you can't actually _install_ anything written with it.  This is a joke, right?


### Unix lied to you

Back in the day, when Windows effectively didn't have users and everyone just ran everything as an administrator, Unix nerds (myself included) would crow about how great Unix was for making heavy use of separate users for everything.

Boy, do I have egg on my face.  Let's recap here:

* If you're missing a library or program, and that library or program happens to be written in C, you either need **root** to install it from your package manager, or you will descend into a lovecraftian nightmare of attempted local builds from which there is no escape.  You say you need `lxml` on shared hosting and they don't have `libxml2` installed?  Well, fuck you.
* Only one thing can bind to port 80 and it has to run as **root**, so your options are to use nginx and need root to add a new app, or use Apache and do `.htaccess` or something equally atrocious.
* You want your app to start automatically, of course.  You can add it to your crontab with `@reboot`, which is kind of a hack and also won't restart it if it dies.  So you can _also_ install your own local process manager, like this app did.  Or you can do what most people do and add it to the system's daemon manager, as **root**.  Allegedly many modern daemon manager things allow non-root users to set their own things up, but I've never seen this actually done or even explained very clearly.
* If you want to rotate your logs, well, that needs **root**.
* You think Docker solves any of this?  Let me know how piping `curl` to a shell script that uses `sudo` works out for you.  Oh, and [if you're in the docker group, you are **root**.](http://reventlov.com/advisories/using-the-docker-command-to-root-the-host)

Modern Linux desktops are pretty alright at the multi-user case, which basically no one uses.  On the server side, well, if you have a server everyone just assumes you have root anyway, so everything is a giant mess.  Even RVM, which is designed for having multiple per-user Ruby installations, prompted me for my password so it could `sudo apt-get install` something.


### It worked on my machine

We are really, really bad at enumerating and handling dependencies.

I mean, we can't even express them in our own software.  System package managers deal with it, and that's great — but I'm a developer, not a packager.  If I write a Python library that wraps a C library, there is _no way_ to express that dependency.  How would I?  There's no canonical repository of C/C++ packages, anywhere.  Even if I could, what good would it do?  Installing a shared C library locally is a gigantic pain in the ass, involving `LD_LIBRARY_PATH`, or maybe it was `LDFLAGS=-rpath`?  See, I don't even know.  Virtually no one does it, because it's a huge pain, because virtually no one does it.

So it should come as no surprise that there is no way _whatsoever_ to list dependencies on _services_.  You'd think that a web app could just have some metadata saying "I need Postgres and, optionally, Redis", but this doesn't exist.  And the other side, where the system can enumerate the services it has available for a user, similarly doesn't exist.  So there's no chance of discovery.  If you're missing a service the app needs but failed to document, or you set it up wrong, you'll just find out on the first request.

Speaking of:


### Web apps suck at reporting problems

For all the moving parts and all the things that can go wrong, there sure is a huge lack of reporting when it breaks.  I basically rely on people tweeting at me or asking on IRC if something is broken.  This particular app relied critically on a job queue, but didn't notice it _wasn't running_.

There are a few widgets that will email all crash logs to you, but what idiot came up with that?  That's completely fucking useless.  I have over two thousand unread crash emails for my perfectly functional modest-traffic website.  Almost all of them are some misconfigured crawler blowing up on bogus URLs in a way I don't strongly care about fixing.

But if the app goes _down_ and completely fails to start, I get _zero_ email.  If the app runs but every request takes 20 seconds, I get _zero_ email.  If every page 404s, I get _zero_ email.  And if real actual pages start to break, I get a flood of email that I'll never notice because I don't even look in that folder any more.

These are not unique problems.  Yet the only solutions I've seen take the form of dozens of graphs you're expected to keep an eye on manually.



## What we should have by now

We should have apps that install with one (1) command, take five minutes to configure, and scale up to multiple servers _and down to shared hosting_.  If I cannot install your _web forum_ on Dreamhost, you have failed spectacularly.

But we haven't even tried to solve this, and all the people who are most capable of solving it are too busy scaling Twitter or Amazon up to ten million servers or whatever.  Installing basic web software gets harder all the time, and shared hosting becomes less useful all the time, and web developers flock to garbage like Docker that basically runs a VM because we can't figure out how to make two apps use the same damned database.

The thing I want, but never figured out how to build, is an intermediate web app for the express purpose of installing and managing web apps.  Yes, sure, like cPanel or whatever, but not with ad-hoc support for some smattering of popular apps; I also want a protocol for apps to explain their own minimal requirements.

I want to be able to say "install the Ruby app 'pisshorse'".  And it goes and finds that gem.  And it sees what Ruby version it claims to work on, and installs an RVM environment with that version.  And it makes a new gemset and installs the gem.  And it looks at a metadata file in a Well-Known Place, and it sees that the file demands a Postgres database and a Redis instance.  And it inspects the common ways you might expect to be able to connect to Postgres or Redis.  And then it asks me where Postgres and Redis are, and it offers whatever it found as defaults, and it accepts something concise like `postgresql:///pisshorse` rather than ten separate fields that make no sense if you're not connecting over TCP.  And it double-checks that those are okay, and it writes them to a very small configuration file in `~/.config/webapps/pisshorse` or wherever.  At no point am I asked to configure some ridiculous value like the TTL of database connections, which _no one_ cares about and which the computer should be smart enough to gauge on its own.

If this is a shared host and you only have one Postgres database, that's totally fine, because this is a magical world where people actually know about and use Postgres schemata, and apps actually support them.

The metadata file also lists any system-level libraries or binaries that are required (or desired), and if any of them aren't installed, you'll be asked to install them, with a single `apt-get` or `yum` or `packer` command you can inspect and then run yourself.  Again, if this is a shared host and you can't install software yourself, then the installer can either attempt to do it locally or just give up, and everything's fine because it turns out web forums don't actually _need_ `optipng` and can just carry on without it.

Then it adds the app to your user-scoped daemon manager, and if you don't have one then it quietly pretends to be one, using the `@reboot` hack.  And it sees that the app also needs a job queue running, so it adds that too.  It uses gunicorn or unicorn or uwsgi or whatever, but you don't actually care which, and if you do then you can ask for a different one.  It defaults to only two workers, but it also keeps an eye on the load and spawns a few more if necessary, learning how much traffic is normal as it goes.  If it thinks it's eating too much of the machine, it sends you an email or pings you on IRC or whatever.

The app is bound to `~/.config/webapps/pisshorse/pisshorse.sock`, which isn't too useful to you.  And this is the hard part that I haven't figured out yet, because there's not really a good way to determine what your HTTP vhost setup looks like, and if you're using nginx then you still need root.  But I have ideas for a couple (convoluted) workarounds, so let's pretend that the world is a nice place and it can set up the reverse proxying for you, without needing root.  It even adds rules for caching the static assets (also defined in the metadata file), and perhaps can ask you for a CDN if you have one.

Now the app runs, but it has no users, and you can't log in because you don't have a confirmed email yet.  But that's okay, because the metadata file also specifies a few administrative commands you can run from the command line, and of course the magical web GUI can also do this for you.

From here you can basically forget about the management GUI.  But it quietly collects logs and stats, and there are graphs to look at if you please.  If at any point the app fails to start, or there's a sharp uptick in failures on pages that used to work, or it can't keep up with requests, or the job queue is broken, you get a ping.

Eventually you'll need to upgrade, and that's also fine, because it's just a single button click.  Your current instance goes into read-only mode, which is a thing that all apps support, because it would be embarrassing if they didn't.  The job queue is shut down, the database is _copied_ and upgraded, and a separate new instance of the app is launched.  New requests are directed to the new code, the old instance is shut down, and the old database is archived.  Or, if the new instance immediately starts to spew errors, the old code is kept up and an irate email is automatically sent to the app's maintainer.  Either way, the disruption is minimal.

And the app benefits as well, because it uses a small library that knows whether it's running under gunicorn or uwsgi or something else, and can perform some simple tasks like inspect its own load or restart itself or run some simple code outside a request.

I can dream.

We've been doing this for 20 years.  We should have this by now.  It should work, it should be pluggable and agnostic, and it should do everything _right_ — so if you threw away the web gui, it would look like something a very tidy sysadmin set up by hand, not autogenerated sludge.

Instead, we stack layer after layer of additional convoluted crap on top of what we've already got because we don't know how to fix it.  Instead, we flit constantly from Thin to Mongrel to Passenger to Heroku to Bitnami to Docker to whatever new way to deploy trivial apps came out yesterday.  Instead, we obsess over adding better Sass integration to our frameworks.

And I'm really not picking on Ruby, or Rails, or this particular app.  I hate deploying _my own_ web software, because there are so many parts all over the system that only barely know about each other, but if any of them fail then the whole shebang stops working.  I have at least five things just running inside `tmux` right now, because at least I can read the logs and restart them easily.

This is terrible and we should all be ashamed.  No wonder PHP is so popular.  How am I supposed to tell a new web developer that this is what they have to look forward to?
