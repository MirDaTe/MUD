"""
낙화검심 - 상점 시드
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Shop
import json

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Shop).count() > 0:
        print("Shops already seeded!"); db.close(); return
    shops = [
        {"id": 1, "name": "입문마을 무기점", "room_id": 6, "npc_id": 4,
         "item_ids": json.dumps([1,2,3,4,5,6,7,8,9,10,21,22,23,24,25,26,27,28,29,30]),
         "description": "검과 도, 각종 무기를 판매합니다."},
        {"id": 2, "name": "입문마을 약방", "room_id": 7, "npc_id": 5,
         "item_ids": json.dumps([31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]),
         "description": "영약과 해독제, 내공 회복약을 판매합니다."},
        {"id": 3, "name": "암시장 밀매상", "room_id": 19, "npc_id": 8,
         "item_ids": json.dumps([61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]),
         "description": "희귀 비급 조각과 금서를 암거래합니다."},
    ]
    for s in shops:
        db.add(Shop(**s))
    db.commit(); db.close()
    print(f"Seeded {len(shops)} shops!")

if __name__ == "__main__":
    seed()
