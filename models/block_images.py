from database import db
from datetime import datetime


class BlockImages:
    image_id: int = db.Column(db.Integer, primary_key=True)
    url: str = db.Column(db.String(180))
    block_id: int = db.Column(db.Integer)

    # def __init__(self, url, : dict):
    #     self.image_id: int = company_info.get("image_id")
    #     self.url: int = company_info.get("url")
    #     self.block_id: str = company_info.get("block_id")
