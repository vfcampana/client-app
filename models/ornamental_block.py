from database import db
from datetime import datetime
from company_user import CompanyUser
from sqlalchemy import ForeignKey
from datetime import datetime


class OrnamentalBlock(db.Model):
    id_bloco: int = db.Column(db.Integer, primary_key=True)
    id_dono: int = db.Column(db.Integer, ForeignKey('companyuser.id_empresa'))
    material: str = db.Column()
    is_active: bool = db.Column(db.Boolean, default=True)
    registrado: datetime = db.Column(db.DateTime)
    atualizado: datetime = db.Column(db.DateTime)

    # def __init__(self, block_info: dict):
    #     self.id_bloco: int = block_info.get("id_bloco")
    #     self.id_dono: int = block_info.get("id_dono")
    #     self.material: str = block_info.get("material")
    #     self.is_active: bool = True
    #     self.registrado: datetime = datetime.now()
    #     self.atualizado: datetime = datetime.now()
    #

        # smartcontract_id : check_sum_address.CheckSumAddress
