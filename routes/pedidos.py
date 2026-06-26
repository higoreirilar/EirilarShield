from flask import Blueprint, render_template, request
from flask_login import login_required

from models import Pedido

pedidos = Blueprint("pedidos", __name__)


# =========================
# LISTA DE PEDIDOS
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

    # busca simples (cliente/email/order_id)
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
