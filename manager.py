import sys

from flask_script import Manager, Shell
from mooches import bootstrap_app, db, models, spreadsheets

if "runserver" in sys.argv:
    app, config = bootstrap_app()
else:
    app, config = bootstrap_app(no_thread=True)

manager = Manager(app)

def make_shell_context():

    """
    Return a shell context with the models and db pre-imported
    """

    return dict(app=app, db=db, models=models, scraper=spreadsheets.Scraper())

@manager.command
def initdb():

    """
    Seeds the configured database
    """

    sys.stdout.write("Seeding configured database...")
    sys.stdout.flush()
    with app.app_context():
        models.seed()
    sys.stdout.write("Done\n")
    sys.stdout.flush()

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
