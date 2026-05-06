
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from ..core.database import Base

class GuildApplication(Base):
    __tablename__ = "guild_applications"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    status = Column(String(10), default="pending")  # pending/accepted/rejected
    applied_at = Column(DateTime, server_default=func.now())
