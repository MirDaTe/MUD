
from sqlalchemy import Column, Integer, String, Float, JSON, Boolean
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

    # 드랍 아이템 (구버전 호환용)
    loot = Column(JSON, default=list)

    # 레벨 기반 드롭테이블 시스템
    min_level = Column(Integer, default=1)       # 최소 출현 레벨대
    max_level = Column(Integer, default=999)     # 최대 출현 레벨대
    drop_table = Column(JSON, default=list)      # [{"item_code":"WPN_...","rate":0.05,"min_qty":1,"max_qty":1}, ...]
    is_boss = Column(Boolean, default=False)     # 보스 몬스터 여부
    gold_reward = Column(Integer, default=0)     # 금화 보상
    fame_reward = Column(Integer, default=0)     # 명성 보상

    # 전투 로그 템플릿 (공격/피격/사망)
    attack_templates = Column(JSON, default=list)
    death_template = Column(String(500), default="")

    # 리스폰 및 선공 설정
    is_aggro = Column(Boolean, default=False)      # 선공 몬스터 여부
    respawn_min = Column(Integer, default=30)       # 최소 리스폰 시간(초)
    respawn_max = Column(Integer, default=120)      # 최대 리스폰 시간(초)

    # ambient 대사 (방에 있을 때 랜덤 출력)
    ambient_lines = Column(JSON, default=list)  # ["크르릉...", "우어어!"]
