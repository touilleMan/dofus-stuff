from umongo import Document, fields
from umongo.dal.pymongo import PyMongoDal


class Panoplie(Document):
    class Meta:
        indexes = ['title', 'level']
        lazy_collection = lambda: current_app.db.equipement
        dal = PyMongoDal

    title = fields.StringField(required=True, unique=True)
    level = fields.IntField(missing=1, required=True)
    # image = fields.fields.URLField(required=True)
    # type = fields.fields.StringField(required=True)
    # effects = fields.fields.ListField(null=True)
    # conditions = fields.fields.ListField(null=True)
    # panoplie = fields.fields.ReferenceField(Panoplie, null=True)
