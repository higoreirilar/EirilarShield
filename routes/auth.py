from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from database import db
from models import Usuario

auth = Blueprint("auth", __name__)


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    # se já estiver logado, vai direto pro dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            flash("Preencha todos os campos", "error")
            return redirect(url_for("auth.login"))

        user = Usuario.query.filter_by(email=email).first()

        if not user:
            flash("Usuário não encontrado", "error")
            return redirect(url_for("auth.login"))

        # verifica senha hash
        if not check_password_hash(user.senha, senha):
            flash("Senha incorreta", "error")
            return redirect(url_for("auth.login"))

        login_user(user)

        flash("Login realizado com sucesso", "success")

        # 🔥 CORREÇÃO PRINCIPAL DO SEU ERRO
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema", "info")
    return redirect(url_for("auth.login"))
