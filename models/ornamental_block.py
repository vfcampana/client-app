from datetime import datetime
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from . import Base


class OrnamentalBlock(Base):
    __tablename__ = 'ornamental_block'

    id_bloco = Column(Integer, primary_key=True, unique=True)
    id_dono = Column(Integer, ForeignKey('company_users.id'))
    material = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registrado = Column(DateTime, default=datetime.now)
    atualizado = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    valor = Column(Float, nullable=False)
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
    
    
    def to_dict(self):
        return {
            'id_bloco': self.id_bloco,
            'id_dono': self.id_dono,
            'material': self.material,
            'is_active': self.is_active,
            'registrado': self.registrado,
            'atualizado': self.atualizado,
            'valor': self.valor,
            'titulo': self.titulo,
            'classificao': self.classificao,
            'coloracao': self.coloracao,
            'medida_bruta': self.medida_bruta,
            'volume_bruto': self.volume_bruto,
            'medida_liquida': self.medida_liquida,
            'volume_liquido': self.volume_liquido,
            'pedreira': self.pedreira,
            'frente_pedreira': self.frente_pedreira,
            'info': self.info,
            'cep': self.cep,
            'frete': self.frete,
            'localizacao': self.localizacao
        }
        
    def trasferir_propriedade(self, novo_dono):
        self.id_dono = novo_dono
        self.atualizado = datetime.now()
    
    