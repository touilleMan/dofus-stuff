from flask import current_app
from umongo import Document, fields, validate, pymongo_lazy_loader

from dofus.model.panoplie import Panoplie


EQUIPEMENT_TYPE = ("Amulette", "Anneau", "Bottes", "Cape", "Bouclier",
                   "Ceinture", "Chapeau", "Dofus", "Trophée", "Sac à dos")


class Equipement(Document):
    class Meta:
        indexes = ['title', 'level', 'type', 'dofus_link']
        lazy_collection = pymongo_lazy_loader(lambda: current_app.db.equipement)

    title = fields.StringField(required=True, unique=True)
    level = fields.IntField(default=1, required=True)
    dofus_link = fields.URLField(null=True)
    image = fields.URLField(required=True)
    type = fields.StringField(validate=validate.OneOf(EQUIPEMENT_TYPE),
                       required=True)
    effects = fields.DictField(null=True)
    conditions = fields.ListField(fields.DictField(), null=True)
    panoplie = fields.ReferenceField(Panoplie, null=True)
