from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from models.base import Base

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

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "classificacao": self.classificacao,
            "coloracao": self.coloracao,
            "material": self.material,
            "medida_bruta": self.medida_bruta,
            "volume_bruto": self.volume_bruto,
            "medida_liquida": self.medida_liquida,
            "volume_liquido": self.volume_liquido,
            "pedreira": self.pedreira,
            "observacoes": self.observacoes,
            "cep": self.cep,
            "logradouro": self.logradouro,
            "pais": self.pais,
            "cidade": self.cidade,
            "valor": self.valor,
            "data_criacao": self.data_criacao,
            "data_alteracao": self.data_alteracao,
            "estado": self.estado,
            "id_usuario": self.id_usuario,
            "status": self.status
        }