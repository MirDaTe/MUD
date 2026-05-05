
from sqlalchemy import Column, Integer, String, Float, JSON
from ..core.database import Base

class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), default="")
    hp = Column(Integer, default=50)
    max_hp = Column(Integer, default=50)
    attack = Column(Integer, default=8)
    defense = Column(Integer, default=3)
    speed = Column(Integer, default=8)
    exp_reward = Column(Integer, default=20)

    # 드랍 아이템
    loot = Column(JSON, default=list)

    # 전투 로그 템플릿 (공격/피격/사망)
    attack_templates = Column(JSON, default=list)
    death_template = Column(String(500), default="")
