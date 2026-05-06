
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from ..core.database import Base

class GuildMember(Base):
    __tablename__ = "guild_members"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, unique=True)
    rank = Column(String(20), default="신입")  # 신입→일반→정예→부길드장→길드장
    contribution = Column(Integer, default=0)  # 개인 기여도
    joined_at = Column(DateTime, server_default=func.now())
