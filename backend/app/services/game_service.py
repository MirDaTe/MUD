"""
게임 명령어 처리 서비스
"""
import random
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.room import Room
from ..models.npc import NPC
from ..models.monster import Monster


def parse_command(cmd: str) -> tuple[str, str]:
    parts = cmd.strip().lower().split(maxsplit=1)
    verb = parts[0] if parts else ""
    rest = parts[1] if len(parts) > 1 else ""
    return verb, rest


def execute_command(db: Session, char: Character, cmd: str) -> list[dict]:
    messages = []
    verb, rest = parse_command(cmd)
    room = db.query(Room).filter(Room.id == char.current_room_id).first()

    # ── look ──
    if verb in ("look", "l", "주변", "보기"):
        if not room:
            messages.append({"type": "system", "content": "허공입니다...", "style": "normal"})
            return messages
        messages.append({"type": "room_desc", "content": f"[{room.name}]", "style": "room"})
        messages.append({"type": "room_desc", "content": room.description, "style": "room"})
        # exits
        ex = {k: v for k, v in (room.exits or {}).items() if v}
        if ex:
            dirs = ", ".join(ex.keys())
            messages.append({"type": "system", "content": f"갈 수 있는 곳: {dirs}", "style": "normal"})
        # npcs / monsters
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc:
                tag = "[적대]" if npc.is_hostile else ""
                messages.append({"type": "npc_present", "content": f"{tag} {npc.name}(이)가 여기에 있습니다.", "style": "npc"})
        for mid in (room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon:
                messages.append({"type": "monster_present", "content": f"위협적인 {mon.name}(이)가 노려보고 있습니다!", "style": "warning"})
        return messages

    # ── movement ──
    dir_map = {
        "north": "북", "n": "북", "south": "남", "s": "남",
        "east": "동", "e": "동", "west": "서", "w": "서",
        "북": "north", "남": "south", "동": "east", "서": "west",
    }
    if verb in dir_map or verb in ("go", "이동"):
        if verb in ("go", "이동"):
            direction = dir_map.get(rest, rest)
        else:
            direction = dir_map.get(verb, verb)

        # eng key for room exit lookup
        eng_key = direction
        for en, ko in [("north", "북"), ("south", "남"), ("east", "동"), ("west", "서")]:
            if direction == ko:
                eng_key = en
                break
        if direction in ("n", "북"):
            eng_key = "north"
        elif direction in ("s", "남"):
            eng_key = "south"
        elif direction in ("e", "동"):
            eng_key = "east"
        elif direction in ("w", "서"):
            eng_key = "west"

        target_id = (room.exits or {}).get(eng_key) if room else None
        if target_id:
            char.current_room_id = target_id
            db.commit()
            # get ko direction name
            ko_dir = {"north": "북", "south": "남", "east": "동", "west": "서"}.get(eng_key, eng_key)
            messages.append({"type": "system", "content": f"{ko_dir}쪽으로 이동합니다...", "style": "normal"})
            return messages + execute_command(db, char, "look")
        else:
            messages.append({"type": "system", "content": "그 방향으로는 갈 수 없습니다.", "style": "warning"})
            return messages

    # ── attack ──
    if verb in ("attack", "공격", "공"):
        target_name = rest
        room = db.query(Room).filter(Room.id == char.current_room_id).first()
        for mid in list(room.monster_ids or []):
            mon = db.query(Monster).filter(Monster.id == mid).first()
            if mon and mon.name.lower() == target_name.lower():
                dmg = max(1, char.attack - mon.defense + random.randint(-2, 4))
                crit = random.random() < char.crit_rate
                if crit:
                    dmg = int(dmg * 1.8)
                    messages.append({"type": "battle_log", "content": f"치명타! 당신의 검이 {mon.name}의 급소를 꿰뚫습니다! {dmg}의 피해!", "style": "critical"})
                else:
                    messages.append({"type": "battle_log", "content": f"당신의 일격! {mon.name}에게 {dmg}의 피해를 입혔습니다.", "style": "battle"})
                mon.hp -= dmg
                if mon.hp <= 0:
                    death_msg = mon.death_template or f"{mon.name}(이)가 쓰러집니다. 마지막 숨결이 허공으로 흩어집니다."
                    messages.append({"type": "battle_log", "content": death_msg, "style": "battle"})
                    char.exp += mon.exp_reward
                    room.monster_ids.remove(mid)
                    db.delete(mon)
                    db.commit()
                else:
                    # 반격
                    m_dmg = max(1, mon.attack - char.defense + random.randint(-2, 2))
                    char.hp -= m_dmg
                    messages.append({"type": "battle_log", "content": f"{mon.name}(이)가 반격합니다! {m_dmg}의 피해를 받았습니다. (HP: {char.hp}/{char.max_hp})", "style": "battle"})
                    if char.hp <= 0:
                        char.hp = char.max_hp
                        char.current_room_id = 1
                        messages.append({"type": "system", "content": "치명상을 입고 정신을 잃었습니다... 마을에서 깨어납니다.", "style": "warning"})
                db.commit()
                return messages
        messages.append({"type": "system", "content": f"주변에 '{target_name}'(이)라는 적이 없습니다.", "style": "warning"})
        return messages

    # ── talk ──
    if verb in ("talk", "대화", "말"):
        target_name = rest
        for nid in (room.npc_ids or []):
            npc = db.query(NPC).filter(NPC.id == nid).first()
            if npc and npc.name.lower() == target_name.lower():
                msg = npc.dialogue or f"[{npc.name}]: ...할 말이 없군."
                messages.append({"type": "npc_dialogue", "content": msg, "style": "npc"})
                return messages
        messages.append({"type": "system", "content": "대화할 상대가 주변에 없습니다.", "style": "warning"})
        return messages

    # ── status ──
    if verb in ("status", "stat", "상태", "스탯", "정보"):
        stat = f"""
=== {char.name} [{char.origin}] ===
  Lv.{char.level}  EXP: {char.exp}  경지: {char.martial_stage}
  HP: {char.hp}/{char.max_hp}  MP: {char.mp}/{char.max_mp}
  공격: {char.attack}  방어: {char.defense}  속도: {char.speed}
  근골:{char.physique} 기맥:{char.ki} 신법:{char.agility} 심안:{char.insight} 매력:{char.charm} 복운:{char.luck}
"""
        messages.append({"type": "system", "content": stat, "style": "normal"})
        return messages

    # ── help ──
    if verb in ("help", "도움", "?"):
        messages.append({"type": "system", "content": """
[명령어 목록]
  look / 보기      - 주변을 살펴봅니다
  북/남/동/서      - 해당 방향으로 이동
  attack <대상>    - 대상을 공격
  talk <대상>      - NPC와 대화
  status / 상태    - 캐릭터 정보
  chat <메시지>    - 전체 채팅
  save / 저장      - 수동 저장
  help / 도움      - 이 도움말
""", "style": "normal"})
        return messages

    # ── save ──
    if verb in ("save", "저장"):
        db.commit()
        messages.append({"type": "system", "content": "기록되었습니다.", "style": "normal"})
        return messages

    # ── default ──
    messages.append({"type": "system", "content": f"'{cmd}'? 알 수 없는 명령입니다. 'help'를 입력해보세요.", "style": "warning"})
    return messages
