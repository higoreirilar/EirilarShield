import os
from dotenv import load_dotenv

# Carrega variáveis do .env (desenvolvimento local)
load_dotenv()


class Config:
    # Segurança
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "eirilar_shield_super_secret_key_2026"
    )

    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # Railway às vezes usa postgres://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Engine SQLAlchemy
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # Configurações da aplicação
    APP_NAME = "EIRILAR SHIELD"

    VERSION = "2.0"

    ITEMS_PER_PAGE = 20
