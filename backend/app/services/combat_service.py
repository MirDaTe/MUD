"""전투 시스템 - 무공 발동, 경지, 상태이상, 전투 로그"""
from typing import Optional as _Optional
import random
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.monster import Monster
from ..models.martial_art import MartialArt
from ..models.character_martial_art import CharacterMartialArt
from ..models.item import Item
from ..models.inventory import Inventory

# 경지별 위력 계수
STAGE_MULTIPLIER = {
    "입문": 1.0, "소성": 1.2, "대성": 1.5, "원만": 1.8,
    "절정": 2.2, "초절정": 2.7, "화경": 3.3, "현경": 4.0, "신화경": 5.0
}

# 경지별 필요 경험치 (누적)
STAGE_EXP = {
    "입문": 0, "소성": 200, "대성": 600, "원만": 1500,
    "절정": 3500, "초절정": 7500, "화경": 15000, "현경": 30000, "신화경": 60000
}


def calc_damage(attacker_atk: int, defender_def: int, multiplier: float = 1.0, stage_mult: float = 1.0) -> int:
    """기본 데미지 계산"""
    base = attacker_atk - defender_def // 2
    variance = random.randint(-3, 5)
    return max(1, int((base + variance) * multiplier * stage_mult))


def check_crit(chance: float) -> bool:
    return random.random() < chance


def check_hit(speed_diff: int) -> bool:
    """명중 판정: speed 차이가 클수록 유리"""
    return random.random() > 0.05 - speed_diff * 0.005


def cast_martial_art(db: Session, char: Character, art_name: str, target: Monster) -> list[dict]:
    """무공 발동"""
    messages = []
    # 무공 찾기
    art = db.query(MartialArt).filter(MartialArt.name.ilike(f"%{art_name}%")).first()
    if not art:
        return [{"type": "system", "content": f"'{art_name}'이라는 무공을 모릅니다.", "style": "warning"}]

    # 캐릭터가 해당 무공을 배웠는지 확인
    cma = db.query(CharacterMartialArt).filter(
        CharacterMartialArt.character_id == char.id,
        CharacterMartialArt.martial_art_id == art.id
    ).first()
    if not cma:
        return [{"type": "system", "content": "아직 익히지 않은 무공입니다.", "style": "warning"}]

    # 경지 체크
    stage_order = ["입문", "소성", "대성", "원만", "절정", "초절정", "화경", "현경", "신화경"]
    if stage_order.index(char.martial_stage) < stage_order.index(art.stage_required):
        return [{"type": "system", "content": f"경지가 부족합니다. ({art.stage_required} 이상 필요)", "style": "warning"}]

    # 내공 체크
    if char.mp < art.mp_cost:
        return [{"type": "system", "content": "내공이 부족합니다.", "style": "warning"}]

    # 소모
    char.mp -= art.mp_cost

    # 스테이지 보정
    stage_mult = STAGE_MULTIPLIER.get(char.martial_stage, 1.0)

    # 피해 계산
    if art.effect_type == "damage":
        dmg = calc_damage(char.attack, target.defense, art.damage_multiplier, stage_mult)
        is_crit = check_crit(char.crit_rate + 0.05)
        if is_crit:
            dmg = int(dmg * 2)
            msg = art.crit_text or f"치명타! {art.name}의 진정한 위력이 폭발합니다! {dmg}의 피해!"
            messages.append({"type": "battle_log", "content": msg, "style": "critical"})
        else:
            msg = art.flavor_text or f"{art.name}! {dmg}의 피해를 입힙니다."
            messages.append({"type": "battle_log", "content": msg, "style": "battle"})

        # dot 효과
        params = art.effect_params or {}
        if params.get("dot_dmg"):
            dot = params["dot_dmg"]
            duration = params.get("dot_duration", 3)
            messages.append({"type": "battle_log", "content": f"잔향이 적을 감싸며 매 초 {dot}의 추가 피해! ({duration}틱)", "style": "battle"})
            target.hp -= dot * duration

        target.hp -= dmg

    elif art.effect_type == "heal":
        heal = int(char.max_hp * 0.15 * stage_mult)
        char.hp = min(char.hp + heal, char.max_hp)
        messages.append({"type": "battle_log", "content": f"내공이 온몸을 감싸며 {heal}의 체력을 회복합니다.", "style": "healing"})

    elif art.effect_type == "buff":
        char.attack += int(char.attack * 0.2)
        messages.append({"type": "battle_log", "content": "기세가 솟구칩니다! 공격력이 일시 상승!", "style": "battle"})

    elif art.effect_type == "debuff":
        target.defense = max(1, target.defense - 2)
        messages.append({"type": "battle_log", "content": f"적의 방어를 무너뜨립니다! 방어력 하락!", "style": "battle"})

    # 숙련도 상승
    cma.proficiency = min(1000, cma.proficiency + random.randint(5, 15))

    # 죽음 체크
    if target.hp <= 0:
        death_msg = target.death_template or f"{target.name}(이)가 마지막 숨을 거둡니다."
        messages.append({"type": "battle_log", "content": death_msg, "style": "battle"})
        char.exp += target.exp_reward

    db.commit()
    return messages


