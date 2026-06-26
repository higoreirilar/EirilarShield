from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from database import db
from sqlalchemy import text
import random
import math

dashboard = Blueprint("dashboard", __name__)


# =========================
# DASHBOARD PRINCIPAL
# =========================
@dashboard.route("/dashboard")
@login_required
def dashboard_page():

    # =========================
    # PAGINAÇÃO
    # =========================
    page = request.args.get("page", 1, type=int)
    per_page = 12

    # =========================
    # CLIENTES
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento
            FROM clientes
            ORDER BY id DESC
        """))

        rows_clientes = result.fetchall()

        clientes = []
        for r in rows_clientes:
            clientes.append({
                "nome": r[0] or "",
                "cpf": r[1] or "",
                "ip": r[2] or "",
                "cidade": r[3] or "",
                "estado": r[4] or "",
                "score": r[5] if r[5] is not None else 0,
                "forma_pagamento": r[6] or "N/A"
            })

    except Exception as e:
        print("ERRO CLIENTES:", e)
        clientes = []

    # =========================
    # TOTAL PÁGINAS + SLICE
    # =========================
    total_pages = math.ceil(len(clientes) / per_page) if clientes else 1
    clientes = clientes[(page - 1) * per_page : page * per_page]

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

        rows_pedidos = result.fetchall()

        ultimos_pedidos = []

        for r in rows_pedidos:
            ultimos_pedidos.append({
                "id": r[0],
                "status": r[1] or "indefinido",
                "valor": r[2] or 0,
                "forma_pagamento": r[3] or "N/A",
                "ip": r[4] or "",
                "nome_cliente": r[5] or "",
                "risco": random.randint(10, 100)
            })

    except Exception as e:
        print("ERRO PEDIDOS:", e)
        ultimos_pedidos = []

    # =========================
    # MÉTRICAS
    # =========================
    total_usuarios = len(clientes) * total_pages if total_pages > 0 else len(clientes)
    total_pedidos = len(ultimos_pedidos)
    total_logs = 120

    risco_alto = len([c for c in clientes if c.get("score", 0) >= 70])
    risco_medio = len([c for c in clientes if 40 <= c.get("score", 0) < 70])
    risco_baixo = len([c for c in clientes if c.get("score", 0) < 40])

    media_risco = (
        sum(c.get("score", 0) for c in clientes) / len(clientes)
        if clientes else 0
    )

    print(f"[DASHBOARD] clientes={len(clientes)} pedidos={total_pedidos}")
    print("CLIENTES EXEMPLO:", clientes[:2])

    # =========================
    # RENDER TEMPLATE
    # =========================
    return render_template(
        "dashboard.html",
        clientes=clientes,
        ultimos_pedidos=ultimos_pedidos,
        user=current_user,

        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        total_logs=total_logs,

        media_risco=round(media_risco, 2),
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,

        page=page,
        total_pages=total_pages
    )
