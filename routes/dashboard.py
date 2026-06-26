from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Usuario, Pedido, Log, RiskAnalysis, LoginSession

dashboard = Blueprint("dashboard", __name__)


# =========================
# DASHBOARD PRINCIPAL
# =========================
@dashboard.route("/dashboard")
@login_required
def home():

    # =========================
    # KPIs PRINCIPAIS
    # =========================
    total_usuarios = Usuario.query.count()
    total_pedidos = Pedido.query.count()
    total_logs = Log.query.count()
    total_sessoes = LoginSession.query.count()

    # =========================
    # RISCO
    # =========================
    risco_total = RiskAnalysis.query.count()

    risco_alto = RiskAnalysis.query.filter_by(risk_level="alto").count()
    risco_medio = RiskAnalysis.query.filter_by(risk_level="medio").count()
    risco_baixo = RiskAnalysis.query.filter_by(risk_level="baixo").count()

    # média de score (seguro contra None)
    scores = [r.score for r in RiskAnalysis.query.all() if r.score is not None]
    media_risco = sum(scores) / len(scores) if scores else 0

    # =========================
    # ÚLTIMOS REGISTROS
    # =========================
    ultimos_pedidos = Pedido.query.order_by(Pedido.id.desc()).limit(5).all()
    ultimos_logs = Log.query.order_by(Log.id.desc()).limit(5).all()
    ultimas_sessoes = LoginSession.query.order_by(LoginSession.id.desc()).limit(5).all()

    # =========================
    # RETORNO PARA TEMPLATE
    # =========================
    return render_template(
        "dashboard.html",

        user=current_user,

        # KPIs
        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        total_logs=total_logs,
        total_sessoes=total_sessoes,

        # risco
        risco_total=risco_total,
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,
        media_risco=round(media_risco, 2),

        # listas
        ultimos_pedidos=ultimos_pedidos,
        ultimos_logs=ultimos_logs,
        ultimas_sessoes=ultimas_sessoes
    )
