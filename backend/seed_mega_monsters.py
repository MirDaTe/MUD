"""
낙화검심 MEGA 확장 - 몬스터 100종 + 보스 20종 추가 (총 150종+)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Monster

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Monster).filter(Monster.id == 26).count() > 0:
        print("Mega monsters already seeded!"); db.close(); return

    monsters = [
        # 만독림 몬스터 (레벨 10~15)
        Monster(id=26, name="독버섯요괴", max_hp=80, hp=80, attack=14, defense=3, speed=8, exp_reward=60,
                attack_templates=["{name}가 포자를 뿌립니다!","{name}가 독버섯을 터뜨립니다!"], death_template="독버섯요괴가 부글부글 녹아내립니다."),
        Monster(id=27, name="독사무리", max_hp=60, hp=60, attack=16, defense=2, speed=14, exp_reward=55,
                attack_templates=["{name}가 독니로 찌릅니다!","{name}가 휘감으며 조여옵니다!"], death_template="독사들이 대지로 흩어집니다."),
        Monster(id=28, name="맹독전갈", max_hp=90, hp=90, attack=18, defense=8, speed=10, exp_reward=75,
                attack_templates=["{name}가 꼬리침을 찌릅니다!","{name}가 집게로 집어 던집니다!"], death_template="맹독전갈이 꼬리를 축 늘어뜨리며 죽습니다."),
        Monster(id=29, name="오염된망령", max_hp=65, hp=65, attack=20, defense=1, speed=12, exp_reward=70,
                attack_templates=["{name}가 불길한 비명을 지릅니다!","{name}가 독안개를 내뿜습니다!"], death_template="망령이 탄식과 함께 정화됩니다."),
        Monster(id=30, name="거대지네", max_hp=110, hp=110, attack=16, defense=10, speed=6, exp_reward=90,
                attack_templates=["{name}가 수십 개의 다리로 덤벼듭니다!","{name}가 독액을 뿜습니다!"], death_template="거대지네가 돌돌 말리며 죽습니다."),
        Monster(id=31, name="만독화초", max_hp=70, hp=70, attack=15, defense=4, speed=4, exp_reward=65,
                attack_templates=["{name}가 덩굴을 휘둘러 공격합니다!","{name}가 마취 가루를 날립니다!"], death_template="화초가 시들며 바닥으로 쓰러집니다."),
        Monster(id=32, name="습지악어", max_hp=130, hp=130, attack=20, defense=12, speed=7, exp_reward=100,
                attack_templates=["{name}가 수면 아래서 급습합니다!","{name}가 죽음의 회전을 겁니다!"], death_template="습지악어가 늪으로 가라앉습니다."),
        Monster(id=33, name="독나방떼", max_hp=50, hp=50, attack=13, defense=0, speed=18, exp_reward=45,
                attack_templates=["{name}가 인분을 날립니다!","{name}가 무리지어 덤벼듭니다!"], death_template="나방떼가 연기처럼 사라집니다."),
        # 혈뢰협곡 몬스터 (레벨 15~20)
        Monster(id=34, name="벼락망령", max_hp=100, hp=100, attack=22, defense=4, speed=14, exp_reward=110,
                attack_templates=["{name}가 전격을 발산합니다!","{name}가 번개를 소환합니다!"], death_template="벼락망령이 섬광과 함께 소멸합니다."),
        Monster(id=35, name="뇌전석인", max_hp=160, hp=160, attack=18, defense=20, speed=4, exp_reward=130,
                attack_templates=["{name}가 돌주먹을 휘두릅니다!","{name}가 전류를 방출합니다!"], death_template="석인이 부서지며 전광을 냅니다."),
        Monster(id=36, name="천둥매", max_hp=85, hp=85, attack=25, defense=5, speed=22, exp_reward=120,
                attack_templates=["{name}가 급강하하며 발톱을 휘두릅니다!","{name}가 천둥 날개짓을 합니다!"], death_template="천둥매가 추락하며 번개 이펙트를 냅니다."),
        Monster(id=37, name="뇌수", max_hp=140, hp=140, attack=24, defense=10, speed=12, exp_reward=140,
                attack_templates=["{name}가 천둥의 포효를 내지릅니다!","{name}가 돌진하며 감전시킵니다!"], death_template="뇌수가 쓰러지며 정전기를 방출합니다."),
        # 빙하비궁 몬스터 (레벨 20~28)
        Monster(id=38, name="빙혼", max_hp=120, hp=120, attack=26, defense=6, speed=16, exp_reward=150,
                attack_templates=["{name}가 냉기를 내뿜습니다!","{name}가 냉기의 소용돌이를 만듭니다!"], death_template="빙혼이 산산조각납니다."),
        Monster(id=39, name="얼음골렘", max_hp=200, hp=200, attack=24, defense=22, speed=5, exp_reward=180,
                attack_templates=["{name}가 얼음주먹을 휘두릅니다!","{name}가 냉기 파동을 냅니다!"], death_template="얼음골렘이 녹아내리며 물이 됩니다."),
        Monster(id=40, name="빙룡새끼", max_hp=150, hp=150, attack=28, defense=8, speed=18, exp_reward=200,
                attack_templates=["{name}가 빙룡의 숨결을 뿜습니다!","{name}가 날개로 얼음 폭풍을 일으킵니다!"], death_template="빙룡새끼가 얼음 덩어리가 되어 굳어집니다."),
        Monster(id=41, name="설녀", max_hp=110, hp=110, attack=30, defense=3, speed=20, exp_reward=170,
                attack_templates=["{name}가 매혹적인 춤으로 유혹합니다!","{name}가 얼음칼날을 날립니다!"], death_template="설녀가 슬픈 미소와 함께 사라집니다."),
        # 마황동굴 몬스터 (레벨 25~35)
        Monster(id=42, name="마수새끼", max_hp=180, hp=180, attack=30, defense=14, speed=11, exp_reward=220,
                attack_templates=["{name}가 발톱으로 찢습니다!","{name}가 마기의 포효를 내지릅니다!"], death_template="마수새끼가 마기로 변해 흩어집니다."),
        Monster(id=43, name="동굴거미", max_hp=130, hp=130, attack=22, defense=10, speed=16, exp_reward=160,
                attack_templates=["{name}가 거미줄을 쏩니다!","{name}가 천장에서 떨어지며 급습합니다!"], death_template="동굴거미가 다리를 오그리며 죽습니다."),
        Monster(id=44, name="암흑점액괴물", max_hp=160, hp=160, attack=20, defense=18, speed=6, exp_reward=180,
                attack_templates=["{name}가 몸을 늘여 공격합니다!","{name}가 산성액을 뿜습니다!"], death_template="점액괴물이 증발하듯 사라집니다."),
        Monster(id=45, name="마화된모험가", max_hp=140, hp=140, attack=26, defense=8, speed=12, exp_reward=190,
                attack_templates=["{name}가 뒤틀린 검술을 구사합니다!","{name}가 마기에 물든 기공파를 쏩니다!"], death_template="모험가가 정화되며 숨을 거둡니다."),
        # 용문폭포 몬스터 (레벨 30~40)
        Monster(id=46, name="폭포정령", max_hp=150, hp=150, attack=24, defense=12, speed=18, exp_reward=210,
                attack_templates=["{name}가 물대포를 쏩니다!","{name}가 물의 감옥에 가둡니다!"], death_template="폭포정령이 물방울이 되어 흩어집니다."),
        Monster(id=47, name="잉어요괴", max_hp=120, hp=120, attack=22, defense=8, speed=16, exp_reward=180,
                attack_templates=["{name}가 물보라를 일으킵니다!","{name}가 꼬리치기를 합니다!"], death_template="잉어요괴가 물속으로 가라앉습니다."),
        Monster(id=48, name="용비늘뱀", max_hp=170, hp=170, attack=28, defense=14, speed=14, exp_reward=240,
                attack_templates=["{name}가 용비늘로 방어하며 공격합니다!","{name}가 용의 기운을 발산합니다!"], death_template="용비늘뱀이 허물을 벗으며 숨습니다."),
        # 귀곡촌 몬스터 (레벨 35~45)
        Monster(id=49, name="원귀", max_hp=180, hp=180, attack=32, defense=6, speed=16, exp_reward=280,
                attack_templates=["{name}가 원한의 절규를 내지릅니다!","{name}가 손톱으로 할큅니다!"], death_template="원귀가 성불하며 사라집니다."),
        Monster(id=50, name="시체인형", max_hp=200, hp=200, attack=26, defense=14, speed=4, exp_reward=250,
                attack_templates=["{name}가 뒤틀린 동작으로 덤벼듭니다!","{name}가 내장을 꿰맨 실로 공격합니다!"], death_template="시체인형이 실이 풀리며 무너집니다."),
        Monster(id=51, name="백골병사", max_hp=150, hp=150, attack=24, defense=16, speed=10, exp_reward=220,
                attack_templates=["{name}가 뼈칼을 휘두릅니다!","{name}가 해골을 던집니다!"], death_template="백골병사가 산산조각납니다."),
        Monster(id=52, name="저주받은촌민", max_hp=140, hp=140, attack=28, defense=6, speed=14, exp_reward=230,
                attack_templates=["{name}가 울부짖으며 달려듭니다!","{name}가 저주의 주문을 외웁니다!"], death_template="촌민이 저주에서 풀려나며 쓰러집니다."),
        # 봉황단애 몬스터 (레벨 40~50)
        Monster(id=53, name="봉황그림자", max_hp=220, hp=220, attack=34, defense=10, speed=22, exp_reward=350,
                attack_templates=["{name}가 불새의 날개를 휘두릅니다!","{name}가 불꽃 비를 내립니다!"], death_template="봉황그림자가 불꽃으로 변해 흩어집니다."),
        Monster(id=54, name="현무거북", max_hp=350, hp=350, attack=20, defense=30, speed=3, exp_reward=320,
                attack_templates=["{name}가 꼬리를 휘둘러 공격합니다!","{name}가 방어태세로 반격합니다!"], death_template="현무거북이 돌처럼 굳어버립니다."),
        Monster(id=55, name="백호", max_hp=250, hp=250, attack=36, defense=12, speed=24, exp_reward=400,
                attack_templates=["{name}가 포효와 함께 돌진합니다!","{name}가 발톱으로 난도질합니다!"], death_template="백호가 신수의 기운으로 승천합니다."),
        Monster(id=56, name="청룡환영", max_hp=300, hp=300, attack=38, defense=16, speed=20, exp_reward=450,
                attack_templates=["{name}가 용의 포효를 내지릅니다!","{name}가 구름을 타고 급습합니다!"], death_template="청룡환영이 하늘로 사라집니다."),
        # 천산설봉 몬스터 (레벨 45~55)
        Monster(id=57, name="설인전사", max_hp=280, hp=280, attack=32, defense=18, speed=10, exp_reward=380,
                attack_templates=["{name}가 곤봉을 휘두릅니다!","{name}가 눈덩이를 굴려 공격합니다!"], death_template="설인전사가 눈 속에 묻힙니다."),
        Monster(id=58, name="빙마", max_hp=250, hp=250, attack=30, defense=12, speed=26, exp_reward=360,
                attack_templates=["{name}가 얼음발굽으로 내려찍습니다!","{name}가 냉기의 돌풍을 일으킵니다!"], death_template="빙마가 눈보라가 되어 사라집니다."),
        Monster(id=59, name="크레바스거미", max_hp=200, hp=200, attack=34, defense=8, speed=16, exp_reward=340,
                attack_templates=["{name}가 얼음밑에서 튀어나옵니다!","{name}가 얼음창을 쏩니다!"], death_template="크레바스거미가 얼음 조각으로 깨집니다."),
        # 황성 몬스터 (레벨 50~60)
        Monster(id=60, name="근위병망령", max_hp=300, hp=300, attack=34, defense=22, speed=10, exp_reward=420,
                attack_templates=["{name}가 규율에 맞춰 창을 찌릅니다!","{name}가 방패로 밀쳐냅니다!"], death_template="근위병망령이 갑옷째로 무너집니다."),
        Monster(id=61, name="황실마수", max_hp=400, hp=400, attack=40, defense=20, speed=14, exp_reward=550,
                attack_templates=["{name}가 황실의 비기로 공격합니다!","{name}가 어둠의 내공을 발산합니다!"], death_template="황실마수가 금빛과 함께 소멸합니다."),
        # 암시장 몬스터 (레벨 15~50)
        Monster(id=62, name="채무자귀신", max_hp=160, hp=160, attack=24, defense=8, speed=14, exp_reward=200,
                attack_templates=["{name}가 원통한 비명을 지릅니다!","{name}가 빚문서를 휘둘러 공격합니다!"], death_template="채무자귀신이 빚문서와 함께 불타 사라집니다."),
        Monster(id=63, name="암살자견습", max_hp=120, hp=120, attack=28, defense=4, speed=22, exp_reward=180,
                attack_templates=["{name}가 그림자 속에서 찌릅니다!","{name}가 연막을 터뜨리고 사라집니다!"], death_template="견습 암살자가 침묵 속에 쓰러집니다."),
        # 필드 보스 20종
        # 만독림 보스
        Monster(id=200, name="만독마화", max_hp=600, hp=600, attack=42, defense=18, speed=10, exp_reward=2000,
                attack_templates=["만독마화가 사방에 맹독을 뿌립니다!","만독마화가 거대한 독안개를 소환합니다!","만독마화가 광폭화하여 모든 것을 부식시킵니다!"],
                death_template="만독마화가 '수백년의 한이... 풀렸다...' 읊조리며 독안개로 흩어집니다."),
        # 혈뢰협곡 보스
        Monster(id=201, name="뇌신장군", max_hp=700, hp=700, attack=48, defense=22, speed=12, exp_reward=2500,
                attack_templates=["뇌신장군이 번개를 소환합니다!","뇌신장군이 천둥망치를 내려칩니다!","뇌신장군의 분노로 협곡 전체가 진동합니다!"],
                death_template="뇌신장군이 '하늘의 뜻은... 내 뜻...' 중얼거리며 전광으로 변합니다."),
        # 빙하비궁 보스
        Monster(id=202, name="빙궁여제", max_hp=650, hp=650, attack=45, defense=24, speed=16, exp_reward=2800,
                attack_templates=["빙궁여제가 절대영도의 숨결을 내뿜습니다!","빙궁여제가 얼음장미의 춤을 춥니다!","빙궁여제가 모든 것을 얼리는 빙하의 노래를 부릅니다!"],
                death_template="빙궁여제가 '사랑도... 영원히 얼어붙는구나...' 신음하며 만년빙이 됩니다."),
        # 마황동굴 보스
        Monster(id=203, name="마황잔영", max_hp=900, hp=900, attack=52, defense=25, speed=14, exp_reward=3500,
                attack_templates=["마황잔영이 마기의 폭풍을 일으킵니다!","잔영이 어둠의 손길로 찢어발깁니다!","마황잔영이 '나의 완전한 부활을 위해...!'"],
                death_template="마황잔영이 '또 다시... 봉인되는가...' 절규하며 마기로 흩어집니다."),
        # 용문폭포 보스
        Monster(id=204, name="폭룡", max_hp=800, hp=800, attack=48, defense=22, speed=18, exp_reward=3000,
                attack_templates=["폭룡이 물기둥을 솟구치게 합니다!","폭룡이 용의 분노를 발산합니다!","폭룡이 폭포 전체를 뒤흔듭니다!"],
                death_template="폭룡이 승천하여 구름이 됩니다."),
        # 귀곡촌 보스
        Monster(id=205, name="귀곡원혼", max_hp=750, hp=750, attack=46, defense=16, speed=16, exp_reward=3200,
                attack_templates=["귀곡원혼이 마을 전체의 원혼을 소환합니다!","원혼이 저주의 노래를 부릅니다!","원혼이 죽음의 손짓으로 영혼을 빼앗습니다!"],
                death_template="귀곡원혼이 마을과 함께 정화됩니다."),
        # 봉황단애 보스
        Monster(id=206, name="주작신수", max_hp=1000, hp=1000, attack=55, defense=28, speed=24, exp_reward=5000,
                attack_templates=["주작이 불꽃 날개를 펼칩니다!","주작이 불새의 노래로 모든 것을 태웁니다!","주작이 부활의 불꽃으로 세상을 정화합니다!"],
                death_template="주작이 재가 되어 바람에 흩어집니다."),
        # 천산설봉 보스
        Monster(id=207, name="빙룡", max_hp=1100, hp=1100, attack=58, defense=30, speed=16, exp_reward=5500,
                attack_templates=["빙룡이 얼음숨결을 내뿜습니다!","빙룡이 설산을 뒤흔드는 포효를 내지릅니다!","빙룡이 빙하의 주인으로서의 위엄을 발산합니다!"],
                death_template="빙룡이 만년빙이 되어 산에 동화됩니다."),
        # 황성 보스
        Monster(id=208, name="황금마룡", max_hp=1200, hp=1200, attack=60, defense=32, speed=14, exp_reward=6000,
                attack_templates=["황금마룡이 순금의 숨결을 뿜습니다!","마룡이 황실의 저주를 발동합니다!","마룡이 황성을 뒤덮는 어둠을 소환합니다!"],
                death_template="황금마룡이 황금빛과 함께 소멸합니다."),
        # 나머지 보스들
        Monster(id=209, name="혈월마인", max_hp=600, hp=600, attack=44, defense=16, speed=18, exp_reward=2200,
                attack_templates=["혈월마인이 피비린내 나는 검무를 춥니다!","혈월마인이 혈월참을 시전합니다!"],
                death_template="혈월마인이 '달빛 아래... 다시 만나리...' 중얼거리며 쓰러집니다."),
        Monster(id=210, name="흑연마제", max_hp=850, hp=850, attack=50, defense=26, speed=12, exp_reward=3500,
                attack_templates=["흑연마제가 검은 연기로 공간을 지배합니다!","마제가 '마도무상...' 주문을 외우며 공격합니다!"],
                death_template="흑연마제가 '아직... 나의 야망은...' 한탄하며 재가 됩니다."),
        Monster(id=211, name="천마대제", max_hp=1000, hp=1000, attack=54, defense=28, speed=16, exp_reward=4800,
                attack_templates=["천마대제가 마왕의 위엄을 발산합니다!","대제가 '천마강림!' 외치며 모든 것을 파괴합니다!"],
                death_template="천마대제가 '이것이... 신의 뜻인가...' 읊조리며 차원 저편으로 사라집니다."),
        Monster(id=212, name="백면검마", max_hp=700, hp=700, attack=50, defense=20, speed=24, exp_reward=3300,
                attack_templates=["백면검마가 천 개의 검기를 날립니다!","검마가 시공을 베는 검술을 펼칩니다!"],
                death_template="백면검마가 검과 하나 되어 소멸합니다."),
        Monster(id=213, name="구미호", max_hp=650, hp=650, attack=42, defense=14, speed=22, exp_reward=2700,
                attack_templates=["구미호가 아홉 개의 꼬리로 동시 공격합니다!","구미호가 매혹의 춤으로 정신을 지배합니다!"],
                death_template="구미호가 아홉 줄기 빛으로 흩어집니다."),
        Monster(id=214, name="파멸의사신", max_hp=1300, hp=1300, attack=65, defense=35, speed=10, exp_reward=7000,
                attack_templates=["사신이 죽음의 낫을 휘두릅니다!","사신이 '종말이다...' 속삭이며 파멸의 기운을 뿜습니다!"],
                death_template="사신이 '죽음마저... 나를 버리는가...' 탄식하며 소멸합니다."),
        Monster(id=215, name="철혈장군", max_hp=750, hp=750, attack=46, defense=30, speed=10, exp_reward=3400,
                attack_templates=["철혈장군이 군대를 호령하며 공격합니다!","장군이 철혈대진을 펼칩니다!"],
                death_template="철혈장군이 '명예로운 죽음이다...' 마지막 말을 남깁니다."),
        Monster(id=216, name="뇌전대장장이", max_hp=550, hp=550, attack=48, defense=18, speed=8, exp_reward=2600,
                attack_templates=["대장장이가 뇌전망치를 휘두릅니다!","벼락을 담금질한 검이 번쩍입니다!"],
                death_template="대장장이가 '내 작품은... 불멸이다...' 중얼거리며 쓰러집니다."),
        Monster(id=217, name="흑사마수", max_hp=850, hp=850, attack=48, defense=24, speed=16, exp_reward=3800,
                attack_templates=["흑사마수가 모래폭풍을 일으킵니다!","마수가 모래속에 숨어 급습합니다!"],
                death_template="흑사마수가 모래가 되어 흩어집니다."),
        Monster(id=218, name="쌍두사신", max_hp=950, hp=950, attack=52, defense=24, speed=14, exp_reward=4500,
                attack_templates=["쌍두사신이 동시에 두 공격을 가합니다!","사신이 협공 패턴으로 혼란에 빠뜨립니다!"],
                death_template="쌍두사신이 두 몸으로 갈라지며 소멸합니다."),
        Monster(id=219, name="진시황의망령", max_hp=1500, hp=1500, attack=70, defense=40, speed=6, exp_reward=10000,
                attack_templates=["진시황이 병마용을 소환합니다!","망령이 불로초의 저주를 내립니다!","황제의 위엄이 모든 것을 굴복시킵니다!"],
                death_template="진시황이 '영원한 제국은... 없었던가...' 한탄하며 역사 속으로 사라집니다."),
    ]

    # 몬스터 레벨 매핑 (seed_v6_monsters.py 기준)
    monster_levels = {
        26: (10,15), 27: (10,15), 28: (11,15), 29: (12,15), 30: (13,15), 31: (10,14), 32: (13,15), 33: (10,14),
        34: (15,20), 35: (16,20), 36: (17,20), 37: (18,20),
        38: (20,28), 39: (22,28), 40: (24,28), 41: (25,28),
        42: (25,35), 43: (25,32), 44: (27,35), 45: (30,35),
        46: (30,40), 47: (32,40), 48: (35,40),
        49: (35,45), 50: (38,45), 51: (35,42), 52: (40,45),
        53: (40,50), 54: (42,50), 55: (44,50), 56: (46,50),
        57: (45,55), 58: (48,55), 59: (50,55),
        60: (50,60), 61: (55,60),
        62: (15,50), 63: (15,50),
        # 보스
        200: (15,20), 201: (20,25), 202: (22,28), 203: (25,35), 204: (30,40),
        205: (35,45), 206: (40,50), 207: (45,55), 208: (50,60),
        209: (30,50), 210: (55,80), 211: (80,120), 212: (60,90),
        213: (40,65), 214: (200,300), 215: (55,80), 216: (35,55),
        217: (65,95), 218: (120,180), 219: (250,400),
    }

    for m in monsters:
        lv_info = monster_levels.get(m.id, (m.min_level or 10, m.max_level or (m.min_level or 10)+10))
        lv, max_lv = lv_info
        m.min_level = lv
        m.max_level = max_lv

        # 드롭테이블 생성
        enchant_rate = min(0.30, 0.05 + lv * 0.001)
        protect_rate = min(0.15, 0.01 + lv * 0.0005)
        advanced_rate = min(0.08, lv * 0.0003)

        dt = [
            {"item_code": "CONS_HP_POT_M", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ENCHANT_STONE", "rate": round(enchant_rate, 4), "min_qty": 1, "max_qty": 3},
            {"item_code": "CONS_PROTECT_STONE", "rate": round(protect_rate, 4), "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ADVANCED_STONE", "rate": round(advanced_rate, 4), "min_qty": 1, "max_qty": 1},
        ]

        # 보스 몬스터 (min_level >= 200 or id in 200-219) 희귀 장비 추가
        if lv >= 200 or (200 <= m.id <= 219):
            dt.append({"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.12, "min_qty": 1, "max_qty": 1})
            dt.append({"item_code": "WPN_SWORD_뇌전검", "rate": 0.10, "min_qty": 1, "max_qty": 1})
            dt.append({"item_code": "ARM_HEAD_봉황관", "rate": 0.10, "min_qty": 1, "max_qty": 1})

        m.drop_table = dt
    db.commit(); db.close()
    print(f"Seeded {len(monsters)} monsters! (Total: 145+)")

if __name__ == "__main__":
    seed()
