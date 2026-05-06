
from sqlalchemy import Column, Integer, String, JSON, Float
from ..core.database import Base

class MartialArt(Base):
    __tablename__ = "martial_arts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    category = Column(String(20), nullable=False)  # 검법/도법/장법/권법/지법/암기/경공/호신강기/내공심법/진법/독공/악기공
    description = Column(String(500), default="")
    stage_required = Column(String(20), default="입문")  # 필요 경지
    damage_multiplier = Column(Float, default=1.0)
    mp_cost = Column(Integer, default=10)
    cooldown_ticks = Column(Integer, default=3)
    cast_time_ticks = Column(Integer, default=1)
    effect_type = Column(String(20), default="damage")  # damage/heal/buff/debuff/dot
    effect_params = Column(JSON, default=dict)  # {dmg_bonus, dot_dmg, dot_duration, ...}
    flavor_text = Column(String(500), default="")  # 발동 시 문구
    crit_text = Column(String(500), default="")
    rarity = Column(Integer, default=1)  # 1-5
    faction_id = Column(Integer, nullable=True)  # 특정 문파 소속 무공