def check_stage_up(db: Session, char: Character) -> _Optional[str]:
    """경지 돌파 체크"""
    stage_order = ["입문", "소성", "대성", "원만", "절정", "초절정", "화경", "현경", "신화경"]
    curr = stage_order.index(char.martial_stage)
    if curr >= len(stage_order) - 1:
        return None
    next_stage = stage_order[curr + 1]
    if char.exp >= STAGE_EXP[next_stage]:
        char.martial_stage = next_stage
        char.max_hp += 30
        char.hp = char.max_hp
        char.max_mp += 15
        char.mp = char.max_mp
        char.attack += 5
        char.defense += 3
        db.commit()
        return next_stage
    return None


def _process_drops(db: Session, char: Character, monster: Monster) -> list[str]:
    """drop_table 기반 아이템 드롭 처리"""
    drop_messages = []
    if not monster.drop_table:
        return drop_messages

    for drop_entry in monster.drop_table:
        item_code = drop_entry.get("item_code", "")
        rate = drop_entry.get("rate", 0)
        min_qty = drop_entry.get("min_qty", 1)
        max_qty = drop_entry.get("max_qty", 1)

        # 확률 체크
        if random.random() >= rate:
            continue

        # Item 검색
        item = db.query(Item).filter(Item.code == item_code).first()
        if not item:
            continue

        # 수량 결정
        qty = random.randint(min_qty, max_qty)

        # 인벤토리 용량 체크
        current_items = db.query(Inventory).filter(
            Inventory.character_id == char.id,
            Inventory.equipped == 0
        ).count()
        if current_items >= char.inventory_limit:
            drop_messages.append("인벤토리가 가득 차서 아이템을 획득하지 못했습니다")
            continue

        # 이미 같은 아이템이 있고 stack_limit > 1 이면 중첩
        existing = db.query(Inventory).filter(
            Inventory.character_id == char.id,
            Inventory.item_id == item.id,
            Inventory.equipped == 0
        ).first()
        if existing and item.stack_limit > 1:
            existing.quantity = min(existing.quantity + qty, item.stack_limit)
            drop_messages.append(f"{item.name} x{qty} 획득! (총 {existing.quantity}개)")
        else:
            if current_items >= char.inventory_limit:
                drop_messages.append("인벤토리가 가득 차서 아이템을 획득하지 못했습니다")
                continue
            inv = Inventory(
                character_id=char.id,
                item_id=item.id,
                quantity=qty,
                equipped=0,
                slot=""
            )
            db.add(inv)
            drop_messages.append(f"{item.name} x{qty} 획득!")

    return drop_messages


def attack_monster(db: Session, char: Character, monster: Monster) -> list[dict]:
    """기본 공격"""
    messages = []
    dmg = calc_damage(char.attack, monster.defense)
    is_crit = check_crit(char.crit_rate)
    if is_crit:
        dmg = int(dmg * 1.8)
        messages.append({"type": "battle_log", "content": f"치명타! 검끝이 급소를 꿰뚫습니다! {dmg}의 피해!", "style": "critical"})
    else:
        messages.append({"type": "battle_log", "content": f"당신의 일격! {monster.name}에게 {dmg}의 피해!", "style": "battle"})

    monster.hp -= dmg

    if monster.hp <= 0:
        death_msg = monster.death_template or f"{monster.name}(이)가 쓰러집니다."
        messages.append({"type": "battle_log", "content": death_msg, "style": "battle"})

        # 경험치 보상
        char.exp += monster.exp_reward

        # 금화 보상
        if monster.gold_reward:
            char.gold = min(char.gold + monster.gold_reward, char.max_gold)
            messages.append({"type": "battle_log", "content": f"💰 {monster.gold_reward} 금화를 획득했습니다!", "style": "system"})

        # 드롭테이블 처리
        drop_msgs = _process_drops(db, char, monster)
        for dm in drop_msgs:
            messages.append({"type": "battle_log", "content": dm, "style": "system"})

        # 명성 보상 (TODO: Character에 fame 필드가 없으므로 로그만 출력)
        if monster.fame_reward:
            messages.append({"type": "battle_log", "content": f"✨ 명성 +{monster.fame_reward} 상승!", "style": "system"})
    else:
        # 반격
        m_dmg = max(1, monster.attack - char.defense + random.randint(-2, 2))
        char.hp -= m_dmg
        messages.append({"type": "battle_log", "content": f"{monster.name}의 반격! {m_dmg}의 피해! (HP: {char.hp}/{char.max_hp})", "style": "battle"})

    db.commit()

    # 경지 체크
    stage_up = check_stage_up(db, char)
    if stage_up:
        messages.append({"type": "system", "content": f"── 경지돌파! 당신은 이제 '{stage_up}'의 경지에 올랐습니다! 온몸에 내공이 넘쳐흐릅니다! ──", "style": "critical"})

    return messages


def meditate(db: Session, char: Character) -> list[dict]:
    """수련 (내공 회복 + 소량 경험치)"""
    recover = int(char.max_mp * 0.3)
    char.mp = min(char.mp + recover, char.max_mp)
    char.exp += random.randint(5, 15)
    db.commit()

    msg = f"눈을 감고 내공을 운행합니다... (+{recover} MP)"
    stage_up = check_stage_up(db, char)
    if stage_up:
        msg += f"\n── 경지돌파! '{stage_up}'의 경지에 올랐습니다! ──"

    return [{"type": "battle_log", "content": msg, "style": "healing"}]
