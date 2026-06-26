from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Usuario, Pedido, Log, RiskAnalysis, LoginSession

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():

    # =========================
    # KPIs
    # =========================
    total_usuarios = Usuario.query.count() or 0
    total_pedidos = Pedido.query.count() or 0
    total_logs = Log.query.count() or 0
    total_sessoes = LoginSession.query.count() or 0

    # =========================
    # RISCO (SAFE)
    # =========================
    try:
        risco_total = RiskAnalysis.query.count() or 0

        risco_alto = RiskAnalysis.query.filter_by(risk_level="alto").count() or 0
        risco_medio = RiskAnalysis.query.filter_by(risk_level="medio").count() or 0
        risco_baixo = RiskAnalysis.query.filter_by(risk_level="baixo").count() or 0

        scores = [
            r.score for r in RiskAnalysis.query.all()
            if r.score is not None
        ]

        media_risco = round(sum(scores) / len(scores), 2) if scores else 0

    except Exception as e:
        print("ERRO RISCO:", e)

        risco_total = 0
        risco_alto = 0
        risco_medio = 0
        risco_baixo = 0
        media_risco = 0

    # =========================
    # ÚLTIMOS REGISTROS (SAFE)
    # =========================
    try:
        ultimos_pedidos = Pedido.query.order_by(Pedido.id.desc()).limit(5).all()
    except:
        ultimos_pedidos = []

    try:
        ultimos_logs = Log.query.order_by(Log.id.desc()).limit(5).all()
    except:
        ultimos_logs = []

    try:
        ultimas_sessoes = LoginSession.query.order_by(LoginSession.id.desc()).limit(5).all()
    except:
        ultimas_sessoes = []

    # =========================
    # TEMPLATE
    # =========================
    return render_template(
        "dashboard.html",
        user=current_user,

        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        total_logs=total_logs,
        total_sessoes=total_sessoes,

        risco_total=risco_total,
        risco_alto=risco_alto,
        risco_medio=risco_medio,
        risco_baixo=risco_baixo,
        media_risco=media_risco,

        ultimos_pedidos=ultimos_pedidos,
        ultimos_logs=ultimos_logs,
        ultimas_sessoes=ultimas_sessoes
    )
