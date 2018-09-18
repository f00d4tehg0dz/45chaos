from mooches import bootstrap_app
application, config = bootstrap_app()

if __name__ == "__main__":
    application.run(
        debug=bool(config["debug"]),
        host=config["host"],
        port=int(config["port"])
    )
