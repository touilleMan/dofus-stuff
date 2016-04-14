from mongoengine import Document
from mongoengine.fields import *


class Panoplie(Document):
    meta = {'indexes': ['title', 'level']}
    #
    title = StringField(required=True, unique=True)
    level = IntField(default=1, required=True)
    # image = fields.URLField(required=True)
    # type = fields.StringField(required=True)
    # effects = fields.ListField(null=True)
    # conditions = fields.ListField(null=True)
    # panoplie = fields.ReferenceField(Panoplie, null=True)
