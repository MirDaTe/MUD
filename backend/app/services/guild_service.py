"""길드 시스템 서비스 — 문파 생성, 명성, 버프, 보관함, 초대/추방"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.guild import Guild
from ..models.guild_member import GuildMember
from ..models.guild_storage import GuildStorage
from ..models.guild_buff import GuildBuff
from ..models.guild_application import GuildApplication
from ..models.character import Character
from ..models.item import Item

# ── 길드 생성 비용 ──
GUILD_CREATE_GOLD = 5000
GUILD_CREATE_EXP = 1000

# ── 길드 명성 단계별 버프 ──
GUILD_BUFF_MILESTONES = [
    (100, "초심자의 의지", "길드 명성 100 달성", {"attack": 2, "defense": 1, "max_hp": 20}),
    (500, "단결된 무인", "길드 명성 500 달성", {"attack": 5, "defense": 3, "max_hp": 50, "max_mp": 20}),
    (1500, "정예 문파", "길드 명성 1,500 달성", {"attack": 10, "defense": 6, "max_hp": 120, "max_mp": 50, "speed": 2}),
    (5000, "강호의 명문", "길드 명성 5,000 달성", {"attack": 20, "defense": 12, "max_hp": 300, "max_mp": 120, "speed": 5, "crit_rate": 0.03}),
    (15000, "천하제일문", "길드 명성 15,000 달성", {"attack": 40, "defense": 25, "max_hp": 800, "max_mp": 300, "speed": 10, "crit_rate": 0.07}),
    (50000, "전설의 문파", "길드 명성 50,000 달성", {"attack": 80, "defense": 50, "max_hp": 2000, "max_mp": 800, "speed": 20, "crit_rate": 0.12}),
    (150000, "신화의 경지", "길드 명성 150,000 달성", {"attack": 160, "defense": 100, "max_hp": 5000, "max_mp": 2000, "speed": 40, "crit_rate": 0.20}),
]


def create_guild(db: Session, leader_char: Character, name: str, description: str = "") -> Optional[str]:
    """길드 생성"""
    if db.query(Guild).filter(Guild.name == name).first():
        return "이미 존재하는 문파 이름입니다."
    if db.query(GuildMember).filter(GuildMember.character_id == leader_char.id).first():
        return "이미 다른 문파에 소속되어 있습니다."
    if leader_char.gold < GUILD_CREATE_GOLD:
        return f"은전이 부족합니다. (필요: {GUILD_CREATE_GOLD}은전, 보유: {leader_char.gold}은전)"
    if leader_char.exp < GUILD_CREATE_EXP:
        return f"경험치가 부족합니다. (필요: {GUILD_CREATE_EXP}, 보유: {leader_char.exp})"

    leader_char.gold -= GUILD_CREATE_GOLD
    leader_char.exp -= GUILD_CREATE_EXP

    guild = Guild(name=name, description=description, leader_id=leader_char.id)
    db.add(guild)
    db.flush()

    member = GuildMember(guild_id=guild.id, character_id=leader_char.id, rank="길드장")
    db.add(member)
    db.commit()
    return None


def join_guild(db: Session, char: Character, guild_name: str) -> Optional[str]:
    """문파 가입 (신청 승인 방식)"""
    if db.query(GuildMember).filter(GuildMember.character_id == char.id).first():
        return "이미 문파에 소속되어 있습니다."
    guild = db.query(Guild).filter(Guild.name.ilike(f"%{guild_name}%")).first()
    if not guild:
        return "해당 문파를 찾을 수 없습니다."

    # 가입 신청 생성
    existing = db.query(GuildApplication).filter(
        GuildApplication.guild_id == guild.id,
        GuildApplication.character_id == char.id,
        GuildApplication.status == "pending"
    ).first()
    if existing:
        return "이미 가입 신청 중입니다."
    db.add(GuildApplication(guild_id=guild.id, character_id=char.id))
    db.commit()
    return None


def approve_application(db: Session, leader_char: Character, applicant_name: str) -> Optional[str]:
    """가입 승인 (길드장만 가능)"""
    guild = db.query(Guild).filter(Guild.leader_id == leader_char.id).first()
    if not guild:
        return "문파의 장만 승인할 수 있습니다."

    applicant = db.query(Character).filter(Character.name == applicant_name).first()
    if not applicant:
        return "해당 캐릭터를 찾을 수 없습니다."

    app = db.query(GuildApplication).filter(
        GuildApplication.guild_id == guild.id,
        GuildApplication.character_id == applicant.id,
        GuildApplication.status == "pending"
    ).first()
    if not app:
        return "해당 가입 신청이 없습니다."

    app.status = "accepted"
    db.add(GuildMember(guild_id=guild.id, character_id=applicant.id, rank="신입"))
    guild.member_count += 1
    db.commit()
    return None


def leave_guild(db: Session, char: Character) -> Optional[str]:
    """문파 탈퇴"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return "소속된 문파가 없습니다."
    guild = db.query(Guild).filter(Guild.id == member.guild_id).first()
    if guild and guild.leader_id == char.id:
        return "길드장은 탈퇴할 수 없습니다. 길드장을 위임하거나 문파를 해산하세요."

    db.delete(member)
    if guild:
        guild.member_count = max(0, guild.member_count - 1)
    db.commit()
    return None


