"""어픽스 서비스 — 접두/접미 랜덤 부여, 스탯 계산, 이름 생성"""
import random
from typing import Optional
from sqlalchemy.orm import Session
from ..models.item_affix import ItemAffix


def roll_affixes_for_item(db: Session, item_id: int) -> dict:
    """아이템에 접두/접미 랜덤 부여. affix_data dict 반환"""
    affix_data = {}

    # 접두어 롤 (60%)
    if random.random() < 0.60:
        prefixes = db.query(ItemAffix).filter(
            ItemAffix.affix_type == "prefix"
        ).all()
        if prefixes:
            # 낮은 등급이 더 많이 나오도록 가중치
            weights = [6 - p.tier for p in prefixes]
            chosen = random.choices(prefixes, weights=weights, k=1)[0]
            affix_data["prefix_name"] = chosen.name
            affix_data["prefix_stats"] = chosen.stats or {}

    # 접미사 롤 (50%)
    if random.random() < 0.50:
        suffixes = db.query(ItemAffix).filter(
            ItemAffix.affix_type == "suffix"
        ).all()
        if suffixes:
            weights = [6 - s.tier for s in suffixes]
            chosen = random.choices(suffixes, weights=weights, k=1)[0]
            affix_data["suffix_name"] = chosen.name
            affix_data["suffix_stats"] = chosen.stats or {}

    return affix_data


def get_affix_display_name(base_name: str, affix_data: Optional[dict]) -> str:
    """어픽스 적용된 표시 이름"""
    if not affix_data:
        return base_name
    prefix = affix_data.get("prefix_name", "")
    suffix = affix_data.get("suffix_name", "")
    if prefix and suffix:
        return f"{prefix} {base_name} {suffix}"
    elif prefix:
        return f"{prefix} {base_name}"
    elif suffix:
        return f"{base_name} {suffix}"
    return base_name


def get_affix_tier_icon(tier: int) -> str:
    """등급에 따른 아이콘"""
    if tier >= 5:
        return "💎"
    elif tier >= 4:
        return "🔮"
    elif tier >= 3:
        return "✨"
    elif tier >= 2:
        return "⚡"
    return "·"


def apply_affix_stats_to_char(char, affix_data: dict, equip: bool = True):
    """어픽스 스탯을 캐릭터에 적용 (equip=True=장착, False=해제)"""
    if not affix_data:
        return
    sign = 1 if equip else -1

    for key in ("prefix_stats", "suffix_stats"):
        stats = affix_data.get(key, {})
        if not stats:
            continue
        for stat, val in stats.items():
            if stat == "attack":
                char.attack += val * sign
            elif stat == "defense":
                char.defense += val * sign
            elif stat == "speed":
                char.speed += val * sign
            elif stat == "hp":
                char.max_hp += val * sign
                if equip:
                    char.hp += val
                else:
                    char.hp = min(char.hp, char.max_hp)
            elif stat == "mp":
                char.max_mp += val * sign
                if equip:
                    char.mp += val
                else:
                    char.mp = min(char.mp, char.max_mp)
            elif stat == "crit_rate":
                char.crit_rate += val * sign
            elif stat == "charm":
                char.charm += val * sign
            elif stat == "insight":
                char.insight += val * sign
            elif stat == "gold_reward":
                pass  # 전리품 증가는 combat_service에서 처리
