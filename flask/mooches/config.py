import yaml
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SUPPORTED_ENGINES = ["sqlite", "mysql", "postgres"]

DEFAULTS = {
    "host": "0.0.0.0",
    "port": 5000,
    "database_uri": "sqlite:///%s" % os.path.join(basedir, "data.sqlite"),
    "update_interval": 60,
    "debug": False
}


def load_config():

    """
    If the file does not exist, or does not contain any parsable YAML, return DEFAULTS

    Otherwise validate the configuration options
    """

    try:
        with open("config.yml", "r") as f:
            config = f.read()
    except:
        print("No config found, using defaults")
        return DEFAULTS
    loaded = yaml.load(config)
    if not loaded:
        return DEFAULTS
    else:
        return parse_config(loaded)


def parse_config(config):

    """
    For each of the generic configuration options, return the provided value or default
    """

    parsed_config = {}
    for key in ["host", "port", "update_interval", "debug"]:
        if not config.get(key):
            parsed_config[key] = DEFAULTS[key]
        else:
            parsed_config[key] = config[key]
    if not config.get("database_engine"):
        parsed_config["database_uri"] = DEFAULTS["database_uri"]
    else:
        parsed_config["database_uri"] = parse_db_config(config)
    return parsed_config


def parse_db_config(config):

    """
    Given a database configuration, format a SQL URI to hand to SQLAlchemy
    """

    if config["database_engine"].lower() not in SUPPORTED_ENGINES:
        print("Invalid database engine: %s" % config["database_engine"])
        print("Using default sqlite database")
        return DEFAULTS["database_uri"]

    if config["database_engine"] == "sqlite":
        if not config.get("database_uri"):
            return DEFAULTS["database_uri"]
        if config["database_uri"].startswith("/"):
            return "sqlite:///%s" % config["database_uri"]
        else:
            return "sqlite:///%s" % os.path.join(basedir, config["database_uri"])

    if not config.get("database_name") or not config.get("database_uri"):
        print("Not using sqlite and no database name and/or host provided.")
        print("Reverting to default sqlite")
        return DEFAULTS["database_uri"]

    if config["database_engine"].lower() in SUPPORTED_ENGINES:
        if config["database_engine"] == "mysql":
            prefix = "mysql"
        elif config["database_engine"] == "postgres":
            prefix = "postgresql"
    else:
        print("%s is not a supported database engine" % config["database_engine"])
        print("Using default SQLite")
        return DEFAULTS["database_uri"]

    if not config.get("database_username") or not config.get("database_password"):
        print("No sql username or password specified, attempting anonymous access")
        return "%s://%s/%s" % (
            prefix,
            config["database_uri"],
            config["database_name"]
        )
    else:
        return "%s://%s:%s@%s/%s" % (
            prefix,
            config["database_username"],
            config["database_password"],
            config["database_uri"],
            config["database_name"]
        )
