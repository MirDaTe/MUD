"""
낙화검심 - MVP 시드 데이터
실행: python seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models import User, Character, Room, NPC, Monster
from app.core.security import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 이미 데이터 있으면 스킵
    if db.query(Room).count() > 0:
        print("Already seeded!")
        db.close()
        return

    print("Seeding database...")

    # ── Rooms ──
    rooms = [
        Room(id=1, name="입문마을 - 장터", region="입문마을",
             description="석양빛이 비스듬히 내리쬐는 장터. 먼지 낀 포장마차 사이로 장사꾼들의 목소리가 오간다. 낡은 무기점 앞에는 녹슨 검이 담벼락에 기대어 있고, 대나무 통에서 나는 약초 향이 코끝을 스친다. 누군가 뒤에서 당신을 훔쳐보는 듯한 기분이 든다.",
             exits={"north": 2, "east": 3}),
        Room(id=2, name="입문마을 - 객잔", region="입문마을",
             description="'청풍루'라 쓰인 간판이 바람에 삐걱인다. 안에서는 술잔 부딪히는 소리와 무림인들의 담소가 흘러나온다. 구석 탁자에는 검은 두건을 쓴 사내가 홀로 술을 기울이고 있다. 주인장이 피곤한 눈으로 당신을 흘낏 본다.",
             exits={"south": 1}),
        Room(id=3, name="입문마을 - 대나무숲 입구", region="입문마을",
             description="대나무가 빽빽이 들어선 숲길. 바람 한 점 없는데 이파리들이 서걱인다. 흙길에는 말발굽 자국과 함께 핏자국 같은 검붉은 얼룩이 군데군데 말라붙어 있다. 숲 속에서 무엇인가 당신을 기다리고 있는 듯하다.",
             exits={"west": 1, "north": 4}),
        Room(id=4, name="청람산 - 산길", region="청람산",
             description="안개가 옅게 깔린 구불구불한 산길. 저 멀리 청람검문의 석문이 희미하게 보인다. 길옆 바위에는 검자국이 선명하고, 계곡에서 흘러내리는 물소리가 적막을 깨운다. 기척 하나 없는데도 당신의 손은 어느새 검자루에 닿아 있다.",
             exits={"south": 3, "up": 5}),
        Room(id=5, name="청람산 - 검문 입구", region="청람산",
             description="거대한 석문에 '청람검문(靑嵐劍門)' 네 글자가 웅장하게 새겨져 있다. 문지기 두 명이 날카로운 눈빛으로 방문객을 살피고 있다. 바람이 검은 소매를 스치자 풍경소리 같은 쇳소리가 산 전체에 울려 퍼진다. 이곳에 발을 들이는 순간, 평범한 삶과는 영원히 이별이다.",
             exits={"down": 4}),
    ]
    db.add_all(rooms)

    # ── NPCs ──
    npcs = [
        NPC(id=1, name="주점 주인", dialogue="[주인장] 어서 오시오. 방 하나와 술 한잔? 아니면... 정보가 필요하신가? 이 동네는 돈 되는 얘기가 많지.", is_hostile=False, occupation="주점주인/정보상", ambient_lines=["손님! 오늘의 특별주는 어떠신가?", "강호 소식이라면 나한테 물어봐."], quest_giver=True),
        NPC(id=2, name="청람문지기", dialogue="[문지기] 청람검문에 무슨 일이시오? 검을 배우러 왔다면 시험부터 치르시오. 사절이라면... 용건을 말씀하시지.", is_hostile=False, occupation="문지기", ambient_lines=["검문의 평화는 우리가 지킨다.", "수련은 고통, 하지만 열매는 달콤하지."], quest_giver=True),
        NPC(id=3, name="의문의검객", dialogue="[의문의 검객] ...자네, 낙화검결에 대해 뭔가 알고 있나? 모른다면 상관없네. 하지만 안다면... 조심하게. 귀화천의 눈은 어디에나 있으니.", is_hostile=False, occupation="검객/정보원", ambient_lines=["...", "*검만 매만지며 당신을 응시한다*"], quest_giver=True),
    ]
    db.add_all(npcs)
    db.flush()

    # ── Monsters ──
    monsters = [
        Monster(id=1, name="산적패잔병", max_hp=40, hp=40, attack=8, defense=3, speed=10, exp_reward=25, is_aggro=False, respawn_min=30, respawn_max=120,
                ambient_lines=["이 근방은 우리 구역이다!", "돈 내놔! 목숨은 덤!", "흐흐... 또 한 놈 걸렸군."],
                description="때가 꼬질꼬질한 산적. 손에 녹슨 식칼을 쥐고 험악한 표정이다.",
                attack_templates=["{name}(이)가 식칼을 휘두릅니다!", "{name}(이)가 욕설을 내뱉으며 달려듭니다!"],
                death_template="산적패잔병이 비명도 없이 풀썩 쓰러집니다."),
        Monster(id=2, name="검은이리", max_hp=30, hp=30, attack=12, defense=1, speed=14, exp_reward=30, is_aggro=True, respawn_min=20, respawn_max=80,
                ambient_lines=["크르릉...", "컹! 컹!", "낮은 으르렁거림이 들린다."],
                description="붉은 눈을 번뜩이는 거대한 이리. 낮게 으르렁거리며 이빨을 드러내고 있다.",
                attack_templates=["{name}가 날카로운 발톱으로 할큅니다!", "{name}가 빠르게 달려들어 물어뜯습니다!"],
                death_template="검은이리가 긴 울부짖음을 남기고 숨을 거둡니다."),
        Monster(id=3, name="의문의암살자", max_hp=60, hp=60, attack=15, defense=6, speed=12, exp_reward=80, is_aggro=True, respawn_min=60, respawn_max=180,
                ambient_lines=["...", "*그림자 속에 숨을 죽이고 있다*"],
                description="검은 밀복 차림. 얼굴은 복면으로 가려져 있다. 손에는 기름 먹인 단검이 빛난다.",
                attack_templates=["{name}가 그림자처럼 파고들어 단검을 찌릅니다!", "{name}가 어둠 속에서 표창을 날립니다!"],
                death_template="암살자가 '귀화천은... 반드시...' 중얼거리며 쓰러집니다."),
        Monster(id=4, name="청람훈련인형", max_hp=80, hp=80, attack=6, defense=8, speed=5, exp_reward=15, is_aggro=False, respawn_min=10, respawn_max=30,
                ambient_lines=["*딸깍딸깍*", "*기계적인 소음*"],
                description="청람검문의 수련용 목인형. 하지만 이건... 움직이고 있다!",
                attack_templates=["{name}가 둔탁한 주먹을 휘두릅니다!", "목인형이 기계적으로 팔을 뻗어 타격합니다!"],
                death_template="훈련인형이 산산조각나 바닥에 흩어집니다."),
        Monster(id=5, name="혈랑객", max_hp=70, hp=70, attack=14, defense=5, speed=11, exp_reward=100, is_aggro=True, respawn_min=60, respawn_max=180,
                ambient_lines=["피... 더 많은 피를...!", "하하하! 오늘도 즐거운 하루다!"],
                description="눈에 핏발이 선 흉악한 무인. 입가에는 비릿한 미소가 걸려 있다.",
                attack_templates=["{name}(이)가 광포한 기세로 검을 휘둘러 옵니다!", "{name}(이)가 악에 받친 목소리로 고함을 지르며 덤벼듭니다!", "혈랑객이 당신의 빈틈을 파고들어 급소를 노립니다!"],
                death_template="혈랑객이 분노에 찬 비명을 지르며 땅에 무릎 꿇습니다."),
    ]
    db.add_all(monsters)
    db.flush()

    # ── Assign NPCs and Monsters to Rooms ──
    room_npc_map = {2: [1], 5: [2], 1: [3]}
    room_mon_map = {3: [1, 2], 4: [4], 5: [5]}

    for room_id, npc_ids in room_npc_map.items():
        room = db.query(Room).filter(Room.id == room_id).first()
        room.npc_ids = npc_ids
    for room_id, mon_ids in room_mon_map.items():
        room = db.query(Room).filter(Room.id == room_id).first()
        room.monster_ids = mon_ids

    db.commit()
    db.close()
    print("Seed complete! 5 rooms, 3 NPCs, 5 monsters.")

if __name__ == "__main__":
    seed()
