
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    item_type = Column(String(20), nullable=False)  # weapon/armor/accessory/consumable/rare/misc
    sub_type = Column(String(20), default="")  # 검/도/창/도포/연갑/영약/독/비급조각...
    description = Column(String(500), default="")
    stats = Column(JSON, default=dict)  # {attack, defense, speed, hp, mp, ...}
    effects = Column(JSON, default=dict)  # {heal_amount, buff_type, buff_duration, ...}
    price = Column(Integer, default=0)
    rarity = Column(Integer, default=1)  # 1-5
    stackable = Column(Integer, default=0)  # 0=no, max stack
