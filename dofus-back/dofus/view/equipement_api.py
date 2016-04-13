import json
from bson import errors as bson_errors, ObjectId
from flask import abort
from flask.ext.restful import Resource
from werkzeug import Response

from dofus.model.equipement import Equipement


class EquipementListAPI(Resource):

    def get(self):
        equipements = Equipement.find()
        return [e.dump() for e in equipements]


class EquipementAPI(Resource):

    def get(self, item_id=None):
        try:
            item_id = ObjectId(item_id)
        except (TypeError, ValueError, bson_errors.InvalidId):
            abort(400, 'Invalid item id')
        equipement = Equipement.find_one({'_id': item_id})
        if not equipement:
            abort(404)
        return equipement.dump()
