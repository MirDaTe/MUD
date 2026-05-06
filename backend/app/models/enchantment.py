"""인챈트/강화 모델 - 아이템 강화 시스템"""
from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base


class Enchantment(Base):
    __tablename__ = "enchantments"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"), nullable=False, unique=True)
    enchant_level = Column(Integer, default=0)  # 0~15 강화 단계
    upgrade_count = Column(Integer, default=0)  # 시도 횟수
    fail_count = Column(Integer, default=0)
