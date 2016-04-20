The Drinking Gourd
===============================

A app to process audio and house the drinking gourd dharma podcast


TO DO
=====
* Settings -> Set Recaptcha Keys
* Settings -> Set Email info
* Settings -> Set DB Info
* Public -> emails -> Set contact email address

It is recomended you set these all as environment variables


Quickstart
----------
Generate a secret key:

    $ python
    >>> import os
    >>> os.urandom(24)
    "\x08'\\\xef\xe5\xea\xef\x9b}\xb4\x93\xed\xe9f-\xbd\x8c8\x11\xc9\x11\x1d\x0e%"

(Make sure to generate your own) Copy that mess of string and then set the secret key
in an enviornment variable 

    export DRINKING_GOURD_SECRET="\x08'\\\xef\xe5\xea\xef\x9b}\xb4\x93\xed\xe9f-\xbd\x8c8\x11\xc9\x11\x1d\x0e%"

Then make your virtualenv

    mkvirtualenv myNewProject
    workon myNewProject    

Clone the repo and fire it up

    git clone https://github.com/Shonin/drinking-gourd.git
    cd drinking-gourd
    pip install -r requirements/dev.txt
    bower install
    python manage.py server

You will see the homepage on localhost:5000


Database Setup
--------------

Run the following to create your app's database tables and perform the initial migration:

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server


Deployment
----------

In your production environment, make sure the ``DRINKING_GOURD_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.