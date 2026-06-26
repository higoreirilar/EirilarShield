from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from database import init_db, db
from models import Usuario

# Blueprints
from routes.auth import auth
from routes.dashboard import dashboard
from routes.usuarios import usuarios
from routes.pedidos import pedidos
from routes.logs import logs
from routes.bloqueios import bloqueios
from routes.risco import risco


login_manager = LoginManager()
login_manager.login_view = "auth.login"

from models import Usuario
from database import db

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except Exception as e:
        print("USER LOADER ERROR:", e)
        return None


@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    return Usuario.query.filter_by(id=int(user_id)).first()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Proxy (Railway)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Segurança de sessão
    app.secret_key = app.config["SECRET_KEY"]

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_PROTECTION"] = "strong"

    # DB
    init_db(app)

    # LOGIN
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # BLUEPRINTS
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(usuarios)
    app.register_blueprint(pedidos)
    app.register_blueprint(logs)
    app.register_blueprint(bloqueios)
    app.register_blueprint(risco)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
