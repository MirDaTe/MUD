
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class CharacterFaction(Base):
    __tablename__ = "character_factions"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    faction_id = Column(Integer, ForeignKey("factions.id"), nullable=False)
    rank = Column(String(20), default="외문제자")  # 외문제자/내문제자/정식제자/수석제자/장로/문주
    contribution = Column(Integer, default=0)
