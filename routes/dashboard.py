from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Usuario, Pedido, Log, RiskAnalysis, LoginSession

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():

    # =========================
    # FUNÇÃO SEGURA PARA COUNT
    # =========================
    def safe_count(model):
        try:
            return model.query.count() or 0
        except Exception as e:
            print(f"COUNT ERROR {model}: {e}")
            return 0

    def safe_query_list(model, limit=5):
        try:
            return model.query.order_by(model.id.desc()).limit(limit).all()
        except Exception as e:
            print(f"QUERY ERROR {model}: {e}")
            return []

    def safe_risk_counts():
        try:
            total = RiskAnalysis.query.count() or 0

            alto = RiskAnalysis.query.filter_by(risk_level="alto").count() or 0
            medio = RiskAnalysis.query.filter_by(risk_level="medio").count() or 0
            baixo = RiskAnalysis.query.filter_by(risk_level="baixo").count() or 0

            scores = [
                r.score for r in RiskAnalysis.query.all()
                if r.score is not None
            ]

            media = round(sum(scores) / len(scores), 2) if scores else 0

            return total, alto, medio, baixo, media

        except Exception as e:
            print("RISK ERROR:", e)
            return 0, 0, 0, 0, 0

    # =========================
    # KPIs
    # =========================
    total_usuarios = safe_count(Usuario)
    total_pedidos = safe_count(Pedido)
    total_logs = safe_count(Log)
    total_sessoes = safe_count(LoginSession)

    # =========================
    # RISCO
    # =========================
    risco_total, risco_alto, risco_medio, risco_baixo, media_risco = safe_risk_counts()

    # =========================
    # LISTAS
    # =========================
    ultimos_pedidos = safe_query_list(Pedido)
    ultimos_logs = safe_query_list(Log)
    ultimas_sessoes = safe_query_list(LoginSession)

    # =========================
    # RENDER
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
