title: Quick doesn't have to mean dirty
date: 2012-07-28 12:40
tags: python, tech, web, follow along
category: blog

From [TechCrunch][Quick and Filthy]:

> Anyway, my sympathy for PHP’s deviltry is because I appreciate its ethos. Its just-get-it-done attitude. Or, as Melvin Tercan put it in his recent blog post, “here’s to the PHP Misfits. The pragmatic ones who would pick up anything – even double-clawed hammers – to build their own future. Often ridiculed and belittled by the hip guys in class who write cool code in Ruby or Python, but always the ones who just get shit done.”
> 
> He’s on to something there. The best is the enemy of the good, and shipping some working PHP code is approximately a million times better than designing something mindblowing in Haskell that never actually ships. I fully support Jeff Atwood’s call to replace PHP once and for all–but I hope that everyone realizes that eliminating its many, many, multitudinous flaws won’t be enough; they’ll have to somehow duplicate its just-make-it-work ethos, too.

This is a recurring sentiment: developers telling me, well, yeah, Python may be all cool in your ivory tower, _man_, but like, I just want to write some programs.

To which I say: what the **fuck** are you people smoking?  Whence comes this belief that anything claimed to be a better tool must be some hellacious academic-only monstrosity which actively resists real-world use?

But, hey, I'm sick of talking about PHP.  So let's talk about Python.  In honor of the 90s, let's make a guestbook.

<!-- more -->


## Flask

[Flask][] is the thing you use to get up and running quickly.  Let's do that.  I don't think I've actually built a real thing with Flask, so this will be fun times for me, too.  I'm even doing this in REAL TIME.

    eevee@perushian ~/dev/blog ⚘ cd ~/dev
    eevee@perushian ~/dev ⚘ mkdir guestbook_demo
    eevee@perushian ~/dev ⚘ cd guestbook_demo
    eevee@perushian ~/dev/guestbook_demo ⚘ git init
    Initialized empty Git repository in /home/eevee/dev/guestbook_demo/.git/
    eevee@perushian ~/dev/guestbook_demo ⚘ mkdir guestbook_demo
    eevee@perushian ~/dev/guestbook_demo ⚘ touch guestbook_demo/__init__.py
    eevee@perushian ~/dev/guestbook_demo ⚘ pip2 install --user flask

Yes, my shell prompt ends with a flower.  (If I'm root, it's a [hammer and sickle][zshrc prompt].)

Make a directory, make a git repository, make a blank Python namespace to stick it in.  (I like to start with a package from the beginning—top-level things named "app" gross me out—but this is entirely optional.)  Install Flask.  `--user` installs it to my home directory; I probably could've gotten it from my package manager, but I was too lazy to look.  I have to say `pip2` because this is Arch Linux, which is a super special snowflake and considers Python 3 to be the default Python now.

Okay, write some code.  Look at all this boilerplate I had to copy from Flask's front page oh no!

###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/7fa216c5dc0f73615434d3812d69cfc88a16cfa1/guestbook_demo/app.py)
```python
from __future__ import absolute_import, unicode_literals

from flask import Flask
app = Flask(__name__)


@app.route("/")
def root():
    return "Wow this is totally useless so far!"
```
###### [guestbook_demo/__main__.py](https://github.com/eevee/guestbook_demo/blob/7fa216c5dc0f73615434d3812d69cfc88a16cfa1/guestbook_demo/__main__.py)
```python
from __future__ import absolute_import

from guestbook_demo.app import app

app.run()
```

Again, half of what I've done here is unnecessary.  The [`__future__`][__future__] stuff just makes some of Python's behavior a little nicer.  I made a file called `__main__` so I can run my app with `python2 -m guestbook_demo`.  I love `-m`.  Also, this avoids the `if __name__ == "__main__"` incantation.

Fire it up.

    eevee@perushian ~/dev/guestbook_demo ⚘ python2 -m guestbook_demo
     * Running on http://127.0.0.1:5000/

