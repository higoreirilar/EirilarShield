from flask import Blueprint, render_template, request
from flask_login import login_required

from models import Log, LogAntifraude

logs = Blueprint("logs", __name__)


# =========================
# SOC DASHBOARD DE LOGS
# =========================
@logs.route("/logs")
@login_required
def painel():

    tipo = request.args.get("tipo")

    # logs gerais do sistema
    logs_sistema = Log.query.order_by(Log.id.desc()).limit(50).all()

    # logs antifraude
    antifraude = LogAntifraude.query.order_by(LogAntifraude.id.desc()).limit(50).all()

    # filtros visuais
    if tipo == "sistema":
        antifraude = []
    elif tipo == "antifraude":
        logs_sistema = []

    # métricas estilo SOC
    total_logs = Log.query.count()
    total_af = LogAntifraude.query.count()

    return render_template(
        "logs.html",
        logs=logs_sistema,
        antifraude=antifraude,
        total_logs=total_logs,
        total_af=total_af,
        tipo=tipo
    )
