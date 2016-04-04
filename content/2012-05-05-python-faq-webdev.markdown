title: Python FAQ: Webdev
date: 2012-05-05 21:22
tags: python, web
category: blog

Part of my [Python FAQ][].

**I only know PHP.  How do I write a Web application in Python?**

<!-- more -->

This is a deeply complex question.  I could easily fill a _book_ on web development and Python and how to make the two interact, so I was hoping to put this one off for a while.  But given that I just [trashed PHP rather harshly][PHP sux], it seems prudent to answer it sooner rather than later.

The dead simple answer is to stop reading here, get [Flask][], and start building a thing.  I prefer a bit more nuance, though.

This _is not_ a tutorial.  I may write one in the future, but for now, plenty of them already exist, and I assume you can read documentation.  Instead, this is an overview of the current state of affairs for someone new to Python web development.

## Getting started

Obviously, you'll need to have Python installed.  Be sure to use Python 2, not 3; Python 3 made some backwards-incompatible changes, and not all libraries have updated yet.

For installing Python libraries, consider [`pip`][pip].  (If you're on a Unixlike, you can probably get it from your package manager, or with `easy_install pip`.)  `pip` is a little package manager for Python; it can easily install, remove, upgrade, and examine Python libraries.  Use your system package manager whenever possible, of course, but use `pip` for everything else.

You can install Python libraries to your home directory with `pip install --user ...`, but it's even better to keep libraries local to each project you work on—that way, you can upgrade dependencies for one project without potentially breaking all the others.  (Or breaking system software written in Python.  I have done this.)  [`virtualenv`][virtualenv] helps with this by creating a separate Python installation with a single command.

And, of course, you're already planning to use source control.  _Right?_  I like [git][], but anything is better than nothing at all.


## Framework

The first hurdle is somehow connecting your code to a browser.  In PHP, the simplest thing is to install Apache and point it at some files.  In Python, as with larger PHP projects, you'll generally do this with a web framework.

Frameworks all tend to have a similar workflow:

1. Install it, with a tool like `pip`.

2. Create a skeleton project.

    The complexity of the skeleton varies.  In the now-defunct Pylons, you'd end up with a good chunk of somewhat-mysterious code that you had to manually upgrade for new releases.  Flask is so simple that there _is_ no skeleton.  Somewhere in the middle is Pyramid, where a skeleton project is nothing more than some common boilerplate that you'd end up writing yourself if you started from scratch.

3. Configure some things, like databases.

4. Start up the development server.

    This tends to be a terminal program that runs your app without need for a dedicated HTTP server.  It'll reload your code when it changes, and spit out stack traces and other debugging information.

5. Hack away!

What, then, should you use?  There are zillions of options, but a few that are clearly the most popular.

I'm a fan of [Pyramid][], which hits a sweet spot somewhere between minimalism and batteries-included monolith.  It's a somewhat recent contender, but it evolved from two older and well-established projects; the result is well-designed, well-documented, and fairly transparent.  A simple app needs no automatic boilerplate at all, there are skeletons to get you up and running, and the core library is overflowing with extension points.  There's a growing collection of helpful addons, as well.

For an even quicker start, [Flask][] is about as simple as it gets, but has plenty of room to grow with crazy amounts of extensibility if you're willing to build on top of it.  It's designed to do fairly reasonable things out of the box, without forcing much on you.

[Bottle][] is similar to Flask, though arguably even simpler: it's distributed as a single file and has zero dependencies.  Whether this is good or bad is up to you, but it does mean that nothing in Bottle will be shared with any other framework, ever.  Admittedly I don't know too much about it, but I gave it a brief shot once and didn't have any major complaints.

On the other end of the spectrum, [Django][] is a massive beast designed for CMS-likes and other content-rich sites.  It has a large ecosystem of pluggable components, built-in everythings from templates to an ORM, and piles of documentation and community resources.  Django is generally cited as the Python equivalent to Ruby on Rails.  The downside is that convincing it to do things it doesn't want to do can be...  awkward.  (Many of the more obtuse questions in `#python` are caused by attempts to tinker with Django.)  Possibly a little heavy for a first attempt.

[web2py][] exists.  I, er, don't know much else about it.  Allegedly it injects variables into your modules' namespaces, and that's gross, so don't use it if you care what I think is gross.  Or do.  Whatever.

There used to be a `mod_python` Apache module that was spiritually similar to `mod_perl`, but it's long since been abandoned.  Please **do not** use it.

Lastly, you _can_ write Python web code "manually", but that's largely an exercise in frustration.  It's not faster, it's not educational, it's not really very useful.  Don't bother.

My suggestion?  If you just want to tinker, start with Flask and add on stuff as you go.  If you have an idea for a site in mind and want to hit the ground running, use a Pyramid scaffold and follow along with its narrative documentation.


## Routing

While PHP executes an entire file based on the URL, Python web applications tend to "own" an entire directory structure (or even the entire domain).  Connecting particular URLs to particular code is thus a bit more flexible, and is usually handled by a routing system.

Routes are URLs with optional placeholders, like these:

    /users/{name}
    /companies/{id}/products
    /blog/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}/{title}

