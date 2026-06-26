from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instâncias globais
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """
    Inicializa o banco de dados e o sistema de migrações.
    """
    db.init_app(app)
    migrate.init_app(app, db)

    # Testa a conexão ao iniciar
    with app.app_context():
        try:
            from sqlalchemy import text

            db.session.execute(text("SELECT 1"))
            print("========================================")
            print("✅ PostgreSQL conectado com sucesso!")
            print("🚀 EIRILAR SHIELD iniciado.")
            print("========================================")

        except Exception as e:
            print("========================================")
            print("❌ Erro ao conectar ao PostgreSQL")
            print(e)
            print("========================================")
