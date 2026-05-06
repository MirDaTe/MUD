"""몬스터 재생성 서비스 — 선공 몬스터 리스폰 + 랜덤 타이머"""
import random
import threading
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.monster import Monster
from ..models.room import Room

# 전역 리스폰 스케줄
_respawn_timers = {}  # {monster_id: timer_thread}
_respawn_times = {}   # {monster_id: datetime_of_respawn}


def _respawn_monster(monster_id: int, room_ids: list):
    """지정된 몬스터를 해당 방들 중 하나에 리스폰"""
    try:
        db = SessionLocal()
        # 몬스터가 이미 존재하는지 확인 (다른 스레드가 먼저 생성했을 수 있음)
        existing = db.query(Monster).filter(Monster.id == monster_id).first()
        if existing:
            db.close()
            return

        # 원본 몬스터 데이터 로드 (seed에서 생성된 Monster 기록 찾기)
        # 이미 삭제된 상태이므로, 새로운 Monster 객체 생성
        # monster_id는 고유 ID이므로 새로운 ID로 생성
        new_id = _get_next_monster_id(db)
        
        # 동일한 monster_id로 재생성하려면? 
        # monster_id를 고정 ID로 사용하는 시스템이기 때문에
        # 기존 monster_id로 새 객체 생성
        monster_data = _get_monster_template(monster_id)
        if not monster_data:
            db.close()
            return
        
        new_monster = Monster(
            id=monster_id,
            name=monster_data["name"],
            description=monster_data.get("description", ""),
            hp=monster_data["max_hp"],
            max_hp=monster_data["max_hp"],
            attack=monster_data["attack"],
            defense=monster_data.get("defense", 0),
            speed=monster_data.get("speed", 10),
            exp_reward=monster_data.get("exp_reward", 20),
            gold_reward=monster_data.get("gold_reward", 0),
            fame_reward=monster_data.get("fame_reward", 0),
            min_level=monster_data.get("min_level", 1),
            max_level=monster_data.get("max_level", 999),
            drop_table=monster_data.get("drop_table", []),
            is_boss=monster_data.get("is_boss", False),
            is_aggro=monster_data.get("is_aggro", False),
            respawn_min=monster_data.get("respawn_min", 30),
            respawn_max=monster_data.get("respawn_max", 120),
            attack_templates=monster_data.get("attack_templates", [f"{monster_data['name']}의 공격!"]),
            death_template=monster_data.get("death_template", f"{monster_data['name']}이(가) 쓰러졌다!"),
            ambient_lines=monster_data.get("ambient_lines", [])
        )
        db.add(new_monster)
        db.flush()
        
        # 방에 monster_id 추가
        if room_ids:
            for rid in room_ids:
                room = db.query(Room).filter(Room.id == rid).first()
                if room:
                    mon_ids = list(room.monster_ids or [])
                    if monster_id not in mon_ids:
                        mon_ids.append(monster_id)
                        room.monster_ids = mon_ids

        db.commit()
        db.close()
        
        # 타이머 정리
        monster_id_key = f"{monster_id}_{'_'.join(str(r) for r in (room_ids or []))}"
        if monster_id_key in _respawn_timers:
            del _respawn_timers[monster_id_key]
        if monster_id_key in _respawn_times:
            del _respawn_times[monster_id_key]
            
    except Exception as e:
        print(f"[Respawn] Error respawning monster {monster_id}: {e}")
        try:
            db.close()
        except:
            pass


def _get_next_monster_id(db):
    """사용 가능한 다음 monster ID 반환"""
    max_id = db.query(Monster.id).order_by(Monster.id.desc()).first()
    return (max_id[0] + 1) if max_id else 10000


# 몬스터 템플릿 캐시 (seed 데이터를 저장)
_monster_templates = {}


def register_monster_templates():
    """Seed 데이터로부터 몬스터 템플릿 등록 (서버 시작 시 호출)"""
    global _monster_templates
    try:
        db = SessionLocal()
        monsters = db.query(Monster).all()
        for m in monsters:
            _monster_templates[m.id] = {
                "name": m.name,
                "description": m.description,
                "max_hp": m.max_hp,
                "attack": m.attack,
                "defense": m.defense,
                "speed": m.speed,
                "exp_reward": m.exp_reward,
                "gold_reward": getattr(m, "gold_reward", 0),
                "fame_reward": getattr(m, "fame_reward", 0),
                "min_level": getattr(m, "min_level", 1),
                "max_level": getattr(m, "max_level", 999),
                "drop_table": getattr(m, "drop_table", []),
                "is_boss": getattr(m, "is_boss", False),
                "is_aggro": getattr(m, "is_aggro", False),
                "respawn_min": getattr(m, "respawn_min", 30),
                "respawn_max": getattr(m, "respawn_max", 120),
                "attack_templates": getattr(m, "attack_templates", [f"{m.name}의 공격!"]),
                "death_template": getattr(m, "death_template", f"{m.name}이(가) 쓰러졌다!")
            }
        db.close()
        print(f"[Respawn] Registered {len(_monster_templates)} monster templates")
    except Exception as e:
        print(f"[Respawn] Error registering templates: {e}")


def _get_monster_template(monster_id: int) -> dict:
    """몬스터 ID로 템플릿 조회"""
    return _monster_templates.get(monster_id)


def schedule_respawn(monster_id: int, room_ids: list):
    """몬스터 사망 시 리스폰 스케줄링"""
    template = _get_monster_template(monster_id)
    if not template:
        print(f"[Respawn] No template for monster {monster_id}")
        return
    
    min_sec = template.get("respawn_min", 30)
    max_sec = template.get("respawn_max", 120)
    delay = random.randint(min_sec, max_sec)
    
    monster_key = f"{monster_id}_{'_'.join(str(r) for r in (room_ids or []))}"
    _respawn_times[monster_key] = datetime.now() + timedelta(seconds=delay)
    
    # 백그라운드 타이머 시작
    timer = threading.Timer(delay, _respawn_monster, args=[monster_id, room_ids])
    timer.daemon = True
    timer.start()
    _respawn_timers[monster_key] = timer
    
    print(f"[Respawn] Scheduled {template['name']}(ID:{monster_id}) in {delay}s")


def get_respawn_info(monster_id: int, room_ids: list = None) -> dict:
    """리스폰 정보 조회"""
    key_base = str(monster_id)
    for k, v in _respawn_times.items():
        if k.startswith(key_base):
            remaining = (v - datetime.now()).total_seconds()
            return {
                "monster_id": monster_id,
                "respawn_at": v.isoformat(),
                "remaining_seconds": max(0, int(remaining))
            }
    return None
