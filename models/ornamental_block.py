from datetime import datetime
from company_user import CompanyUser
from sqlalchemy import ForeignKey
from flask_login import UserMixin

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey


class OrnamentalBlock(Base, UserMixin):
    __tablename__ = 'ornamental_block'

    id_bloco = Column(Integer, primary_key=True, autoincrement=True)
    id_dono = Column(Integer, ForeignKey('companyuser.id_empresa'))
    material = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registrado = Column(DateTime, default=datetime.now)
    atualizado = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    valor = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    classificao = Column(String, nullable=False)
    coloracao = Column(String, nullable=False)
    medida_bruta = Column(String, nullable=False)
    volume_bruto = Column(String, nullable=False)
    medida_liquida = Column(String, nullable=False)
    volume_liquido = Column(String, nullable=False)
    pedreira = Column(String, nullable=False)
    frente_pedreira = Column(String, nullable=False)
    info = Column(Text, nullable=False)
    cep = Column(String, nullable=False)
    frete = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    
    def __init__(self, id_dono, material):
        self.id_dono = id_dono
        self.material = material
        self.is_active = True
        self.registrado = datetime.now()
        self.atualizado = datetime.now()