def kick_member(db: Session, leader_char: Character, target_name: str) -> Optional[str]:
    """길드원 추방"""
    guild = db.query(Guild).filter(Guild.leader_id == leader_char.id).first()
    if not guild:
        return "문파를 소유하고 있지 않습니다."

    target = db.query(Character).filter(Character.name == target_name).first()
    if not target:
        return "해당 캐릭터를 찾을 수 없습니다."

    member = db.query(GuildMember).filter(
        GuildMember.guild_id == guild.id,
        GuildMember.character_id == target.id
    ).first()
    if not member:
        return "해당 캐릭터는 이 문파의 길드원이 아닙니다."
    if member.rank == "길드장":
        return "길드장은 추방할 수 없습니다."

    db.delete(member)
    guild.member_count = max(0, guild.member_count - 1)
    db.commit()
    return None


def change_rank(db: Session, leader_char: Character, target_name: str, new_rank: str) -> Optional[str]:
    """계급 변경"""
    valid_ranks = ["신입", "일반", "정예", "부길드장"]
    if new_rank not in valid_ranks:
        return f"유효하지 않은 계급입니다. 사용 가능: {', '.join(valid_ranks)}"

    guild = db.query(Guild).filter(Guild.leader_id == leader_char.id).first()
    if not guild:
        return "문파의 장만 변경할 수 있습니다."

    target = db.query(Character).filter(Character.name == target_name).first()
    if not target:
        return "해당 캐릭터를 찾을 수 없습니다."

    member = db.query(GuildMember).filter(
        GuildMember.guild_id == guild.id,
        GuildMember.character_id == target.id
    ).first()
    if not member:
        return "해당 캐릭터는 이 문파의 길드원이 아닙니다."

    member.rank = new_rank
    db.commit()
    return None


def get_guild_info(db: Session, char: Character) -> Optional[dict]:
    """내 문파 정보 조회"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return None
    guild = db.query(Guild).filter(Guild.id == member.guild_id).first()
    if not guild:
        return None

    leader = db.query(Character).filter(Character.id == guild.leader_id).first()
    members = db.query(GuildMember).filter(GuildMember.guild_id == guild.id).all()
    buffs = db.query(GuildBuff).filter(GuildBuff.guild_id == guild.id, GuildBuff.is_unlocked == 1).all()

    return {
        "guild_id": guild.id, "name": guild.name, "description": guild.description,
        "reputation": guild.reputation, "gold": guild.gold, "member_count": guild.member_count,
        "leader": leader.name if leader else "알 수 없음",
        "my_rank": member.rank, "my_contribution": member.contribution,
        "members": [{"name": db.query(Character).filter(Character.id == m.character_id).first().name,
                      "rank": m.rank, "contribution": m.contribution}
                     for m in members if db.query(Character).filter(Character.id == m.character_id).first()],
        "buffs": [{"name": b.buff_name, "description": b.buff_description} for b in buffs],
        "next_milestone": _next_milestone(guild.reputation),
    }


def add_reputation(db: Session, char: Character, amount: int):
    """문파 명성 추가 (퀘스트 완료, 보스 격파 시)"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return
    guild = db.query(Guild).filter(Guild.id == member.guild_id).first()
    if not guild:
        return
    guild.reputation += amount
    member.contribution += amount
    db.commit()

    # 버프 해금 체크
    _check_unlock_buffs(db, guild)


def add_guild_gold(db: Session, char: Character, amount: int):
    """문파 금고에 금액 추가"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return False
    guild = db.query(Guild).filter(Guild.id == member.guild_id).first()
    if not guild:
        return False
    if amount > 0 and char.gold < amount:
        return False
    char.gold -= amount
    guild.gold += amount
    db.commit()
    return True


def withdraw_guild_gold(db: Session, char: Character, amount: int) -> Optional[str]:
    """문파 금고에서 출금 (부길드장 이상)"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return "소속된 문파가 없습니다."
    if member.rank not in ("길드장", "부길드장"):
        return "부길드장 이상만 출금할 수 있습니다."
    guild = db.query(Guild).filter(Guild.id == member.guild_id).first()
    if guild.gold < amount:
        return "문파 금고의 은전이 부족합니다."
    guild.gold -= amount
    char.gold += amount
    db.commit()
    return None


