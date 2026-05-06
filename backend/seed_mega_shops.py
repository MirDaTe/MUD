"""
낙화검심 MEGA 확장 - 상점 10곳 추가 (총 13곳)
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Shop

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Shop).filter(Shop.id == 4).count() > 0:
        print("Mega shops already seeded!"); db.close(); return

    shops = [
        Shop(id=4, name="황성 장비점", room_id=21, npc_id=41,
             item_ids=json.dumps([105,106,107,108,109,110,111,112,113,114,115,145,146,147,148,149,150]),
             description="황성 최고의 무기와 방어구"),
        Shop(id=5, name="만독림 약초상", room_id=23, npc_id=30,
             item_ids=json.dumps([175,176,177,178,179,180,181,182,183,184,215,216,217,218,219]),
             description="만독림에서 채취한 희귀 약재와 독약"),
        Shop(id=6, name="뇌전대장간", room_id=38, npc_id=26,
             item_ids=json.dumps([151,152,153,154,155,116,117,118,119,120]),
             description="뇌전석으로 만든 특별 강화석 판매"),
        Shop(id=7, name="빙궁 보물창고", room_id=41, npc_id=25,
             item_ids=json.dumps([175,176,177,255,256,257,258,259,260,261,262,263,264]),
             description="만년빙 속에 잠든 보물들"),
        Shop(id=8, name="암시장 비급밀매", room_id=18, npc_id=9,
             item_ids=json.dumps([255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274]),
             description="금지된 비급과 금서"),
        Shop(id=9, name="용문폭포 비전상", room_id=47, npc_id=66,
             item_ids=json.dumps([151,152,153,275,276,277,278,279,280,281,282,283]),
             description="용문비전과 특별 강화 아이템"),
        Shop(id=10, name="귀곡촌 잡화점", room_id=56, npc_id=37,
             item_ids=json.dumps([295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310]),
             description="귀곡촌의 생존자들이 모은 잡화"),
        Shop(id=11, name="봉황단애 성물점", room_id=59, npc_id=55,
             item_ids=json.dumps([151,152,153,235,236,237,238,239,311,312,313,314,315,316,317,318]),
             description="봉황의 축복이 깃든 성물들"),
        Shop(id=12, name="황금석 교환소", room_id=60, npc_id=42,
             item_ids=json.dumps([151,152,153,154,155,321,322,323,324,325,326,327,328,329,330]),
             description="강화석과 희귀석 교환 전문"),
        Shop(id=13, name="신비한 노파의 가게", room_id=50, npc_id=52,
             item_ids=json.dumps([151,152,153,154,155,331,332,333,334,335,336,337,338,339,340,341]),
             description="나타났다 사라지는 신비한 가게. 운이 좋아야 만날 수 있다."),
    ]

    for s in shops:
        db.add(s)
    db.commit(); db.close()
    print(f"Seeded {len(shops)} shops! (Total: 13)")

if __name__ == "__main__":
    seed()
