
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    npc_id = Column(Integer, nullable=True)
    room_id = Column(Integer, nullable=True)
    item_ids = Column(JSON, default=list)
    description = Column(String(200), default="")
