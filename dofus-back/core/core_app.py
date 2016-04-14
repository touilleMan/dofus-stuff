from flask import Flask
from flask.ext.mongoengine import MongoEngine

from core.encoders import ObjectIdConverter

class CoreApp(Flask):
    """
    CoreApp is a regular :class:`Flask` app with cors, flask-principal,
    "restfulness" flavors
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Support objectid in url routing
        self.url_map.converters['objectid'] = ObjectIdConverter
        self.db = MongoEngine()

    def bootstrap(self):
        self.db.init_app(self)
