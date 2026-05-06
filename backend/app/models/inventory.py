
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from ..core.database import Base

class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    equipped = Column(Integer, default=0)  # 0=inventory, 1=equipped
    slot = Column(String(20), default="")  # 장착 슬롯명 (빈칸=가방)
    instance_id = Column(String(36), default="")  # 아이템 인스턴스 UUID (장비/강화 추적용)
    affix_data = Column(JSON, default=dict)  # {"prefix_name":"날카로운","prefix_stats":{"attack":5},"suffix_name":"[용의]","suffix_stats":{"crit_rate":0.02}}
