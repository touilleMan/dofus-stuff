from flask import Flask
from flask.ext import cors
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
        """
        Initialize modules needing configuration

        :example:

            >>> app = CoreApp("my-app")
            >>> app.config['MY_CONF'] = 'DEFAULT_VALUE'
            >>> app.bootstrap()
        """
        # Principal and CORS support must be initialized at bootstrap time
        # in order to have up-to-date config
        self._cors = cors.CORS(self)
        self.db.init_app(self)