Click the link.  I have a website.  Hey, I didn't even have to install Apache.


## Templates

Well, no, first things first.

    eevee@perushian ~/dev/guestbook_demo ⚘ vim .gitignore
    # *.pyc
    # .*.swp
    eevee@perushian ~/dev/guestbook_demo ⚘ git add guestbook_demo/
    eevee@perushian ~/dev/guestbook_demo ⚘ git add .gitignore
    eevee@perushian ~/dev/guestbook_demo ⚘ git commit -m 'Initial commit'
    [master (root-commit) 7fa216c] Initial commit
     3 files changed, 16 insertions(+)
     create mode 100644 .gitignore
     create mode 100644 guestbook_demo/__init__.py
     create mode 100644 guestbook_demo/__main__.py
     create mode 100644 guestbook_demo/app.py

Okay, now templates.  Hurriedly consult [documentation][flask docs: templates].  Blah, blah, autoescaping, how do I [use it][flask tutorial: views].  Okay, so Flask looks for templates in a `templates/` directory by default.  How eerily convenient.

###### [guestbook_demo/templates/_base.html](https://github.com/eevee/guestbook_demo/blob/9aca69520bb5bd3dba18221ca2f2dab4161fa122/guestbook_demo/templates/_base.html)
```python
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{% block page_title %}{% endblock %}</title>
    </head>
    <body>
        <section id="content">
            {% block content %}
            {% endblock %}
        </section>
        <footer id="footer">
            My Cool Guestbook 2000 © me forever
        </footer>
    </body>
</html>
```
###### [guestbook_demo/templates/index.html](https://github.com/eevee/guestbook_demo/blob/9aca69520bb5bd3dba18221ca2f2dab4161fa122/guestbook_demo/templates/index.html)
```python
{% extends "_base.html" %}

{% block title %}Guestbook{% endblock %}

{% block content %}
    <h1>Guestbook</h1>

    <p>Hello, and welcome to my guestbook, because it's 1997!</p>

    <ul class="guests">
        <li>...</li>
    </ul>
{% endblock %}
```

And update the Python side.

###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/9aca69520bb5bd3dba18221ca2f2dab4161fa122/guestbook_demo/app.py)
```python
@app.route("/")
def root():
    return render_template('index.html')
```

Now we have some templates.  Hey, that wasn't too bad.  Could stand to have some data, though.


## An aside: debugging

I learned something doing this, because I made a typo in my template: Flask only does live debugging if I set `debug=True` when I run it.

###### [guestbook_demo/__main__.py](https://github.com/eevee/guestbook_demo/blob/5f9e225ed3960ddd8685399ad4f11f195293bab0/guestbook_demo/__main__.py)
```python
app.run(debug=True)
```

This also provides automatic code reloading.  Unfortunately, due to some arcane interaction between the reloader and `python -m`'s behavior, I have to use `PYTHONPATH=. python2 -m guestbook_demo` to run my app now.  Boo.  Look at the silly problems I've inflicted on myself.  That's what I get for not following the tutorial.

Incidentally, it seems that if I'm putting my code in a package, I oughta hardcode the package name instead of using `__name__`.  (The documentation for the `Flask` class explains this.)

###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/5f9e225ed3960ddd8685399ad4f11f195293bab0/guestbook_demo/app.py)
```python
app = Flask('guestbook_demo')
```


## Database

I like [SQLAlchemy][].  I could write a bunch of queries by hand for something simple like this, but honestly, fuck that noise.

