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
    parsed_config = {}
    if not config.get("host"):
        parsed_config["host"] = DEFAULTS["host"]
    else:
        parsed_config["host"] = config["host"]
    if not config.get("port"):
        parsed_config["port"] = DEFAULTS["port"]
    else:
        parsed_config["port"] = int(config["port"])
    if not config.get("database_engine"):
        parsed_config["database_uri"] = DEFAULTS["database_uri"]
    else:
        parsed_config["database_uri"] = parse_db_config(config)
    if not config.get("update_interval"):
        parsed_config["update_interval"] = DEFAULTS["update_interval"]
    else:
        parsed_config["update_interval"] = int(config["update_interval"])
    if not config.get("debug"):
        parsed_config["debug"] = DEFAULTS["debug"]
    else:
        parsed_config["debug"] = bool(config["debug"])
    return parsed_config

def parse_db_config(config):
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

    if config["database_engine"] == "mysql":
        prefix = "mysql"
    elif config["database_engine"] == "postgres":
        prefix = "postgresql"

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
