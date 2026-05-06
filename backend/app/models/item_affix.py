
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class ItemAffix(Base):
    __tablename__ = "item_affixes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True)  # AFF_PREFIX_SHARP / AFF_SUFFIX_DRAGON
    name = Column(String(30))  # "날카로운" / "[용의]"
    affix_type = Column(String(10))  # "prefix" / "suffix"
    tier = Column(Integer, default=1)  # 1~5 등급
    apply_to = Column(JSON, default=list)  # ["weapon","armor"] 등 적용 장비 타입
    stats = Column(JSON, default=dict)  # {"attack": 5, "crit_rate": 0.02} 등 추가 스탯
    description = Column(String(100), default="")
