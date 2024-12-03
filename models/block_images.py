from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from . import Base

    
class BlockImages(Base):
    __tablename__ = 'block_images'

    image_id = Column(Integer, primary_key=True)
    url = Column(String(180), nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.id'), nullable=False)

    # def __init__(self, url, : dict):
    #     self.image_id: int = company_info.get("image_id")
    #     self.url: int = company_info.get("url")
    #     self.block_id: str = company_info.get("block_id")

