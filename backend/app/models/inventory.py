
from sqlalchemy import Column, Integer, ForeignKey
from ..core.database import Base

class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    equipped = Column(Integer, default=0)  # 0=inventory, 1=equipped