You'd attach a route like this to a function.  Then when you browse to `/users/eevee`, that function would be run, and the placeholders would be available in a structure like `dict(name=u'eevee')`.

Some frameworks (like Pyramid) take this a step further: instead of attaching a route directly to a function, you give the route a _name_, and then attach the name to the function.  It's a little extra work, but the advantage is a central list of every page in your app.  You can also use a route name and placeholder values to generate a URL—then, later, you can change a URL in a single place without touching anything else, and a typo in development will cause an error instead of a 404.

The syntax and exact implementation varies a little, but every framework uses some variation of this system.  Some have helpers for creating RESTful routes or other common patterns, or you can easily write your own.


## Request cycle

An HTTP request tends to run a function somewhere (chosen by the router) and pass it a `request` object.

The request object's exact interface will depend on the particular framework, but they tend to be similar: parsed query data, cookies, headers, and so forth.  As an example, take [`webob`][webob]'s `Request` object, which includes:

* `request.GET` and `request.POST` are "multidicts" of parsed query data.  (A multidict returns a single value for `request.GET['foo']`, but exposes all values with a `getall()` method.)
* `request.params` is a multidict combining both of the above.
* `request.cookies` is a parsed dict of cookies.
* `request.headers` is a dict of HTTP request headers, but with the keys treated as case-insensitive.
* `request.is_xhr` returns whether the `X-Requested-With: XMLHttpRequest` header is present, to identify ajax requests from libraries like jQuery that set it.

Request objects tend to be pretty thoroughly documented, so just have a flip through the docs of your chosen framework and pick out the important stuff.

When your app is done doing whatever cool thing it does, you send back a response.  You usually have the option of either explicitly constructing a `Response` object (including HTTP headers and other manual fiddling) or just returning a chunk of HTML and using the defaults for everything else.  You very rarely need to create a response yourself; for common cases like returning JSON, every framework has some shortcut or helper decorator.


## Templates

Assembling HTML tends to be done with a template engine.  The two major contenders are [Mako][] and [Jinja2][].

I really like Mako.  Really, really, really.  Go use it.  It uses unadorned Python for its syntax, and manages to do so in a very natural way.  You can even write blocks of pure Python within templates, though of course you should exercise restraint and do this as little as possible.  :)

