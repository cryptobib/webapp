# CryptoBib Web Application (for web2py)

**WARNING**: This is probably not the repository your are interested in. This repository is only for *cryptobib* developers. The repositories containing the public *bib* files are [cryptobib/export](https://github.com/cryptobib/export) and  [cryptobib/export_crossref](https://github.com/cryptobib/export_crossref).

**WARNING**: This project shall only be used as a subfolder of the main project [cryptobib/cryptobib](https://github.com/cryptobib/cryptobib). Please read the documentation of the main project.

## Getting started

This is a web2py (http://web2py.com) application.
You need to use it only if you wan to create a mirror of the cryptobib website.

### Requirements

- python >= 3.5
- pip (if you want to install python libraries below)
- httplib2, ...
- ipython (not necessary bu recommended for shell)

        pip install ipython

### Download web2py and install the application

1. Download web2py 2.20.4 source code from http://web2py.com/init/default/download
2. Unzip it under the root folder `cryptobib`
3. Create a link from `webapp` to the subfolder `web2py/applications/cryptobib`:

        cd web2py/applications
        ln -s ../../webapp cryptobib

4. For a production server, you may want to remove all the other applications, or at least to restrict access to the admin application to local ips.

In the sequel we suppose that you are in the `web2py` folder.

### Configure the application 

1. create folders in `applications/cryptobib`

        mkdir applications/cryptobib/cache applications/cryptobib/databases applications/cryptobib/errors applications/cryptobib/sessions applications/cryptobib/uploads

2. `cp applications/cryptobib/routes.web2py.sample.py routes.py` and change it
3. `cp applications/cryptobib/models/0_settings.py.sample applications/cryptobib/models/0_settings.py` and change it to connect to the correct database

You may want to update `applications/cryptobib/models/1_settings.py` too.

### Run the application

#### Development

In development, just run

    python3 web2py.py

#### Production

For production, we recommend you to run it as a wsgi script on an Apache server:

1. copy `handlers/wsgihandler.py` to `wsgihandler.py`
2. set the admin password

        sudo -u www-data python -c "from gluon.main import save_password; save_password(raw_input('admin password: '),443)"

and restrict access to `admin` (in apache with `Location` directive) to DI IP addresses.
2. set up the wsgi server as explained in http://web2py.com/books/default/chapter/29/13/deployment-recipes#mod_wsgi

Configuration example (in virtual host):

    WSGIDaemonProcess web2py-ssl user=www-data group=www-data display-name=%{GROUP}
    WSGIProcessGroup web2py-ssl
    WSGIScriptAlias /web2py /var/www/web2py/wsgihandler.py

    <Location /web2py>
        WSGIProcessGroup web2py-ssl
        Order deny,allow
        Allow from all
    </Location>

    <Location /web2py/admin>
        Order deny,allow
        Deny from all
        Allow from 129.199.99.0/255.255.255.0
        Allow from 127.0.0.1
    </Location>

    <Directory /var/www/web2py>
        AllowOverride None
        Order allow,deny
        Deny from all
        <Files wsgihandler.py>
            Allow from all
        </Files>
    </Directory>

    AliasMatch ^/web2py/([^/]+)/static/(?:_[\d]+.[\d]+.[\d]+/)?(.*) \
            /var/www/web2py/applications/$1/static/$2

    <Directory /var/www/web2py/applications/*/static/>
        Options -Indexes
        ExpiresActive On
        ExpiresDefault "access plus 1 hour"
        Order deny,allow
        Deny from all
        Allow from 129.199.99.0/255.255.255.0
        Allow from 127.0.0.1
    </Directory>

It is highly recommended to serve the website via https.

Remark: if you use multiple web2py servers (e.g., one for development and one for production), please take care of https://github.com/web2py/web2py/issues/834#issuecomment-83986269

Reload page:

    curl -k https://localhost/web2py-dev/crypto/admin/reload > /dev/null

### Update database

Run

    make web

in the root folder.

This operation has to be done after any modification of the database.

### Reload application

Reload application:

- in production (wsgi), reload everything (except maybe cache):

        touch wsgihandler.py

- in development: normally, if `applications/crypto/0_settings.py` is setup correctly modules are reloaded automatically, however routes may not. If you want to reload routes (very rare), you may need them (either via restarting the server or using the admin console)

Cache can be reloaded by:

    curl -k https://localhost/crypto/admin/reload > /dev/null

This can only be done from localhost.

### Practical update script

It is practical to create the following script `update.sh`:

    #!/bin/sh
    set -e
    (cd export && git reset --hard HEAD)
    (cd export_crossref && git reset --hard HEAD)
    mr update
    make web
    touch web2py/wsgihandler.py
    curl -k https://localhost/crypto/admin/reload > /dev/null

## Administration / Backup

### Shell

    python2 web2py.py -S crypto -M

WARNING: never forget to commit the database after doing any modification:

    db.commit()

### Export/import database

In `web2py/applications/crypto`:

    python2 tools/export_db > db.csv
    python2 tools/import_db < db.csv

You may need to truncate all tables before doing the import.
You can do it via:

    python2 tools/truncate_db

You can also manually remove all tables:
- with sqllite 3:

        rm -rf databases/*

- with mysql:

        rm -rf datatases/*

AND manually remove tables, e.g. using PhpMyAdmin.

This may be necessary in case of changes in attributes of tables (such as ondelete).

### Backup

You may want to backup:

- databases: see above
- `uploads` folder (uploads to database)
- `static/uploads` folder (uploads from forms, such as the job contact form)
- `models/0_settings`

The other folders are normally either automatically generated or in the git repository.

If you want to test the website locally, you just need to import the databases and `uploads` folder.

### Known Issues

- In dev mode, if a module `a` imports a module `b`, and if `b` is changed, it will not be reloaded in `a` (but it will still be reloaded in controllers and models.

### Long term TODO

- Needs to check that

  - `static/uploads` does not grow too much
  - `sessions` either

  cf deployment recipes on web2py website

- Minify properly everything (using `grunt`?)

### Day to day maintenance

- Check tickets regularly (in admin interface)
- Update of the server
- Check SSL security (e.g., ssl labs)

## More documentation

- bootstrap3: http://getbootstrap.com/
- web2py: http://www.web2py.com/books/default/chapter/29



