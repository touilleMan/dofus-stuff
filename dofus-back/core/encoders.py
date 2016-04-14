import bson

from werkzeug.routing import BaseConverter, ValidationError


class ObjectIdConverter(BaseConverter):
    """
    werkzeug converter to use ObjectId in url ::
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.url_map.converters['objectid'] = ObjectIdConverter
        >>> @app.route('/objs/<objectid:object_id>')
        ... def route(object_id): return 'ok'
        ...
    """
    def to_python(self, value):
        try:
            return bson.ObjectId(value)
        except bson.errors.InvalidId:
            raise ValidationError()

    def to_url(self, value):
        return str(value)
