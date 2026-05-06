
from sqlalchemy import Column, Integer, String, Boolean, JSON
from ..core.database import Base

class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    title = Column(String(100), default="")
    description = Column(String(1000), default="")
    dialogue = Column(String(2000), default="")
    is_hostile = Column(Boolean, default=False)
    hp = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    faction = Column(String(50), default="")
    occupation = Column(String(50), default="")  # 직업 (상인/의원/스승/정보상 등)
    shop_id = Column(Integer, default=None)  # 연결된 상점 ID (상인 NPC용)
    dialogue_options = Column(JSON, default=list)  # 추가 대화 옵션 리스트
    ambient_lines = Column(JSON, default=list)  # 유저가 방에 들어왔을 때 랜덤 출력할 대사
    quest_giver = Column(Boolean, default=False)  # 퀘스트 주는 NPC 여부
