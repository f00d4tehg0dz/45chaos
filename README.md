# Mooches Flask App

## Installing Deps for Local Development

```bash
$> cd flask
$> pip3 install -r requirements.txt
```
## For Windows make sure Ubuntu from AppStore is installed
```bash
$> cd flask
$> apt-get update
$> apt-get install python3-pip
$> apt-get install apache2-dev
$> apt-get install mysql-server

# $> set MOD_WSGI_APACHE_ROOTDIR="C:/xampp/apache"


## Server Configuration

The configuration is at `config.yml`. Leaving as is will assume the defaults.
This is where you can specify an alternative database, listen port, update interval, etc.

## Using Docker for Local Dev

I slapped together a Dockerfile in case you don't want to mess with python deps or virtualenvs.
Just edit files as you wish and then:

```bash
$> cd flask && docker build . -t mooches
$> docker run --rm -p 5000:5000 mooches # --rm (don't save container) -p (forward port on host to container)
```

## Using the manager for local dev

```bash
$> python3 manager.py
usage: manager.py [-?] {shell,runserver} ... # shell is useless currently

positional arguments:
  {initdb,shell,runserver}
    initdb           Seeds the configured database
    shell            Runs a Python shell inside Flask application context.
    runserver        Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help         show this help message and exit

$> python3 manager.py runserver # use -r to monitor files for changes without having to restart
 * Serving Flask app "mooches" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

## Using the Database

The `models` define a function to seed the database for you

```bash
$> python3 manager.py shell
>>> models.seed()

# to query the database
>>> records = models.Mooch.query.all()
>>> print(records[0].LastName) # get the last name

# to check for updates to the db
>>> models.update() # will be threaded off on schedule during runtime
```

See `flask/mooches/models.py` for the model definition
