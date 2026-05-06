"""
낙화검심 - 문파/세력 10개 시드
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Faction
import json

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Faction).count() > 0:
        print("Factions already seeded!"); db.close(); return
    factions = [
        {"id": 1, "name": "청람검문", "faction_type": "정파",
         "description": "절제된 검식과 굳은 의지. 청람산에 본거지를 둔 정파의 대표 문파.",
         "benefits": json.dumps({"attack": 3, "defense": 5}), "join_requirements": json.dumps({"level": 3})},
        {"id": 2, "name": "운소궁", "faction_type": "정파",
         "description": "구름 위에 세워진 궁궐. 여성 고수들이 주류를 이루며 경공과 기공술에 능하다.",
         "benefits": json.dumps({"speed": 5, "mp": 20}), "join_requirements": json.dumps({"level": 5})},
        {"id": 3, "name": "백운서원", "faction_type": "정파",
         "description": "선비들의 무림. 무예보다 책략과 진법을 중시하는 지식의 전당.",
         "benefits": json.dumps({"insight": 3, "crit_rate": 0.03}), "join_requirements": json.dumps({"level": 3})},
        {"id": 4, "name": "혈하문", "faction_type": "사파",
         "description": "피의 강을 거슬러 올라온 살수 집단. 출혈과 흡혈, 광폭화를 중시한다.",
         "benefits": json.dumps({"attack": 8, "defense": -2}), "join_requirements": json.dumps({"level": 7})},
        {"id": 5, "name": "야명곡", "faction_type": "사파",
         "description": "어둠의 계곡. 독공과 암습, 환술에 능한 사파.",
         "benefits": json.dumps({"speed": 3, "attack": 4}), "join_requirements": json.dumps({"level": 9})},
        {"id": 6, "name": "흑련교", "faction_type": "마도",
         "description": "검은 연꽃을 숭배하는 마교. 내공을 오염시키는 사악한 무공을 사용한다.",
         "benefits": json.dumps({"mp": 30, "attack": 6}), "join_requirements": json.dumps({"level": 11})},
        {"id": 7, "name": "유성상단", "faction_type": "중립",
         "description": "강호 최대의 상업 조직. 은전만 충분하다면 못 구할 물건이 없다.",
         "benefits": json.dumps({"charm": 2, "luck": 2}), "join_requirements": json.dumps({"level": 1})},
        {"id": 8, "name": "무명각", "faction_type": "중립",
         "description": "이름 없는 자들의 길드. 암살, 정보 수집, 현상금 사냥.",
         "benefits": json.dumps({"attack": 5, "speed": 3}), "join_requirements": json.dumps({"level": 15})},
        {"id": 9, "name": "금풍표국", "faction_type": "중립",
         "description": "황금 바람의 깃발. 호위와 호송을 전문으로 하는 무인 집단.",
         "benefits": json.dumps({"defense": 6, "hp": 60}), "join_requirements": json.dumps({"level": 5})},
        {"id": 10, "name": "황영사", "faction_type": "특수",
         "description": "황실의 그림자. 공식적으로는 존재하지 않는 첩보 조직.",
         "benefits": json.dumps({"insight": 4, "speed": 2}), "join_requirements": json.dumps({"level": 20})},
    ]
    for f in factions:
        db.add(Faction(**f))
    db.commit(); db.close()
    print(f"Seeded {len(factions)} factions!")

if __name__ == "__main__":
    seed()
