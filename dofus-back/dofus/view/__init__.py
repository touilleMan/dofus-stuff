from flask_restful import Api

from dofus.view import equipement_api

api = Api()


# equipement
api.add_resource(equipement_api.EquipementListAPI, '/')
api.add_resource(equipement_api.EquipementAPI, '/<objectid:item_id>')


__all__ = ('api')
