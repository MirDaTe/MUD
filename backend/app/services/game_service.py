"""게임 명령어 처리 서비스 (영어/한글 병행, 관리자 명령어, 레벨 디자인)"""
import random
from typing import Optional
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.room import Room
from ..models.npc import NPC
from ..models.monster import Monster
from ..models.martial_art import MartialArt
from ..models.character_martial_art import CharacterMartialArt
from ..models.item import Item as ItemModel
from ..models.inventory import Inventory
from ..models.quest import Quest
from ..models.character_quest import CharacterQuest
from ..models.affection import Affection
from ..models.shop import Shop
from ..models.faction import Faction
from ..models.character_faction import CharacterFaction
from ..models.user import User
from .combat_service import attack_monster, cast_martial_art, meditate as meditate_service, check_stage_up
from .enchant_service import upgrade_item
from .admin_service import (
    is_admin, admin_set_stat, admin_teleport, admin_give_item,
    get_all_users, get_all_characters, admin_list_rooms
)


def parse_command(cmd: str) -> tuple[str, str]:
    parts = cmd.strip().split(maxsplit=1)
    verb = parts[0].lower() if parts else ""
    rest = parts[1] if len(parts) > 1 else ""
    return verb, rest


# ── 영어/한글 명령어 매핑 ──
def normalize_verb(verb: str, rest: str) -> tuple[str, str]:
    """영어/한글 명령어를 통일된 내부 명령어로 변환"""
    mapping = {
        # 기본
        "look": "look", "l": "look", "주변": "look", "보기": "look", "살펴보다": "look",
        # 이동 (8방향 + 특수)
        "north": "north", "n": "north", "북": "north", "북쪽": "north",
        "south": "south", "s": "south", "남": "south", "남쪽": "south",
        "east": "east", "e": "east", "동": "east", "동쪽": "east",
        "west": "west", "w": "west", "서": "west", "서쪽": "west",
        "up": "up", "u": "up", "위": "up", "올라가다": "up",
        "down": "down", "d": "down", "아래": "down", "내려가다": "down",
        "enter": "enter", "in": "enter", "들어가다": "enter", "입장": "enter",
        "out": "out", "exit": "out", "나가다": "out", "퇴장": "out",
        "go": "go", "이동": "go", "가다": "go",
        # 전투
        "attack": "attack", "공격": "attack", "공": "attack", "때리다": "attack",
        "cast": "cast", "무공": "cast", "시전": "cast", "사용": "cast",
        "meditate": "meditate", "명상": "meditate", "수련": "meditate", "운기": "meditate",
        # 대화
        "talk": "talk", "대화": "talk", "말": "talk", "말걸기": "talk", "이야기": "talk",
        # 정보
        "status": "status", "stat": "status", "상태": "status", "스탯": "status", "정보": "status",
        "inv": "inv", "inventory": "inv", "가방": "inv", "인벤": "inv", "소지품": "inv", "아이템": "inv",
        "arts": "arts", "skills": "arts", "무공목록": "arts", "배운무공": "arts", "기술": "arts",
        # 장비
        "equip": "equip", "장착": "equip", "착용": "equip",
        "use": "use", "사용하기": "use", "먹다": "use",
        # 상점
        "shop": "shop", "상점": "shop", "물품": "shop", "상인": "shop",
        "buy": "buy", "구매": "buy", "사다": "buy",
        # 강화
        "enchant": "enchant", "upgrade": "enchant", "강화": "enchant", "인챈트": "enchant", "강화하기": "enchant",
        # 퀘스트
        "quest": "quest", "퀘스트": "quest", "의뢰": "quest", "임무": "quest",
        # 저장
        "save": "save", "저장": "save", "기록": "save",
        # 도움말
        "help": "help", "도움": "help", "도움말": "help", "?": "help", "명령": "help", "명령어": "help",
        # 관리자
        "admin_set": "admin_set", "관리자설정": "admin_set",
        "admin_tp": "admin_tp", "tp": "admin_tp", "순간이동": "admin_tp",
        "admin_give": "admin_give", "give": "admin_give", "아이템지급": "admin_give",
        "admin_users": "admin_users", "users": "admin_users", "유저목록": "admin_users",
        "admin_chars": "admin_chars", "chars": "admin_chars", "캐릭터목록": "admin_chars",
        "admin_rooms": "admin_rooms", "rooms": "admin_rooms", "방목록": "admin_rooms",
        "admin_god": "admin_god", "god": "admin_god", "무적": "admin_god",
    }
    key = verb.lower()
    if key in mapping:
        return mapping[key], rest
    return verb, rest


