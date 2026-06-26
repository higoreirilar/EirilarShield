import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# FUNÇÃO SEGURA PARA DB URL
# =========================
def get_database_url():
    url = os.getenv("DATABASE_URL")

    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


# =========================
# CONFIG
# =========================
class Config:

    # Segurança
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "eirilar_shield_super_secret_key_2026"
    )

    # Banco de dados (corrigido)
    SQLALCHEMY_DATABASE_URI = get_database_url()

    # Evita crash silencioso no Railway
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL não foi definida no ambiente")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Performance Railway / Postgres
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # App metadata
    APP_NAME = "EIRILAR SHIELD"
    VERSION = "2.0"
    ITEMS_PER_PAGE = 20
