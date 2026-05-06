
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from ..core.database import Base

class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(500), default="")
    leader_id = Column(Integer, ForeignKey("characters.id"), nullable=False)  # 길드장 캐릭터ID
    faction_id = Column(Integer, nullable=True)  # 소속 문파 (선택)
    reputation = Column(Integer, default=0)  # 길드 명성
    gold = Column(Integer, default=0)  # 길드 공용 금고
    member_count = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
