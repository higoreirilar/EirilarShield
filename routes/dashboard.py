from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import db

dashboard = Blueprint("dashboard", __name__)


# =========================
# DASHBOARD PRINCIPAL
# =========================
@dashboard.route("/dashboard")
@login_required
def dashboard_page():

    # =========================
    # CLIENTES
    # =========================
    cur = db.engine.raw_connection().cursor()

    cur.execute("""
        SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento
        FROM clientes
        ORDER BY id DESC
    """)
    rows = cur.fetchall()

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
        for r in rows
    ]

    # =========================
    # PEDIDOS (EXEMPLO)
    # =========================
    cur.execute("""
        SELECT id, status, valor
        FROM pedidos
        ORDER BY id DESC
        LIMIT 10
    """)
    rows_pedidos = cur.fetchall()

    ultimos_pedidos = [
        {
            "id": r[0],
            "status": r[1],
            "valor": r[2]
        }
        for r in rows_pedidos
    ]

    # =========================
    # MÉTRICAS (EXEMPLO SIMPLES)
    # =========================
    total_usuarios = len(clientes)
    total_pedidos = len(ultimos_pedidos)
    total_logs = 120  # se ainda não tiver tabela de logs

    risco_alto = len([c for c in clientes if c["score"] >= 70])
    risco_medio = len([c for c in clientes if 40 <= c["score"] < 70])
    risco_baixo = len([c for c in clientes if c["score"] < 40])

    media_risco = (
        sum([c["score"] for c in clientes]) / total_usuarios
        if total_usuarios > 0 else 0
    )

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
