from .websoket import web
from .First import blue
from .second import blue2


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(blue2)
    app.register_blueprint(web)
    # app.register_blueprint(html)
    # app.register_blueprint(ws)
