from database import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================
# USUÁRIOS
# ==========================================
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, unique=True, nullable=False)

    senha = db.Column(db.Text, nullable=False)

    role = db.Column(db.Text, default="usuario")

    created_at = db.Column(db.Text)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def __repr__(self):
        return f"<Usuario {self.email}>"

# ==========================================
# PEDIDOS
# ==========================================
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.String(100))

    cliente = db.Column(db.String(255))
    email = db.Column(db.String(255))
    cpf = db.Column(db.String(20))
    telefone = db.Column(db.Text)

    valor = db.Column(db.Numeric)

    status = db.Column(db.String(50))
    motivo = db.Column(db.Text)

    ip = db.Column(db.String(50))
    pais = db.Column(db.String(80))
    estado = db.Column(db.String(80))
    cidade = db.Column(db.String(80))

    rua = db.Column(db.Text)
    bairro = db.Column(db.Text)
    cep = db.Column(db.Text)

    dispositivo = db.Column(db.Text)

    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)

    score_risco = db.Column(db.Integer)

    analisado_por = db.Column(db.String(255))

    created_at = db.Column(db.DateTime)
    data_analise = db.Column(db.DateTime)


# ==========================================
# ORDERS (inglês)
# ==========================================
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    order_code = db.Column(db.String(120))

    user_id = db.Column(db.Integer)

    amount = db.Column(db.Numeric)

    status = db.Column(db.String(60))

    risk_score = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)


# ==========================================
# LOGIN SESSIONS
# ==========================================
class LoginSession(db.Model):
    __tablename__ = "login_sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    ip = db.Column(db.String(60))

    user_agent = db.Column(db.Text)

    status = db.Column(db.String(60))

    created_at = db.Column(db.DateTime)


# ==========================================
# LOGS
# ==========================================
class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.Text)

    acao = db.Column(db.Text)

    detalhes = db.Column(db.Text)

    created_at = db.Column(db.DateTime)


# ==========================================
# LOGS ANTIFRAUDE
# ==========================================
class LogAntifraude(db.Model):
    __tablename__ = "logs_antifraude"

    id = db.Column(db.Integer, primary_key=True)

    usuario = db.Column(db.String(255))

    acao = db.Column(db.String(255))

    detalhe = db.Column(db.Text)

    pedido_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)


# ==========================================
# ANTIFRAUD LOGS
# ==========================================
class AntifraudLog(db.Model):
    __tablename__ = "antifraud_logs"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.String(120))

    ip = db.Column(db.String(60))

    status = db.Column(db.String(60))

    reason = db.Column(db.Text)

    risk_score = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)


# ==========================================
# RISK ANALYSIS
# ==========================================
class RiskAnalysis(db.Model):
    __tablename__ = "risk_analysis"

    id = db.Column(db.Integer, primary_key=True)

    target_type = db.Column(db.String(60))

    target_value = db.Column(db.String(255))

    risk_level = db.Column(db.String(40))

    score = db.Column(db.Integer)

    status = db.Column(db.String(40))

    created_at = db.Column(db.DateTime)


# ==========================================
# BLOCKED IPS
# ==========================================
class BlockedIP(db.Model):
    __tablename__ = "blocked_ips"

    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.String(50), nullable=False, unique=True)

    reason = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<BlockedIP {self.ip}>"

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "reason": self.reason,
            "created_at": (
                self.created_at.strftime("%d/%m/%Y %H:%M")
                if self.created_at
                else None
            )
        }
