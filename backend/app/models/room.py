
from sqlalchemy import Column, Integer, String, Boolean, JSON
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

    # 안전지역 여부 (전투 불가)
    is_safe = Column(Boolean, default=False)

    # 여관 여부 (귀환장소 지정 가능)
    is_inn = Column(Boolean, default=False)
