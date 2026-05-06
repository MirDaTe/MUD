"""인챈트/강화 서비스"""
import random
from typing import Optional
from sqlalchemy.orm import Session
from ..models.inventory import Inventory
from ..models.item import Item
from ..models.enchantment import Enchantment
from ..models.character import Character

# 강화 단계별 성공률 (0→15)
ENCHANT_SUCCESS_RATE = [
    100, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25
]

# 강화 단계별 스탯 증가율
ENCHANT_STAT_BONUS = {
    "weapon": [0, 2, 4, 6, 8, 10, 13, 16, 19, 22, 26, 30, 35, 40, 46, 52],
    "armor": [0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 16, 19, 22, 26, 30, 35],
    "accessory": [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 17, 20, 23, 27, 31],
}

# 강화 재료 요구량
ENCHANT_MATERIAL_COST = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10]

# 강화 재료 아이템 ID
MATERIAL_STONE_ID = 151  # 강화석
MATERIAL_PROTECT_ID = 152  # 보호석 (실패 시 레벨 유지)
MATERIAL_ADVANCED_ID = 153  # 고급강화석 (+성공률 20%)


def get_enchant(db: Session, inventory_id: int) -> Optional[Enchantment]:
    """강화 정보 조회"""
    return db.query(Enchantment).filter(Enchantment.inventory_id == inventory_id).first()


def ensure_enchant(db: Session, inventory_id: int) -> Enchantment:
    """강화 정보 생성/조회"""
    ench = get_enchant(db, inventory_id)
    if not ench:
        ench = Enchantment(inventory_id=inventory_id, enchant_level=0)
        db.add(ench)
        db.commit()
        db.refresh(ench)
    return ench


def upgrade_item(db: Session, char: Character, item_name: str, use_protect: bool = False, use_advanced: bool = False) -> list[dict]:
    """아이템 강화"""
    messages = []

    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 1
    ).first()

    if not inv:
        inv = db.query(Inventory).join(Item).filter(
            Inventory.character_id == char.id,
            Item.name.ilike(f"%{item_name}%")
        ).first()

    if not inv:
        return [{"type": "system", "content": "해당 아이템을 소지하고 있지 않습니다.", "style": "warning"}]

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    if item.item_type not in ("weapon", "armor", "accessory"):
        return [{"type": "system", "content": "이 아이템은 강화할 수 없습니다.", "style": "warning"}]

    ench = ensure_enchant(db, inv.id)

    if ench.enchant_level >= 15:
        return [{"type": "system", "content": "이미 최고 단계(+15)로 강화된 아이템입니다!", "style": "warning"}]

    next_level = ench.enchant_level + 1
    mat_needed = ENCHANT_MATERIAL_COST[next_level]

    # 재료 체크
    if use_advanced:
        mat_needed += 1

    has_stone = _count_material(db, char, MATERIAL_STONE_ID)
    if has_stone < mat_needed:
        return [{"type": "system", "content": f"강화석이 부족합니다. (필요: {mat_needed}개, 보유: {has_stone}개)", "style": "warning"}]

    if use_protect:
        has_protect = _count_material(db, char, MATERIAL_PROTECT_ID)
        if has_protect < 1:
            return [{"type": "system", "content": "보호석이 부족합니다.", "style": "warning"}]

    # 재료 소모
    _consume_material(db, char, MATERIAL_STONE_ID, mat_needed)

    # 성공률 계산
    base_rate = ENCHANT_SUCCESS_RATE[next_level]
    if use_advanced:
        base_rate = min(100, base_rate + 20)

    success = random.random() * 100 < base_rate

    ench.upgrade_count += 1
    stats = item.stats or {}
    stat_key = _get_stat_key(item.item_type)

    if success:
        # 기존 강화 스탯 제거 후 새로 적용
        old_bonus = ENCHANT_STAT_BONUS.get(item.item_type, [0]*16)[ench.enchant_level]
        new_bonus = ENCHANT_STAT_BONUS.get(item.item_type, [0]*16)[next_level]
        enchant_bonus = new_bonus - old_bonus

        if stat_key in stats:
            stats[stat_key] += enchant_bonus
        else:
            stats[stat_key] = item.stats.get(stat_key, 0) + enchant_bonus
        item.stats = stats

        # 캐릭터 스탯 갱신
        if _get_char_attr(char, stat_key) is not None:
            current = _get_char_attr(char, stat_key)
            _set_char_attr(char, stat_key, current + enchant_bonus)

        ench.enchant_level = next_level

        msg = f"✦ 강화 성공! +{next_level} {item.name} ✦\n{stat_key} +{enchant_bonus} 상승! (성공률: {base_rate}%)"
        messages.append({"type": "battle_log", "content": msg, "style": "critical"})
    else:
        ench.fail_count += 1
        if not use_protect and ench.enchant_level > 0:
            ench.enchant_level -= 1
            rollback = ENCHANT_STAT_BONUS.get(item.item_type, [0]*16)[next_level-1]
            old = ENCHANT_STAT_BONUS.get(item.item_type, [0]*16)[ench.enchant_level+1]
            penalty = old - rollback
            if stat_key in stats:
                stats[stat_key] -= penalty
            item.stats = stats
            if _get_char_attr(char, stat_key) is not None:
                _set_char_attr(char, stat_key, _get_char_attr(char, stat_key) - penalty)
            msg = f"강화 실패! 아이템이 손상되어 +{ench.enchant_level}로 떨어졌습니다. (성공률: {base_rate}%)"
        else:
            msg = f"강화 실패... 보호석의 힘으로 레벨이 유지됩니다. (성공률: {base_rate}%)"
        messages.append({"type": "system", "content": msg, "style": "warning"})

    db.commit()
    return messages


def _get_stat_key(item_type: str) -> str:
    return {"weapon": "attack", "armor": "defense", "accessory": "hp"}.get(item_type, "attack")


def _get_char_attr(char: Character, key: str) -> int | None:
    return getattr(char, key, None)


def _set_char_attr(char: Character, key: str, value: int):
    setattr(char, key, value)


def _count_material(db: Session, char: Character, item_id: int) -> int:
    inv = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == item_id
    ).first()
    return inv.quantity if inv else 0


def _consume_material(db: Session, char: Character, item_id: int, amount: int):
    inv = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == item_id
    ).first()
    if inv:
        inv.quantity -= amount
        if inv.quantity <= 0:
            db.delete(inv)
