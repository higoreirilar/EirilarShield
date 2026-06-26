from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func

from models import Usuario

auth = Blueprint("auth", __name__)


# =========================
# REDIRECIONAMENTO INICIAL
# =========================
@auth.route("/")
def home():
    return redirect(url_for("auth.login"))


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("login.html")

        # busca usuário (case-insensitive)
        usuario = Usuario.query.filter(
            func.lower(Usuario.email) == email.lower()
        ).first()

        # valida senha (hash)
        if usuario and usuario.check_password(senha):

            login_user(usuario)

            return redirect(url_for("dashboard.dashboard"))

        flash("Email ou senha inválidos.", "danger")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logout realizado com sucesso.", "success")

    return redirect(url_for("auth.login"))