Jinja2 is _okay_, with a gruff caveat: `foo.bar` is treated as `foo['bar']` if `foo` looks like a dict and vice versa.  I happen to think this is a really bad idea, and have been bitten by numerous subtle problems it causes in multiple template systems with the same "feature".  (Also, the `{{ }}` syntax is really noisy, but that's splitting hairs.)  That aside, Jinja2 is a plenty solid library and you could definitely do worse.  [Much, much worse.][Cheetah]

Both of these tools are pretty speedy, automatically compile to Python modules behind the scenes, have excellent debugging (with crazy hacks to get stack traces from your original template source), and should be plenty powerful enough to do whatever you want.  Have a glance over both, pick one, and get going.  If you don't know or care which to use, use Mako.

(Note that while Flask uses Jinja2 by default, it's [fairly easy][flask-mako] to use Mako instead.)

There are some other contenders, of course: the third-place winner is probably Genshi, but it's so incredibly convoluted that the [homepage](http://genshi.edgewall.org/) starts off with a flow diagram; Django has its own template engine that tries very hard to keep logic out of your templates (imo to its detriment); Bottle likewise has its own drop-dead-simple templates that will probably cause growing pains pretty quickly; Pyramid's other builtin template engine is Chameleon, which uses HTML-ish attributes for loops and other logic, and that's fucking batty.

Maybe you'll like one of these; I haven't used them non-trivially myself.

Whatever you do, do not use Cheetah.  **DO NOT** use Cheetah.  It is an unholy abomination.  Let's not speak of it further.


### Logic in templates

Perhaps you haven't used templates before.  If so, you'll inevitably run into the question of whether some complex rendering code should live in Python or live in your template.

This is an old and silly argument, but I will say this: like many architectural decisions in programming, it comes down to minimizing how much you'll hate yourself for it later.  Keep complexity out of your templates if you can, but don't jump through hoops to avoid it if you can't.  Remember that you can always just write plain Python functions in plain Python modules and import them.  A powerful template language might even have a creative solution to your problem built in; glance over the docs again while you're thinking.


### Unicode

Unicode sucks.  This is a universal truth.  (I'm lying.  Dealing with _encodings_ sucks.  Unicode is great.  It's complicated.  I'll write about it later.)

Python (2) has two "string" types: `str` and `unicode`.  There's a clever lie here, and that is: a `str` isn't really a string.  It's just a series of bytes.  Sometimes that happens to _look_ like a string, but it's really just a binary representation, the same way `85 00 00 00` is a common binary representation of the number 133.  A _real_ number is an `int`, and a _real_ string is a `unicode`.

The issue is complicated enough to deserve its own article (which I will totally write sooner or later), but some quick notes:

* Your program should only worry about real strings (that is, `unicode`s) internally.  You have to decode strings that come into your program and encode ones that leave, but luckily, most web frameworks will do that for you.
* You can use the `u` prefix on a literal string to make it a `unicode`, e.g., `u'foo'`.
* You can use `from __future__ import unicode_literals` at the top of a file to make _all_ literal strings within that file be `unicode` by default.  If you really really want a `str`, use a `b` prefix.
* If you want to use non-ASCII characters in Python source code, add an `#encoding: utf8` magic comment to the top.  (Assuming of course that your source code is saved as UTF-8, which it had damn well better be.)
* **NEVER** solve a Unicode problem by stripping out non-ASCII characters!  That's incredibly rude to a huge number of people; just imagine how you'd feel trying to use a website that decided you weren't allowed to use English letters, because some programmer was too lazy to figure out how to handle them.
* In fact, accented letters and Asian characters are great for shaking out encoding problems.  Paste some non-ASCII gibberish into forms on your site and see what happens.


### XSS

Virtually everything nowadays has some form of automatic HTML escaping filter built in.  The idea is that a template like this:

    <p>Hello, ${name}!</p>

will, when given `name = '<b>'`, safely print out `Hello, &lt;b&gt;!`.  This means that, for the most part, you don't have to worry about XSS.

For the _most_ part.  If nothing else, you _must_ check the docs for your framework and template engine to make sure this is turned on by default, or turn it on if it's not.  (Off the top of my head: you get it for free with Pyramid, Django, and Flask.  Bottle does it automatically if your template file has an HTML-sounding extension.)

The tricky bit, then, is knowing when and how to turn it _off_.  If you construct some complex HTML in Python code, you don't want it all escaped when sticking it in your template.  Merely disabling the escaping behavior is a crappy solution, though; anywhere you do it is a potential source of injection.  Luckily, many frameworks (Pyramid and Flask, at least) use the [markupsafe][] library, which cleverly helps avoid this problem.

markupsafe provides a single class, `Markup`, which inherits from `unicode`.  `Markup(u'Hello!')` will produce an object that acts pretty much like a string.  The classmethod `Markup.escape` works the same way, but it escapes any HTML characters in the wrapped string.

There are two sneaky tricks here.  The first is that a `Markup` object will never be escaped a second time.  Observe:

```python
>>> s = u'<b>oh noo xss</b>'
>>> Markup.escape(s)
Markup(u'&lt;b&gt;oh noo xss&lt;/b&gt;')
>>> Markup.escape(Markup.escape(s))
Markup(u'&lt;b&gt;oh noo xss&lt;/b&gt;')
```

So once you've created a `Markup`, you can feed it to your template, and the filter will leave it alone—even if it contains HTML.

The other trick is that `Markup` overrides _every string method_ and automatically escapes all the arguments.  That means you can do stuff like this in Python land:

```python
>>> user_input = u'<script>alert("pwn");</script>'
>>> Markup(u'<p>Hello, %s!</p>') % user_input
Markup(u'<p>Hello, &lt;script&gt;alert(&#34;pwn&#34;);&lt;/script&gt;!</p>')
```

You can thus build complex HTML fairly safely, without worrying too much about underescaping or overescaping.

It's not perfect, of course; the primary gotcha is that you need to use `Markup().join(...)` on a sequence of other `Markup` objects, not `''.join(...)`.  And some operations like slicing, splitting, and regexes are likely to produce nonsensical results.  **Never** try to decompose a `Markup` object or any other string of HTML; if you absolutely must, use a real parser like `lxml`, but in most cases you can do whatever transformation you need on a plain string before wrapping it in HTML.


## Forms

I hate all form handling libraries.  Every single one.  They all enforce the author's crazy naming scheme on my forms.  I don't even like the PHP behavior of using `foo[]` as a field name; that's just so astoundingly ugly.

The one I hate the least so far is [wtforms][]; it enforces fairly few design constraints and is pretty simple to use.  It even has built-in support for working with markupsafe.  The major downsides are that it's difficult to remove those few design constraints (every form element gets an `id` attribute matching its name—_argh!_), and implementing a new kind of field can be a little complex.

I can't speak much to any others, alas.  [FormEncode][] is a thing.  Pyramid's maintainers also own [deform][].  They both do some dumb thing that bothers me for really nitpicky reasons.  Shop around.

Whatever you do, just make sure you use _something_ before your project grows too big.  The one thing I hate more than form handling libraries is writing validation code by hand.  :)


### "Sanitizing"

A note on a common trend in PHP land.

**Do not** "sanitize".

The word itself makes no sense.  There is no process by which you can take an arbitrary string and make it "safe".  This kind of thinking is why I keep running into bank websites with contact forms that tell me I can't use the `<` character; some numbskull enterprise developer doesn't have a clue how to deal with data, so he just enforces that all data must be idiot-proof.

Don't be an idiot.

Most of the time, "sanitizing" is referring to making user input "safe" to embed in HTML, pass to SQL, or use as a command-like argument.  You can do all of these things without changing the original data at _all_.  For HTML, there are filters like markupsafe, mentioned above.  For SQL, there are bound parameters and ORMs.  For running commands, you should avoid the shell entirely and just pass the arguments as a list (see [`subprocess`][subprocess]).

These are all problems of language barriers: HTML, SQL, and shell are all structured languages, and you can't just dump mystery junk into them and hope for the best.  You wouldn't use string concatenation to create JSON, so don't do it to run `convert`.  Use tools that understand the underlying structure.

This isn't to say that you should never modify or filter user input, but you should avoid it whenever possible, and be damn careful when you do.  For a common example of passwords, why is it so common to prohibit spaces in passwords or limit them to 16 characters?  There's no clear reason; it's just a thing that's done.

I'm still baffled by this one: the same places that cry foul when I try to type a `<` also insist that I type my credit card number as a solid string of sixteen digits.  That makes it really hard to verify at a glance that I typed it correctly—and besides, the number _on my card_ has spaces in it!  Why not strip spaces and hyphens?

Just think carefully about what you're doing and what problem you're trying to solve.  Are people using Unicode right-to-left characters to do dumb things to your site, and you want to stop them?  No reason to force everyone to use ASCII; Unicode has [categories][unicode categories], and you could just filter out characters in the weirder categories.  Better yet, just fix your website so people who speak Hebrew can use it.  :)


## Debugging

If you're lucky (i.e., using Pyramid), when your program crashes, you'll get an interactive debugger that lets you examine the live state of your program.  You can run arbitrary Python code, look at the state of variables, walk the stack, and otherwise screw around.

If you're unlucky, don't worry; you can still get this by using the [werkzeug debugger][].  It's pretty simple to use; it wraps any WSGI application and catches exceptions.  (See?  WSGI is awesome.)

Just make sure you don't leave debugging on when deploying your app or otherwise sharing it with others; "arbitrary Python code" means anyone seeing the debug screen can do anything to your computer that you can.


## Databases

What a can of worms.  This is as opinionated as I'm going to get.

For one: you should use an ORM.  That's a thingy that tries valiantly to map database tables to Python classes, rows to objects, and queries to method calls.  The result is more concise, often easier to understand, and sometimes even more correct.

The ORM you should use is [SQLAlchemy][].  Pyramid has some builtin support for it; if you're using a framework that doesn't, SQLAlchemy is popular enough that the framework documentation assuredly has instructions for wiring it in.  If you're using Django, it has its own ORM; it's not as good as SQLAlchemy, but replacing it is more of a bother than it's worth unless you have a compelling need.

Many detractors will tell you that ORMs generate bad SQL.  Yes, bad ORMs will do this.  Good ORMs, like SQLAlchemy, understand SQL as well as you do.  If you understand SQL, SQLAlchemy will be great for you; if you don't understand SQL, SQLAlchemy will at least save you some embarrassment by writing bad SQL in your stead.  Remember that you can always look at the queries being run; SQLAlchemy can log them all, and various debug toolbars will show a list with execution times.  (Also keep an eye out for the same query being run many times; that's a sign you want some eagerloading.)

