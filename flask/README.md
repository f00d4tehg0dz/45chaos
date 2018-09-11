# Mooches Flask App

## Installing Deps for Local Development

```bash
$> cd flask
$> pip3 install -r requirements.txt
```

## Using the manager

```bash
$> python3 manager.py
usage: manager.py [-?] {shell,runserver} ... # shell is useless currently

positional arguments:
  {shell,runserver}
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
