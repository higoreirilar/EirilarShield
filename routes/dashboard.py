from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from database import db
from sqlalchemy import text
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
    # TOTAL USUÁRIOS
    # =========================
    total_usuarios = db.session.execute(
        text("SELECT COUNT(*) FROM clientes")
    ).scalar() or 0

    # =========================
    # CLIENTES
    # =========================
    result = db.session.execute(text("""
        SELECT id, nome, cpf, ip, cidade, estado, score, forma_pagamento
        FROM clientes
        ORDER BY id DESC
        LIMIT :limit OFFSET :offset
    """), {"limit": per_page, "offset": offset})

    clientes = []
    for r in result.fetchall():
        clientes.append({
            "id": r[0],
            "nome": r[1] or "",
            "cpf": r[2] or "",
            "ip": r[3] or "",
            "cidade": r[4] or "",
            "estado": r[5] or "",
            "score": r[6] or 0,
            "forma_pagamento": r[7] or "N/A"
        })

    # =========================
    # TOTAL PÁGINAS
    # =========================
    total_pages = max(1, math.ceil(total_usuarios / per_page))

    # =========================
    # PEDIDOS
    # =========================
    result = db.session.execute(text("""
        SELECT 
            p.id,
            p.status,
            p.valor,
            c.nome
        FROM pedidos p
        LEFT JOIN clientes c ON c.id = p.cliente_id
        ORDER BY p.id DESC
        LIMIT 10
    """))

    ultimos_pedidos = []
    for r in result.fetchall():
        ultimos_pedidos.append({
            "id": r[0],
            "status": r[1] or "indefinido",
            "valor": float(r[2] or 0),
            "nome_cliente": r[3] or "Desconhecido"
        })

    # =========================
    # TOTAL PEDIDOS
    # =========================
    total_pedidos = db.session.execute(
        text("SELECT COUNT(*) FROM pedidos")
    ).scalar() or 0

    # =========================
    # LOGS (placeholder)
    # =========================
    total_logs = 120

    # =========================
    # RISCO GLOBAL (SEM ERRO)
    # =========================
    media_risco = db.session.execute(
        text("SELECT COALESCE(AVG(score), 0) FROM clientes")
    ).scalar() or 0

    risco_alto = db.session.execute(
        text("SELECT COUNT(*) FROM clientes WHERE score >= 70")
    ).scalar() or 0

    risco_medio = db.session.execute(
        text("SELECT COUNT(*) FROM clientes WHERE score >= 40 AND score < 70")
    ).scalar() or 0

    risco_baixo = db.session.execute(
        text("SELECT COUNT(*) FROM clientes WHERE score < 40")
    ).scalar() or 0

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
