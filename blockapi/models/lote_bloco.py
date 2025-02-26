from sqlalchemy import Column, Integer, ForeignKey
from extensions import Base

class LoteBlocos(Base):
    __tablename__ = 'lote_blocos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bloco = Column(Integer, ForeignKey('bloco.id'))
    id_lote = Column(Integer, ForeignKey('lote.id'), nullable=False)