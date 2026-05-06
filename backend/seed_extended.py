"""
낙화검심 - 확장 시드: 방 20개, NPC 20명, 몬스터 20종, 보스 5종
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Room, NPC, Monster

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Room).filter(Room.id == 6).count() > 0:
        print("Extended already seeded!"); db.close(); return

    rooms = [
        Room(id=6, name="입문마을 - 무기점", region="입문마을",
             description="석양빛이 스며드는 낡은 무기점. 벽에는 장검이 가지런히 걸려 있고, 대장간의 매캐한 연기가 바람결에 흩어진다. 주인장은 돌확에 칼날을 갈고 있다. 쇳소리가 규칙적으로 울릴 때마다 칼집 속 검들이 공명한다.",
             exits={"west": 1}),
        Room(id=7, name="입문마을 - 약방", region="입문마을",
             description="문을 열자 쓴 약초향이 코를 찌른다. 천장에는 말린 당귀와 인삼이 주렁주렁 매달려 있고, 구석에서는 탕약이 은은히 끓고 있다. 약장수 할멈은 침대 위 환자의 맥을 짚으며 눈썹 하나 까딱하지 않는다.",
             exits={"east": 1}),
        Room(id=8, name="입문마을 - 대나무숲 깊은 곳", region="입문마을",
             description="햇살조차 닿지 않는 대밭의 속내. 바람이 불 때마다 대나무들이 뼈 부딪히는 소리를 낸다. 바닥은 축축하고, 발밑에서 정체 모를 벌레들이 스멀댄다. 누군가의 숨소리가 대나무 뒤에서 들려오는 듯도 하다.",
             exits={"south": 3, "north": 9}),
        Room(id=9, name="폐사찰", region="입문마을",
             description="부서진 법당. 금박이 벗겨진 불상의 갈라진 눈매가 허공을 응시한다. 찢겨나간 탱화 사이로 쥐들이 기어다니고, 향내 대신 곰팡내가 가득하다. 제단 아래로 이어지는 어두운 지하통로가 입을 벌리고 있다.",
             exits={"south": 8, "down": 10}),
        Room(id=10, name="지하밀실", region="입문마을",
             description="석실. 벽면에는 알아볼 수 없는 문자들이 칼로 새겨져 있다. 중앙의 돌제단 위에서 낡은 비급 한 권이 희미하게 빛나고 있다. 귀화천을 상징하는 검붉은 문양이 벽에 칠해져 있다. 여기... 무언가 있다.",
             exits={"up": 9}),
        Room(id=11, name="청람산 - 검문 내부", region="청람산",
             description="청람검문의 중정. 백색 석판이 깔린 널따란 마당. 대련하는 제자들의 검끝이 부딪히며 파란 불꽃을 튀긴다. 중앙 연못가의 노송 아래서 백발의 장문인이 눈을 감고 좌선 중이다. 검문의 기풍이 공기마저 무겁게 짓누른다.",
             exits={"north": 5, "east": 12, "west": 13}),
        Room(id=12, name="청람산 - 비급고", region="청람산",
             description="검문의 심장부. 삼중 철문 너머로 고서들이 벽을 가득 메운 서가가 보인다. 두 명의 호법장로가 입구를 지키고 있고, 공기가 얼얼할 정도의 진기가 감돈다. 일반 제자는 발조차 들일 수 없는 금역이다.",
             exits={"west": 11}),
        Room(id=13, name="청람산 - 수련장", region="청람산",
             description="절벽을 깎아 만든 야외 수련장. 바닥에는 검자국이 수없이 패여 있고, 벽면의 구멍마다 촛불이 깜박인다. 제자들은 목인형과 대련하며 땀을 흘리고 있다. 누군가의 외마디 고함이 계곡에 메아리친다.",
             exits={"east": 11}),
        Room(id=14, name="청람산 - 후산절벽", region="청람산",
             description="청람산 최고봉. 구름이 발아래로 흐르고, 세상 만물이 손바닥 안처럼 작아 보인다. 절벽 끝에는 단 한 사람만이 오를 수 있는 돌좌가 놓여 있다. 이곳에서 무공을 익히면 그 어떤 경지도 단숨에 넘을 수 있다고 전해진다.",
             exits={"down": 13}),
        Room(id=15, name="낙화곡 - 벚꽃 계곡", region="낙화곡",
             description="사방이 분홍빛. 바람에 흩날리는 벚꽃잎이 눈보라처럼 쏟아진다. 계곡물은 벚꽃잎을 싣고 잔잔히 흐르고, 나무다리 너머에는 붉은 누각이 어렴풋이 보인다. 어디선가 들려오는 비파 소리. 이곳의 아름다움에는 어딘지 모를 슬픔이 깃들어 있다.",
             exits={"north": 16, "south": 3}),
        Room(id=16, name="낙화곡 - 홍련누각", region="낙화곡",
             description="벚꽃나무에 둘러싸인 붉은 누각. 대청마루에는 주안상이 차려져 있고, 흰 옷의 여인이 혼자 비파를 타고 있다. 바람이 불면 벚꽃잎이 날아들어 술잔 위에 내려앉는다. 이곳은 강호의 고수들이 은밀히 만나는 장소다.",
             exits={"south": 15}),
        Room(id=17, name="암시장 - 지하상가", region="암시장",
             description="햇빛 대신 등불만이 비추는 지하 세계. 밀무기, 금서, 독약, 그리고 사람마저 거래되는 이곳은 강호의 뒷골목이다. 상인들은 모두 얼굴을 가리고 있고, 공기는 습하고 비릿하다. 이곳에서 모든 것은 은전보다 정보가 먼저다.",
             exits={"north": 18, "west": 19}),
        Room(id=18, name="암시장 - 살수 길드", region="암시장",
             description="'무명각'의 지부. 붉은 가면을 쓴 접수원이 묵묵히 의뢰서를 분류한다. 벽에는 현상수배서들이 빼곡히 붙어 있다. 공기는 서늘하고, 누구도 서로의 눈을 쳐다보지 않는다. 이곳에서는 이름보다 살수의 번호가 먼저다.",
             exits={"south": 17}),
        Room(id=19, name="암시장 - 암거래소", region="암시장",
             description="탁자마다 정체 모를 물건들이 진열되어 있다. 비급 조각, 독약, 도난당한 문파의 신물까지. 암거래상들은 날카로운 눈빛으로 손님을 훑는다. 흥정은 대부분 눈빛과 손짓으로 이루어진다.",
             exits={"east": 17}),
        Room(id=20, name="황성 - 성문 앞", region="황성",
             description="십 장 높이의 거대한 성문. 금박으로 새겨진 황실 문장이 석양을 받아 타오른다. 갑옷 입은 근위병 여덟이 창을 교차해 입구를 막고 있다. 이 문을 통과하는 순간, 강호의 법칙 대신 황실의 질서가 당신을 기다린다.",
             exits={"north": 21, "south": 1}),
        Room(id=21, name="황성 - 번화가", region="황성",
             description="중원 최대의 번화가. 양옆으로 고급 객잔, 포목점, 보석상이 즐비하다. 비단옷의 귀족, 검은 띠를 두른 무인, 이국의 상인들이 거리를 가득 메운다. 높은 누각에서는 시녀들이 부채 뒤로 거리를 내려다본다.",
             exits={"south": 20, "west": 22}),
        Room(id=22, name="황성 - 황영사 분관", region="황성",
             description="겉보기에는 평범한 서점. 하지만 안으로 들어서면 수상한 인물들이 은밀히 대화를 나누고 있다. 벽의 비밀문 뒤에는 황실의 첩보 보고서가 가득하다. 이곳의 책들은 글자보다 암호가 더 많다.",
             exits={"east": 21}),
    ]
    for r in rooms: db.add(r)

    # NPC
    npcs = [
        NPC(id=4, name="무기점 주인", dialogue="[무기점 주인] 새 검인가? 아니면 수리인가? 명검이 필요하면 은전 스무 닢이고, 평범한 건 다섯 닢이오. 하지만... 자네 손에는 이 가게의 검보다 더 날카로운 인연이 깃들어 있군.", is_hostile=False),
        NPC(id=5, name="약방 할멈", dialogue="[할멈] 어디가 아픈가? 보아하니 몸보다 마음이 더 아픈 모양이구먼. 자, 이 약차 한잔 하게. 강호에서 상처 없이 살 수 있는 사람은 아무도 없지.", is_hostile=False),
        NPC(id=6, name="청람장문인", dialogue="[장문인] 자네 안에서 흔들리는 검의를 느꼈네. 하지만 검은 단순한 쇠붙이가 아니야. 네 마음이 곧은 만큼 검도 곧아지는 법이지. 청람검문에 입문하겠다면, 수련장에서 네 실력을 증명하게.", is_hostile=False),
        NPC(id=7, name="호법장로", dialogue="[호법장로] 여긴 비급고. 허가 없는 자는 출입 금지일세. 무공의 비급은 단순한 책이 아니야. 한 사람의 인생을 송두리째 바꾸는 힘이지. 함부로 탐해서는 안 돼.", is_hostile=False),
        NPC(id=8, name="암시장 중개인", dialogue="[중개인] 원하는 게 있으면 먼저 정보를 내놔. 은전만으로는 부족해. 강호에서 가장 비싼 건... 사람의 약점이지.", is_hostile=False),
        NPC(id=9, name="무명각 접수원", dialogue="[접수원] 의뢰인가? 표적의 이름과 은전을 먼저. 결과는 3일 이내. 실패하면 은전은 반환하지 않네. 그리고... 의뢰인의 신원은 절대 묻지도 말고 말하지도 말게.", is_hostile=False),
        NPC(id=10, name="황영사 서기", dialogue="[서기] 서점에 무슨 용건인가? 아... 그쪽인가. 3번 서가 뒤의 밀실로 가시게. 주임께서 기다리고 계실 거야. 단, 묻는 말에만 대답하게.", is_hostile=False),
        # Romance NPCs
        NPC(id=11, name="설매화", title="청람검희",
            dialogue="[설매화] 내 검은 의리를 위해 존재하오. 하지만 복수와 의리 사이에서 검집이 무거워질 때가 있지. 당신은... 어느 쪽을 선택하겠소?",
            description="청람검문 최고의 여검객. 눈빛은 칼날처럼 서늘하지만, 그 이면에는 깊은 슬픔이 깃들어 있다. 의리와 복수 사이에서 흔들리는 검희.",
            is_hostile=False),
        NPC(id=12, name="연비홍", title="사파 정보상",
            dialogue="[연비홍] 정보 하나에 은전 백 닢! ...농담이야~ 하지만 당신 얘기는 특별히 공짜로 해줄 수도 있고? 먼저 나랑 술 한잔 어때?",
            description="사파의 정보상. 장난기 가득한 미소 뒤에 날카로운 지성을 숨기고 있다. 강호의 모든 비밀을 알고 있지만, 자신의 비밀은 절대 드러내지 않는다.",
            is_hostile=False),
        NPC(id=13, name="묵련", title="독의",
            dialogue="[묵련] 가까이 오지 마. 내 몸에는 스스로도 두려워하는 독이 흐르고 있어. 날 구하려 하지 마... 구원받기엔 내 손에 묻은 피가 너무 많아.",
            description="독과 의술 모두에 통달한 수수께끼의 여인. 만지는 것만으로 상대를 죽일 수 있는 극독을 체내에 지니고 있다. 구원을 원하지만 구원을 거부하는 모순된 존재.",
            is_hostile=False),
        NPC(id=14, name="소하린", title="궁중무희",
            dialogue="[소하린] 이 춤은 황제의 목숨을 빼앗기 위한 춤이었어요. 하지만... 당신이 보는 앞에서는 그저 아름답고 싶어요. 어리석은 일인가요?",
            description="황실의 비밀을 쥔 궁중 무희. 우아한 춤사위 속에 암살자의 기술을 숨겼다. 진실을 알게 된 순간 그녀는 도망자 신세가 되었다.",
            is_hostile=False),
        NPC(id=15, name="담월", title="경계의 천재",
            dialogue="[담월] 정파? 사파? 그런 구분이 무슨 의미가 있지? 나는 그저... 더 강해지고 싶을 뿐이야. 설령 그 길이 마도의 끝이라 해도.",
            description="마도와 정파의 경계에 선 천재 무인. 어떤 문파도 그녀의 재능을 감당하지 못했다. 검의 본질을 추구할수록 인간성이 닳아지는 비극의 인물.",
            is_hostile=False),
        # More NPCs
        NPC(id=16, name="유성상단주", dialogue="[상단주] 거래하러 왔나? 유성상단은 강호 최대의 상단. 원하는 물건이 있다면 구해주지. 하지만... 대가 없는 거래는 없네.", is_hostile=False),
        NPC(id=17, name="금풍표국장", dialogue="[표국장] 호위 의뢰인가? 금풍표국은 물건이 아니라 의리를 운송하오. 표물을 건드리는 자는... 강호 전체의 적이 될 것이오.", is_hostile=False),
        NPC(id=18, name="검문수련교관", dialogue="[교관] 기합! 자네 검은 아직 힘만 실렸군. 기술이란 상대를 베는 게 아니라 상대의 흐름을 끊는 거야. 다시!", is_hostile=False),
        NPC(id=19, name="객잔주인", dialogue="[주인] 방이 필요하신가? 지금은 방이 없네만... 뒷골목으로 들어가면 싸구려 여관이 하나 있지. 다만 거긴, 도둑 조심하게.", is_hostile=False),
        NPC(id=20, name="행상인", dialogue="행상인은 소매를 걷으며 특이한 물건들을 꺼내 보인다. '이것 봐. 북쪽 사막에서 구한 희귀 약재야. 내공을 순식간에 채워주지.'", is_hostile=False),
    ]
    for n in npcs: db.add(n)
    db.flush()

    # Monsters
    monsters = [
        Monster(id=6, name="대나무도적", max_hp=50, hp=50, attack=10, defense=4, speed=9, exp_reward=35,
                attack_templates=["{name}이 대나무 뒤에서 튀어나옵니다!", "{name}이 죽창을 겨누며 돌진합니다!"],
                death_template="대나무도적이 바스락거리는 잎새 사이로 쓰러집니다."),
        Monster(id=7, name="사찰귀영", max_hp=45, hp=45, attack=14, defense=2, speed=15, exp_reward=50,
                attack_templates=["{name}이 음산한 울음소리와 함께 달려듭니다!", "{name}이 허공에서 손톱을 휘두릅니다!"],
                death_template="사찰귀영이 한 줄기 연기가 되어 흩어집니다."),
        Monster(id=8, name="비급수호자", max_hp=120, hp=120, attack=18, defense=10, speed=7, exp_reward=200,
                attack_templates=["{name}이 고서를 수호하는 진기를 발산합니다!", "{name}이 무거운 손바닥을 내려칩니다!"],
                death_template="수호자가 마지막 힘을 다해 비급을 봉인하고 소멸합니다."),
        Monster(id=9, name="검문훈련생", max_hp=60, hp=60, attack=12, defense=5, speed=10, exp_reward=30,
                attack_templates=["{name}이 청람검식으로 공격합니다!", "{name}이 날렵한 찌르기를 시도합니다!"],
                death_template="훈련생이 넋을 잃고 주저앉습니다."),
        Monster(id=10, name="계류산적", max_hp=55, hp=55, attack=11, defense=3, speed=11, exp_reward=40,
                attack_templates=["{name}이 협곡에서 뛰쳐나옵니다!", "{name}이 돌을 던지며 달려듭니다!"],
                death_template="산적이 비틀거리며 계곡 아래로 떨어집니다."),
        Monster(id=11, name="벚꽃요정", max_hp=35, hp=35, attack=16, defense=1, speed=18, exp_reward=60,
                attack_templates=["{name}이 환상의 베기를 펼칩니다!", "{name}이 꽃잎에 숨어 급습합니다!"],
                death_template="벚꽃요정이 흩날리는 꽃잎과 함께 사라집니다."),
        Monster(id=12, name="홍련암살자", max_hp=65, hp=65, attack=17, defense=6, speed=13, exp_reward=90,
                attack_templates=["{name}이 비파 소리에 맞춰 단검을 휘두릅니다!", "{name}이 그림자 속에서 찔러옵니다!"],
                death_template="암살자가 '주인님께서... 기다리신다...' 중얼거리며 숨을 거둡니다."),
        Monster(id=13, name="암시장패거리", max_hp=70, hp=70, attack=14, defense=6, speed=10, exp_reward=70,
                attack_templates=["{name}이 욕설을 내뱉으며 몽둥이를 휘두릅니다!", "{name}이 협공으로 밀어붙입니다!"],
                death_template="패거리가 도망치듯 어둠 속으로 사라집니다."),
        Monster(id=14, name="길드경호원", max_hp=80, hp=80, attack=16, defense=8, speed=9, exp_reward=85,
                attack_templates=["{name}이 무표정하게 검을 뽑습니다!", "{name}이 기계적인 동작으로 공격합니다!"],
                death_template="경호원이 마지막 의식처럼 정중히 인사하고 쓰러집니다."),
        Monster(id=15, name="암거래경계병", max_hp=75, hp=75, attack=15, defense=7, speed=10, exp_reward=75,
                attack_templates=["{name}이 단검으로 위협하며 다가옵니다!", "{name}이 표창을 날려 견제합니다!"],
                death_template="경계병이 쓰러지며 품속에서 문서가 흘러나옵니다."),
        Monster(id=16, name="황성근위병", max_hp=100, hp=100, attack=18, defense=12, speed=8, exp_reward=120,
                attack_templates=["{name}이 창을 겨누고 진형을 갖춥니다!", "{name}이 규율에 맞춰 일제히 찌릅니다!"],
                death_template="근위병이 갑옷 째로 무너집니다."),
        Monster(id=17, name="황실첩자", max_hp=60, hp=60, attack=20, defense=4, speed=16, exp_reward=110,
                attack_templates=["{name}이 은밀하게 독침을 날립니다!", "{name}이 순식간에 거리를 좁혀 급소를 찌릅니다!"],
                death_template="첩자가 독약을 삼키며 자결합니다."),
        Monster(id=18, name="번화가부랑배", max_hp=45, hp=45, attack=9, defense=2, speed=12, exp_reward=25,
                attack_templates=["{name}이 시비를 걸며 밀쳐옵니다!", "{name}이 술병을 휘두릅니다!"],
                death_template="부랑배가 비명과 함께 골목으로 도망칩니다."),
        Monster(id=19, name="낙화곡암랑", max_hp=40, hp=40, attack=13, defense=2, speed=18, exp_reward=55,
                attack_templates=["{name}이 달빛 아래 은밀히 기어듭니다!", "{name}이 날카로운 이빨로 할큅니다!"],
                death_template="암랑이 긴 울부짖음을 남기고 쓰러집니다."),
        Monster(id=20, name="귀화천밀사", max_hp=90, hp=90, attack=22, defense=8, speed=12, exp_reward=180,
                attack_templates=["{name}이 검붉은 내공을 휘감으며 접근합니다!", "{name}이 귀화천의 비전 무공을 펼칩니다!"],
                death_template="밀사가 '귀화천은... 영원하다...' 읊조리며 무너집니다."),
        Monster(id=21, name="산적두목", max_hp=100, hp=100, attack=16, defense=8, speed=10, exp_reward=130,
                attack_templates=["{name}이 쌍도끼를 휘두르며 포효합니다!", "{name}이 무리를 소집해 총공세를 펼칩니다!"],
                death_template="산적두목이 산을 뒤흔드는 절규와 함께 무너집니다."),
        Monster(id=22, name="독거미", max_hp=30, hp=30, attack=15, defense=0, speed=19, exp_reward=45,
                attack_templates=["{name}이 독사를 뿜으며 덤벼듭니다!"],
                death_template="독거미가 다리를 오그리며 죽습니다."),
        Monster(id=23, name="청람검령", max_hp=110, hp=110, attack=20, defense=10, speed=12, exp_reward=140,
                attack_templates=["{name}이 청람검문의 전설적인 검법을 구사합니다!", "{name}이 검기로 공간을 베어냅니다!"],
                death_template="검령이 허공에 한 획을 긋고 사라집니다."),
        Monster(id=24, name="혈랑객정예", max_hp=85, hp=85, attack=17, defense=7, speed=11, exp_reward=95,
                attack_templates=["{name}이 악에 받친 기세로 덤벼듭니다!", "{name}이 핏발 선 눈으로 검을 휘두릅니다!"],
                death_template="혈랑객이 분노에 찬 외침을 남기고 쓰러집니다."),
        Monster(id=25, name="석상병사", max_hp=130, hp=130, attack=22, defense=14, speed=5, exp_reward=160,
                attack_templates=["{name}이 느리지만 강력한 일격을 가합니다!", "{name}이 돌주먹을 휘둘러 충격파를 냅니다!"],
                death_template="석상병사가 부서지며 돌조각으로 흩어집니다."),
    ]
    # Bosses
    bosses = [
        Monster(id=100, name="폐사찰혈승", max_hp=300, hp=300, attack=25, defense=12, speed=8, exp_reward=500,
                attack_templates=["혈승이 검붉은 장법을 펼칩니다!", "혈승이 광기 어린 웃음을 흘리며 달려듭니다!", "혈승이 바닥을 내리쳐 충격파를 발생시킵니다!"],
                death_template="혈승이 '이것이... 낙화검결의... 저주...' 신음하며 재가 되어 흩어집니다."),
        Monster(id=101, name="월하검귀", max_hp=350, hp=350, attack=30, defense=8, speed=15, exp_reward=600,
                attack_templates=["월하검귀가 달빛을 받아 검강을 펼칩니다!", "검귀의 환영이 사방에서 덤벼듭니다!"],
                death_template="검귀가 허망한 미소와 함께 달빛 속으로 사라집니다."),
        Monster(id=102, name="흑련마후", max_hp=400, hp=400, attack=28, defense=15, speed=10, exp_reward=700,
                attack_templates=["흑련마후가 독무를 사방에 뿌립니다!", "마후가 환술로 분신을 만들어 공격합니다!"],
                death_template="흑련마후가 '흑련은... 지지 않는다...' 중얼거리며 연기로 변합니다."),
        Monster(id=103, name="철혈노조", max_hp=450, hp=450, attack=35, defense=18, speed=7, exp_reward=800,
                attack_templates=["철혈노조가 체인 연타를 휘두릅니다!", "노조가 반격의 태세를 취합니다!"],
                death_template="철혈노조가 굴하지 않는 눈빛으로 무릎 꿇습니다."),
        Monster(id=104, name="귀화천장로", max_hp=500, hp=500, attack=40, defense=20, speed=12, exp_reward=1200,
                attack_templates=["귀화천장로가 탁한 흑기를 내뿜습니다!", "장로가 귀화천의 사파 무공을 펼칩니다!", "장로가 내공을 역류시켜 공간을 뒤틉니다!"],
                death_template="장로가 '주인님... 용서하소서...' 바닥에 엎드려 숨을 거둡니다."),
    ]
    for m in monsters + bosses: db.add(m)
    db.flush()

    # Assign NPCs and monsters to rooms
    room_npc_map = {6: [4], 7: [5], 11: [6, 11, 18], 12: [7], 17: [8], 18: [9], 22: [10],
                    15: [12], 13: [13, 15], 16: [14], 20: [16, 17, 19, 20]}
    room_mon_map = {8: [6, 21], 9: [7, 22], 10: [8], 11: [9, 24], 13: [10, 23], 14: [25],
                    15: [11], 16: [12], 17: [13], 18: [14], 19: [15], 20: [16], 22: [17], 21: [18], 3: [19], 4: [20]}

    for rid, nids in room_npc_map.items():
        room = db.query(Room).filter(Room.id == rid).first()
        if room:
            existing = set(room.npc_ids or [])
            existing.update(nids)
            room.npc_ids = list(existing)
    for rid, mids in room_mon_map.items():
        room = db.query(Room).filter(Room.id == rid).first()
        if room:
            existing = set(room.monster_ids or [])
            existing.update(mids)
            room.monster_ids = list(existing)

    db.commit(); db.close()
    print("Extended seed complete: 17 new rooms, 17 NPCs, 20 monsters, 5 bosses.")

if __name__ == "__main__":
    seed()
