from flask import Blueprint, jsonify
from database import db
from sqlalchemy import text

acoes = Blueprint("acoes", __name__)


# =========================
# 🔴 BLOQUEAR CLIENTE
# =========================
@acoes.route("/cliente/bloquear/<int:id>", methods=["POST"])
def bloquear(id):
    try:
        db.session.execute(
            text("UPDATE clientes SET status='bloqueado' WHERE id=:id"),
            {"id": id}
        )
        db.session.commit()
        return jsonify({"status": "bloqueado", "id": id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# 🟢 DESBLOQUEAR CLIENTE
# =========================
@acoes.route("/cliente/desbloquear/<int:id>", methods=["POST"])
def desbloquear(id):
    try:
        db.session.execute(
            text("UPDATE clientes SET status='ativo' WHERE id=:id"),
            {"id": id}
        )
        db.session.commit()
        return jsonify({"status": "ativo", "id": id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# 🟡 EM ANÁLISE
# =========================
@acoes.route("/cliente/analise/<int:id>", methods=["POST"])
def analise(id):
    try:
        db.session.execute(
            text("UPDATE clientes SET status='analise' WHERE id=:id"),
            {"id": id}
        )
        db.session.commit()
        return jsonify({"status": "analise", "id": id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# 🔵 DETALHES COMPLETOS
# =========================
@acoes.route("/cliente/detalhes/<int:id>")
def detalhes(id):
    try:
        r = db.session.execute(text("""
            SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento, telefone
            FROM clientes
            WHERE id=:id
        """), {"id": id}).fetchone()

        if not r:
            return jsonify({"error": "Cliente não encontrado"}), 404

        return jsonify({
            "nome": r[0],
            "cpf": r[1],
            "ip": r[2],
            "cidade": r[3],
            "estado": r[4],
            "score": r[5],
            "forma_pagamento": r[6],
            "telefone": r[7]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🟣 LIGAR CLIENTE (SIMULAÇÃO)
# =========================
@acoes.route("/cliente/ligar/<int:id>", methods=["POST"])
def ligar(id):
    try:
        r = db.session.execute(
            text("SELECT telefone FROM clientes WHERE id=:id"),
            {"id": id}
        ).fetchone()

        if not r:
            return jsonify({"error": "Cliente não encontrado"}), 404

        return jsonify({"telefone": r[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
