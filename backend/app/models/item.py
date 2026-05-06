
from sqlalchemy import Column, Integer, String, JSON
from ..core.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), default="")  # 고유 아이템 코드 (예: "WPN_SWORD_IRON_01")
    name = Column(String(50), nullable=False)
    item_type = Column(String(20), nullable=False)  # weapon/armor/accessory/consumable/rare/misc
    sub_type = Column(String(20), default="")  # 검/도/창/도포/연갑/영약/독/비급조각...
    slot = Column(String(20), default="")  # head/chest/legs/feet/hands/cloak/necklace/ring/underwear/trinket/mainhand/offhand/twohand
    weapon_type = Column(String(20), default="")  # sword/blade/spear/staff/bow/dagger 등
    description = Column(String(500), default="")
    stats = Column(JSON, default=dict)  # {attack, defense, speed, hp, mp, ...}
    effects = Column(JSON, default=dict)  # {heal_amount, buff_type, buff_duration, ...}
    price = Column(Integer, default=0)
    rarity = Column(Integer, default=1)  # 1-5
    stack_limit = Column(Integer, default=1)  # 최대 중첩 수 (장비=1, 소모품=100)
    level_required = Column(Integer, default=1)  # 착용 요구 레벨
