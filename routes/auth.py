from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func

from models import Usuario

auth = Blueprint("auth", __name__)


# =========================
# REDIRECIONA ROOT
# =========================
@auth.route("/")
def home():
    return redirect(url_for("auth.login"))


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    # 🔥 se já estiver logado, vai pro dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":

        email = (request.form.get("email") or "").strip()
        senha = request.form.get("senha") or ""

        # validação básica
        if not email or not senha:
            flash("Preencha todos os campos", "danger")
            return render_template("login.html")

        # busca usuário (case insensitive)
        usuario = Usuario.query.filter(
            func.lower(Usuario.email) == email.lower()
        ).first()

        # valida senha
        if usuario and usuario.check_password(senha):

            login_user(usuario, remember=True)

            flash("Login realizado com sucesso", "success")

            return redirect(url_for("dashboard.home"))

        flash("Email ou senha inválidos", "danger")

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
