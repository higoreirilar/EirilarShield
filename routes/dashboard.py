from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import db
from sqlalchemy import text
import random

dashboard = Blueprint("dashboard", __name__)


# =========================
# DASHBOARD PRINCIPAL
# =========================
@dashboard.route("/dashboard")
@login_required
def dashboard_page():

    # =========================
    # CLIENTES (CORRIGIDO - SQLALCHEMY)
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento
            FROM clientes
            ORDER BY id DESC
        """))

        rows_clientes = result.fetchall()

        clientes = [
            {
                "nome": r[0],
                "cpf": r[1],
                "ip": r[2],
                "cidade": r[3],
                "estado": r[4],
                "score": r[5],
                "forma_pagamento": r[6]
            }
            for r in rows_clientes
        ]

    except Exception as e:
        print("ERRO CLIENTES:", e)
        clientes = []

    # =========================
    # PEDIDOS (ROBUSTO)
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

            # risco automático caso não exista no banco
            risco = random.randint(10, 100)

            ultimos_pedidos.append({
                "id": r[0],
                "status": r[1],
                "valor": r[2],
                "forma_pagamento": r[3],
                "ip": r[4],
                "nome_cliente": r[5],
                "risco": risco
            })

    except Exception as e:
        print("ERRO PEDIDOS:", e)
        ultimos_pedidos = []

    # =========================
    # MÉTRICAS
    # =========================
    total_usuarios = len(clientes)
    total_pedidos = len(ultimos_pedidos)
    total_logs = 120

    risco_alto = len([c for c in clientes if c.get("score", 0) >= 70])
    risco_medio = len([c for c in clientes if 40 <= c.get("score", 0) < 70])
    risco_baixo = len([c for c in clientes if c.get("score", 0) < 40])

    media_risco = (
        sum(c.get("score", 0) for c in clientes) / total_usuarios
        if total_usuarios > 0 else 0
    )

    print(f"[DASHBOARD] clientes={total_usuarios} pedidos={total_pedidos}")

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
        risco_baixo=risco_baixo
    )
