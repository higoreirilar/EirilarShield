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
    # CLIENTES (COM COUNT REAL)
    # =========================
    try:
        # total real de clientes
        total_clientes = db.session.execute(text(
            "SELECT COUNT(*) FROM clientes"
        )).scalar()

        # clientes paginados
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
                "score": r[5] if r[5] is not None else 0,
                "forma_pagamento": r[6] or "N/A"
            }
            for r in result.fetchall()
        ]

    except Exception as e:
        print("ERRO CLIENTES:", e)
        clientes = []
        total_clientes = 0

    total_pages = math.ceil(total_clientes / per_page) if total_clientes else 1

    # =========================
    # PEDIDOS
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT id, status, valor, forma_pagamento, ip, nome_cliente
            FROM pedidos
            ORDER BY id DESC
            LIMIT 10
        """))

        ultimos_pedidos = [
            {
                "id": r[0],
                "status": r[1] or "indefinido",
                "valor": float(r[2] or 0),
                "forma_pagamento": r[3] or "N/A",
                "ip": r[4] or "",
                "nome_cliente": r[5] or "",
                "risco": random.randint(10, 100)
            }
            for r in result.fetchall()
        ]

    except Exception as e:
        print("ERRO PEDIDOS:", e)
        ultimos_pedidos = []

    # =========================
    # MÉTRICAS DE RISCO
    # =========================
    scores = [c["score"] for c in clientes if c.get("score") is not None]

    risco_alto = len([s for s in scores if s >= 70])
    risco_medio = len([s for s in scores if 40 <= s < 70])
    risco_baixo = len([s for s in scores if s < 40])

    media_risco = round(sum(scores) / len(scores), 2) if scores else 0

    # =========================
    # MÉTRICAS GERAIS
    # =========================
    total_usuarios = total_clientes
    total_pedidos = len(ultimos_pedidos)
    total_logs = 120  # futuramente pode vir do banco

    # =========================
    # DEBUG
    # =========================
    print(f"[DASHBOARD] clientes={len(clientes)} pedidos={total_pedidos}")

    # =========================
    # RENDER
    # =========================
    return render_template(
        "dashboard.html",
        clientes=clientes,
        ultimos_pedidos=ultimos_pedidos,
        user=current_user,

        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        total_logs=total_logs,

        media_risco=media_risco,
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,

        page=page,
        total_pages=total_pages
    )
