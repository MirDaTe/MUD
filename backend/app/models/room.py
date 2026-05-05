
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)

    # 이동 경로: {"north": 2, "south": 3, "east": None, ...}
    exits = Column(JSON, default=dict)

    # 이 방에 있는 NPC / 몬스터 (ID 리스트)
    npc_ids = Column(JSON, default=list)
    monster_ids = Column(JSON, default=list)

    # 지역 분류
    region = Column(String(50), default="입문마을")
