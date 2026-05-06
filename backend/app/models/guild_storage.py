
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class GuildStorage(Base):
    __tablename__ = "guild_storage"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=0)
    deposited_by = Column(Integer, nullable=True)  # 넣은 캐릭터ID
