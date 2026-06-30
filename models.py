from database import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================
# USUÁRIOS
# ==========================================
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    senha = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, default="usuario")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    data_analise = db.Column(db.DateTime)


# ==========================================
# ORDERS
# ==========================================
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(120))
    user_id = db.Column(db.Integer)

    amount = db.Column(db.Numeric)
    status = db.Column(db.String(60))
    risk_score = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# LOGS
# ==========================================
class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Text)
    acao = db.Column(db.Text)
    detalhes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# BLOCKED IPS
# ==========================================
class BlockedIP(db.Model):
    __tablename__ = "blocked_ips"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), unique=True, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# BLOCKED EMAILS
# ==========================================
class BlockedEmail(db.Model):
    __tablename__ = "blocked_emails"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# BLOCKED CPFS
# ==========================================
class BlockedCPF(db.Model):
    __tablename__ = "blocked_cpfs"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# BLOCKED DEVICES
# ==========================================
class BlockedDevice(db.Model):
    __tablename__ = "blocked_devices"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(255), unique=True, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# TRUSTED IPS
# ==========================================
class TrustedIP(db.Model):
    __tablename__ = "trusted_ips"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), unique=True, nullable=False)
    observation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# ALERTAS DO SISTEMA (FALTAVA ISSO)
# ==========================================
class Alerta(db.Model):
    __tablename__ = "alertas"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(255), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    nivel = db.Column(db.String(50), default="info")
    # info | success | warning | danger

    status = db.Column(db.String(20), default="nao_lido")
    # nao_lido | lido

    origem = db.Column(db.String(100))
    # ex: antifraude, login, pedido, sistema

    usuario_id = db.Column(db.Integer, nullable=True)

    pedido_id = db.Column(db.Integer, nullable=True)

    ip = db.Column(db.String(60))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
