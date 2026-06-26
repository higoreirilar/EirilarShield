from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from models import Pedido

pedidos = Blueprint("pedidos", __name__)

# =========================
# LISTA DE PEDIDOS (HTML)
# =========================
@pedidos.route("/pedidos")
@login_required
def listar():

    status = request.args.get("status")
    busca = request.args.get("busca")

    query = Pedido.query

    # filtro por status
    if status:
        query = query.filter(Pedido.status == status)

    # busca simples
    if busca:
        query = query.filter(
            (Pedido.cliente.ilike(f"%{busca}%")) |
            (Pedido.email.ilike(f"%{busca}%")) |
            (Pedido.order_id.ilike(f"%{busca}%"))
        )

    lista = query.order_by(Pedido.id.desc()).limit(100).all()

    return render_template(
        "pedidos.html",
        pedidos=lista,
        status=status,
        busca=busca
    )


# =========================
# API JSON (DASHBOARD)
# =========================
@pedidos.route("/api/pedidos")
@login_required
def api_pedidos():

    lista = Pedido.query.order_by(Pedido.id.desc()).limit(100).all()

    return jsonify([
        {
            "id": p.id,
            "ip": p.ip,
            "nome": p.cliente,
            "cpf": getattr(p, "cpf", ""),
            "telefone": getattr(p, "telefone", ""),
            "cidade": getattr(p, "cidade", ""),
            "estado": getattr(p, "estado", ""),
            "valor": p.valor,
            "pagamento": p.pagamento,
            "status": getattr(p, "status", "")
        }
        for p in lista
    ])