def execute_command(db: Session, char: Character, cmd: str) -> list[dict]:
    messages = []
    verb, rest = parse_command(cmd)
    verb, rest = normalize_verb(verb, rest)
    room = db.query(Room).filter(Room.id == char.current_room_id).first()

    # ── look ──
    if verb == "look":
        if not room: return [{"type": "system", "content": "허공입니다...", "style": "normal"}]
        messages.append({"type": "room_desc", "content": f"[{room.name}] (#{room.id})", "style": "room"})
        messages.append({"type": "room_desc", "content": room.description, "style": "room"})
        ex = {k: v for k, v in (room.exits or {}).items() if v}
        if ex:
            ko = {"north": "북", "south": "남", "east": "동", "west": "서", "up": "위", "down": "아래",
                  "enter": "입장", "out": "퇴장", "cross": "건너", "deep": "깊은", "escape": "도망",
                  "inner": "안", "secret": "비밀", "back": "뒤로", "edge": "끝"}
            dirs = ", ".join(f"[{ko.get(k, k)}]" for k in ex)
            messages.append({"type": "system", "content": f"갈 수 있는 곳: {dirs}", "style": "normal"})
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc:
                tag = "⚔" if npc.is_hostile else ""
                messages.append({"type": "npc_present", "content": f"{tag} {npc.name}(이)가 여기에 있습니다.", "style": "npc"})
        for mid in (room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon:
                messages.append({"type": "monster_present", "content": f"위협적인 {mon.name}(이)가 노려보고 있습니다! (HP:{mon.hp}/{mon.max_hp})", "style": "warning"})
        return messages

    # ── movement ──
    if verb in ("north", "south", "east", "west", "up", "down", "enter", "out", "go"):
        if verb == "go":
            direction_raw = rest.strip().lower()
            dir_short = {"n": "north", "s": "south", "e": "east", "w": "west",
                         "북": "north", "남": "south", "동": "east", "서": "west",
                         "u": "up", "d": "down"}.get(direction_raw, direction_raw)
        else:
            dir_short = verb

        target_id = (room.exits or {}).get(dir_short) if room else None
        if target_id:
            char.current_room_id = target_id
            db.commit()
            ko = {"north": "북", "south": "남", "east": "동", "west": "서",
                  "up": "위", "down": "아래", "enter": "안"}.get(dir_short, dir_short)
            messages.append({"type": "system", "content": f"{ko}쪽으로 이동...", "style": "normal"})
            return messages + execute_command(db, char, "look")
        else:
            messages.append({"type": "system", "content": "그 방향으로는 갈 수 없습니다.", "style": "warning"})
            return messages

    # ── attack ──
    if verb == "attack":
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
                # 레벨업 체크
                _check_levelup(db, char, msgs)
                return msgs
        return [{"type": "system", "content": f"주변에 '{rest}'(이)라는 적이 없습니다.", "style": "warning"}]

    # ── cast ──
    if verb == "cast":
        for mid in list(room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon:
                msgs = cast_martial_art(db, char, rest, mon)
                if mon.hp <= 0 and mid in (room.monster_ids or []):
                    room.monster_ids.remove(mid)
                    db.delete(mon)
                    db.commit()
                    _check_levelup(db, char, msgs)
                return msgs
        return [{"type": "system", "content": "적이 없습니다.", "style": "warning"}]

    # ── meditate ──
    if verb == "meditate":
        msgs = meditate_service(db, char)
        _check_levelup(db, char, msgs)
        return msgs

    # ── talk ──
    if verb == "talk":
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc and npc.name.lower() == rest.lower():
                return [{"type": "npc_dialogue", "content": npc.dialogue or f"[{npc.name}]: ...", "style": "npc"}]
        return [{"type": "system", "content": "대화할 상대가 없습니다.", "style": "warning"}]

    # ── status ──
    if verb == "status":
        faction = db.query(CharacterFaction).filter(CharacterFaction.character_id == char.id).first()
        faction_name = db.query(Faction).filter(Faction.id == faction.faction_id).first().name if faction else "무소속"
        to_next = _exp_to_next(char)
        stat = f"""
══ {char.name} [{char.origin}] ══
  Lv.{char.level}  EXP: {char.exp}/{to_next}  경지: {char.martial_stage}
  HP: {char.hp}/{char.max_hp}  MP: {char.mp}/{char.max_mp}
  공격: {char.attack}  방어: {char.defense}  속도: {char.speed}
  자질: 근골{char.physique} 기맥{char.ki} 신법{char.agility} 심안{char.insight} 매력{char.charm} 복운{char.luck}
  문파: {faction_name}  위치: #{char.current_room_id}"""
        messages.append({"type": "system", "content": stat, "style": "normal"})
        return messages

    # ── inv ──
    if verb == "inv":
        invs = db.query(Inventory).filter(Inventory.character_id == char.id).all()
        if not invs:
            return [{"type": "system", "content": "소지품이 비어있습니다.", "style": "normal"}]
        lines = ["[소지품]"]
        for inv in invs:
            item = db.query(ItemModel).filter(ItemModel.id == inv.item_id).first()
            eq = " [장착중]" if inv.equipped else ""
            lines.append(f"  {item.name} x{inv.quantity}{eq}")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # ── arts ──
    if verb == "arts":
        cmas = db.query(CharacterMartialArt).filter(CharacterMartialArt.character_id == char.id).all()
        if not cmas:
            return [{"type": "system", "content": "아직 배운 무공이 없습니다.", "style": "normal"}]
        lines = ["[습득한 무공]"]
        for cma in cmas:
            art = db.query(MartialArt).filter(MartialArt.id == cma.martial_art_id).first()
            lines.append(f"  {art.name} 숙련:{cma.proficiency}/1000 MP:{art.mp_cost}")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # ── equip ──
    if verb == "equip":
        inv = db.query(Inventory).join(ItemModel).filter(
            Inventory.character_id == char.id, ItemModel.name.ilike(f"%{rest}%")
        ).first()
        if not inv: return [{"type": "system", "content": "해당 아이템이 없습니다.", "style": "warning"}]
        item = db.query(ItemModel).filter(ItemModel.id == inv.item_id).first()
        if item.item_type not in ("weapon", "armor", "accessory"):
            return [{"type": "system", "content": "장착할 수 없는 아이템입니다.", "style": "warning"}]
        inv.equipped = 1
        stats = item.stats or {}
        char.attack += stats.get("attack", 0)
        char.defense += stats.get("defense", 0)
        char.max_hp += stats.get("hp", 0)
        char.max_mp += stats.get("mp", 0)
        db.commit()
        return [{"type": "system", "content": f"{item.name} 장착 완료!", "style": "normal"}]

    # ── use ──
    if verb == "use":
        inv = db.query(Inventory).join(ItemModel).filter(
            Inventory.character_id == char.id, ItemModel.name.ilike(f"%{rest}%")
        ).first()
        if not inv: return [{"type": "system", "content": "해당 아이템이 없습니다.", "style": "warning"}]
        item = db.query(ItemModel).filter(ItemModel.id == inv.item_id).first()
        if item.item_type != "consumable":
            return [{"type": "system", "content": "사용할 수 없는 아이템입니다.", "style": "warning"}]
        effects = item.effects or {}
        heal = effects.get("heal_amount", 15)
        char.hp = min(char.hp + heal, char.max_hp)
        inv.quantity -= 1
        if inv.quantity <= 0:
            db.delete(inv)
        db.commit()
        return [{"type": "battle_log", "content": f"{item.name} 사용! 체력 +{heal}!", "style": "healing"}]

    # ── quest ──
    if verb == "quest":
        cqs = db.query(CharacterQuest).filter(CharacterQuest.character_id == char.id, CharacterQuest.status == "active").all()
        if not cqs: return [{"type": "system", "content": "의뢰가 없습니다.", "style": "normal"}]
        lines = ["[진행 중인 의뢰]"]
        for cq in cqs:
            q = db.query(Quest).filter(Quest.id == cq.quest_id).first()
            if q:
                obj = q.objectives or {}
                lines.append(f"  {q.name}: {obj.get('type','')} {obj.get('target','')} ({cq.progress}/{obj.get('count',1)})")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # ── shop / buy ──
    if verb == "shop":
        shop = db.query(Shop).filter(Shop.room_id == char.current_room_id).first()
        if not shop: return [{"type": "system", "content": "주변에 상점이 없습니다.", "style": "warning"}]
        lines = [f"[{shop.name}]"]
        for iid in (shop.item_ids or [])[:15]:
            item = db.query(ItemModel).filter(ItemModel.id == iid).first()
            if item: lines.append(f"  {item.name} — {item.price}은전")
        lines.append("'buy <아이템명>' 으로 구매")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    if verb == "buy":
        shop = db.query(Shop).filter(Shop.room_id == char.current_room_id).first()
        if not shop: return [{"type": "system", "content": "상점이 없습니다.", "style": "warning"}]
        item = db.query(ItemModel).filter(ItemModel.name.ilike(f"%{rest}%"), ItemModel.id.in_(shop.item_ids or [])).first()
        if not item: return [{"type": "system", "content": "상점에 없는 물품입니다.", "style": "warning"}]
        db.add(Inventory(character_id=char.id, item_id=item.id, quantity=1))
        db.commit()
        return [{"type": "system", "content": f"{item.name} 구매 완료!", "style": "normal"}]

    # ── enchant ──
    if verb == "enchant":
        p = rest.split()
        use_protect = "-p" in p or "보호" in p
        use_advanced = "-a" in p or "고급" in p
        item_part = " ".join(w for w in p if not w.startswith("-") and w not in ("보호", "고급"))
        if not item_part:
            return [{"type": "system", "content": "사용법: enchant <아이템명> [-p 보호] [-a 고급강화석]", "style": "warning"}]
        return upgrade_item(db, char, item_part, use_protect, use_advanced)

    # ── 관리자 명령어 ──
    # admin_set <char_id> <field> <value>
    if verb == "admin_set":
        user = db.query(User).filter(User.username == "admin").first()
        if not is_admin(db, user.id if user else 0):
            return [{"type": "system", "content": "관리자 권한이 필요합니다.", "style": "warning"}]
        p = rest.split()
        if len(p) < 3: return [{"type": "system", "content": "사용법: admin_set <캐릭터ID> <필드> <값>", "style": "warning"}]
        err = admin_set_stat(db, int(p[0]), p[1], int(p[2]))
        if err: return [{"type": "system", "content": err, "style": "warning"}]
        return [{"type": "system", "content": f"설정 완료: char#{p[0]}.{p[1]} = {p[2]}", "style": "normal"}]

    # admin_tp <char_id> <room_id>
    if verb == "admin_tp":
        p = rest.split()
        if len(p) < 2: return [{"type": "system", "content": "사용법: admin_tp <캐릭터ID> <방ID>", "style": "warning"}]
        err = admin_teleport(db, int(p[0]), int(p[1]))
        if err: return [{"type": "system", "content": err, "style": "warning"}]
        return [{"type": "system", "content": f"캐릭터 #{p[0]} → 방 #{p[1]} 순간이동 완료", "style": "normal"}]

    # admin_give <char_id> <item_id> [qty]
    if verb == "admin_give":
        p = rest.split()
        if len(p) < 2: return [{"type": "system", "content": "사용법: admin_give <캐릭터ID> <아이템ID> [수량]", "style": "warning"}]
        qty = int(p[2]) if len(p) > 2 else 1
        err = admin_give_item(db, int(p[0]), int(p[1]), qty)
        if err: return [{"type": "system", "content": err, "style": "warning"}]
        return [{"type": "system", "content": f"아이템 #{p[1]} x{qty} 지급 완료 (캐릭터 #{p[0]})", "style": "normal"}]

    # admin_users — 유저 목록
    if verb == "admin_users":
        users = get_all_users(db)
        lines = ["[유저 목록]"]
        for u in users:
            admin_tag = " ★" if u["is_admin"] else ""
            lines.append(f"  #{u['id']} {u['username']}{admin_tag} ({u['email']})")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # admin_chars — 캐릭터 목록
    if verb == "admin_chars":
        chars = get_all_characters(db)
        lines = ["[캐릭터 목록]"]
        for c in chars:
            lines.append(f"  #{c['id']} {c['name']} Lv.{c['level']} 경지:{c['martial_stage']} 위치:#{c['current_room_id']} (유저#{c['user_id']})")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # admin_rooms — 방 목록
    if verb == "admin_rooms":
        rooms = admin_list_rooms(db)
        lines = ["[방 목록]"]
        for r in rooms:
            exits = ", ".join(r["exits"].keys()) if r["exits"] else "없음"
            lines.append(f"  #{r['id']} {r['name']} ({r['region']}) → {exits}")
        return [{"type": "system", "content": "\n".join(lines), "style": "normal"}]

    # admin_god — 무적 토글
    if verb == "admin_god":
        char.hp = 999999
        char.max_hp = 999999
        char.attack = 9999
        char.defense = 9999
        db.commit()
        return [{"type": "system", "content": "⚡ 무적 모드 활성화! HP/공격/방어 MAX", "style": "critical"}]

    # ── help ──
    if verb == "help":
        return [{"type": "system", "content": """
[명령어 / Commands]
  look / 보기             주변 살펴보기
  북/남/동/서/위/아래      이동 (n/s/e/w/u/d)
  attack <대상> / 공격     기본 공격
  cast <무공명> / 시전     무공 발동
  meditate / 수련          내공 운행
  talk <대상> / 대화       NPC와 대화
  status / 상태            캐릭터 정보
  inv / 가방               소지품
  equip <아이템>           장비 장착
  use <아이템>             소모품 사용
  arts / 무공목록          배운 무공
  quest / 퀘스트           진행중 의뢰
  shop / 상점              상점 보기
  buy <아이템> / 구매      구매
  enchant <아이템>         아이템 강화 (+1~+15)
  save / 저장              저장

[관리자 / Admin]
  admin_set <char_id> <field> <value>
  admin_tp <char_id> <room_id>
  admin_give <char_id> <item_id> [qty]
  admin_users / admin_chars / admin_rooms
  admin_god               무적 모드""", "style": "normal"}]

    # ── save ──
    if verb == "save":
        db.commit()
        return [{"type": "system", "content": "기록되었습니다.", "style": "normal"}]

    return [{"type": "system", "content": f"'{cmd}'? 알 수 없는 명령입니다. 'help'를 확인하세요.", "style": "warning"}]


# ── 레벨 디자인 ──
EXP_TABLE = [
    0,      # 1
    50,     # 2
    120,    # 3
    220,    # 4
    350,    # 5
    520,    # 6
    740,    # 7
    1000,   # 8
    1320,   # 9
    1700,   # 10
    2150,   # 11
    2680,   # 12
    3300,   # 13
    4000,   # 14
    4800,   # 15
    5700,   # 16
    6700,   # 17
    7800,   # 18
    9000,   # 19
    10400,  # 20
    12000,  # 21
    13800,  # 22
    15800,  # 23
    18000,  # 24
    20500,  # 25
    23300,  # 26
    26400,  # 27
    29800,  # 28
    33500,  # 29
    37600,  # 30
    42200,  # 31
    47300,  # 32
    53000,  # 33
    59400,  # 34
    66600,  # 35
    74600,  # 36
    83500,  # 37
    93400,  # 38
    104400, # 39
    116500, # 40
    130000, # 41
    145000, # 42
    162000, # 43
    181000, # 44
    202000, # 45
    225000, # 46
    251000, # 47
    280000, # 48
    312000, # 49
    350000, # 50 (MAX)
]

LEVEL_STAT_GAIN = {
    "attack": 2, "defense": 1, "max_hp": 12, "max_mp": 6, "speed": 1
}


def _exp_to_next(char: Character) -> int:
    if char.level >= len(EXP_TABLE):
        return 0
    return EXP_TABLE[char.level - 1] if char.level <= len(EXP_TABLE) else 999999


def _check_levelup(db: Session, char: Character, msgs: list[dict]):
    while char.level < len(EXP_TABLE) and char.exp >= EXP_TABLE[char.level]:
        char.level += 1
        char.max_hp += LEVEL_STAT_GAIN["max_hp"]
        char.hp = char.max_hp
        char.max_mp += LEVEL_STAT_GAIN["max_mp"]
        char.mp = char.max_mp
        char.attack += LEVEL_STAT_GAIN["attack"]
        char.defense += LEVEL_STAT_GAIN["defense"]
        char.speed += LEVEL_STAT_GAIN["speed"]
        msgs.append({"type": "system", "content": f"── 레벨업! Lv.{char.level} ──", "style": "critical"})
        db.commit()
