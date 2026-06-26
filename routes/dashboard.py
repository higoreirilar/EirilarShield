from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from database import db
from sqlalchemy import text
import random
import math

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_page():

    # =========================
    # PAGINAÇÃO
    # =========================
    page = request.args.get("page", 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # =========================
    # TOTAL DE CLIENTES (REAL)
    # =========================
    try:
        total_usuarios = db.session.execute(
            text("SELECT COUNT(*) FROM clientes")
        ).scalar()
    except:
        total_usuarios = 0

    # =========================
    # CLIENTES (PAGINADO)
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento
            FROM clientes
            ORDER BY id DESC
            LIMIT :limit OFFSET :offset
        """), {"limit": per_page, "offset": offset})

        clientes = [
            {
                "nome": r[0] or "",
                "cpf": r[1] or "",
                "ip": r[2] or "",
                "cidade": r[3] or "",
                "estado": r[4] or "",
                "score": r[5] or 0,
                "forma_pagamento": r[6] or "N/A"
            }
            for r in result.fetchall()
        ]

    except Exception as e:
        print("ERRO CLIENTES:", e)
        clientes = []

    # =========================
    # TOTAL DE PÁGINAS
    # =========================
    total_pages = math.ceil(total_usuarios / per_page) if total_usuarios else 1

    # =========================
    # PEDIDOS (ÚLTIMOS 10)
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT id, status, valor, nome_cliente
            FROM pedidos
            ORDER BY id DESC
            LIMIT 10
        """))

        ultimos_pedidos = [
            {
                "id": r[0],
                "status": r[1] or "indefinido",
                "valor": float(r[2] or 0),
                "nome_cliente": r[3] or ""
            }
            for r in result.fetchall()
        ]

    except Exception as e:
        print("ERRO PEDIDOS:", e)
        ultimos_pedidos = []

    # =========================
    # RISCO (BASEADO NOS CLIENTES DA PÁGINA)
    # =========================
    scores = [c["score"] for c in clientes if c.get("score") is not None]

    risco_alto = len([s for s in scores if s >= 70])
    risco_medio = len([s for s in scores if 40 <= s < 70])
    risco_baixo = len([s for s in scores if s < 40])

    media_risco = round(sum(scores) / len(scores), 2) if scores else 0

    # =========================
    # LOGS (MOCK OU FUTURO BANCO)
    # =========================
    total_logs = 120

    # =========================
    # DEBUG
    # =========================
    print(f"[DASHBOARD] usuários={total_usuarios} clientes_page={len(clientes)}")

    # =========================
    # RENDER
    # =========================
    return render_template(
        "dashboard.html",

        # dados principais
        clientes=clientes,
        ultimos_pedidos=ultimos_pedidos,
        user=current_user,

        # KPIs
        total_usuarios=total_usuarios,
        total_pedidos=len(ultimos_pedidos),
        total_logs=total_logs,
        media_risco=media_risco,

        # risco
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,

        # paginação
        page=page,
        total_pages=total_pages
    )
