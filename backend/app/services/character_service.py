"""캐릭터 서비스"""
from sqlalchemy.orm import Session
from ..models.character import Character
from ..schemas.character import CharacterCreate


def create_character(db: Session, user_id: int, data: CharacterCreate) -> Character:
    if db.query(Character).filter(Character.name == data.name).first():
        raise ValueError("이미 사용 중인 이름입니다.")
    base_hp = 80 + data.physique * 4
    base_mp = 30 + data.ki * 4
    char = Character(
        user_id=user_id, name=data.name, origin=data.origin,
        physique=data.physique, ki=data.ki, agility=data.agility,
        insight=data.insight, charm=data.charm, luck=data.luck,
        hp=base_hp, max_hp=base_hp, mp=base_mp, max_mp=base_mp,
        attack=8 + data.physique // 2, defense=3 + data.physique // 3,
        speed=8 + data.agility // 2
    )
    db.add(char)
    db.commit()
    db.refresh(char)
    return char


def get_characters(db: Session, user_id: int) -> list[Character]:
    return db.query(Character).filter(Character.user_id == user_id).all()
