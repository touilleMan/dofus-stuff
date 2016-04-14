import json

from flask import jsonify
from flask.ext.restful import Resource
from werkzeug import Response

from dofus.model.equipement import Equipement


class EquipementListAPI(Resource):

    def get(self):
        equipements = Equipement.objects()
        return jsonify(items=equipements)


class EquipementAPI(Resource):

    def get(self, item_id=None):
        data = "TOTO"
        return data
