from flask import Blueprint, render_template
from flask_login import login_required

from models import Usuario

usuarios = Blueprint("usuarios", __name__)


# =========================
# LISTA DE USUÁRIOS
# =========================
@usuarios.route("/usuarios")
@login_required
def listar():

    lista_usuarios = Usuario.query.order_by(Usuario.id.desc()).all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )
