
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(30), nullable=False)

    # 신분 / 자질
    origin = Column(String(20), nullable=False)
    physique = Column(Integer, default=10)
    ki = Column(Integer, default=10)
    agility = Column(Integer, default=10)
    insight = Column(Integer, default=10)
    charm = Column(Integer, default=10)
    luck = Column(Integer, default=10)

    # 전투 스탯
    hp = Column(Integer, default=100)
    max_hp = Column(Integer, default=100)
    mp = Column(Integer, default=50)
    max_mp = Column(Integer, default=50)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    speed = Column(Integer, default=10)
    crit_rate = Column(Float, default=0.05)

    # 경험치 / 레벨 / 경제
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    gold = Column(Integer, default=100)  # 초기 지급 골드
    max_gold = Column(Integer, default=9999999999)  # 소지금 상한

    # 위치 / 귀환
    current_room_id = Column(Integer, ForeignKey("rooms.id"), default=1)
    return_room_id = Column(Integer, nullable=True)  # 귀환 지정 방 (NULL=미지정)

    # 무공 경지
    martial_stage = Column(String(20), default="입문")

    # 성향
    righteousness = Column(Integer, default=0)
    heroism = Column(Integer, default=0)
    greed = Column(Integer, default=0)
    coldness = Column(Integer, default=0)
    madness = Column(Integer, default=0)
    affection = Column(Integer, default=0)

    # 인벤토리 제한
    inventory_limit = Column(Integer, default=30)  # 최대 30칸 (장착중 포함)

    # 길드 버프 적용 여부 (캐릭터에 영구 적용)
    guild_buff_attack = Column(Integer, default=0)
    guild_buff_defense = Column(Integer, default=0)
    guild_buff_hp = Column(Integer, default=0)
    guild_buff_mp = Column(Integer, default=0)
    guild_buff_speed = Column(Integer, default=0)
    guild_buff_crit = Column(Float, default=0.0)

    # 스토리 출력 여부 (첫 접속 한정)
    story_shown = False  # 비컬럼 — 세션 내에서만 사용

    created_at = Column(DateTime, server_default=func.now())
    owner = relationship("User")
