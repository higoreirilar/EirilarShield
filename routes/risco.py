from flask import Blueprint, render_template
from flask_login import login_required

from models import RiskAnalysis, Pedido, Log

risco = Blueprint("risco", __name__)


# =========================
# DASHBOARD DE RISCO
# =========================
@risco.route("/risco")
@login_required
def painel():

    analises = RiskAnalysis.query.order_by(RiskAnalysis.id.desc()).limit(100).all()

    pedidos_alto_risco = Pedido.query.filter(Pedido.score_risco >= 70).count()
    pedidos_medio_risco = Pedido.query.filter(Pedido.score_risco.between(30, 69)).count()
    pedidos_baixo_risco = Pedido.query.filter(Pedido.score_risco < 30).count()

    logs_suspeitos = Log.query.filter(Log.acao.ilike("%suspeit%")).count()

    media_risco = 0
    scores = [p.score_risco for p in Pedido.query.all() if p.score_risco is not None]

    if scores:
        media_risco = sum(scores) / len(scores)

    return render_template(
        "risco.html",
        analises=analises,
        alto=pedidos_alto_risco,
        medio=pedidos_medio_risco,
        baixo=pedidos_baixo_risco,
        logs_suspeitos=logs_suspeitos,
        media=round(media_risco, 2)
    )
