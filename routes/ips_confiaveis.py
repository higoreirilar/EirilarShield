from flask import Blueprint, render_template, request, redirect, url_for
from models import TrustedIP
from database import db

ips_confiaveis = Blueprint("ips_confiaveis", __name__)


@ips_confiaveis.route("/ips-confiaveis")
def list():

    ips = TrustedIP.query.all()
    return render_template("ips_confiaveis.html", ips=ips)


@ips_confiaveis.route("/ips-confiaveis/add", methods=["POST"])
def add_ip():

    ip = request.form.get("ip")
    obs = request.form.get("observacao")

    new_ip = TrustedIP(ip=ip, observation=obs)

    db.session.add(new_ip)
    db.session.commit()

    return redirect(url_for("ips_confiaveis.list"))


@ips_confiaveis.route("/ips-confiaveis/delete/<int:id>")
def delete_ip(id):

    ip = TrustedIP.query.get(id)

    db.session.delete(ip)
    db.session.commit()

    return redirect(url_for("ips_confiaveis.list"))
