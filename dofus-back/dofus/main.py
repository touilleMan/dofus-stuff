from core.core_app import CoreApp


def create_app(config=None):
    """
    Build the app build don't initilize it, useful to get back the default
    app config, correct it, then call ``bootstrap_app`` with the now config
    """

    app = CoreApp(__name__)
    if config:
        app.config.update(config)
    app.config.from_pyfile('default_settings.cfg')
    return app


def bootstrap_app(app=None, config=None):
    """
    Create and initilize the dofus app
    """

    if not app:
        app = create_app(config)
    elif config:
        app.config.update(config)

    from dofus.view import api

    app.bootstrap()

    # api
    api.init_app(app)

    return app
