from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from models.base import Base
from datetime import datetime, date

class Bloco(Base):
    __tablename__ = 'bloco'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    classificacao = Column(String, nullable=False)
    coloracao = Column(String, nullable=False)
    material = Column(String, nullable=False)
    medida_bruta = Column(String, nullable=False)
    volume_bruto = Column(String, nullable=False)
    medida_liquida = Column(String, nullable=False)
    volume_liquido = Column(String, nullable=False)
    pedreira = Column(String, nullable=False)
    observacoes = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data_criacao = Column(Date, nullable=False)
    data_alteracao = Column(Date, nullable=False)
    estado = Column(String, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    status = Column(String, nullable=False)
    imagem = Column(String, nullable=False)

    def to_dict(self):
        result = {}
        
        for column in self.__table__.columns:
            value = getattr(self, column.name)            
            if isinstance(value, (datetime, date)):
                result[column.name] = value.isoformat() if value else None
            else:
                result[column.name] = value
                
        return result