Next, _use transactions_.  You hopefully don't have to think about this too much; if a framework has any SQLAlchemy integration at all, it probably does this for you.  The idea is that a transaction starts when a request starts, and it's automatically rolled back if there's an exception.  This is behavior you want _from the start_!  It's half (err, ¼) the point of using a database.

One more thing: since this article is all about trying new things based on what I say, **do not use MySQL**.  In every sense I can imagine, MySQL is the PHP of databases.  Give [PostgreSQL][] a spin; it's no harder to set up, it's nicer to use, and it won't let you do dumb things like store strings in date columns.  (One of the nicest things, imo, is that Postgres can use your Unix user account as a login; no passwords required.)  The only argument anyone ever has against using Postgres is that it "doesn't scale"; rest assured I've yet to see an actual demonstration of that, and either way you can worry about it when you have a million more visitors.


## Sessions

Every framework has session support.  It'll look familiar: a session token is stored in a cookie, and on the backend you magically get a dict that you can store arbitrary junk in.  Use this as you will.  Try _not_ to use it as a dumping ground; it turns out databases are pretty good for, y'know, storing data.

Bonus features include first-class support for CSRF protection (Pyramid, Django has a module) and flash messages (Pyramid, Flask, Django).  Go read your docs.

One word of warning: if you're using Beaker sessions (Pyramid), they tend to accumulate cruft.  By default this is in the form of a file on disk for every session ever, but if you use db-backed sessions, you'll end up with a massive sessions table that never shrinks.  This is a terrible and non-obvious problem, and the fixes are all basically manual.  Sorry.


