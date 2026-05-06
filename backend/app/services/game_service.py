"""게임 명령어 처리 서비스 (무공 전투, 인벤토리, 퀘스트, 상점 포함)"""
import random
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.room import Room
from ..models.npc import NPC
from ..models.monster import Monster
from ..models.martial_art import MartialArt
from ..models.character_martial_art import CharacterMartialArt
from ..models.item import Item
from ..models.inventory import Inventory
from ..models.quest import Quest
from ..models.character_quest import CharacterQuest
from ..models.affection import Affection
from ..models.shop import Shop
from ..models.faction import Faction
from ..models.character_faction import CharacterFaction
from .combat_service import attack_monster, cast_martial_art, meditate as meditate_service, check_stage_up


def parse_command(cmd: str) -> tuple[str, str]:
    parts = cmd.strip().split(maxsplit=1)
    verb = parts[0].lower() if parts else ""
    rest = parts[1] if len(parts) > 1 else ""
    return verb, rest


def execute_command(db: Session, char: Character, cmd: str) -> list[dict]:
    messages = []
    verb, rest = parse_command(cmd)
    room = db.query(Room).filter(Room.id == char.current_room_id).first()

    # ── look ──
    if verb in ("look", "l", "주변", "보기"):
        if not room: return [{"type": "system", "content": "허공입니다...", "style": "normal"}]
        messages.append({"type": "room_desc", "content": f"[{room.name}]", "style": "room"})
        messages.append({"type": "room_desc", "content": room.description, "style": "room"})
        ex = {k: v for k, v in (room.exits or {}).items() if v}
        if ex:
            messages.append({"type": "system", "content": f"갈 수 있는 곳: {', '.join(ex.keys())}", "style": "normal"})
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc:
                tag = "[적대]" if npc.is_hostile else ""
                messages.append({"type": "npc_present", "content": f"{tag} {npc.name}(이)가 여기에 있습니다.", "style": "npc"})
        for mid in (room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon:
                messages.append({"type": "monster_present", "content": f"위협적인 {mon.name}(이)가 노려보고 있습니다! (HP:{mon.hp}/{mon.max_hp})", "style": "warning"})
        return messages

    # ── movement ──
    dir_map = {"north": "북", "n": "북", "south": "남", "s": "남", "east": "동", "e": "동", "west": "서", "w": "서",
               "북": "north", "남": "south", "동": "east", "서": "west"}
    if verb in dir_map or verb in ("go", "이동"):
        if verb in ("go", "이동"):
            direction_val = dir_map.get(rest, rest)
        else:
            direction_val = dir_map.get(verb, verb)
        eng_key = {"북": "north", "n": "north", "남": "south", "s": "south", "동": "east", "e": "east", "서": "west",
                   "w": "west"}.get(direction_val, direction_val)
        target_id = (room.exits or {}).get(eng_key) if room else None
        if target_id:
            char.current_room_id = target_id
            db.commit()
            ko = {"north": "북", "south": "남", "east": "동", "west": "서"}.get(eng_key, eng_key)
            messages.append({"type": "system", "content": f"{ko}쪽으로 이동...", "style": "normal"})
            return messages + execute_command(db, char, "look")
        else:
            messages.append({"type": "system", "content": "그 방향으로는 갈 수 없습니다.", "style": "warning"})
            return messages

    # ── attack ──
    if verb in ("attack", "공격", "공"):
        for mid in list(room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon and mon.name.lower() == rest.lower():
                msgs = attack_monster(db, char, mon)
                if mon.hp <= 0 and mid in (room.monster_ids or []):
                    room.monster_ids.remove(mid)
                    db.delete(mon)
                    db.commit()
                if char.hp <= 0:
                    char.hp = char.max_hp
                    char.current_room_id = 1
                    db.commit()
                    msgs.append({"type": "system", "content": "치명상을 입고 마을에서 깨어납니다...", "style": "warning"})
                return msgs
        return [{"type": "system", "content": f"주변에 '{rest}'(이)라는 적이 없습니다.", "style": "warning"}]

    # ── cast (무공) ──
    if verb in ("cast", "무공", "시전"):
        for mid in list(room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon:
                msgs = cast_martial_art(db, char, rest, mon)
                if mon.hp <= 0 and mid in (room.monster_ids or []):
                    room.monster_ids.remove(mid)
                    db.delete(mon)
                    db.commit()
                return msgs
        return [{"type": "system", "content": "적이 없습니다.", "style": "warning"}]

    # ── meditate ──
    if verb in ("meditate", "명상", "수련", "운기"):
        return meditate_service(db, char)

    # ── talk ──
    if verb in ("talk", "대화", "말"):
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc and npc.name.lower() == rest.lower():
                return [{"type": "npc_dialogue", "content": npc.dialogue or f"[{npc.name}]: ...", "style": "npc"}]
        return [{"type": "system", "content": "대화할 상대가 없습니다.", "style": "warning"}]

    # ── status ──
    if verb in ("status", "stat", "상태", "스탯", "정보"):
        faction = db.query(CharacterFaction).filter(CharacterFaction.character_id == char.id).first()
        faction_name = db.query(Faction).filter(Faction.id == faction.faction_id).first().name if faction else "무소속"
        stat = f"""
=== {char.name} [{char.origin}] ===
  Lv.{char.level}  EXP: {char.exp}  경지: {char.martial_stage}
  HP: {char.hp}/{char.max_hp}  MP: {char.mp}/{char.max_mp}
  공격: {char.attack}  방어: {char.defense}  속도: {char.speed}
  근골:{char.physique} 기맥:{char.ki} 신법:{char.agility} 심안:{char.insight} 매력:{char.charm} 복운:{char.luck}
  문파: {faction_name}
  성향: 의{char.righteousness} 협{char.heroism} 욕{char.greed} 냉{char.coldness} 광{char.madness} 정{char.affection}"""
        messages.append({"type": "system", "content": stat, "style": "normal"})
        return messages

    # ── inventory ──
    if verb in ("inv", "inventory", "가방", "인벤", "아이템", "소지품"):
        invs = db.query(Inventory).filter(Inventory.character_id == char.id).all()
        if not invs:
            return [{"type": "system", "content": "소지품이 비어있습니다.", "style": "normal"}]
        lines = ["[소지품 목록]"]
        for inv in invs:
            item = db.query(Item).filter(Item.id == inv.item_id).first()
            eq = " [장착중]" if inv.equipped else ""
            lines.append(f"  {item.name} x{inv.quantity}{eq} - {item.description[:30]}")
        messages.append({"type": "system", "content": "\n".join(lines), "style": "normal"})
        return messages

    # ── martial arts list ──
    if verb in ("arts", "skills", "무공목록", "배운무공"):
        cmas = db.query(CharacterMartialArt).filter(CharacterMartialArt.character_id == char.id).all()
        if not cmas:
            return [{"type": "system", "content": "아직 배운 무공이 없습니다. 문파에 가입하거나 스승에게 배우세요.", "style": "normal"}]
        lines = ["[습득한 무공]"]
        for cma in cmas:
            art = db.query(MartialArt).filter(MartialArt.id == cma.martial_art_id).first()
            lines.append(f"  {art.name} ({art.category}) 숙련:{cma.proficiency}/1000 숙성:{cma.stage} MP:{art.mp_cost}")
        messages.append({"type": "system", "content": "\n".join(lines), "style": "normal"})
        return messages

    # ── equip / use ──
    if verb in ("equip", "장착"):
        inv = db.query(Inventory).join(Item).filter(
            Inventory.character_id == char.id,
            Item.name.ilike(f"%{rest}%")
        ).first()
        if not inv: return [{"type": "system", "content": "해당 아이템이 없습니다.", "style": "warning"}]
        item = db.query(Item).filter(Item.id == inv.item_id).first()
        if item.item_type not in ("weapon", "armor", "accessory"):
            return [{"type": "system", "content": "장착할 수 없는 아이템입니다.", "style": "warning"}]
        inv.equipped = 1
        stats = item.stats or {}
        char.attack += stats.get("attack", 0)
        char.defense += stats.get("defense", 0)
        char.speed += stats.get("speed", 0)
        char.max_hp += stats.get("hp", 0)
        char.max_mp += stats.get("mp", 0)
        db.commit()
        return [{"type": "system", "content": f"{item.name}을(를) 장착했습니다.", "style": "normal"}]

    if verb in ("use", "사용"):
        inv = db.query(Inventory).join(Item).filter(
            Inventory.character_id == char.id,
            Item.name.ilike(f"%{rest}%")
        ).first()
        if not inv: return [{"type": "system", "content": "해당 아이템이 없습니다.", "style": "warning"}]
        item = db.query(Item).filter(Item.id == inv.item_id).first()
        if item.item_type != "consumable":
            return [{"type": "system", "content": "사용할 수 없는 아이템입니다.", "style": "warning"}]
        effects = item.effects or {}
        heal = effects.get("heal_amount", 0)
        if heal:
            char.hp = min(char.hp + heal, char.max_hp)
            messages.append({"type": "battle_log", "content": f"{item.name}을(를) 사용했습니다. 체력 +{heal}!", "style": "healing"})
        inv.quantity -= 1
        if inv.quantity <= 0:
            db.delete(inv)
        db.commit()
        return messages

    # ── quest ──
    if verb in ("quest", "퀘스트", "의뢰"):
        cqs = db.query(CharacterQuest).filter(CharacterQuest.character_id == char.id, CharacterQuest.status == "active").all()
        if not cqs:
            return [{"type": "system", "content": "진행 중인 의뢰가 없습니다.", "style": "normal"}]
        lines = ["[진행 중인 의뢰]"]
        for cq in cqs:
            quest = db.query(Quest).filter(Quest.id == cq.quest_id).first()
            if quest:
                obj = quest.objectives or {}
                lines.append(f"  {quest.name}: {obj.get('type','')} {obj.get('target','')} ({cq.progress}/{obj.get('count',1)})")
        messages.append({"type": "system", "content": "\n".join(lines), "style": "normal"})
        return messages

    # ── shop ──
    if verb in ("shop", "상점", "물품"):
        if not rest:
            shop = db.query(Shop).filter(Shop.room_id == char.current_room_id).first()
        else:
            shop = db.query(Shop).join(NPC).filter(NPC.name.ilike(f"%{rest}%")).first()
        if not shop:
            return [{"type": "system", "content": "주변에 상점이 없습니다.", "style": "warning"}]
        lines = [f"[{shop.name}] {shop.description}"]
        for item_id in (shop.item_ids or []):
            item = db.query(Item).filter(Item.id == item_id).first()
            if item:
                lines.append(f"  {item.name} - {item.price}은전")
        lines.append("buy <아이템명> 으로 구매하세요.")
        messages.append({"type": "system", "content": "\n".join(lines), "style": "normal"})
        return messages

    if verb in ("buy", "구매"):
        shop = db.query(Shop).filter(Shop.room_id == char.current_room_id).first()
        if not shop: return [{"type": "system", "content": "주변에 상점이 없습니다.", "style": "warning"}]
        item = db.query(Item).filter(Item.name.ilike(f"%{rest}%"), Item.id.in_(shop.item_ids or [])).first()
        if not item: return [{"type": "system", "content": "상점에 없는 물품입니다.", "style": "warning"}]
        # 금전 체크는 추후 구현
        inv = Inventory(character_id=char.id, item_id=item.id, quantity=1)
        db.add(inv)
        db.commit()
        return [{"type": "system", "content": f"{item.name}을(를) 구매했습니다!", "style": "normal"}]

    # ── help ──
    if verb in ("help", "도움", "?"):
        messages.append({"type": "system", "content": """
[명령어]
  look / 보기          주변 살펴보기
  북/남/동/서          이동
  attack <대상>        기본 공격
  cast <무공명>        무공 발동
  meditate / 수련      내공 운행 (+MP, +EXP)
  talk <대상>          NPC와 대화
  status / 상태        캐릭터 정보
  inv / 가방            소지품 확인
  equip <아이템>       장비 장착
  use <아이템>          소모품 사용
  arts / 무공목록      배운 무공 확인
  quest / 퀘스트       진행 중인 의뢰
  shop / 상점           상점 물품 보기
  buy <아이템>         구매
  save / 저장           수동 저장
  help / 도움           도움말""", "style": "normal"})
        return messages

    # ── save ──
    if verb in ("save", "저장"):
        db.commit()
        return [{"type": "system", "content": "기록되었습니다.", "style": "normal"}]

    return [{"type": "system", "content": f"'{cmd}'? 알 수 없는 명령입니다. 'help'를 확인하세요.", "style": "warning"}]
