from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy.orm import relationship
from .company_user import CompanyUser
from .ornamental_block import OrnamentalBlock
from .purchase import Purchase
from .block_images import BlockImages



def define_relationships():
    OrnamentalBlock.dono = relationship("CompanyUser")
    
    
define_relationships()