from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    # Carrega config
    app.config.from_object("config.Config")

    # Inicializa ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # Teste de conexão
    with app.app_context():
        try:
            from sqlalchemy import text

            db.session.execute(text("SELECT 1"))

            print("\n========================================")
            print("✅ PostgreSQL conectado com sucesso!")
            print("🚀 EIRILAR SHIELD online")
            print("========================================\n")

        except Exception as e:
            print("\n========================================")
            print("❌ ERRO ao conectar no PostgreSQL")
            print(e)
            print("========================================\n")
