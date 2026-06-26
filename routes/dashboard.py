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
    # PAGINAÇÃO CLIENTES
    # =========================
    page = request.args.get("page", 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # =========================
    # TOTAL USUÁRIOS
    # =========================
    try:
        total_usuarios = db.session.execute(
            text("SELECT COUNT(*) FROM clientes")
        ).scalar()
    except:
        total_usuarios = 0

    # =========================
    # CLIENTES (🔥 AGORA COM ID)
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT id, nome, cpf, ip, cidade, estado, score, forma_pagamento
            FROM clientes
            ORDER BY id DESC
            LIMIT :limit OFFSET :offset
        """), {"limit": per_page, "offset": offset})

        clientes = [
            {
                "id": r[0],
                "nome": r[1] or "",
                "cpf": r[2] or "",
                "ip": r[3] or "",
                "cidade": r[4] or "",
                "estado": r[5] or "",
                "score": r[6] or 0,
                "forma_pagamento": r[7] or "N/A"
            }
            for r in result.fetchall()
        ]

    except Exception as e:
        print("ERRO CLIENTES:", e)
        clientes = []

    # =========================
    # TOTAL PÁGINAS
    # =========================
    total_pages = math.ceil(total_usuarios / per_page) if total_usuarios else 1

    # =========================
    # PEDIDOS
    # =========================
    try:
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

        ultimos_pedidos = [
            {
                "id": r[0],
                "status": r[1] or "indefinido",
                "valor": float(r[2] or 0),
                "nome_cliente": r[3] or "Desconhecido"
            }
            for r in result.fetchall()
        ]

    except:
        ultimos_pedidos = []

    # =========================
    # TOTAL PEDIDOS
    # =========================
    try:
        total_pedidos = db.session.execute(
            text("SELECT COUNT(*) FROM pedidos")
        ).scalar()
    except:
        total_pedidos = 0

    # =========================
    # LOGS
    # =========================
    total_logs = 120

    # =========================
    # RISCO
    # =========================
    try:
        media_risco = db.session.execute(text("""
            SELECT COALESCE(AVG(score), 0) FROM clientes
        """)).scalar()

        risco_alto = db.session.execute(text("""
            SELECT COUNT(*) FROM clientes WHERE score >= 70
        """)).scalar()

        risco_medio = db.session.execute(text("""
            SELECT COUNT(*) FROM clientes WHERE score >= 40 AND score < 70
        """)).scalar()

        risco_baixo = db.session.execute(text("""
            SELECT COUNT(*) FROM clientes WHERE score < 40
        """)).scalar()

    except:
        media_risco = 0
        risco_alto = 0
        risco_medio = 0
        risco_baixo = 0

    # =========================
    # DEBUG
    # =========================
    print(f"[DASHBOARD] clientes={len(clientes)}")

    # =========================
    # TEMPLATE
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
