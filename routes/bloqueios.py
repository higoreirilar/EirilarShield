from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from database import db
from models import (
    BlockedIP,
    BlockedEmail,
    BlockedCPF,
    BlockedDevice,
    TrustedIP
)

bloqueios = Blueprint("bloqueios", __name__)


# =========================
# DASHBOARD DE BLOQUEIOS
# =========================
@bloqueios.route("/bloqueios")
@login_required
def painel():

    return render_template(
        "bloqueados.html",
        ips=BlockedIP.query.order_by(BlockedIP.id.desc()).all(),
        emails=BlockedEmail.query.order_by(BlockedEmail.id.desc()).all(),
        cpfs=BlockedCPF.query.order_by(BlockedCPF.id.desc()).all(),
        devices=BlockedDevice.query.order_by(BlockedDevice.id.desc()).all(),
        trusted=TrustedIP.query.order_by(TrustedIP.id.desc()).all()
    )


# =========================
# BLOQUEAR IP
# =========================
@bloqueios.route("/bloquear/ip", methods=["POST"])
@login_required
def bloquear_ip():

    ip = request.form.get("ip")
    motivo = request.form.get("motivo")

    if ip:
        db.session.add(BlockedIP(ip=ip, reason=motivo))
        db.session.commit()

    return redirect(url_for("bloqueios.painel"))


# =========================
# BLOQUEAR EMAIL
# =========================
@bloqueios.route("/bloquear/email", methods=["POST"])
@login_required
def bloquear_email():

    email = request.form.get("email")
    motivo = request.form.get("motivo")

    if email:
        db.session.add(BlockedEmail(email=email, reason=motivo))
        db.session.commit()

    return redirect(url_for("bloqueios.painel"))


# =========================
# BLOQUEAR CPF
# =========================
@bloqueios.route("/bloquear/cpf", methods=["POST"])
@login_required
def bloquear_cpf():

    cpf = request.form.get("cpf")
    motivo = request.form.get("motivo")

    if cpf:
        db.session.add(BlockedCPF(cpf=cpf, reason=motivo))
        db.session.commit()

    return redirect(url_for("bloqueios.painel"))


# =========================
# BLOQUEAR DEVICE
# =========================
@bloqueios.route("/bloquear/device", methods=["POST"])
@login_required
def bloquear_device():

    device = request.form.get("device")
    motivo = request.form.get("motivo")

    if device:
        db.session.add(BlockedDevice(device_id=device, reason=motivo))
        db.session.commit()

    return redirect(url_for("bloqueios.painel"))


# =========================
# CONFIAR EM IP
# =========================
@bloqueios.route("/confiar/ip", methods=["POST"])
@login_required
def confiar_ip():

    ip = request.form.get("ip")
    obs = request.form.get("obs")

    if ip:
        db.session.add(TrustedIP(ip=ip, observation=obs))
        db.session.commit()

    return redirect(url_for("bloqueios.painel"))
