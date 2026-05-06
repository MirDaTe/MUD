
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class CharacterQuest(Base):
    __tablename__ = "character_quests"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    status = Column(String(20), default="active")  # active/completed/failed
    progress = Column(Integer, default=0)  # e.g. kill count
