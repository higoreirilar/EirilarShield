from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from models import db

# ⚠️ Ajuste o nome da sua tabela/model se for diferente
from models import Alerta  # precisa existir no seu models.py


alertas = Blueprint("alertas", __name__, url_prefix="/alertas")


# =========================
# LISTAR ALERTAS
# =========================
@alertas.route("/", methods=["GET"])
@login_required
def listar_alertas():

    try:
        todos_alertas = Alerta.query.order_by(Alerta.id.desc()).all()

        return render_template(
            "alerts.html",
            alertas=todos_alertas
        )

    except Exception as e:
        print("ERRO ALERTAS:", e)
        return render_template("alerts.html", alertas=[])


# =========================
# MARCAR COMO LIDO
# =========================
@alertas.route("/marcar/<int:alerta_id>", methods=["POST"])
@login_required
def marcar_como_lido(alerta_id):

    try:
        alerta = Alerta.query.get(alerta_id)

        if not alerta:
            flash("Alerta não encontrado", "danger")
            return redirect(url_for("alertas.listar_alertas"))

        alerta.status = "lido"
        alerta.data_leitura = datetime.utcnow()

        db.session.commit()

        flash("Alerta marcado como lido", "success")

    except Exception as e:
        db.session.rollback()
        print("ERRO AO MARCAR ALERTA:", e)
        flash("Erro ao atualizar alerta", "danger")

    return redirect(url_for("alertas.listar_alertas"))
