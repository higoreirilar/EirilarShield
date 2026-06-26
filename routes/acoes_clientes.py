from flask import Blueprint, jsonify
from database import db
from sqlalchemy import text

acoes = Blueprint("acoes", __name__)

# 🔴 BLOQUEAR
@acoes.route("/cliente/bloquear/<int:id>", methods=["POST"])
def bloquear(id):
    db.session.execute(text("""
        UPDATE clientes
        SET status = 'bloqueado'
        WHERE id = :id
    """), {"id": id})
    db.session.commit()

    return jsonify({"ok": True, "status": "bloqueado"})


# 🟢 DESBLOQUEAR
@acoes.route("/cliente/desbloquear/<int:id>", methods=["POST"])
def desbloquear(id):
    db.session.execute(text("""
        UPDATE clientes
        SET status = 'ativo'
        WHERE id = :id
    """), {"id": id})
    db.session.commit()

    return jsonify({"ok": True, "status": "ativo"})


# 🟡 EM ANÁLISE
@acoes.route("/cliente/analise/<int:id>", methods=["POST"])
def analise(id):
    db.session.execute(text("""
        UPDATE clientes
        SET status = 'analise'
        WHERE id = :id
    """), {"id": id})
    db.session.commit()

    return jsonify({"ok": True, "status": "analise"})
