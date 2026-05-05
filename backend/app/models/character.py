
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(30), nullable=False)

    # ── 신분 / 자질 ──
    origin = Column(String(20), nullable=False)    # 떠돌이 고아, 몰락세가 후예 ...
    physique = Column(Integer, default=10)          # 근골
    ki = Column(Integer, default=10)                # 기맥
    agility = Column(Integer, default=10)           # 신법
    insight = Column(Integer, default=10)           # 심안
    charm = Column(Integer, default=10)             # 매력
    luck = Column(Integer, default=10)              # 복운

    # ── 전투 스탯 ──
    hp = Column(Integer, default=100)
    max_hp = Column(Integer, default=100)
    mp = Column(Integer, default=50)
    max_mp = Column(Integer, default=50)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    speed = Column(Integer, default=10)
    crit_rate = Column(Float, default=0.05)

    # ── 경험치 / 레벨 ──
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # ── 위치 ──
    current_room_id = Column(Integer, ForeignKey("rooms.id"), default=1)

    # ── 무공 경지 ──
    martial_stage = Column(String(20), default="입문")  # 입문→소성→대성→...

    # ── 성향 ──
    righteousness = Column(Integer, default=0)  # 의
    heroism = Column(Integer, default=0)        # 협
    greed = Column(Integer, default=0)          # 욕
    coldness = Column(Integer, default=0)       # 냉
    madness = Column(Integer, default=0)        # 광
    affection = Column(Integer, default=0)       # 정

    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User")
