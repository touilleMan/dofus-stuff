from flask_restful import Api

from dofus.view import equipement_api

api = Api()


# equipement
api.add_resource(equipement_api.EquipementListAPI, '/equipements')
api.add_resource(equipement_api.EquipementAPI, '/equipements/<objectid:item_id>')
#


__all__ = ('api')
