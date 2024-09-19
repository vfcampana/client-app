from database import db
from datetime import datetime


# Responsible for changing block's owners and have the transaction data
class Purchase(db.Model):
    id_transacao: int = db.Column(db.Integer, primary_key=True)
    id_vendedor: int = db.Column(db.Integer)
    id_comprador: int = db.Column(db.Integer)
    data_venda: datetime = db.Column(db.DateTime)
    data_sincronizacaoBC: datetime = db.Column(db.DateTime)

    def __init__(self, company_info: dict):
        self.id_transacao: int = company_info.get("id_empresa")
        self.id_vendedor: str = company_info.get("razao_social")
        self.id_comprador: str = company_info.get("cnpj")
        self.data_venda: str = company_info.get("email")
        self.data_sincronizacaoBC: str = company_info.get("senha")

