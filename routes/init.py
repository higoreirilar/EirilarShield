from .auth import auth
from .dashboard import dashboard
from .usuarios import usuarios
from .pedidos import pedidos
from .logs import logs
from .bloqueios import bloqueios
from .risco import risco
from .ips_confiaveis import ips_confiaveis


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(usuarios)
    app.register_blueprint(pedidos)
    app.register_blueprint(logs)
    app.register_blueprint(bloqueios)
    app.register_blueprint(risco)
    app.register_blueprint(ips_confiaveis)
