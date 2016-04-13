#! /usr/bin/env python3

# from flask import
from flask.ext.script import Manager, Server, Shell

from dofus import bootstrap_app
from dofus.managers import populate_manager

app = bootstrap_app()
app.debug = True

manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port="5000"))
manager.add_command("populate", populate_manager)

if __name__ == "__main__":
    manager.run()
