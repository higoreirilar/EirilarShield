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
    # CLIENTES PAGINADOS
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
    # TOTAL PÁGINAS
    # =========================
    total_pages = math.ceil(total_usuarios / per_page) if total_usuarios else 1

    # =========================
    # PEDIDOS (JOIN CORRETO)
    # =========================
    try:
        result = db.session.execute(text("""
            SELECT 
                p.id,
                p.status,
                p.valor,
                c.nome AS nome_cliente
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

    except Exception as e:
        print("ERRO PEDIDOS:", e)
        ultimos_pedidos = []

    # =========================
    # TOTAL PEDIDOS REAL
    # =========================
    try:
        total_pedidos = db.session.execute(
            text("SELECT COUNT(*) FROM pedidos")
        ).scalar()
    except:
        total_pedidos = 0

    # =========================
    # LOGS (placeholder)
    # =========================
    total_logs = 120

    # =========================
    # RISCO GLOBAL (BANCO TODO)
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
    print(f"[DASHBOARD] usuarios={total_usuarios} clientes_page={len(clientes)}")

    # =========================
    # RENDER TEMPLATE
    # =========================
    return render_template(
        "dashboard.html",

        # dados
        clientes=clientes,
        ultimos_pedidos=ultimos_pedidos,
        user=current_user,

        # KPIs
        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        total_logs=total_logs,
        media_risco=round(media_risco, 2),

        # risco global
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,

        # paginação
        page=page,
        total_pages=total_pages
    )
