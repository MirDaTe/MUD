
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class CharacterMartialArt(Base):
    __tablename__ = "character_martial_arts"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    martial_art_id = Column(Integer, ForeignKey("martial_arts.id"), nullable=False)
    proficiency = Column(Integer, default=0)  # 숙련도 0-1000
    stage = Column(String(20), default="입문")  # 습득→소성→대성→원만
