from flask import Flask
from flask_login import LoginManager

from config import Config
from database import init_db
from models import Usuario

# Blueprints
from routes.auth import auth
from routes.dashboard import dashboard
from routes.usuarios import usuarios
from routes.pedidos import pedidos
from routes.logs import logs
from routes.bloqueios import bloqueios
from routes.risco import risco


# =========================
# LOGIN MANAGER GLOBAL
# =========================
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# =========================
# APP FACTORY (CORRETO)
# =========================
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # DB
    init_db(app)

    # LOGIN
    login_manager.init_app(app)

    # BLUEPRINTS
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(usuarios)
    app.register_blueprint(pedidos)
    app.register_blueprint(logs)
    app.register_blueprint(bloqueios)
    app.register_blueprint(risco)

    # ROTAS BÁSICAS
    @app.route("/")
    def index():
        return "<h2>EIRILAR SHIELD rodando 🚀</h2>"

    # ERROS
    @app.errorhandler(404)
    def not_found(error):
        return "<h3>Página não encontrada</h3>", 404

    @app.errorhandler(500)
    def server_error(error):
        return "<h3>Erro interno do servidor</h3>", 500

    return app


# =========================
# EXECUÇÃO
# =========================
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
