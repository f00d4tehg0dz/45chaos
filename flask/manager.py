from flask_script import Manager, Shell
from mooches import bootstrap_app, db

app = bootstrap_app()
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
