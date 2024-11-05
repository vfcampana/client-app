from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey


# Responsible for changing block's owners and have the transaction data
class Purchase(db.Model):
    __tablename__ = 'purchase'

    id_transacao = Column(Integer, primary_key=True)
    id_vendedor = Column(Integer, nullable=False)
    id_comprador = Column(Integer, nullable=False)
    data_venda = Column(DateTime, nullable=False, default=datetime.now)
    data_sincronizacaoBC = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, company_info: dict):
        self.id_transacao = company_info.get("id_empresa")
        self.id_vendedor = company_info.get("razao_social")
        self.id_comprador = company_info.get("cnpj")
        self.data_venda = company_info.get("email")
        self.data_sincronizacaoBC = company_info.get("senha")

