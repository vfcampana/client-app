from datetime import datetime
from company_user import CompanyUser
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey


class OrnamentalBlock(db.Model):
    __tablename__ = 'ornamental_block'

    id_bloco = Column(Integer, primary_key=True)
    id_dono = Column(Integer, ForeignKey('companyuser.id_empresa'))
    material = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registrado = Column(DateTime, default=datetime.now)
    atualizado = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, id_dono, material):
        self.id_dono = id_dono
        self.material = material
        self.is_active = True
        self.registrado = default=datetime.now()
        self.atualizado = default=datetime.now()
