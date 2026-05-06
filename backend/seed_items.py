"""
낙화검심 - 아이템 100종 시드
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Item

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Item).count() > 0:
        print("Items already seeded!"); db.close(); return
    items = [
  {
    "id": 1,
    "name": "청람철검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "청람철검 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 2,
    "name": "벽력검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "벽력검 — 등급: 3",
    "stats": {
      "attack": 14,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 3
  },
  {
    "id": 3,
    "name": "잔영단검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "잔영단검 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -2
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 4,
    "name": "칠성보검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "칠성보검 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 5,
    "name": "한빙검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "한빙검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 6,
    "name": "수라도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "수라도 — 등급: 3",
    "stats": {
      "attack": 14,
      "speed": -2
    },
    "effects": {},
    "price": 50,
    "rarity": 3
  },
  {
    "id": 7,
    "name": "파천도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "파천도 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -2
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 8,
    "name": "월하도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "월하도 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 9,
    "name": "대검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "대검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": -5
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 10,
    "name": "일섬검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "일섬검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 11,
    "name": "무영단검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "무영단검 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 12,
    "name": "청룡도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "청룡도 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 13,
    "name": "백호검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "백호검 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 14,
    "name": "주작검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "주작검 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 15,
    "name": "현무도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "현무도 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 16,
    "name": "은사검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "은사검 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -2
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 17,
    "name": "용린검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "용린검 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 18,
    "name": "봉황도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "봉황도 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 19,
    "name": "파멸대검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "파멸대검 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -3
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 20,
    "name": "비천도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "비천도 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -4
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 21,
    "name": "뇌검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "뇌검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 22,
    "name": "백련검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "백련검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": -2
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 23,
    "name": "흑월도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "흑월도 — 등급: 4",
    "stats": {
      "attack": 17,
      "speed": -3
    },
    "effects": {},
    "price": 50,
    "rarity": 4
  },
  {
    "id": 24,
    "name": "절영검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "절영검 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 25,
    "name": "통천검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "통천검 — 등급: 3",
    "stats": {
      "attack": 14,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 3
  },
  {
    "id": 26,
    "name": "만파도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "만파도 — 등급: 1",
    "stats": {
      "attack": 8,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 1
  },
  {
    "id": 27,
    "name": "대라도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "대라도 — 등급: 3",
    "stats": {
      "attack": 14,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 3
  },
  {
    "id": 28,
    "name": "옥녀검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "옥녀검 — 등급: 5",
    "stats": {
      "attack": 20,
      "speed": -4
    },
    "effects": {},
    "price": 50,
    "rarity": 5
  },
  {
    "id": 29,
    "name": "쇄혼검",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "쇄혼검 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": 0
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 30,
    "name": "광살도",
    "item_type": "weapon",
    "sub_type": "검",
    "description": "광살도 — 등급: 2",
    "stats": {
      "attack": 11,
      "speed": -1
    },
    "effects": {},
    "price": 50,
    "rarity": 2
  },
  {
    "id": 31,
    "name": "청람도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "청람도포 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 32,
    "name": "금사도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "금사도포 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 33,
    "name": "은린갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "은린갑 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 34,
    "name": "흑월포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "흑월포 — 등급: 5",
    "stats": {
      "defense": 13,
      "hp": 50
    },
    "effects": {},
    "price": 40,
    "rarity": 5
  },
  {
    "id": 35,
    "name": "백학도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "백학도포 — 등급: 4",
    "stats": {
      "defense": 11,
      "hp": 40
    },
    "effects": {},
    "price": 40,
    "rarity": 4
  },
  {
    "id": 36,
    "name": "철포삼",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "철포삼 — 등급: 2",
    "stats": {
      "defense": 7,
      "hp": 20
    },
    "effects": {},
    "price": 40,
    "rarity": 2
  },
  {
    "id": 37,
    "name": "금강연갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "금강연갑 — 등급: 4",
    "stats": {
      "defense": 11,
      "hp": 40
    },
    "effects": {},
    "price": 40,
    "rarity": 4
  },
  {
    "id": 38,
    "name": "벽력갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "벽력갑 — 등급: 1",
    "stats": {
      "defense": 5,
      "hp": 10
    },
    "effects": {},
    "price": 40,
    "rarity": 1
  },
  {
    "id": 39,
    "name": "현무갑주",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "현무갑주 — 등급: 4",
    "stats": {
      "defense": 11,
      "hp": 40
    },
    "effects": {},
    "price": 40,
    "rarity": 4
  },
  {
    "id": 40,
    "name": "칠성도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "칠성도포 — 등급: 1",
    "stats": {
      "defense": 5,
      "hp": 10
    },
    "effects": {},
    "price": 40,
    "rarity": 1
  },
  {
    "id": 41,
    "name": "혈마포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "혈마포 — 등급: 2",
    "stats": {
      "defense": 7,
      "hp": 20
    },
    "effects": {},
    "price": 40,
    "rarity": 2
  },
  {
    "id": 42,
    "name": "비연포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "비연포 — 등급: 4",
    "stats": {
      "defense": 11,
      "hp": 40
    },
    "effects": {},
    "price": 40,
    "rarity": 4
  },
  {
    "id": 43,
    "name": "백운갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "백운갑 — 등급: 5",
    "stats": {
      "defense": 13,
      "hp": 50
    },
    "effects": {},
    "price": 40,
    "rarity": 5
  },
  {
    "id": 44,
    "name": "청운도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "청운도포 — 등급: 4",
    "stats": {
      "defense": 11,
      "hp": 40
    },
    "effects": {},
    "price": 40,
    "rarity": 4
  },
  {
    "id": 45,
    "name": "자하도포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "자하도포 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 46,
    "name": "대라금갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "대라금갑 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 47,
    "name": "와룡갑",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "와룡갑 — 등급: 2",
    "stats": {
      "defense": 7,
      "hp": 20
    },
    "effects": {},
    "price": 40,
    "rarity": 2
  },
  {
    "id": 48,
    "name": "봉황포",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "봉황포 — 등급: 3",
    "stats": {
      "defense": 9,
      "hp": 30
    },
    "effects": {},
    "price": 40,
    "rarity": 3
  },
  {
    "id": 49,
    "name": "파멸갑주",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "파멸갑주 — 등급: 1",
    "stats": {
      "defense": 5,
      "hp": 10
    },
    "effects": {},
    "price": 40,
    "rarity": 1
  },
  {
    "id": 50,
    "name": "옥녀단의",
    "item_type": "armor",
    "sub_type": "도포",
    "description": "옥녀단의 — 등급: 1",
    "stats": {
      "defense": 5,
      "hp": 10
    },
    "effects": {},
    "price": 40,
    "rarity": 1
  },
  {
    "id": 51,
    "name": "소회춘단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "소회춘단 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 52,
    "name": "대회춘단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "대회춘단 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 53,
    "name": "금창약",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "금창약 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 54,
    "name": "천년하수오",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "천년하수오 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 55,
    "name": "만년설삼",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "만년설삼 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 56,
    "name": "영약",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "영약 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 57,
    "name": "구명환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "구명환 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 58,
    "name": "구화옥로환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "구화옥로환 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 59,
    "name": "벽력단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "벽력단 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 60,
    "name": "천향옥로",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "천향옥로 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 61,
    "name": "해독환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "해독환 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 62,
    "name": "통맥환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "통맥환 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 63,
    "name": "증원단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "증원단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 64,
    "name": "빙심단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "빙심단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 65,
    "name": "소환단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "소환단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 66,
    "name": "주사약",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "주사약 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 67,
    "name": "백년인삼",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "백년인삼 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 68,
    "name": "녹삼보환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "녹삼보환 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 69,
    "name": "환골단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "환골단 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 70,
    "name": "탈태환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "탈태환 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 71,
    "name": "내공환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "내공환 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 72,
    "name": "칠보환",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "칠보환 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 73,
    "name": "옥로봉밀",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "옥로봉밀 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 74,
    "name": "혈삼",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "혈삼 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 75,
    "name": "기사회춘단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "기사회춘단 — 등급: 3",
    "stats": {},
    "effects": {
      "heal_amount": 65
    },
    "price": 34,
    "rarity": 3
  },
  {
    "id": 76,
    "name": "구전단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "구전단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 77,
    "name": "소림대환단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "소림대환단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 78,
    "name": "자하증원단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "자하증원단 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 79,
    "name": "흑옥단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "흑옥단 — 등급: 1",
    "stats": {},
    "effects": {
      "heal_amount": 35
    },
    "price": 18,
    "rarity": 1
  },
  {
    "id": 80,
    "name": "백옥단",
    "item_type": "consumable",
    "sub_type": "약",
    "description": "백옥단 — 등급: 2",
    "stats": {},
    "effects": {
      "heal_amount": 50
    },
    "price": 26,
    "rarity": 2
  },
  {
    "id": 81,
    "name": "낙화검결잔장1",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장1 — 등급: 3",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 3
  },
  {
    "id": 82,
    "name": "낙화검결잔장2",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장2 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 83,
    "name": "낙화검결잔장3",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장3 — 등급: 3",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 3
  },
  {
    "id": 84,
    "name": "낙화검결잔장4",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장4 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  },
  {
    "id": 85,
    "name": "낙화검결잔장5",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장5 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 86,
    "name": "낙화검결잔장6",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장6 — 등급: 3",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 3
  },
  {
    "id": 87,
    "name": "낙화검결잔장7",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "낙화검결잔장7 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 88,
    "name": "청람비전",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "청람비전 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  },
  {
    "id": 89,
    "name": "천잠고보",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "천잠고보 — 등급: 3",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 3
  },
  {
    "id": 90,
    "name": "월하검보",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "월하검보 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 91,
    "name": "구음진경잔본",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "구음진경잔본 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  },
  {
    "id": 92,
    "name": "구양신공잔본",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "구양신공잔본 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 93,
    "name": "태현경잔본",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "태현경잔본 — 등급: 3",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 3
  },
  {
    "id": 94,
    "name": "북명신공잔본",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "북명신공잔본 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 95,
    "name": "건곤대나이잔본",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "건곤대나이잔본 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 96,
    "name": "귀화천밀서",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "귀화천밀서 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 97,
    "name": "황실금인",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "황실금인 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  },
  {
    "id": 98,
    "name": "혈하문주령",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "혈하문주령 — 등급: 1",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 1
  },
  {
    "id": 99,
    "name": "흑련교인장",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "흑련교인장 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  },
  {
    "id": 100,
    "name": "운소궁신물",
    "item_type": "rare",
    "sub_type": "보물",
    "description": "운소궁신물 — 등급: 2",
    "stats": {},
    "effects": {},
    "price": 500,
    "rarity": 2
  }
]
    for i in items:
        db.add(Item(**i))
    db.commit(); db.close()
    print(f"Seeded {len(items)} items!")

if __name__ == "__main__":
    seed()
