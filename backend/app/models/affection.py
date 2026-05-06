
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class Affection(Base):
    __tablename__ = "affections"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    npc_id = Column(Integer, ForeignKey("npcs.id"), nullable=False)
    level = Column(Integer, default=0)  # 0-1000
    stage = Column(String(20), default="경계")  # 경계/관심/신뢰/의지/연모/맹약
    flags = Column(String(500), default="")  # comma-separated event flags
