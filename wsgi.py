from mooches import bootstrap_app
application, config = bootstrap_app()

import sys
sys.stdout = sys.stderr

if __name__ == "__main__":
    application.run(
        debug=bool(config["debug"]),
        host=config["host"],
        port=int(config["port"])
    )
