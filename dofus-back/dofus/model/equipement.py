from mongoengine import Document
from mongoengine.fields import StringField, URLField, IntField, ListField, ReferenceField, DictField

from dofus.model.panoplie import Panoplie

class Equipement(Document):
    meta = {'indexes': ['title', 'level', 'type', 'dofus_link']}

    title = StringField(required=True, unique=True)
    level = IntField(default=1, required=True)
    dofus_link = URLField(null=True)
    image = URLField(required=True)
    type = StringField(choices=("Amulette", "Anneau", "Bottes", "Cape", "Bouclier", "Ceinture", "Chapeau", "Dofus", "Trophée", "Sac à dos"),
                       required=True)
    effects = DictField(null=True)
    conditions = ListField(null=True)
    panoplie = ReferenceField(Panoplie, null=True)
