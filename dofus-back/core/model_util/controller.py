from flask.ext.mongoengine import mongoengine, Document


class BaseController:
    """
    Controller base class, providing usefull function for handling document
    """

    def __init__(self, document):
        self.document = document

    def update(self, payload):
        for key, value in payload.items():
            setattr(self.document, key, value)


class ControlledDocument(Document):
    """
    Mongoengine abstract document providing a controller attribute to
    alter with style the document !
    """

    meta = {'abstract': True, 'controller_cls': BaseController}

    @property
    def controller(self):
        controller_cls = self._meta.get('controller_cls')
        if not controller_cls:
            raise NotImplementedError('No controller setted for this document')
        return controller_cls(self)

    def clean(self):
        """Automatically called at save time, triggers controller's clean"""
        ctrl = self.controller
        if hasattr(ctrl, 'clean'):
            ctrl.clean()