## Deployment

Ah, you got me.  There are a lot of ways to deploy, and they deserve more screen time than I can really devote here.

If possible, be willing to spend money.  Providing a service inherently has a cost.  It's easiest by far to deploy apps if you just have your own dedicated (virtual or not) machine to play around with—and a server is a cool thing to have on hand anyway.  You can get a basic [Linode][] for $20/mo., and cheaper providers exist (though are less cool).

[Heroku][] is also an option, and _does_ have a free tier of one worker (similar to the lowest-tier Linode), but it's another $36/mo for every extra worker you add.  (The number of requests you can handle simultaneously is roughly proportional to the number of workers you have.  How many you _need_ depends on your app and how you run it.)  The upside is that deploying your app is pretty much turnkey.  Heroku has a few clones by now, as well.

As they say (do they?), deploying is a good problem to have: it means you've actually built something useful, after all.  So go build something while I scramble to write a whole thing about deployment options.


## Conclusion

The Web is complex.  There are a lot of moving parts.  Smart people have solved a lot of problems for you.  Go tinker.

I hope this is enough to get you started!

And as always, I don't know what I'm doing, so please tell me how to do it better.


[Bottle]: http://bottlepy.org/docs/dev/
[Cheetah]: http://www.cheetahtemplate.org/
[Django]: https://www.djangoproject.com/
[Flask]: http://flask.pocoo.org/
[FormEncode]: http://www.formencode.org/en/latest/index.html
[Heroku]: http://www.heroku.com/
[Jinja2]: http://jinja.pocoo.org/
[Learn Python The Hard Way]: http://learnpythonthehardway.org/book/
[Linode]: http://www.linode.com/?r=c5316aa7d1cfce6f5fe611bb455ef1548cc1946c
[Mako]: http://www.makotemplates.org/
[PHP sux]: /blog/2012/04/09/php-a-fractal-of-bad-design/
[PostgreSQL]: http://www.postgresql.org/
[Pyramid]: http://www.pylonsproject.org/
[Pyramid documentation]: http://docs.pylonsproject.org/en/latest/docs/pyramid.html
[Python FAQ]: /blog/2011/07/22/python-faq/
[SQLAlchemy]: http://www.sqlalchemy.org/
[WSGI]: http://wsgi.readthedocs.org/en/latest/index.html
[canon Python tutorial]: http://docs.python.org/tutorial/
[deform]: http://docs.pylonsproject.org/projects/deform/en/latest/index.html
[flask-mako]: https://github.com/tzellman/flask-mako
[git]: http://www.git-scm.com/
[markupsafe]: http://pypi.python.org/pypi/MarkupSafe
[pip]: http://www.pip-installer.org/en/latest/index.html
[subprocess]: http://docs.python.org/library/subprocess.html
[unicode categories]: http://www.fileformat.info/info/unicode/category/index.htm
[virtualenv]: http://www.virtualenv.org/en/latest/index.html
[web2py]: http://www.web2py.com/
[webob]: http://docs.webob.org/en/latest/modules/webob.html
[werkzeug debugger]: http://werkzeug.pocoo.org/docs/debug/
[wtforms]: http://wtforms.simplecodes.com/docs/dev/
