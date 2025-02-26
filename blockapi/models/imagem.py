from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Imagens(Base):
    __tablename__ = 'imagens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    id_bloco = Column(Integer, ForeignKey('bloco.id'), nullable=False)