First, I need a database.  (`createdb` is a PostgreSQL thing.  I'm amazed at how ballsy they are, claiming a generic name like that.)

    eevee@perushian ~/dev/guestbook_demo ⚘ createdb guestbook_demo

I don't need anything fancy for arranging the DB code, either.  Credentials should go in configuration, yadda yadda, but since I don't really need credentials here (Postgres can authenticate using my local Unixy login), who cares.

###### [guestbook_demo/db.py](https://github.com/eevee/guestbook_demo/blob/92f112dc3701ed5bd68a68c48a3a50b91694a113/guestbook_demo/db.py)
```python
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, Unicode

engine = create_engine('postgresql:///guestbook_demo')
session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base(bind=engine)


### Yonder tables

class GuestbookEntry(Base):
    __tablename__ = 'guestbook_entries'

    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    name = Column(Unicode, nullable=False)
    message = Column(Unicode, nullable=False)

    def __init__(self, **kwargs):
        kwargs.setdefault('timestamp', datetime.utcnow())

        super(GuestbookEntry, self).__init__(**kwargs)
```

This gives me thread-safe transaction support and a canonical copy of my schema with rather little effort or magic.  Most of this can be intuited from SQLAlchemy's hilariously extensive documentation.

Things to note:

* There's a `flask-sqlalchemy` package I could've used which saves a couple lines of boilerplate and automatically handles configuration, but I'm pretty comfortable with SQLAlchemy.
* I added a custom `__init__` that sets the timestamp for a new entry to the current time.  In UTC.  Always, always, UTC.
* I set `autoflush=False`, so I can do batched updates.  This won't really matter now, but it's nice to have from the beginning.

Also, `scoped_session` does some gross things to make a single session variable multiplex across threads, but it requires knowing when I'm done with a thread's session.  So I need this little guy in `app.py`.

###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/92f112dc3701ed5bd68a68c48a3a50b91694a113/guestbook_demo/app.py)
```python
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
```

This is one of those things `flask-sqlalchemy` would've done for me.  C'est la vie.

Create some tables:

    eevee@perushian ~/dev/guestbook_demo ⚘ python2
    Python 2.7.3 (default, Apr 24 2012, 00:00:54)
    [GCC 4.7.0 20120414 (prerelease)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from guestbook_demo import db
    >>> db.Base.metadata.create_all(bind=db.engine)
    >>> 
    eevee@perushian ~/dev/guestbook_demo ⚘ psql guestbook_demo
    psql (9.1.4)
    Type "help" for help.

    guestbook_demo=# \dt
                 List of relations
     Schema |       Name        | Type  | Owner 
    --------+-------------------+-------+-------
     public | guestbook_entries | table | eevee
    (1 row)

Okay, getting somewhere, but it's not very useful yet.

Let's add some data and display it.

    guestbook_demo=# insert into guestbook_entries values (default, now() at time zone 'UTC', 'Eevee', 'hello ur web sight is gr8');
    INSERT 0 1

###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/d2206df584d42ed70665b5a03a8c890883a0acd7/guestbook_demo/app.py)
```python
@app.route("/")
def root():
    # TODO paginate me!
    entries = db.session.query(db.GuestbookEntry) \
        .order_by(db.GuestbookEntry.timestamp.desc())

    return render_template('index.html', entries=entries)
```
###### [guestbook_demo/templates/index.html](https://github.com/eevee/guestbook_demo/blob/d2206df584d42ed70665b5a03a8c890883a0acd7/guestbook_demo/templates/index.html)
```python
    <ul class="guests">
        {% for entry in entries %}
        <li>
            <blockquote>{{ entry.message }}</blockquote>
            <p>— <cite>{{ entry.name }}</cite>, <time>{{ entry.timestamp }}</time></p>
        </li>
        {% endfor %}
    </ul>
```

Flask reloads itself, so I just need to refresh the page, and there it be.


## Spot the bug

I just noticed I didn't have a page title because I called the block `page_title` in the base template and `title` in the inheriting template.

Also, I have `import datetime` in my `db.py`, but it should be `from datetime import datetime`.  `utcnow` is a method on the class, not a function in the module.  (I wish the module and class weren't named the same; [who][i do] _does_ that?!)  The in-browser stack trace helpfully pointed this out to me.


## Signing it

Finally, this isn't very useful unless someone can write in it.  No surprises here; we have all the infrastructure and just need to make use of it.

###### [guestbook_demo/templates/index.html](https://github.com/eevee/guestbook_demo/blob/1b7c80fbd236923c17c14b0ace7bb3e741ca5ee1/guestbook_demo/templates/index.html)
```python
    <hr>

    <form action="{{ url_for('signme') }}" method="POST">
        <p>Name: <input type="text" name="name"></p>
        <p>Message: <textarea name="message" rows="10" cols="40"></textarea></p>
        <p><button>Sign</button></p>
    </form>
```
###### [guestbook_demo/app.py](https://github.com/eevee/guestbook_demo/blob/1b7c80fbd236923c17c14b0ace7bb3e741ca5ee1/guestbook_demo/app.py)
```python
from flask import Flask, redirect, render_template, request, url_for

# ...

@app.route("/sign", methods=['POST'])
def signme():
    new_entry = db.GuestbookEntry(
        name=request.form.get('name') or 'Some dummy who forgot to leave a name',
        message=request.form.get('message') or 'WOW THIS IS THE BEST WEBSITE EVER',
    )
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('root'))
```

Refresh, try it out.  Done.


## Deployment

Arrgh, that thing that's hard!  What do we do now!

We have a few options.

1. There's the...  _classic_ approach of dumping it all on my server and leaving it running in `tmux`.  Let's not do that.  Ever.

2. I already have Python stuff deployed using `gunicorn`, reverse proxying, and an Upstart script.  I like this setup (except that Upstart blows) and could easily just copy it.  That's not very helpful in the context of this "do it fast" post, though.

    Note that Debian-based distributions have packaged `gunicorn` as a daemon itself, so you only have to create a file with a couple lines to get going.  That's awesome.

3. Probably the most brain-dead thing to do is use Apache's `mod_wsgi`, which worries about running your app for you.  It's even Flask's [first choice][flask docs: mod_wsgi] for deployment, and it just takes a few lines of boilerplate Apache configuration, which all PHP devs are surely familiar with.  But I don't have Apache installed, and we've gotten along just fine without it so far, goddammit.

    Dreamhost has some unsupported [instructions][dreamhost and passenger] for using Apache's `mod_passenger` with a Python app, which is basically the same idea.

What else is there?  Plenty, really: FastCGI, or regular CGI (yeargh), or various other options for running a standalone thing, and I will totally blog about all this someday I swear.

But I want something drop-dead simple.  I want this on the interbutts _now_.

I will try something I have never tried before, while you, dear reader, watch me fumble.

I will try Heroku.


## Heroku

Hold up while I sign up for this thing and wait for the confirmation email.

...

Okay it has linked me to the [quickstart guide][heroku quickstart].  Let me remind you that, far moreso than with Flask, I have _no idea what I am doing_.

First I have to install some Ruby thing, naturally.  Let us pause for twenty minutes of reflection while documentation is compiled.

    eevee@perushian ~/dev/blog ⚘ heroku login
    Enter your Heroku credentials.
    Email: eevee.heroku@veekun.com
    Password (typing will be hidden): 
    Found the following SSH public keys:
    ...
    Which would you like to use with your Heroku account? 2
    Uploading SSH public key... done
    Authentication successful.
    eevee@perushian ~/dev/blog ⚘ cd ../guestbook_demo
    eevee@perushian ~/dev/guestbook_demo ⚘ heroku create
    Creating whispering-beach-4961... done, stack is cedar
    http://whispering-beach-4961.herokuapp.com/ | git@heroku.com:whispering-beach-4961.git
    Git remote heroku added

I seem to need a pip-style `requirements.txt` (just a list of Python distributions, one per line) and a `Procfile` (which tells heroku how to launch my thing).  There are [instructions for Flask][heroku flask], but as I already made an app, I'm just beating what I have into submission with minimal changes.  And some trial and error.

###### [requirements.txt](https://github.com/eevee/guestbook_demo/blob/e4ed3a09b271ba00db924391386dc701aa19e084/requirements.txt)
```
    Flask>=0.8
    SQLAlchemy>=0.7
    psycopg2
```

###### [Procfile](https://github.com/eevee/guestbook_demo/blob/e4ed3a09b271ba00db924391386dc701aa19e084/Procfile)
```
    web: python -m guestbook_demo
```

Other changes:

* Remove that `debug=True`, of course.
* Heroku wants my app to run on a port specified in the environment, so use `app.run(port=os.environ['PORT'])`.  And change the host to `0.0.0.0`.  It tells me nicely about these things when I use `heroku logs`.

I went through a couple cycles of `git push heroku master` and `heroku logs`, but I admit this is surprisingly painless and kinda sorta almost like just running it locally.  With a bit of a runaround anytime I change anything.

I have to add a web process before anything will run, I think:

    eevee@perushian ~/dev/guestbook_demo ⚘ heroku ps:scale web=1
    Scaling web processes... done, now running 1
    eevee@perushian ~/dev/guestbook_demo ⚘ heroku ps
    === web: `python -m guestbook_demo`
    web.1: up for 39s

And now I just need to reserve a database, make SQLAlchemy connect to it, and create the tables.

    eevee@perushian ~/dev/guestbook_demo ⚘ heroku addons:add heroku-postgresql:dev
    Adding heroku-postgresql:dev on whispering-beach-4961... done, v9 (free)
    Attached as HEROKU_POSTGRESQL_JADE
    Database has been created and is available
      ! WARNING: dev is in beta
      !          increased risk of data loss and downtime
      !          send feedback to dod-feedback@heroku.com
    Use `heroku addons:docs heroku-postgresql:dev` to view documentation.

###### [guestbook_demo/db.py](https://github.com/eevee/guestbook_demo/blob/e4ed3a09b271ba00db924391386dc701aa19e084/guestbook_demo/db.py)
```python
engine = create_engine(os.environ.get('HEROKU_POSTGRESQL_JADE_URL', 'postgresql:///guestbook_demo'))
```

    eevee@perushian ~/dev/guestbook_demo ⚘ heroku run python
    Running `python` attached to terminal... up, run.1
    from guesPython 2.7.2 (default, Oct 31 2011, 16:22:04) 
    [GCC 4.4.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    t>>> from guestbook_demo import db
    >>> db.Base.metadata.create_all(bind=db.engine)
    >>> 

And then...

Oh.  I'm done.

[http://whispering-beach-4961.herokuapp.com/](http://whispering-beach-4961.herokuapp.com/)

That was actually way, way less painful than I expected.  I would hecka [pay money][heroku pricing] for this thing.


## Recap

So I have a dumb little app that connects to a database, adds things to it, and shows things in it.  It's running live on a free "web host".  And I didn't know how to use half of these things when I started.

This took a couple hours, minus writing this post, and trying to figure out why my changes didn't take effect when I only typed them in the blog post and not the actual code, and playing with my cats, and eating a muffin, and whatever other fucking around I was doing.  In retrospect, I'm probably not the best person to demonstrate speed of doing anything.  But consider what we have here.

* I have routed URLs, and a URL generator, inside the app.  I never once, at any time, wrote any web server configuration whatsoever.  I don't even have a web server installed on my machine.
* I have a full ORM at my disposal that will work on half a dozen different databases.
* There are no SQL injection vulnerabilities; the ORM takes care of that.
* There are no XSS vulnerabilities; the template language takes care of that.  (Which is good, because I see the second entry here is already an attempt at script injection.)
* There are no HTTP header splitting vulnerabilities; I didn't even write any headers manually.

I didn't even touch half of what Flask does: it also has omnipresent sessions, flash messages, lightweight plugins, test amenities, logging, and [god knows what else][flask docs].

Was this quick?  I believe so.  Was it dirty?  Certainly not.  I have a namespace for my app, separate db configuration, separate templates with inheritance.  If I'd been so inclined, I could've been using Flask's configuration stuff to get some hardcoded values out of there as well.

Plus, half of what I did was setup stuff you'd have to do for any application: thinking up a db schema, creating a git repository, finding hosting.  Now all that stuff is ready to go, and the rest is a breeze.

And I _didn't know anything about Flask or Heroku this morning_.

Getting things done is not mutually exclusive with doing them nicely.  None of this was _hard_.  It's just _different_.

Come dip your toes in.  You might like what you find.

I threw the thing, complete with my embarrassing heroku fumbling, on [github][].


## Afterthought: the article

Other choice TechCrunch quotes:

> And yet PHP is allegedly used by more than three-quarters of all web sites.

Alleged, indeed.  This links to [w3techs][], which seems to [indicate][w3techs faq] that it uses URLs and HTTP headers to detect what language a site is written in.  What popular language plugin for Apache reports itself in the `Server` header, whether it's being used for the current page or not?  `mod_php`.  What doesn't?  Everything else!

(Addendum: I am told w3techs is [even less reliable][w3techs on SO] than appears at first glance.  They omit the nearly 20% of sites they can't guess at all.)

> “here’s to the PHP Misfits. The pragmatic ones who would pick up anything – even double-clawed hammers – to build their own future. Often ridiculed and belittled by the hip guys in class who write cool code in Ruby or Python, but always the ones who just get shit done.”

Yeah, well, fuck you.  I don't write Python because it's _cool_, and I'm rapidly tiring of having invented motivations used as a reason to disregard what I say.  I use Python because it balances _getting stuff done_ with _having that stuff not fall over as soon as I turn my back_.  Programming is a world of tradeoffs; most of PHP's trade immediacy for the slightest hint of reliability.  Those geeks writing sites in Haskell aren't always just doing it because it meets some academic (when did learning become _bad_?) standard of purity; very powerful typing often solves very real problems in software engineering.  The tradeoff there is that very powerful typing also makes some common tasks particularly difficult to implement.  Some people find this tradeoff acceptable; many do not.

I know these things because I have a passing familiarity with more than one language, and a passing familiarity with more than one methodology.  If you don't know _why_ your favorite tool's tradeoffs are good or bad but are merely used to them, then for the love of god, _please_ expand your context bubble before passing the rest of us off as squabbling elitist philosophers.

Now let's pretend this post has nothing to do with PHP because I am sick to death of typing about it.


[__future__]: http://docs.python.org/library/__future__.html
[Flask]: http://flask.pocoo.org/
[Quick and Filthy]: http://techcrunch.com/2012/07/28/not-that-kind-of-filthy-get-your-mind-out-of-the-gutter/
[SQLAlchemy]: http://www.sqlalchemy.org/
[dreamhost and passenger]: http://wiki.dreamhost.com/Passenger_WSGI
[flask docs]: http://flask.pocoo.org/docs/
[flask docs: mod_wsgi]: http://flask.pocoo.org/docs/deploying/mod_wsgi/
[flask docs: templates]: http://flask.pocoo.org/docs/templating/
[flask tutorial: views]: http://flask.pocoo.org/docs/tutorial/views/
[github]: https://github.com/eevee/guestbook_demo
[heroku flask]: https://devcenter.heroku.com/articles/python
[heroku pricing]: http://www.heroku.com/pricing
[heroku quickstart]: https://devcenter.heroku.com/articles/quickstart
[i do]: #flask
[w3techs]: http://w3techs.com/technologies/overview/programming_language/all
[w3techs faq]: http://w3techs.com/faq
[w3techs on SO]: http://stackoverflow.com/questions/11576469/why-is-perl-market-position-in-server-side-scripting-so-low-even-less-than-java/11577130#11577130
[zshrc prompt]: https://github.com/eevee/rc/blob/master/.zshrc#L63
