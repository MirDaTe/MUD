
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from ..core.database import Base

class GuildBuff(Base):
    __tablename__ = "guild_buffs"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    buff_name = Column(String(50), nullable=False)
    buff_description = Column(String(200), default="")
    reputation_required = Column(Integer, default=0)  # 해금 필요 명성
    is_unlocked = Column(Integer, default=0)  # 0=잠김 1=해금
    stat_bonus = Column(JSON, default=dict)  # {attack:5, defense:3, hp:100, ...}
