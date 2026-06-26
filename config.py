import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    url = os.getenv("DATABASE_URL")

    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


class Config:

    # =========================
    # SEGURANÇA
    # =========================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "eirilar_shield_super_secret_key_2026"
    )

    # =========================
    # SESSÃO (ESSENCIAL NO RAILWAY)
    # =========================
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # =========================
    # BANCO
    # =========================
    SQLALCHEMY_DATABASE_URI = get_database_url()

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL não foi definida no ambiente")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # =========================
    # APP INFO
    # =========================
    APP_NAME = "EIRILAR SHIELD"
    VERSION = "2.0"
    ITEMS_PER_PAGE = 20
