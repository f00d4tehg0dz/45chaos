## Mooch App Local Development

### Requirements

*NB: If using Windows, it is easiest to use the Windows Subsystem for Linux or Docker for local development*

The web app is written in python >= 3.4 and the required libraries can be installed with:

```bash
$> pip3 install -r requirements.txt
```

Flask-SQLAlchemy is used for the database. The most common missing system packages when encountering issues with SQLAlchemy are the MySQL client development bindings. On Ubuntu/WSL these can be installed with:

```bash
$> apt install libmysqlclient-dev
```

On macOS it is easiest to install Homebrew and run

```bash
$> brew install mysql
```

It is advisable to use a python virtual environment to isolate your dependancies.

```bash
$> python3 -m venv path/to/venv
$> source path/to/venv/bin/activate # for linux/macOS
$> pip install requirements.txt

# to leave the virtual environment
$> deactivate
```

With all the requirements installed you can use `manager.py` to invoke a shell in the application context, or run a development server.

```bash
$> python3 manager.py
usage: manager.py [-?] {shell,runserver} ...

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

### Using Docker

The `Dockerfile` in this repository defines the artifact that gets deployed to the web server.
It can also be used for local development.
Make your modifications then run the following from the repository root to build/run a local container

```bash
$> docker build . -t mooches
$> docker run --rm -p 5000:5000 mooches # --rm (don't save container) -p (forward port on host to container)
```
