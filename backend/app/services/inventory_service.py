"""인벤토리 서비스 — 13슬롯 장비 시스템, 판매, 분해, 버리기, 장비현황"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.inventory import Inventory
from ..models.item import Item

# ──────────────────────────────────────────────
# 13슬롯 장비 그룹 정의
# ──────────────────────────────────────────────
SLOT_GROUPS = {
    "head":      {"max": 1, "names": ["head"]},
    "chest":     {"max": 1, "names": ["chest"]},
    "legs":      {"max": 1, "names": ["legs"]},
    "feet":      {"max": 1, "names": ["feet"]},
    "hands":     {"max": 1, "names": ["hands"]},
    "cloak":     {"max": 1, "names": ["cloak"]},
    "necklace":  {"max": 1, "names": ["necklace"]},
    "underwear": {"max": 1, "names": ["underwear"]},
    "mainhand":  {"max": 1, "names": ["mainhand"]},
    "offhand":   {"max": 1, "names": ["offhand"]},
    "ring":      {"max": 2, "names": ["ring1", "ring2"]},
    "trinket":   {"max": 2, "names": ["trinket1", "trinket2"]},
}

# 모든 표시용 슬롯명 (순서대로)
ALL_SLOT_NAMES = [
    "head", "chest", "legs", "feet", "hands", "cloak",
    "necklace", "ring1", "ring2", "underwear",
    "trinket1", "trinket2", "mainhand", "offhand",
]

# 슬롯 그룹명 → 실제 슬롯명 역매핑 (ring → ring1/ring2, trinket → trinket1/trinket2)
SLOT_GROUP_TO_NAMES = {k: v["names"] for k, v in SLOT_GROUPS.items()}

# ──────────────────────────────────────────────
# 내부 헬퍼 함수
# ──────────────────────────────────────────────

def _get_equipped_by_slot(db: Session, char_id: int, slot_name: str) -> Optional[Inventory]:
    """특정 슬롯에 장착된 인벤토리 항목 조회"""
    return db.query(Inventory).filter(
        Inventory.character_id == char_id,
        Inventory.equipped == 1,
        Inventory.slot == slot_name,
    ).first()


def _get_equipped_in_group(db: Session, char_id: int, group_name: str) -> list:
    """특정 슬롯 그룹에 장착된 모든 인벤토리 항목 조회"""
    slot_names = SLOT_GROUP_TO_NAMES.get(group_name, [group_name])
    return db.query(Inventory).filter(
        Inventory.character_id == char_id,
        Inventory.equipped == 1,
        Inventory.slot.in_(slot_names),
    ).all()


def _find_empty_slot_in_group(db: Session, char_id: int, group_name: str) -> Optional[str]:
    """그룹 내 빈 슬롯명 찾기 (ring/trinket용)"""
    slot_names = SLOT_GROUP_TO_NAMES.get(group_name, [group_name])
    occupied = {
        inv.slot
        for inv in db.query(Inventory).filter(
            Inventory.character_id == char_id,
            Inventory.equipped == 1,
            Inventory.slot.in_(slot_names),
        ).all()
    }
    for sn in slot_names:
        if sn not in occupied:
            return sn
    return None


def _remove_stats(char: Character, stats: dict):
    """캐릭터에서 장비 스탯 제거"""
    s = stats or {}
    char.attack -= s.get("attack", 0)
    char.defense -= s.get("defense", 0)
    char.max_hp -= s.get("hp", 0)
    char.max_mp -= s.get("mp", 0)
    char.speed -= s.get("speed", 0)
    char.crit_rate -= s.get("crit_rate", 0.0)
    char.hp = min(char.hp, char.max_hp)
    char.mp = min(char.mp, char.max_mp)


def _remove_enchant_bonus(char: Character, item_type: str, bonus_value: int):
    """캐릭터에서 인챈트 보너스 제거"""
    if not bonus_value:
        return
    stat_key = {"weapon": "attack", "armor": "defense", "accessory": "hp"}.get(item_type, "attack")
    current = getattr(char, stat_key, 0)
    setattr(char, stat_key, current - bonus_value)


def _apply_stats(char: Character, stats: dict):
    """캐릭터에 장비 스탯 적용"""
    s = stats or {}
    char.attack += s.get("attack", 0)
    char.defense += s.get("defense", 0)
    char.max_hp += s.get("hp", 0)
    char.max_mp += s.get("mp", 0)
    char.speed += s.get("speed", 0)
    char.crit_rate += s.get("crit_rate", 0.0)


def _apply_enchant_bonus(char: Character, item_type: str, bonus_value: int):
    """캐릭터에 인챈트 보너스 적용"""
    if not bonus_value:
        return
    stat_key = {"weapon": "attack", "armor": "defense", "accessory": "hp"}.get(item_type, "attack")
    current = getattr(char, stat_key, 0)
    setattr(char, stat_key, current + bonus_value)


def _unequip_inventory(db: Session, char: Character, inv: Inventory):
    """내부용: 인벤토리 항목 해제 (stats + affix + enchant 제거, 슬롯 초기화)"""
    item = db.query(Item).filter(Item.id == inv.item_id).first()
    if item:
        _remove_stats(char, item.stats or {})
    # 어픽스 스탯도 제거
    affix = getattr(inv, "affix_data", {}) or {}
    for key in ("prefix_stats", "suffix_stats"):
        stats = affix.get(key, {})
        if stats:
            _remove_stats(char, stats)
    # 인챈트 보너스 제거
    from ..models.enchantment import Enchantment
    ench = db.query(Enchantment).filter(Enchantment.inventory_id == inv.id).first()
    if ench and ench.bonus_value:
        _remove_enchant_bonus(char, item.item_type if item else "", ench.bonus_value)
    inv.equipped = 0
    inv.slot = ""
    inv.instance_id = ""


def _cap_gold(char: Character):
    """소지금 상한 체크"""
    max_gold = getattr(char, "max_gold", 9999999999) or 9999999999
    if char.gold > max_gold:
        char.gold = max_gold


# ──────────────────────────────────────────────
# 공개 API
# ──────────────────────────────────────────────

def equip_item(db: Session, char: Character, item_name: str) -> Optional[str]:
    """아이템을 이름으로 찾아 해당 슬롯에 장착합니다.

    - 이미 같은 슬롯에 장착된 아이템이 있으면 자동 해제 후 장착
    - 양손무기(twohand) 장착 시 offhand 자동 해제
    - 한손무기 장착 시 mainhand가 twohand면 해제하고 장착
    - ring/trinket은 빈 슬롯을 먼저 사용
    - instance_id를 UUID로 생성
    """
    # 1. 인벤토리에서 아이템 찾기 (장착되지 않은 것)
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0,
    ).first()
    if not inv:
        return f"'{item_name}' 아이템을 소지하고 있지 않거나 이미 장착 중입니다."

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    if not item:
        return "아이템 정보를 찾을 수 없습니다."

    # 레벨 요구 체크
    lvl_req = getattr(item, "level_required", 1) or 1
    if char.level < lvl_req:
        return f"'{item.name}'은(는) Lv.{lvl_req} 이상만 장착할 수 있습니다. (현재 Lv.{char.level})"

    item_slot = (item.slot or "").strip()
    if not item_slot:
        return f"'{item.name}'은(는) 장착할 수 없는 아이템입니다."

    # 2. 장착 가능한 슬롯인지 확인
    group_info = SLOT_GROUPS.get(item_slot)
    if not group_info:
        slot_ko = {
            "head": "머리", "chest": "상의", "legs": "하의", "feet": "발",
            "hands": "손", "cloak": "망토", "necklace": "목걸이", "underwear": "속옷",
            "mainhand": "주무기", "offhand": "보조무기", "twohand": "양손무기",
            "ring": "반지", "trinket": "장신구",
        }
        item_slot_ko = slot_ko.get(item_slot, item_slot)
        return f"'{item_slot_ko}'은(는) 유효한 장비 슬롯이 아닙니다."

    target_slot: str = ""

    # ── mainhand / twohand 처리 ──
    if item_slot in ("mainhand", "twohand"):
        # mainhand에 현재 twohand가 장착되어 있으면 해제
        existing_main = _get_equipped_by_slot(db, char.id, "mainhand")
        if existing_main:
            existing_item = db.query(Item).filter(Item.id == existing_main.item_id).first()
            # 기존 mainhand가 twohand인 경우 (또는 단순 교체)
            _unequip_inventory(db, char, existing_main)

        # 양손무기 장착 시 offhand 해제
        if item_slot == "twohand":
            existing_off = _get_equipped_by_slot(db, char.id, "offhand")
            if existing_off:
                _unequip_inventory(db, char, existing_off)

        target_slot = "mainhand"

    # ── offhand 처리 ──
    elif item_slot == "offhand":
        # mainhand에 twohand가 장착되어 있으면 offhand 장착 불가
        existing_main = _get_equipped_by_slot(db, char.id, "mainhand")
        if existing_main:
            main_item = db.query(Item).filter(Item.id == existing_main.item_id).first()
            if main_item and (main_item.slot or "").strip() == "twohand":
                return f"양손무기 '{main_item.name}'을(를) 장착 중이므로 보조무기를 장착할 수 없습니다."

        existing_off = _get_equipped_by_slot(db, char.id, "offhand")
        if existing_off:
            _unequip_inventory(db, char, existing_off)

        target_slot = "offhand"

    # ── ring / trinket (다중 슬롯) ──
    elif item_slot in ("ring", "trinket"):
        # 그룹 내 장착된 것들 확인
        equipped_group = _get_equipped_in_group(db, char.id, item_slot)
        if len(equipped_group) >= group_info["max"]:
            # 모두 찼으면 첫 번째 슬롯 해제 후 장착
            first_equipped = equipped_group[0]
            _unequip_inventory(db, char, first_equipped)
            target_slot = first_equipped.slot  # 해제된 슬롯 재사용
        else:
            # 빈 슬롯 찾기
            target_slot = _find_empty_slot_in_group(db, char.id, item_slot)
            if not target_slot:
                return f"'{item_slot}' 슬롯 그룹에 빈 자리가 없습니다."

    # ── 단일 슬롯 (head, chest, legs, feet, hands, cloak, necklace, underwear) ──
    else:
        existing = _get_equipped_by_slot(db, char.id, item_slot)
        if existing:
            _unequip_inventory(db, char, existing)
        target_slot = item_slot

    # 3. 장착 실행
    _apply_stats(char, item.stats or {})
    # 어픽스 스탯도 적용
    affix = getattr(inv, "affix_data", {}) or {}
    for key in ("prefix_stats", "suffix_stats"):
        stats = affix.get(key, {})
        if stats:
            _apply_stats(char, stats)
    # 인챈트 보너스 적용
    from ..models.enchantment import Enchantment
    ench = db.query(Enchantment).filter(Enchantment.inventory_id == inv.id).first()
    if ench and ench.bonus_value:
        _apply_enchant_bonus(char, item.item_type, ench.bonus_value)
    inv.equipped = 1
    inv.slot = target_slot
    inv.instance_id = str(uuid.uuid4())

    db.commit()
    return None  # 성공


def unequip_item(db: Session, char: Character, item_name: str) -> Optional[str]:
    """장착 중인 아이템을 이름으로 찾아 해제합니다.

    stats를 제거하고 슬롯 정보를 초기화합니다.
    """
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 1,
    ).first()
    if not inv:
        return f"'{item_name}' 아이템을 장착하고 있지 않습니다."

    _unequip_inventory(db, char, inv)
    db.commit()
    return None  # 성공


# ── 하위 호환성 유지 (기존 코드에서 unequip으로 호출) ──
def unequip(db: Session, char: Character, item_name: str) -> Optional[str]:
    """장비 해제 (하위 호환성 유지용). unequip_item과 동일합니다."""
    return unequip_item(db, char, item_name)


def equip_status(db: Session, char: Character) -> dict:
    """13개 슬롯 전체 상태를 반환합니다.

    Returns:
        {
            "slots": {
                "head": {"name": ..., "stats": ..., "instance_id": ...} or None,
                ...
            },
            "total_attack": int, "total_defense": int,
            "max_hp": int, "max_mp": int, "speed": int, "crit_rate": float,
        }
    """
    equipped_all = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.equipped == 1,
    ).all()

    # 슬롯별 매핑
    slot_map: dict[str, Inventory] = {}
    for inv in equipped_all:
        if inv.slot:
            slot_map[inv.slot] = inv

    # 모든 슬롯 정보 조립
    slots = {}
    total_stats = {"attack": 0, "defense": 0, "hp": 0, "mp": 0, "speed": 0, "crit_rate": 0.0}

    for slot_name in ALL_SLOT_NAMES:
        inv = slot_map.get(slot_name)
        if inv:
            item = db.query(Item).filter(Item.id == inv.item_id).first()
            if item:
                s = item.stats or {}
                name = item.name
                item_stats = dict(s)
                instance_id = inv.instance_id or ""
                # 인챈트 보너스 조회
                from ..models.enchantment import Enchantment
                ench = db.query(Enchantment).filter(Enchantment.inventory_id == inv.id).first()
                enchant_bonus = 0
                if ench and ench.bonus_value:
                    enchant_bonus = ench.bonus_value
                    sk = ench.stat_key or "attack"
                    item_stats[sk] = item_stats.get(sk, 0) + enchant_bonus
                # 총합 누적
                total_stats["attack"] += s.get("attack", 0)
                total_stats["defense"] += s.get("defense", 0)
                total_stats["hp"] += s.get("hp", 0)
                total_stats["mp"] += s.get("mp", 0)
                total_stats["speed"] += s.get("speed", 0)
                total_stats["crit_rate"] += s.get("crit_rate", 0.0)
                # 인챈트 보너스를 총합에 추가
                if ench and ench.bonus_value:
                    sk = ench.stat_key or "attack"
                    total_stats[sk] = total_stats.get(sk, 0) + enchant_bonus
            else:
                name = "(알 수 없음)"
                item_stats = {}
                instance_id = ""
            slots[slot_name] = {
                "name": name,
                "stats": item_stats,
                "instance_id": instance_id,
            }
        else:
            slots[slot_name] = None

    return {
        "slots": slots,
        "total_attack": total_stats["attack"],
        "total_defense": total_stats["defense"],
        "max_hp": total_stats["hp"],
        "max_mp": total_stats["mp"],
        "speed": total_stats["speed"],
        "crit_rate": total_stats["crit_rate"],
    }


# ──────────────────────────────────────────────
# 판매 / 분해 / 버리기 (기존 함수 유지, gold 상한 추가)
# ──────────────────────────────────────────────

def sell_item(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """아이템 판매 (반값에 매각)"""
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0,  # 장착 중이 아닌 것만 판매 가능
    ).first()
    if not inv:
        return "판매 가능한 해당 아이템이 없습니다 (장착 중이면 해제 후 판매하세요)."
    if inv.quantity < quantity:
        return f"수량이 부족합니다. (보유: {inv.quantity})"

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    sell_price = (item.price or 10) // 2  # 반값

    inv.quantity -= quantity
    if inv.quantity <= 0:
        db.delete(inv)

    char.gold += sell_price * quantity
    _cap_gold(char)
    db.commit()
    return None


def dismantle_item(db: Session, char: Character, item_name: str) -> Optional[str]:
    """아이템 분해 (강화석 획득 확률)"""
    import random
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0,
    ).first()
    if not inv:
        return "분해 가능한 해당 아이템이 없습니다."

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    rarity = item.rarity or 1

    # 분해 보상: 강화석 (ID 151)
    stone_count = random.randint(rarity, rarity * 2)
    stone = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == 151,
    ).first()
    if stone:
        stone.quantity += stone_count
    else:
        db.add(Inventory(character_id=char.id, item_id=151, quantity=stone_count))

    inv.quantity -= 1
    if inv.quantity <= 0:
        db.delete(inv)
    db.commit()
    return None


def discard_item(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """아이템 버리기"""
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0,
    ).first()
    if not inv:
        return "버릴 수 있는 해당 아이템이 없습니다."
    if inv.quantity < quantity:
        return f"수량이 부족합니다. (보유: {inv.quantity})"

    inv.quantity -= quantity
    if inv.quantity <= 0:
        db.delete(inv)
    db.commit()
    return None
