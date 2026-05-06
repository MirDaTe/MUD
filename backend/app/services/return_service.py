"""귀환 서비스 — 귀환 지점 설정, 귀환서/마을귀환서 사용"""
from typing import Optional
from collections import deque

from sqlalchemy.orm import Session

from ..models.character import Character
from ..models.room import Room
from ..models.inventory import Inventory
from ..models.item import Item


def set_return_point(db: Session, char: Character, room_id: int) -> Optional[str]:
    """현재 방이 is_inn=True 여관이면 char.return_room_id에 저장. 아니면 오류."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return "존재하지 않는 방입니다."

    if not room.is_inn:
        return "이곳은 여관이 아닙니다. 귀환 지점은 여관에서만 지정할 수 있습니다."

    char.return_room_id = room_id
    db.commit()
    return None


def use_return_scroll(db: Session, char: Character) -> Optional[str]:
    """
    char.return_room_id가 설정되어 있으면 그 방으로 이동.
    소지품에서 '귀환서' (CONS_RETURN_SCROLL) 아이템 1개 소모. 없으면 오류.
    """
    if not char.return_room_id:
        return "귀환 지점이 지정되지 않았습니다. 먼저 여관에서 귀환 지점을 설정하세요."

    return_room = db.query(Room).filter(Room.id == char.return_room_id).first()
    if not return_room:
        return "지정된 귀환 지점이 더 이상 존재하지 않습니다."

    # 귀환서 아이템 조회
    scroll = db.query(Item).filter(Item.code == "CONS_RETURN_SCROLL").first()
    if not scroll:
        return "귀환서 아이템 정보를 찾을 수 없습니다."

    # 소지품에서 귀환서 찾기
    inv = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == scroll.id
    ).first()

    if not inv or inv.quantity < 1:
        return "귀환서가 없습니다. 귀환서를 구매하여 사용하세요."

    # 아이템 1개 소모
    inv.quantity -= 1
    if inv.quantity <= 0:
        db.delete(inv)

    char.current_room_id = char.return_room_id
    db.commit()
    return None


def use_town_scroll(db: Session, char: Character) -> Optional[str]:
    """
    가장 가까운 is_inn=True 방으로 이동. 마을귀환서 (CONS_TOWN_SCROLL) 소모.
    BFS로 가장 가까운 여관 탐색.
    """
    scroll = db.query(Item).filter(Item.code == "CONS_TOWN_SCROLL").first()
    if not scroll:
        return "마을귀환서 아이템 정보를 찾을 수 없습니다."

    # 소지품에서 마을귀환서 찾기
    inv = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == scroll.id
    ).first()

    if not inv or inv.quantity < 1:
        return "마을귀환서가 없습니다."

    current_room = db.query(Room).filter(Room.id == char.current_room_id).first()
    if not current_room:
        return "현재 방 정보를 찾을 수 없습니다."

    # BFS로 가장 가까운 is_inn=True 방 찾기
    target_room_id = _find_nearest_inn(db, current_room.id)
    if target_room_id is None:
        return "이동할 수 있는 여관이 없습니다."

    # 아이템 1개 소모
    inv.quantity -= 1
    if inv.quantity <= 0:
        db.delete(inv)

    char.current_room_id = target_room_id
    db.commit()
    return None


def _find_nearest_inn(db: Session, start_room_id: int) -> Optional[int]:
    """
    BFS로 시작 방에서 가장 가까운 is_inn=True 방을 찾아 room_id 반환.
    찾지 못하면 None 반환.
    """
    # 모든 방 정보를 한 번에 가져와서 메모리에서 BFS 수행
    all_rooms = db.query(Room).all()
    room_map: dict[int, Room] = {r.id: r for r in all_rooms}

    if start_room_id not in room_map:
        return None

    # 시작 방이 이미 여관이면 즉시 반환
    if room_map[start_room_id].is_inn:
        return start_room_id

    visited = {start_room_id}
    queue = deque([start_room_id])

    while queue:
        current_id = queue.popleft()
        current = room_map[current_id]
        exits = current.exits or {}

        for direction, neighbor_id in exits.items():
            if neighbor_id is None:
                continue
            if neighbor_id in visited:
                continue
            if neighbor_id not in room_map:
                continue

            if room_map[neighbor_id].is_inn:
                return neighbor_id

            visited.add(neighbor_id)
            queue.append(neighbor_id)

    return None
