## Server Configuration

The configuration is at `config.yml`. Leaving as is will assume the defaults.
This is where you can tweak various aspects of the server.

Below are the configuration options at their defaults.
If you leave `config.yml` in this repository as is it will assume these values.

```yaml
# SERVER CONFIG
# All commented values are at their defaults

###
# Listener Configuration
###
#
#  These values only matter for the uwsgi runtime (docker containers or other server uwsgi instance)
#  If using manager.py you can specify these options on the command line
#
debug: false
#host: 0.0.0.0 # not configurable currently
#port: 5000 # not configuragble currently

###
# Database Configuration
###
#
# Defaults to a local sqlite instance.
# Supported engines are ["mysql", "postgres", "sqlite"]
# For sqlite URI, use absolute path to a file or relative path to mooches folder
#
# For MySQL ensure you have the mysql client installed on the system (already included in Docker container)
# macOS: brew install mysql
# ubuntu: apt install libmysqlclient-dev

database_engine: sqlite
database_uri: data.sqlite

# Below values only apply to MySQL and PostgreSQL

database_username:
database_password:
database_name:

###
# Spreadsheet Polling
###

# How often in seconds to poll the spreadsheet for updates

update_interval: 60
```
