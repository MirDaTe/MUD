"""
낙화검심 v0.6 - 몬스터 100종 (기존 50종 갱신 + 신규 50종)
지역: 황룡산맥, 폭풍해안, 마도의탑, 천공성, 명계의문, 신마대륙, 혼돈의틈새
레벨 10 ~ 999 분포
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Monster
import json

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    monsters = []

    # ======================== 기존 몬스터 50종 (drop_table, min/max_level 추가) ========================

    # 만독림 몬스터 (레벨 10~15)
    monsters.append(Monster(id=26, name="독버섯요괴", max_hp=80, hp=80, attack=14, defense=3, speed=8, exp_reward=60,
        min_level=10, max_level=15,
        drop_table=[
            {"item_code": "CONS_HP_POT_S", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ANTIDOTE", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_비수", "rate": 0.03, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 포자를 뿌립니다!","{name}가 독버섯을 터뜨립니다!"],
        death_template="독버섯요괴가 부글부글 녹아내립니다."))

    monsters.append(Monster(id=27, name="독사무리", max_hp=60, hp=60, attack=16, defense=2, speed=14, exp_reward=55,
        min_level=10, max_level=15,
        drop_table=[
            {"item_code": "CONS_HP_POT_S", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ANTIDOTE", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HANDS_가죽장갑", "rate": 0.03, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 독니로 찌릅니다!","{name}가 휘감으며 조여옵니다!"],
        death_template="독사들이 대지로 흩어집니다."))

    monsters.append(Monster(id=28, name="맹독전갈", max_hp=90, hp=90, attack=18, defense=8, speed=10, exp_reward=75,
        min_level=11, max_level=15,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "CONS_ANTIDOTE", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_독비수", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 꼬리침을 찌릅니다!","{name}가 집게로 집어 던집니다!"],
        death_template="맹독전갈이 꼬리를 축 늘어뜨리며 죽습니다."))

    monsters.append(Monster(id=29, name="오염된망령", max_hp=65, hp=65, attack=20, defense=1, speed=12, exp_reward=70,
        min_level=12, max_level=15,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "CONS_RETURN_SCROLL", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_철검", "rate": 0.03, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 불길한 비명을 지릅니다!","{name}가 독안개를 내뿜습니다!"],
        death_template="망령이 탄식과 함께 정화됩니다."))

    monsters.append(Monster(id=30, name="거대지네", max_hp=110, hp=110, attack=16, defense=10, speed=6, exp_reward=90,
        min_level=13, max_level=15,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_철창", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_철갑옷", "rate": 0.03, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 수십 개의 다리로 덤벼듭니다!","{name}가 독액을 뿜습니다!"],
        death_template="거대지네가 돌돌 말리며 죽습니다."))

    monsters.append(Monster(id=31, name="만독화초", max_hp=70, hp=70, attack=15, defense=4, speed=4, exp_reward=65,
        min_level=10, max_level=14,
        drop_table=[
            {"item_code": "CONS_HP_POT_S", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ANTIDOTE", "rate": 0.10, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 덩굴을 휘둘러 공격합니다!","{name}가 마취 가루를 날립니다!"],
        death_template="화초가 시들며 바닥으로 쓰러집니다."))

    monsters.append(Monster(id=32, name="습지악어", max_hp=130, hp=130, attack=20, defense=12, speed=7, exp_reward=100,
        min_level=13, max_level=15,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_곡도", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_철각반", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 수면 아래서 급습합니다!","{name}가 죽음의 회전을 겁니다!"],
        death_template="습지악어가 늪으로 가라앉습니다."))

    monsters.append(Monster(id=33, name="독나방떼", max_hp=50, hp=50, attack=13, defense=0, speed=18, exp_reward=45,
        min_level=10, max_level=14,
        drop_table=[
            {"item_code": "CONS_HP_POT_S", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_BANDAGE", "rate": 0.12, "min_qty": 1, "max_qty": 2},
        ],
        attack_templates=["{name}가 인분을 날립니다!","{name}가 무리지어 덤벼듭니다!"],
        death_template="나방떼가 연기처럼 사라집니다."))

    # 혈뢰협곡 몬스터 (레벨 15~20)
    monsters.append(Monster(id=34, name="벼락망령", max_hp=100, hp=100, attack=22, defense=4, speed=14, exp_reward=110,
        min_level=15, max_level=20,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_강철검", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_철투구", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 전격을 발산합니다!","{name}가 번개를 소환합니다!"],
        death_template="벼락망령이 섬광과 함께 소멸합니다."))

    monsters.append(Monster(id=35, name="뇌전석인", max_hp=160, hp=160, attack=18, defense=20, speed=4, exp_reward=130,
        min_level=16, max_level=20,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_MACE_철퇴", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_강철갑옷", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 돌주먹을 휘두릅니다!","{name}가 전류를 방출합니다!"],
        death_template="석인이 부서지며 전광을 냅니다."))

    monsters.append(Monster(id=36, name="천둥매", max_hp=85, hp=85, attack=25, defense=5, speed=22, exp_reward=120,
        min_level=17, max_level=20,
        drop_table=[
            {"item_code": "CONS_SPD_BUFF", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_독비수", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_가죽신발", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 급강하하며 발톱을 휘두릅니다!","{name}가 천둥 날개짓을 합니다!"],
        death_template="천둥매가 추락하며 번개 이펙트를 냅니다."))

    monsters.append(Monster(id=37, name="뇌수", max_hp=140, hp=140, attack=24, defense=10, speed=12, exp_reward=140,
        min_level=18, max_level=20,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_뇌정창", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_철갑옷", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 천둥의 포효를 내지릅니다!","{name}가 돌진하며 감전시킵니다!"],
        death_template="뇌수가 쓰러지며 정전기를 방출합니다."))

    # 빙하비궁 몬스터 (레벨 20~28)
    monsters.append(Monster(id=38, name="빙혼", max_hp=120, hp=120, attack=26, defense=6, speed=16, exp_reward=150,
        min_level=20, max_level=28,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_청룡검", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_강철투구", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 냉기를 내뿜습니다!","{name}가 냉기의 소용돌이를 만듭니다!"],
        death_template="빙혼이 산산조각납니다."))

    monsters.append(Monster(id=39, name="얼음골렘", max_hp=200, hp=200, attack=24, defense=22, speed=5, exp_reward=180,
        min_level=22, max_level=28,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_MACE_강철퇴", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_용비늘갑", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 얼음주먹을 휘두릅니다!","{name}가 냉기 파동을 냅니다!"],
        death_template="얼음골렘이 녹아내리며 물이 됩니다."))

    monsters.append(Monster(id=40, name="빙룡새끼", max_hp=150, hp=150, attack=28, defense=8, speed=18, exp_reward=200,
        min_level=24, max_level=28,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_벽력검", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_혈마갑", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 빙룡의 숨결을 뿜습니다!","{name}가 날개로 얼음 폭풍을 일으킵니다!"],
        death_template="빙룡새끼가 얼음 덩어리가 되어 굳어집니다."))

    monsters.append(Monster(id=41, name="설녀", max_hp=110, hp=110, attack=30, defense=3, speed=20, exp_reward=170,
        min_level=25, max_level=28,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_마검", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_용뿔투구", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 매혹적인 춤으로 유혹합니다!","{name}가 얼음칼날을 날립니다!"],
        death_template="설녀가 슬픈 미소와 함께 사라집니다."))

    # 마황동굴 몬스터 (레벨 25~35)
    monsters.append(Monster(id=42, name="마수새끼", max_hp=180, hp=180, attack=30, defense=14, speed=11, exp_reward=220,
        min_level=25, max_level=35,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_참마도", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_강철각반", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 발톱으로 찢습니다!","{name}가 마기의 포효를 내지릅니다!"],
        death_template="마수새끼가 마기로 변해 흩어집니다."))

    monsters.append(Monster(id=43, name="동굴거미", max_hp=130, hp=130, attack=22, defense=10, speed=16, exp_reward=160,
        min_level=25, max_level=32,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_ANTIDOTE", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_암살검", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 거미줄을 쏩니다!","{name}가 천장에서 떨어지며 급습합니다!"],
        death_template="동굴거미가 다리를 오그리며 죽습니다."))

    monsters.append(Monster(id=44, name="암흑점액괴물", max_hp=160, hp=160, attack=20, defense=18, speed=6, exp_reward=180,
        min_level=27, max_level=35,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_MACE_벽력퇴", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_마계갑옷", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 몸을 늘여 공격합니다!","{name}가 산성액을 뿜습니다!"],
        death_template="점액괴물이 증발하듯 사라집니다."))

    monsters.append(Monster(id=45, name="마화된모험가", max_hp=140, hp=140, attack=26, defense=8, speed=12, exp_reward=190,
        min_level=30, max_level=35,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_벽력검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_마수투구", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 뒤틀린 검술을 구사합니다!","{name}가 마기에 물든 기공파를 쏩니다!"],
        death_template="모험가가 정화되며 숨을 거둡니다."))

    # 용문폭포 몬스터 (레벨 30~40)
    monsters.append(Monster(id=46, name="폭포정령", max_hp=150, hp=150, attack=24, defense=12, speed=18, exp_reward=210,
        min_level=30, max_level=40,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.15, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_청룡창", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_마수각반", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 물대포를 쏩니다!","{name}가 물의 감옥에 가둡니다!"],
        death_template="폭포정령이 물방울이 되어 흩어집니다."))

    monsters.append(Monster(id=47, name="잉어요괴", max_hp=120, hp=120, attack=22, defense=8, speed=16, exp_reward=180,
        min_level=32, max_level=40,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_성검", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_철신발", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 물보라를 일으킵니다!","{name}가 꼬리치기를 합니다!"],
        death_template="잉어요괴가 물속으로 가라앉습니다."))

    monsters.append(Monster(id=48, name="용비늘뱀", max_hp=170, hp=170, attack=28, defense=14, speed=14, exp_reward=240,
        min_level=35, max_level=40,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_혈월도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_천신갑", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 용비늘로 방어하며 공격합니다!","{name}가 용의 기운을 발산합니다!"],
        death_template="용비늘뱀이 허물을 벗으며 숨습니다."))

    # 귀곡촌 몬스터 (레벨 35~45)
    monsters.append(Monster(id=49, name="원귀", max_hp=180, hp=180, attack=32, defense=6, speed=16, exp_reward=280,
        min_level=35, max_level=45,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_용살검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_왕관", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 원한의 절규를 내지릅니다!","{name}가 손톱으로 할큅니다!"],
        death_template="원귀가 성불하며 사라집니다."))

    monsters.append(Monster(id=50, name="시체인형", max_hp=200, hp=200, attack=26, defense=14, speed=4, exp_reward=250,
        min_level=38, max_level=45,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_MACE_벽력퇴", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_마계갑옷", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 뒤틀린 동작으로 덤벼듭니다!","{name}가 내장을 꿰맨 실로 공격합니다!"],
        death_template="시체인형이 실이 풀리며 무너집니다."))

    monsters.append(Monster(id=51, name="백골병사", max_hp=150, hp=150, attack=24, defense=16, speed=10, exp_reward=220,
        min_level=35, max_level=42,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_혈극창", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_강철투구", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 뼈칼을 휘두릅니다!","{name}가 해골을 던집니다!"],
        death_template="백골병사가 산산조각납니다."))

    monsters.append(Monster(id=52, name="저주받은촌민", max_hp=140, hp=140, attack=28, defense=6, speed=14, exp_reward=230,
        min_level=40, max_level=45,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.08, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_암살검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_비룡각반", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 울부짖으며 달려듭니다!","{name}가 저주의 주문을 외웁니다!"],
        death_template="촌민이 저주에서 풀려나며 쓰러집니다."))

    # 봉황단애 몬스터 (레벨 40~50)
    monsters.append(Monster(id=53, name="봉황그림자", max_hp=220, hp=220, attack=34, defense=10, speed=22, exp_reward=350,
        min_level=40, max_level=50,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_신검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_성기사갑옷", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 불새의 날개를 휘두릅니다!","{name}가 불꽃 비를 내립니다!"],
        death_template="봉황그림자가 불꽃으로 변해 흩어집니다."))

    monsters.append(Monster(id=54, name="현무거북", max_hp=350, hp=350, attack=20, defense=30, speed=3, exp_reward=320,
        min_level=42, max_level=50,
        drop_table=[
            {"item_code": "CONS_DEF_BUFF", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_산붕괴", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_어둠의갑주", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 꼬리를 휘둘러 공격합니다!","{name}가 방어태세로 반격합니다!"],
        death_template="현무거북이 돌처럼 굳어버립니다."))

    monsters.append(Monster(id=55, name="백호", max_hp=250, hp=250, attack=36, defense=12, speed=24, exp_reward=400,
        min_level=44, max_level=50,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_BLADE_비황도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_성스러운관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 포효와 함께 돌진합니다!","{name}가 발톱으로 난도질합니다!"],
        death_template="백호가 신수의 기운으로 승천합니다."))

    monsters.append(Monster(id=56, name="청룡환영", max_hp=300, hp=300, attack=38, defense=16, speed=20, exp_reward=450,
        min_level=46, max_level=50,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_멸룡창", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_마수의발톱", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 용의 포효를 내지릅니다!","{name}가 구름을 타고 급습합니다!"],
        death_template="청룡환영이 하늘로 사라집니다."))

    # 천산설봉 몬스터 (레벨 45~55)
    monsters.append(Monster(id=57, name="설인전사", max_hp=280, hp=280, attack=32, defense=18, speed=10, exp_reward=380,
        min_level=45, max_level=55,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_MACE_산붕괴", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_비룡각반", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 곤봉을 휘두릅니다!","{name}가 눈덩이를 굴려 공격합니다!"],
        death_template="설인전사가 눈 속에 묻힙니다."))

    monsters.append(Monster(id=58, name="빙마", max_hp=250, hp=250, attack=30, defense=12, speed=26, exp_reward=360,
        min_level=48, max_level=55,
        drop_table=[
            {"item_code": "CONS_SPD_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_혼돈검", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_비룡신발", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 얼음발굽으로 내려찍습니다!","{name}가 냉기의 돌풍을 일으킵니다!"],
        death_template="빙마가 눈보라가 되어 사라집니다."))

    monsters.append(Monster(id=59, name="크레바스거미", max_hp=200, hp=200, attack=34, defense=8, speed=16, exp_reward=340,
        min_level=50, max_level=55,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_그림자검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_암흑투구", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 얼음밑에서 튀어나옵니다!","{name}가 얼음창을 쏩니다!"],
        death_template="크레바스거미가 얼음 조각으로 깨집니다."))

    # 황성 몬스터 (레벨 50~60)
    monsters.append(Monster(id=60, name="근위병망령", max_hp=300, hp=300, attack=34, defense=22, speed=10, exp_reward=420,
        min_level=50, max_level=60,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_파멸창", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_성기사갑옷", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 규율에 맞춰 창을 찌릅니다!","{name}가 방패로 밀쳐냅니다!"],
        death_template="근위병망령이 갑옷째로 무너집니다."))

    monsters.append(Monster(id=61, name="황실마수", max_hp=400, hp=400, attack=40, defense=20, speed=14, exp_reward=550,
        min_level=55, max_level=60,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_폭풍검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_정령왕관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 황실의 비기로 공격합니다!","{name}가 어둠의 내공을 발산합니다!"],
        death_template="황실마수가 금빛과 함께 소멸합니다."))

    # 암시장 몬스터 (레벨 15~50)
    monsters.append(Monster(id=62, name="채무자귀신", max_hp=160, hp=160, attack=24, defense=8, speed=14, exp_reward=200,
        min_level=15, max_level=50,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "CONS_RETURN_SCROLL", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_비수", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 원통한 비명을 지릅니다!","{name}가 빚문서를 휘둘러 공격합니다!"],
        death_template="채무자귀신이 빚문서와 함께 불타 사라집니다."))

    monsters.append(Monster(id=63, name="암살자견습", max_hp=120, hp=120, attack=28, defense=4, speed=22, exp_reward=180,
        min_level=15, max_level=50,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_독비수", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_철신발", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 그림자 속에서 찌릅니다!","{name}가 연막을 터뜨리고 사라집니다!"],
        death_template="견습 암살자가 침묵 속에 쓰러집니다."))

    # ======================== 신규 몬스터 50종 (v0.6 지역) ========================

    # ── 황룡산맥 몬스터 (레벨 10~25) ──
    monsters.append(Monster(id=64, name="산적패거리", max_hp=100, hp=100, attack=16, defense=6, speed=10, exp_reward=80, gold_reward=15,
        min_level=10, max_level=18,
        drop_table=[
            {"item_code": "CONS_HP_POT_S", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_곡도", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 패거리를 이끌고 덤벼듭니다!","{name}가 협공을 시도합니다!"],
        death_template="산적패거리가 도망치듯 흩어집니다."))

    monsters.append(Monster(id=65, name="황룡산호랑이", max_hp=140, hp=140, attack=22, defense=8, speed=16, exp_reward=130, gold_reward=25,
        min_level=12, max_level=22,
        drop_table=[
            {"item_code": "CONS_HP_POT_M", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "ARM_HEAD_철투구", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_청룡검", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 포효하며 덤벼듭니다!","{name}가 발톱으로 할큅니다!"],
        death_template="호랑이가 쓰러지며 산의 기운이 흩어집니다."))

    monsters.append(Monster(id=66, name="바위골렘", max_hp=200, hp=200, attack=18, defense=22, speed=3, exp_reward=150, gold_reward=30,
        min_level=15, max_level=25,
        drop_table=[
            {"item_code": "CONS_DEF_BUFF", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_강철퇴", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_강철갑옷", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 바위주먹을 휘두릅니다!","{name}가 지면을 내려찍습니다!"],
        death_template="바위골렘이 돌무더기로 무너집니다."))

    monsters.append(Monster(id=67, name="산의정령", max_hp=90, hp=90, attack=20, defense=12, speed=14, exp_reward=110, gold_reward=20,
        min_level=14, max_level=22,
        drop_table=[
            {"item_code": "CONS_MP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_강철투구", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "CONS_TOWN_SCROLL", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 산의 기운을 발산합니다!","{name}가 바람을 일으킵니다!"],
        death_template="정령이 바람이 되어 사라집니다."))

    monsters.append(Monster(id=68, name="황룡산맹금", max_hp=80, hp=80, attack=24, defense=4, speed=20, exp_reward=120, gold_reward=18,
        min_level=16, max_level=25,
        drop_table=[
            {"item_code": "CONS_SPD_BUFF", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_비수", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_가죽신발", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 급강하합니다!","{name}가 날카로운 발톱을 휘두릅니다!"],
        death_template="맹금이 추락하며 바위에 부딪힙니다."))

    monsters.append(Monster(id=69, name="도적대장", max_hp=180, hp=180, attack=26, defense=10, speed=14, exp_reward=200, gold_reward=50,
        min_level=18, max_level=25,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_참마도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_강철각반", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 쌍도술을 구사합니다!","{name}가 '목숨을 내놔라!' 외칩니다!"],
        death_template="도적대장이 '이럴 수는...' 중얼거리며 쓰러집니다."))

    # ── 폭풍해안 몬스터 (레벨 25~50) ──
    monsters.append(Monster(id=70, name="해안괴어", max_hp=160, hp=160, attack=24, defense=10, speed=12, exp_reward=210, gold_reward=35,
        min_level=25, max_level=35,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_청룡창", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 기습적으로 튀어오릅니다!","{name}가 날카로운 이빨을 드러냅니다!"],
        death_template="괴어가 파도에 휩쓸려 사라집니다."))

    monsters.append(Monster(id=71, name="폭풍세이렌", max_hp=130, hp=130, attack=30, defense=4, speed=20, exp_reward=230, gold_reward=30,
        min_level=28, max_level=40,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_왕관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_암살검", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 치명적인 노래를 부릅니다!","{name}가 물보라를 조종합니다!"],
        death_template="세이렌이 바다거품으로 변해 사라집니다."))

    monsters.append(Monster(id=72, name="모래폭풍전갈", max_hp=190, hp=190, attack=28, defense=16, speed=14, exp_reward=260, gold_reward=40,
        min_level=30, max_level=42,
        drop_table=[
            {"item_code": "CONS_HP_POT_L", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_독비수", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HANDS_철장갑", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 모래 속에서 불쑥 나타납니다!","{name}가 치명적인 독침을 찌릅니다!"],
        death_template="전갈이 모래 속으로 스며들듯 사라집니다."))

    monsters.append(Monster(id=73, name="해일정령", max_hp=150, hp=150, attack=26, defense=14, speed=16, exp_reward=250, gold_reward=35,
        min_level=32, max_level=44,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.08, "min_qty": 1, "max_qty": 2},
            {"item_code": "ARM_CHEST_용비늘갑", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_뇌정창", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 파도를 소환합니다!","{name}가 소금기를 머금은 바람을 뿜습니다!"],
        death_template="정령이 잔잔한 물결로 돌아갑니다."))

    monsters.append(Monster(id=74, name="심해거인", max_hp=300, hp=300, attack=32, defense=20, speed=6, exp_reward=320, gold_reward=60,
        min_level=38, max_level=50,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_벽력퇴", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_천신갑", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 집게발을 휘두릅니다!","{name}가 해저의 진흙을 뿌립니다!"],
        death_template="거인이 바다 밑으로 천천히 가라앉습니다."))

    monsters.append(Monster(id=75, name="폭풍해적선장", max_hp=250, hp=250, attack=36, defense=14, speed=18, exp_reward=350, gold_reward=80,
        min_level=40, max_level=50,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_BLADE_비황도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_비룡각반", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 해적검법을 휘두릅니다!","{name}가 '놈들을 바다 밥으로!' 명령을 내립니다!"],
        death_template="해적선장이 갑판에 쓰러지며 파도가 배를 집어삼킵니다."))

    # ── 마도의탑 몬스터 (레벨 50~100) ──
    monsters.append(Monster(id=76, name="마도서지기", max_hp=320, hp=320, attack=38, defense=18, speed=12, exp_reward=450, gold_reward=70,
        min_level=50, max_level=70,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_마검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_암흑투구", "rate": 0.05, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 금지된 주문을 외웁니다!","{name}가 어둠의 마법진을 소환합니다!"],
        death_template="지기가 마도서와 함께 재가 됩니다."))

    monsters.append(Monster(id=77, name="칠흑의기사", max_hp=380, hp=380, attack=42, defense=22, speed=10, exp_reward=500, gold_reward=80,
        min_level=55, max_level=75,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_폭풍검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_어둠의갑주", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 저주받은 검을 휘두릅니다!","{name}가 어둠의 돌진을 합니다!"],
        death_template="기사의 갑옷이 텅 빈 채로 무너집니다."))

    monsters.append(Monster(id=78, name="탑의환영", max_hp=250, hp=250, attack=44, defense=8, speed=22, exp_reward=480, gold_reward=60,
        min_level=58, max_level=78,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_그림자검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "CONS_ADV_RETURN", "rate": 0.04, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 현실과 환상을 뒤섞습니다!","{name}가 분신술을 사용합니다!"],
        death_template="환영이 거울처럼 깨집니다."))

    monsters.append(Monster(id=79, name="흡혈마", max_hp=300, hp=300, attack=40, defense=14, speed=18, exp_reward=520, gold_reward=75,
        min_level=62, max_level=82,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_DAGGER_혈뢰비수", "rate": 0.07, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_정령왕관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 피의 화살을 날립니다!","{name}가 생명력을 흡수합니다!"],
        death_template="흡혈마가 피안개가 되어 흩어집니다."))

    monsters.append(Monster(id=80, name="고대마법사", max_hp=280, hp=280, attack=46, defense=10, speed=14, exp_reward=550, gold_reward=90,
        min_level=68, max_level=88,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_암흑검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_마계갑옷", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 금단의 마법을 시전합니다!","{name}가 시간을 왜곡합니다!"],
        death_template="마법사가 시공간의 균열 속으로 빨려들어갑니다."))

    monsters.append(Monster(id=81, name="타락한현자", max_hp=350, hp=350, attack=48, defense=16, speed=12, exp_reward=600, gold_reward=100,
        min_level=75, max_level=95,
        drop_table=[
            {"item_code": "CONS_FULL_HEAL", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_마창", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_신의투구", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 타락한 지식으로 공격합니다!","{name}가 '진리는 어둠 속에...' 읊조립니다!"],
        death_template="현자가 마지막 지혜를 남기고 석화됩니다."))

    monsters.append(Monster(id=82, name="탑주마도사", max_hp=450, hp=450, attack=50, defense=24, speed=14, exp_reward=700, gold_reward=150,
        min_level=85, max_level=100,
        drop_table=[
            {"item_code": "CONS_STRENGTH_ELIXIR", "rate": 0.03, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_혼돈검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 탑의 모든 마력을 집중시킵니다!","{name}가 금지된 차원문을 엽니다!"],
        death_template="탑주가 탑과 함께 무너지며 마력의 폭풍이 일어납니다."))

    # ── 천공성 몬스터 (레벨 100~200) ──
    monsters.append(Monster(id=83, name="천공수호병", max_hp=500, hp=500, attack=52, defense=28, speed=12, exp_reward=800, gold_reward=120,
        min_level=100, max_level=130,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SPEAR_신창", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 천공의 창을 휘두릅니다!","{name}가 빛의 방패를 소환합니다!"],
        death_template="수호병이 빛의 입자로 승천합니다."))

    monsters.append(Monster(id=84, name="빛의정령", max_hp=350, hp=350, attack=50, defense=16, speed=24, exp_reward=780, gold_reward=110,
        min_level=105, max_level=135,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_태양검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_성스러운관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 치유의 빛과 함께 공격합니다!","{name}가 광휘의 파동을 냅니다!"],
        death_template="정령이 따뜻한 빛으로 사라집니다."))

    monsters.append(Monster(id=85, name="폭풍천사", max_hp=420, hp=420, attack=56, defense=20, speed=22, exp_reward=850, gold_reward=130,
        min_level=115, max_level=150,
        drop_table=[
            {"item_code": "CONS_SPD_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_뇌전검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_신풍화", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 폭풍의 날개를 펼칩니다!","{name}가 천둥과 함께 강림합니다!"],
        death_template="천사가 번갯불과 함께 소멸합니다."))

    monsters.append(Monster(id=86, name="천공검사", max_hp=480, hp=480, attack=58, defense=24, speed=20, exp_reward=900, gold_reward=140,
        min_level=125, max_level=160,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_냉철검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_신속각반", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 비천검법을 펼칩니다!","{name}가 하늘을 가르는 검기를 날립니다!"],
        death_template="검사가 검과 하나 되어 빛이 됩니다."))

    monsters.append(Monster(id=87, name="성스러운사제", max_hp=380, hp=380, attack=54, defense=18, speed=16, exp_reward=880, gold_reward=150,
        min_level=140, max_level=170,
        drop_table=[
            {"item_code": "CONS_FULL_HEAL", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_금강저", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 신성한 심판을 내립니다!","{name}가 성스러운 불꽃으로 정화합니다!"],
        death_template="사제가 성스러운 빛으로 감싸이며 승천합니다."))

    monsters.append(Monster(id=88, name="천공대천사", max_hp=600, hp=600, attack=62, defense=28, speed=18, exp_reward=1100, gold_reward=200,
        min_level=155, max_level=190,
        drop_table=[
            {"item_code": "CONS_HPMP_POT", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_태양검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 여섯 날개를 펼치며 빛의 심판을 내립니다!","{name}가 천상의 합창으로 공격합니다!"],
        death_template="대천사가 하늘의 별이 됩니다."))

    monsters.append(Monster(id=89, name="천공성주", max_hp=750, hp=750, attack=68, defense=32, speed=16, exp_reward=1400, gold_reward=300,
        min_level=170, max_level=200,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.03, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_뇌전검", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_봉황관", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 천공성의 모든 힘을 모읍니다!","{name}가 차원을 베는 일격을 날립니다!"],
        death_template="성주가 '하늘의 뜻은... 여기까지인가...' 읊조리며 성좌가 됩니다."))

    # ── 명계의문 몬스터 (레벨 200~400) ──
    monsters.append(Monster(id=90, name="망자의인도자", max_hp=700, hp=700, attack=66, defense=26, speed=18, exp_reward=1300, gold_reward=180,
        min_level=200, max_level=250,
        drop_table=[
            {"item_code": "CONS_REVIVE", "rate": 0.03, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_멸혼비수", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_암흑투구", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 죽은 자들의 탄식을 소환합니다!","{name}가 저승의 바람을 불러옵니다!"],
        death_template="인도자가 자신의 등불을 끄며 사라집니다."))

    monsters.append(Monster(id=91, name="명계견", max_hp=850, hp=850, attack=70, defense=30, speed=14, exp_reward=1500, gold_reward=220,
        min_level=220, max_level=280,
        drop_table=[
            {"item_code": "CONS_HP_POT_XL", "rate": 0.10, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_파천도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_어둠의갑주", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 영혼을 찢는 포효를 내지릅니다!","{name}가 사슬을 끊고 덤벼듭니다!"],
        death_template="명계견이 어둠 속으로 물러납니다."))

    monsters.append(Monster(id=92, name="죽음의마녀", max_hp=600, hp=600, attack=72, defense=18, speed=20, exp_reward=1400, gold_reward=200,
        min_level=240, max_level=300,
        drop_table=[
            {"item_code": "CONS_FULL_HEAL", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_암흑검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_정령왕관", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 죽음의 저주를 내립니다!","{name}가 생명력을 빨아들입니다!"],
        death_template="마녀가 '영원한 젊음은... 없구나...' 탄식하며 재가 됩니다."))

    monsters.append(Monster(id=93, name="지옥의집행자", max_hp=1000, hp=1000, attack=78, defense=34, speed=10, exp_reward=1800, gold_reward=280,
        min_level=270, max_level=340,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_멸마봉", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_천신갑", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 죄인의 사슬을 휘두릅니다!","{name}가 업화의 철퇴를 내리칩니다!"],
        death_template="집행자가 자신의 업보에 짓눌려 쓰러집니다."))

    monsters.append(Monster(id=94, name="명계의파수꾼", max_hp=1200, hp=1200, attack=82, defense=38, speed=12, exp_reward=2200, gold_reward=350,
        min_level=310, max_level=380,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_혼돈창", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 명계의 문을 열어 영혼을 빨아들입니다!","{name}가 '돌아갈 수 없다...' 경고합니다!"],
        death_template="파수꾼이 명계의 문과 함께 봉인됩니다."))

    monsters.append(Monster(id=95, name="사신의대리인", max_hp=900, hp=900, attack=80, defense=28, speed=22, exp_reward=2000, gold_reward=320,
        min_level=340, max_level=400,
        drop_table=[
            {"item_code": "CONS_REVIVE", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_어둠의이빨", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_암흑신발", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 죽음의 낫을 휘두릅니다!","{name}가 영혼을 수확합니다!"],
        death_template="대리인이 사신에게 소환되어 사라집니다."))

    # ── 신마대륙 몬스터 (레벨 400~700) ──
    monsters.append(Monster(id=96, name="신마전사", max_hp=1500, hp=1500, attack=85, defense=42, speed=16, exp_reward=2600, gold_reward=400,
        min_level=400, max_level=480,
        drop_table=[
            {"item_code": "CONS_HP_POT_XL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_BLADE_역린도", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_성기사갑옷", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 신마의 힘을 동시에 발산합니다!","{name}가 혼돈의 검기를 날립니다!"],
        death_template="전사가 신력과 마력으로 분리되어 소멸합니다."))

    monsters.append(Monster(id=97, name="혼돈마수", max_hp=1800, hp=1800, attack=88, defense=44, speed=14, exp_reward=3000, gold_reward=480,
        min_level=430, max_level=520,
        drop_table=[
            {"item_code": "CONS_HP_POT_XL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_냉철검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_거신각반", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 혼돈의 포효를 내지릅니다!","{name}가 현실을 왜곡합니다!"],
        death_template="마수가 차원의 균열 속으로 빨려들어갑니다."))

    monsters.append(Monster(id=98, name="신마술사", max_hp=1300, hp=1300, attack=90, defense=30, speed=20, exp_reward=2800, gold_reward=450,
        min_level=460, max_level=550,
        drop_table=[
            {"item_code": "CONS_MP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_마창", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_신의투구", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 신마합일의 주문을 외웁니다!","{name}가 금지된 대마법을 시전합니다!"],
        death_template="술사가 마법의 폭풍에 휩싸여 사라집니다."))

    monsters.append(Monster(id=99, name="용맹한투사", max_hp=2000, hp=2000, attack=92, defense=48, speed=12, exp_reward=3400, gold_reward=550,
        min_level=500, max_level=600,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_BLADE_광룡도", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 불굴의 의지로 돌격합니다!","{name}가 전장을 지배하는 기합을 내지릅니다!"],
        death_template="투사가 서서 눈을 감으며 전사합니다."))

    monsters.append(Monster(id=100, name="대륙의수호룡", max_hp=2500, hp=2500, attack=96, defense=50, speed=16, exp_reward=4000, gold_reward=650,
        min_level=540, max_level=640,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_태양검", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 용의 숨결로 대륙을 수호합니다!","{name}가 별의 힘을 빌려 공격합니다!"],
        death_template="수호룡이 대지의 정기가 되어 흩어집니다."))

    monsters.append(Monster(id=101, name="신마대장군", max_hp=3000, hp=3000, attack=100, defense=54, speed=14, exp_reward=5000, gold_reward=800,
        min_level=600, max_level=700,
        drop_table=[
            {"item_code": "CONS_STRENGTH_ELIXIR", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_혼돈창", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_봉황관", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 천군만마의 기세로 진격합니다!","{name}가 신마의 힘을 방출합니다!"],
        death_template="대장군이 '내가... 지다니...' 충격에 빠지며 쓰러집니다."))

    # ── 혼돈의틈새 몬스터 (레벨 700~999) ──
    monsters.append(Monster(id=102, name="혼돈의파편", max_hp=3500, hp=3500, attack=105, defense=56, speed=18, exp_reward=6000, gold_reward=900,
        min_level=700, max_level=800,
        drop_table=[
            {"item_code": "CONS_HP_POT_XL", "rate": 0.15, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_혼돈검", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 혼돈의 에너지를 방출합니다!","{name}가 형체를 바꾸며 공격합니다!"],
        death_template="파편이 더 작은 조각으로 흩어집니다."))

    monsters.append(Monster(id=103, name="시공의추적자", max_hp=4000, hp=4000, attack=110, defense=58, speed=24, exp_reward=7000, gold_reward=1100,
        min_level=730, max_level=830,
        drop_table=[
            {"item_code": "CONS_SPD_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_명계단검", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_질풍신발", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 시간을 멈추고 공격합니다!","{name}가 과거와 미래에서 동시에 덤벼듭니다!"],
        death_template="추적자가 시공간 속으로 사라집니다."))

    monsters.append(Monster(id=104, name="공허의군주", max_hp=5000, hp=5000, attack=115, defense=62, speed=14, exp_reward=8500, gold_reward=1400,
        min_level=770, max_level=870,
        drop_table=[
            {"item_code": "CONS_FULL_HEAL", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_MACE_멸마봉", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_신의투구", "rate": 0.09, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 공허의 손길로 모든 것을 무화시킵니다!","{name}가 존재 자체를 부정합니다!"],
        death_template="군주가 공허 속으로 되돌아갑니다."))

    monsters.append(Monster(id=105, name="혼돈의화신", max_hp=5500, hp=5500, attack=120, defense=64, speed=20, exp_reward=10000, gold_reward=1600,
        min_level=800, max_level=900,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_BLADE_폭염도", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.09, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 혼돈의 권능을 발동합니다!","{name}가 창조와 파괴를 동시에 행합니다!"],
        death_template="화신이 무(無)로 돌아가며 혼돈이 잠식합니다."))

    monsters.append(Monster(id=106, name="심연의지배자", max_hp=6000, hp=6000, attack=125, defense=66, speed=16, exp_reward=12000, gold_reward=1900,
        min_level=840, max_level=930,
        drop_table=[
            {"item_code": "CONS_STRENGTH_ELIXIR", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_혼돈창", "rate": 0.14, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_LEGS_암흑각반", "rate": 0.09, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 심연의 입을 열어 모든 것을 빨아들입니다!","{name}가 궁극의 어둠을 소환합니다!"],
        death_template="지배자가 '아직... 심연은... 남아있다...' 읊조리며 침묵합니다."))

    monsters.append(Monster(id=107, name="종말의사도", max_hp=7000, hp=7000, attack=130, defense=70, speed=18, exp_reward=15000, gold_reward=2300,
        min_level=880, max_level=970,
        drop_table=[
            {"item_code": "CONS_REVIVE", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_뇌전검", "rate": 0.14, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_HEAD_봉황관", "rate": 0.10, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 종말의 예언을 읊습니다!","{name}가 7개의 재앙을 소환합니다!"],
        death_template="사도가 '예언은... 이루어졌다...' 외치며 소멸합니다."))

    monsters.append(Monster(id=108, name="혼돈룡", max_hp=8000, hp=8000, attack=135, defense=72, speed=22, exp_reward=18000, gold_reward=2800,
        min_level=920, max_level=999,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.06, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_태양검", "rate": 0.15, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.10, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 혼돈의 브레스를 뿜습니다!","{name}가 모든 차원을 뒤흔드는 포효를 내지릅니다!"],
        death_template="혼돈룡이 시공간의 파편이 되어 흩어집니다."))

    # ── 추가 필드 몬스터 (레벨 혼합) ──
    monsters.append(Monster(id=109, name="방랑검객", max_hp=2000, hp=2000, attack=85, defense=40, speed=22, exp_reward=3500, gold_reward=500,
        min_level=350, max_level=500,
        drop_table=[
            {"item_code": "CONS_HP_POT_EL", "rate": 0.12, "min_qty": 1, "max_qty": 2},
            {"item_code": "WPN_SWORD_냉철검", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_신풍화", "rate": 0.06, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 유성검법을 펼칩니다!","{name}가 바람처럼 움직이며 찌릅니다!"],
        death_template="검객이 검을 땅에 꽂고 조용히 눈을 감습니다."))

    monsters.append(Monster(id=110, name="화염정령왕", max_hp=4500, hp=4500, attack=100, defense=50, speed=20, exp_reward=6500, gold_reward=1000,
        min_level=550, max_level=700,
        drop_table=[
            {"item_code": "CONS_ATK_BUFF", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_BLADE_폭염도", "rate": 0.10, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.07, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 지옥불의 소용돌이를 만듭니다!","{name}가 용암비를 내립니다!"],
        death_template="정령왕이 꺼져가는 불꽃이 됩니다."))

    monsters.append(Monster(id=111, name="고대드래곤", max_hp=6500, hp=6500, attack=120, defense=68, speed=12, exp_reward=14000, gold_reward=2200,
        min_level=750, max_level=900,
        drop_table=[
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.05, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SPEAR_혼돈창", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.09, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 파멸의 숨결을 뿜습니다!","{name}가 고대의 마법을 발동합니다!"],
        death_template="드래곤이 뼈만 남기고 사라집니다."))

    monsters.append(Monster(id=112, name="시공의현자", max_hp=3000, hp=3000, attack=110, defense=30, speed=26, exp_reward=9000, gold_reward=1500,
        min_level=650, max_level=850,
        drop_table=[
            {"item_code": "CONS_STRENGTH_ELIXIR", "rate": 0.04, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_DAGGER_명계단검", "rate": 0.12, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_FEET_천둥신발", "rate": 0.08, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}가 시간을 거꾸로 돌립니다!","{name}가 미래의 공격을 미리 가합니다!"],
        death_template="현자가 '모든 시간은... 하나로...' 중얼거리며 소멸합니다."))

    monsters.append(Monster(id=113, name="절대자", max_hp=10000, hp=10000, attack=150, defense=80, speed=20, exp_reward=25000, gold_reward=5000,
        min_level=900, max_level=999,
        is_boss=True,
        drop_table=[
            {"item_code": "CONS_STRENGTH_ELIXIR", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "CONS_VITALITY_ELIXIR", "rate": 0.08, "min_qty": 1, "max_qty": 1},
            {"item_code": "WPN_SWORD_뇌전검", "rate": 0.20, "min_qty": 1, "max_qty": 1},
            {"item_code": "ARM_CHEST_신의갑옷", "rate": 0.12, "min_qty": 1, "max_qty": 1},
        ],
        attack_templates=["{name}이 절대의 권능을 발동합니다!","{name}이 우주의 법칙을 재구성합니다!","{name}이 창조와 소멸을 동시에 행합니다!"],
        death_template="절대자가 '이 또한... 순리로다...' 미소 지으며 우주로 흩어집니다."))

    # ======================== 저장 ========================
    updated = 0
    added = 0
    for m in monsters:
        # ── 인챈트 재료 동적 추가 ──
        lv = m.min_level or 10
        enchant_rate = min(0.30, 0.05 + lv * 0.001)
        protect_rate = min(0.15, 0.01 + lv * 0.0005)
        advanced_rate = min(0.08, lv * 0.0003)
        if m.drop_table is None:
            m.drop_table = []
        dt = list(m.drop_table)
        dt.append({"item_code": "CONS_ENCHANT_STONE", "rate": round(enchant_rate, 4), "min_qty": 1, "max_qty": 3})
        dt.append({"item_code": "CONS_PROTECT_STONE", "rate": round(protect_rate, 4), "min_qty": 1, "max_qty": 2})
        dt.append({"item_code": "CONS_ADVANCED_STONE", "rate": round(advanced_rate, 4), "min_qty": 1, "max_qty": 1})
        # ── 보스 몬스터 (min_level >= 200) 희귀 장비 추가 ──
        if lv >= 200:
            dt.append({"item_code": "ARM_CHEST_봉황갑옷", "rate": 0.12, "min_qty": 1, "max_qty": 1})
            dt.append({"item_code": "WPN_SWORD_뇌전검", "rate": 0.10, "min_qty": 1, "max_qty": 1})
            dt.append({"item_code": "ARM_HEAD_봉황관", "rate": 0.10, "min_qty": 1, "max_qty": 1})
        m.drop_table = dt
        existing = db.query(Monster).filter(Monster.id == m.id).first()
        if existing:
            # 기존 몬스터 업데이트
            existing.min_level = m.min_level
            existing.max_level = m.max_level
            existing.drop_table = m.drop_table
            existing.gold_reward = m.gold_reward
            existing.fame_reward = m.fame_reward
            existing.is_boss = m.is_boss
            updated += 1
        else:
            db.add(m)
            added += 1
    db.commit()
    db.close()
    print(f"v6 monsters seeded: {updated} updated + {added} added (total {len(monsters)})")

if __name__ == "__main__":
    seed()
