from flask import Blueprint, jsonify
from database import db
from sqlalchemy import text

acoes = Blueprint("acoes", __name__)

# 🔴 BLOQUEAR
@acoes.route("/cliente/bloquear/<int:id>", methods=["POST"])
def bloquear(id):
    db.session.execute(text("""
        UPDATE clientes SET status='bloqueado' WHERE id=:id
    """), {"id": id})
    db.session.commit()
    return jsonify({"status": "bloqueado"})


# 🟢 DESBLOQUEAR
@acoes.route("/cliente/desbloquear/<int:id>", methods=["POST"])
def desbloquear(id):
    db.session.execute(text("""
        UPDATE clientes SET status='ativo' WHERE id=:id
    """), {"id": id})
    db.session.commit()
    return jsonify({"status": "ativo"})


# 🟡 ANÁLISE
@acoes.route("/cliente/analise/<int:id>", methods=["POST"])
def analise(id):
    db.session.execute(text("""
        UPDATE clientes SET status='analise' WHERE id=:id
    """), {"id": id})
    db.session.commit()
    return jsonify({"status": "analise"})


# 🔵 DETALHES
@acoes.route("/cliente/detalhes/<int:id>")
def detalhes(id):
    r = db.session.execute(text("""
        SELECT nome, cpf, ip, cidade, estado, score, forma_pagamento, telefone
        FROM clientes WHERE id=:id
    """)).fetchone()

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


# 🟣 LIGAR
@acoes.route("/cliente/ligar/<int:id>", methods=["POST"])
def ligar(id):
    r = db.session.execute(text("""
        SELECT telefone FROM clientes WHERE id=:id
    """)).fetchone()

    return jsonify({"telefone": r[0]})