# ── 창고 ──
def deposit_to_storage(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """문파 창고에 아이템 보관"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return "소속된 문파가 없습니다."

    from ..models.inventory import Inventory as Inv
    inv = db.query(Inv).join(Item).filter(
        Inv.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inv.equipped == 0
    ).first()
    if not inv:
        return "해당 아이템을 소지하고 있지 않습니다 (장착중인 아이템은 보관 불가)."
    if inv.quantity < quantity:
        return f"보유 수량이 부족합니다. (보유: {inv.quantity})"

    storage = db.query(GuildStorage).filter(
        GuildStorage.guild_id == member.guild_id,
        GuildStorage.item_id == inv.item_id
    ).first()
    if storage:
        storage.quantity += quantity
    else:
        db.add(GuildStorage(guild_id=member.guild_id, item_id=inv.item_id, quantity=quantity, deposited_by=char.id))

    inv.quantity -= quantity
    if inv.quantity <= 0:
        db.delete(inv)
    db.commit()
    return None


def withdraw_from_storage(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """문파 창고에서 아이템 인출"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return "소속된 문파가 없습니다."

    item = db.query(Item).filter(Item.name.ilike(f"%{item_name}%")).first()
    if not item:
        return "해당 아이템을 찾을 수 없습니다."

    storage = db.query(GuildStorage).filter(
        GuildStorage.guild_id == member.guild_id,
        GuildStorage.item_id == item.id
    ).first()
    if not storage or storage.quantity < quantity:
        return "창고에 해당 아이템이 부족합니다."

    from ..models.inventory import Inventory as Inv
    inv = db.query(Inv).filter(
        Inv.character_id == char.id,
        Inv.item_id == item.id,
        Inv.equipped == 0
    ).first()
    if inv:
        inv.quantity += quantity
    else:
        db.add(Inv(character_id=char.id, item_id=item.id, quantity=quantity))

    storage.quantity -= quantity
    if storage.quantity <= 0:
        db.delete(storage)
    db.commit()
    return None


def get_storage_contents(db: Session, char: Character) -> Optional[list]:
    """창고 내용물 조회"""
    member = db.query(GuildMember).filter(GuildMember.character_id == char.id).first()
    if not member:
        return None
    storages = db.query(GuildStorage).filter(GuildStorage.guild_id == member.guild_id).all()
    result = []
    for s in storages:
        item = db.query(Item).filter(Item.id == s.item_id).first()
        if item:
            result.append({"name": item.name, "quantity": s.quantity, "item_id": item.id})
    return result


# ── 버프 ──
def _check_unlock_buffs(db: Session, guild: Guild):
    """명성 기준 도달 시 버프 해금"""
    for rep, name, desc, bonus in GUILD_BUFF_MILESTONES:
        if guild.reputation >= rep:
            existing = db.query(GuildBuff).filter(
                GuildBuff.guild_id == guild.id, GuildBuff.buff_name == name
            ).first()
            if not existing:
                db.add(GuildBuff(
                    guild_id=guild.id, buff_name=name, buff_description=desc,
                    reputation_required=rep, is_unlocked=1, stat_bonus=bonus
                ))
                db.commit()

                # 모든 길드원에게 버프 적용
                members = db.query(GuildMember).filter(GuildMember.guild_id == guild.id).all()
                for m in members:
                    c = db.query(Character).filter(Character.id == m.character_id).first()
                    if c:
                        _apply_buff_to_character(c, bonus)

    db.commit()


def _apply_buff_to_character(c: Character, bonus: dict):
    """캐릭터에 길드 버프 영구 적용"""
    c.guild_buff_attack += bonus.get("attack", 0)
    c.guild_buff_defense += bonus.get("defense", 0)
    c.guild_buff_hp += bonus.get("max_hp", 0)
    c.guild_buff_mp += bonus.get("max_mp", 0)
    c.guild_buff_speed += bonus.get("speed", 0)
    c.guild_buff_crit += bonus.get("crit_rate", 0.0)

    c.attack += bonus.get("attack", 0)
    c.defense += bonus.get("defense", 0)
    c.max_hp += bonus.get("max_hp", 0)
    c.hp += bonus.get("max_hp", 0)
    c.max_mp += bonus.get("max_mp", 0)
    c.mp += bonus.get("max_mp", 0)
    c.speed += bonus.get("speed", 0)
    c.crit_rate += bonus.get("crit_rate", 0.0)


def _next_milestone(reputation: int) -> Optional[dict]:
    """다음 달성할 명성 마일스톤"""
    for rep, name, desc, bonus in GUILD_BUFF_MILESTONES:
        if rep > reputation:
            return {"reputation": rep, "name": name, "description": desc}
    return None
