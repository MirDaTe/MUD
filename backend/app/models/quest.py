
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quest_type = Column(String(20), nullable=False)  # main/side/faction/romance/bounty/event
    description = Column(String(1000), default="")
    objectives = Column(JSON, default=dict)  # {type: "kill"/"talk"/"collect", target: "...", count: N}
    rewards = Column(JSON, default=dict)  # {exp, gold, items: [...], martial_art_id, affection_target, ...}
    prerequisites = Column(JSON, default=dict)  # {level, faction_id, affection_min, quest_ids_done, ...}
    next_quest_id = Column(Integer, nullable=True)
    faction_id = Column(Integer, nullable=True)
    min_level = Column(Integer, default=1)
    giver_npc_id = Column(Integer, nullable=True)  # 퀘스트 주는 NPC ID
    story_text = Column(String(2000), default="")  # NPC가 퀘스트 줄 때 하는 스토리 대사
    accept_text = Column(String(500), default="")  # 수락 시 출력
    complete_text = Column(String(500), default="")  # 완료 시 NPC 대사
