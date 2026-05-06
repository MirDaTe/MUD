
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Faction(Base):
    __tablename__ = "factions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    faction_type = Column(String(20), nullable=False)  # 정파/사파/마도/중립/특수
    description = Column(String(1000), default="")
    benefits = Column(JSON, default=dict)  # {stat_bonus, martial_art_ids, ...}
    join_requirements = Column(JSON, default=dict)  # {level, reputation, quest_id, ...}
    rival_faction_id = Column(Integer, nullable=True)
