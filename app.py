from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

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
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(int(user_id))
    except Exception as e:
        print("USER LOADER ERROR:", e)
        return None


# =========================
# APP FACTORY
# =========================
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # =========================
    # PROXY FIX (DEPLOY)
    # =========================
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1
    )

    # =========================
    # DB INIT
    # =========================
    init_db(app)

    # =========================
    # LOGIN INIT
    # =========================
    login_manager.init_app(app)

    # =========================
    # BLUEPRINTS (COMPATÍVEIS COM DASHBOARD)
    # =========================
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(usuarios)
    app.register_blueprint(pedidos)
    app.register_blueprint(logs)
    app.register_blueprint(bloqueios)
    app.register_blueprint(risco)

    # =========================
    # HOME (REDIRECIONA PRO DASHBOARD)
    # =========================
    @app.route("/")
    def index():
        return render_template("index.html")

    # =========================
    # ERROS COMPATÍVEIS COM FRONT
    # =========================
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"), 500

    return app


# =========================
# RUN
# =========================
app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
