from database import db
from datetime import datetime

from flask_login import UserMixin


class CompanyUser(db.Model, UserMixin):
    # precisa se chamar id pra login, eu acho
    id: int = db.Column(db.Integer, primary_key=True, unique=True)
    razao_social: str = db.Column(db.String(80), nullable=True)
    cnpj: str = db.Column(db.String(80), nullable=False)
    email: str = db.Column(db.String(80), nullable=False)
    senha: str = db.Column(db.String(80), nullable=False)
    telefones: list = db.Column(db.String(255), nullable=True)
    is_active: bool = db.Column(db.Boolean, default=True)
    registrado: datetime = db.Column(db.DateTime)
    atualizado: datetime = db.Column(db.DateTime)
    qtd_blocos: int = db.Column(db.Integer, default=0)
    role: str = db.Column(db.String(80), nullable=False, default='user')

    def to_dict(self):
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "email": self.email,
            "senha": self.senha,
            "telefones": self.telefones,
            "is_active": self.is_active,
            "registrado": self.registrado,
            "atualizado": self.atualizado,
            "qtd_blocos": self.qtd_blocos,
            "role": self.role
        }
