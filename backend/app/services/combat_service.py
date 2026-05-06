"""전투 서비스 — 틱 기반 자동 전투, 드롭, 도망 시스템"""
import random
from typing import Optional
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.monster import Monster
from ..models.item import Item
from ..models.inventory import Inventory


def attack_monster(db: Session, char: Character, mon: Monster) -> list:
    """단일 전투 틱: 캐릭터 → 몬스터 공격 후 몬스터 반격. 메시지 리스트 반환."""
    msgs = []

    # 치명타 판정
    crit = random.random() < char.crit_rate
    dmg = char.attack + random.randint(-3, 3)
    if crit:
        dmg = int(dmg * 1.8)
    dmg = max(1, dmg - mon.defense // 2)
    mon.hp = max(0, mon.hp - dmg)

    crit_text = " 💥치명타!" if crit else ""
    msgs.append({
        "type": "battle_log",
        "content": f"⚔️ {mon.name}(을)를 공격! —{dmg} 피해{crit_text} (적HP {mon.hp}/{mon.max_hp})",
        "style": "attack"
    })

    if mon.hp <= 0:
        return msgs  # 몬스터 사망 → 반격 없음

    # 몬스터 반격
    att_templates = mon.attack_templates or [f"{mon.name}의 공격!"]
    att_text = random.choice(att_templates).replace("{name}", mon.name)
    m_crit = random.random() < 0.05
    m_dmg = mon.attack + random.randint(-3, 3)
    if m_crit:
        m_dmg = int(m_dmg * 1.5)
    m_dmg = max(1, m_dmg - char.defense // 3)
    char.hp = max(0, char.hp - m_dmg)

    m_crit_text = " 💥치명타!" if m_crit else ""
    msgs.append({
        "type": "battle_log",
        "content": f"🗡️ {att_text} —{m_dmg} 피해{m_crit_text} (내HP {char.hp}/{char.max_hp})",
        "style": "defense"
    })

    return msgs


def auto_combat(db: Session, char: Character, mon: Monster, use_martial: str = "", room_ids: Optional[list] = None) -> dict:
    """자동 전투: 전투 종료까지 틱 반복. 결과 요약 반환."""
    ticks = []
    initial_hp = char.hp

    if use_martial:
        # 무공 사용 → 첫 틱은 무공, 이후 일반 공격
        art_msg = _use_martial_tick(db, char, mon, use_martial)
        if art_msg:
            ticks.append(art_msg)

        while mon.hp > 0 and char.hp > 0:
            tick_msgs = attack_monster(db, char, mon)
            ticks.extend(tick_msgs)
            db.flush()
    else:
        while mon.hp > 0 and char.hp > 0:
            tick_msgs = attack_monster(db, char, mon)
            ticks.extend(tick_msgs)
            db.flush()

    result = {"ticks": ticks, "victory": mon.hp <= 0, "death": False}

    if mon.hp <= 0:
        # ── 리스폰 스케줄링 (몬스터 삭제 전 room 정보 저장) ──
        if room_ids is None:
            from ..models.room import Room
            rooms = db.query(Room).filter(Room.monster_ids.contains(mon.id)).all()
            room_ids = [r.id for r in rooms]

        from .respawn_service import schedule_respawn
        schedule_respawn(mon.id, room_ids)

        # ── 전리품 처리 ──
        drop_msgs = _process_drops(db, char, mon)
        result["drops"] = drop_msgs

        # 경험치 + 골드 — 개선된 계산식
        exp_gain = mon.exp_reward or (mon.max_hp // 2 + mon.attack * 3)
        exp_gain = int(exp_gain + (mon.max_hp * 0.5) + (mon.attack * 2))
        gold_gain = getattr(mon, "gold_reward", 0) or (mon.max_hp // 3 + random.randint(0, mon.attack))
        char.exp += exp_gain
        char.gold = min(char.gold + gold_gain, getattr(char, "max_gold", 9999999999))

        result["exp_gain"] = exp_gain
        result["gold_gain"] = gold_gain

        # 몬스터 제거
        db.delete(mon)
        db.commit()

    elif char.hp <= 0:
        # 사망 처리
        char.hp = char.max_hp
        char.current_room_id = 1
        result["death"] = True
        db.commit()

    return result


def _use_martial_tick(db: Session, char: Character, mon: Monster, art_name: str) -> Optional[dict]:
    """무공 1회 시전 후 메시지 반환. MP 부족 시 None."""
    from ..models.martial_art import MartialArt
    from ..models.character_martial_art import CharacterMartialArt

    cma = db.query(CharacterMartialArt).join(MartialArt).filter(
        CharacterMartialArt.character_id == char.id,
        MartialArt.name.ilike(f"%{art_name}%")
    ).first()

    if not cma:
        return {"type": "system", "content": "배우지 않은 무공입니다.", "style": "warning"}

    art = db.query(MartialArt).filter(MartialArt.id == cma.martial_art_id).first()
    if char.mp < art.mp_cost:
        return {"type": "system", "content": f"MP가 부족합니다. (필요: {art.mp_cost})", "style": "warning"}

    char.mp -= art.mp_cost
    dmg = int(art.damage * (1 + cma.proficiency / 2000))
    dmg = max(1, dmg - mon.defense // 3)
    mon.hp = max(0, mon.hp - dmg)

    # 숙련도 증가
    cma.proficiency = min(1000, cma.proficiency + random.randint(5, 15))
    db.flush()

    return {
        "type": "battle_log",
        "content": f"✨ {art.name}! —{dmg} 피해 (적HP {mon.hp}/{mon.max_hp})",
        "style": "special"
    }


def _process_drops(db: Session, char: Character, mon: Monster) -> list:
    """몬스터 드롭테이블 처리. 드롭 메시지 리스트 반환."""
    msgs = []
    drop_table = getattr(mon, "drop_table", []) or []

    for drop in drop_table:
        item_code = drop.get("item_code", "")
        rate = drop.get("rate", 0.05)
        min_q = drop.get("min_qty", 1)
        max_q = drop.get("max_qty", 1)

        if random.random() >= rate:
            continue

        item = db.query(Item).filter(Item.code == item_code).first()
        if not item:
            continue

        qty = random.randint(min_q, max_q)

        # 인벤토리 용량 체크 (장착 제외)
        cnt = db.query(Inventory).filter(
            Inventory.character_id == char.id,
            Inventory.equipped == 0
        ).count()

        if cnt >= char.inventory_limit:
            msgs.append({
                "type": "system",
                "content": "🎒 인벤토리가 가득 차서 아이템을 획득하지 못했습니다.",
                "style": "warning"
            })
            continue

        # 기존 스택 찾기 (소모품 등)
        existing = db.query(Inventory).filter(
            Inventory.character_id == char.id,
            Inventory.item_id == item.id,
            Inventory.equipped == 0
        ).first()

        if existing and item.stack_limit > 1:
            existing.quantity = min(existing.quantity + qty, item.stack_limit)
        else:
            import uuid
            db.add(Inventory(
                character_id=char.id,
                item_id=item.id,
                quantity=qty,
                instance_id=str(uuid.uuid4()) if item.stack_limit == 1 else ""
            ))

        msgs.append({
            "type": "system",
            "content": f"📦 {item.name} x{qty} 획득!{' ' + '⭐' * item.rarity if item.rarity > 1 else ''}",
            "style": "loot"
        })

    db.flush()
    return msgs


def try_flee(db: Session, char: Character, mon: Monster) -> list:
    """도망 시도. 성공 확률 = 30% + (속도 차이 / 몬스터 속도) * 40%.
    성공 시 귀환장소 또는 입문마을로 이동."""
    speed_diff = char.speed - mon.speed
    flee_chance = 0.30 + max(0, speed_diff / max(mon.speed, 1)) * 0.40
    flee_chance = min(0.85, max(0.15, flee_chance))

    if random.random() < flee_chance:
        # 도망 성공
        dest = char.return_room_id or 1
        char.current_room_id = dest
        db.commit()
        return [{
            "type": "system",
            "content": f"🏃 도망쳤습니다! ({int(flee_chance*100)}% 확률) 안전한 곳으로 이동합니다.",
            "style": "normal"
        }]
    else:
        # 도망 실패 → 몬스터 반격 1회
        m_dmg = mon.attack + random.randint(-3, 3)
        m_dmg = max(1, m_dmg - char.defense // 3)
        char.hp = max(0, char.hp - m_dmg)
        db.commit()
        msgs = [{
            "type": "battle_log",
            "content": f"😰 도망 실패! ({int(flee_chance*100)}% 확률) {mon.name}의 반격! —{m_dmg} 피해 (HP {char.hp}/{char.max_hp})",
            "style": "warning"
        }]
        if char.hp <= 0:
            char.hp = char.max_hp
            char.current_room_id = 1
            db.commit()
            msgs.append({
                "type": "system",
                "content": "사망하여 마을에서 깨어납니다...",
                "style": "warning"
            })
        return msgs


def cast_martial_art(db: Session, char: Character, art_name: str, mon: Monster) -> list:
    """무공 시전 (기존 로직 유지, 개선)."""
    from ..models.martial_art import MartialArt
    from ..models.character_martial_art import CharacterMartialArt

    cma = db.query(CharacterMartialArt).join(MartialArt).filter(
        CharacterMartialArt.character_id == char.id,
        MartialArt.name.ilike(f"%{art_name}%")
    ).first()

    if not cma:
        return [{"type": "system", "content": "배우지 않은 무공입니다.", "style": "warning"}]

    art = db.query(MartialArt).filter(MartialArt.id == cma.martial_art_id).first()
    if char.mp < art.mp_cost:
        return [{"type": "system", "content": f"MP가 부족합니다. (필요: {art.mp_cost})", "style": "warning"}]

    char.mp -= art.mp_cost
    dmg = int(art.damage * (1 + cma.proficiency / 2000))
    dmg = max(1, dmg - mon.defense // 3)
    mon.hp = max(0, mon.hp - dmg)

    # 숙련도 증가
    cma.proficiency = min(1000, cma.proficiency + random.randint(5, 15))

    msgs = [{
        "type": "battle_log",
        "content": f"✨ {art.name}! —{dmg} 피해 (적HP {mon.hp}/{mon.max_hp})",
        "style": "special"
    }]

    # 몬스터 반격
    if mon.hp > 0:
        m_dmg = mon.attack + random.randint(-3, 3)
        m_dmg = max(1, m_dmg - char.defense // 3)
        char.hp = max(0, char.hp - m_dmg)
        msgs.append({
            "type": "battle_log",
            "content": f"🗡️ {mon.name}의 반격! —{m_dmg} 피해 (HP {char.hp}/{char.max_hp})",
            "style": "defense"
        })

    _check_level(db, char)
    db.commit()
    return msgs


def meditate(db: Session, char: Character) -> list:
    """명상: MP 회복 + 약간의 EXP."""
    gain = 10 + char.ki
    char.mp = min(char.max_mp, char.mp + gain)
    char.exp += 5
    _check_level(db, char)
    db.commit()
    return [{
        "type": "system",
        "content": f"🧘 명상... MP +{gain} (MP {char.mp}/{char.max_mp})",
        "style": "healing"
    }]


# ═══════════════ 경지 체크 ═══════════════
STAGE_THRESHOLDS = [
    (0, "입문"), (30, "삼류"), (45, "이류"), (60, "일류"),
    (80, "절정"), (100, "초절정"), (150, "화경"), (250, "현경"), (500, "생사경")
]


def check_stage_up(db: Session, char: Character) -> Optional[str]:
    """경지 승급 체크. 승급 시 새 경지명 반환."""
    total = char.physique + char.ki + char.agility + char.insight + char.charm + char.luck
    for threshold, stage_name in reversed(STAGE_THRESHOLDS):
        if total >= threshold and char.martial_stage != stage_name:
            char.martial_stage = stage_name
            db.commit()
            return stage_name
    return None


def _check_level(db: Session, char: Character):
    """레벨업 체크 (game_service의 exp 커브 사용)."""
    from .game_service import _exp_for_level
    while char.level < 999 and char.exp >= _exp_for_level(char.level + 1):
        char.level += 1
        char.max_hp += 12
        char.hp = char.max_hp
        char.max_mp += 6
        char.mp = char.max_mp
        char.attack += 2
        char.defense += 1
        char.speed += 1
    db.commit()
