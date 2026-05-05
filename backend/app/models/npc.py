
from sqlalchemy import Column, Integer, String, Boolean
from ..core.database import Base

class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    title = Column(String(100), default="")
    description = Column(String(1000), default="")
    dialogue = Column(String(2000), default="")
    is_hostile = Column(Boolean, default=False)
    hp = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    faction = Column(String(50), default="")
