"""
낙화검심 - 퀘스트 20종 시드
실행: python seed_quests.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models import Quest

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Quest).filter(Quest.id == 1).count() > 0:
        print("Quests already seeded!")
        db.close()
        return

    quests = [
        Quest(id=1, name="떠돌이 고아의 첫걸음", quest_type="main", min_level=1,
              giver_npc_id=62,
              story_text="[촌장] 자네... 강호에 첫발을 내딛는군. 이 마을 근처 대나무숲에 산적패잔병들이 출몰해 마을을 위협하고 있네. 상인들은 길을 잃고, 아이들은 숲에서 놀지 못해. 자네 검술이라면 충분히 상대할 수 있을 거야. 마을 사람들을 위해 저놈들을 3마리만 처치해주게.",
              accept_text="좋아! 마을의 영웅이 될 준비가 되었군. 대나무숲 입구 쪽에 녀석들이 주로 출몰하네.",
              complete_text="고맙네! 자네 덕분에 마을이 평화를 되찾았어. 아이들이 다시 숲에서 뛰어놀 수 있게 됐다네. 이 은전은 보잘것없지만... 작은 보답일세. 강호에서 자네의 명성이 퍼져나가길 기원하네.",
              description="입문마을 근처 산적패잔병 3마리 처치",
              objectives={"type": "kill", "target": "산적패잔병", "count": 3},
              rewards={"exp": 50, "gold": 30},
              next_quest_id=None),

        Quest(id=2, name="검은이리의 위협", quest_type="side", min_level=3,
              giver_npc_id=62,
              story_text="[촌장] 산적은 처리했지만 또 다른 문제가 생겼네. 대나무숲 깊은 곳에 검은이리 한 쌍이 나타났어. 짐승이지만 보통 솜씨가 아니야. 이미 양치기 두 명이 크게 다쳤지. 자네만 믿네, 2마리만 제거해주게.",
              accept_text="조심하게. 보통 이리가 아니야. 무리에서 떨어진 녀석들은 더 사납다네.",
              complete_text="이리가 사라졌다니 안심이 되는군. 부상당한 양치기들에게도 좋은 소식이 될 거야. 약소하지만 사례금을 받아주게.",
              description="검은이리 2마리 처치",
              objectives={"type": "kill", "target": "검은이리", "count": 2},
              rewards={"exp": 80, "gold": 40},
              next_quest_id=None),

        Quest(id=3, name="의문의암살자 추적", quest_type="main", min_level=5,
              giver_npc_id=3,
              story_text="[의문의검객] ...자네, 낙화검결에 대해 뭔가 알고 있나? 모른다면 상관없네. 하지만 최근 암살자 한 명이 이 주변을 배회하고 있어. 귀화천의 앞잡이임이 분명하네. 자네 실력이라면 녀석을 상대할 수 있을 걸세. 그가 알 수도 있는 정보를 위해서라도... 반드시 생포하지는 않아도 되네. 증거만 있으면 돼.",
              accept_text="잘 생각했네. 녀석은 청람산 근처에서 마지막으로 목격됐어. 조심하게, 그림자 속에서 공격해올 거야.",
              complete_text="역시 보통내기가 아니었군. 암살자의 품에서 귀화천의 암호문이 나왔네. 아직 해독은 못했지만... 단서가 될 거야. 자네에게 이걸 맡기겠네. 내 보답은 여기까지일세.",
              description="의문의암살자 1마리 처치",
              objectives={"type": "kill", "target": "의문의암살자", "count": 1},
              rewards={"exp": 120, "gold": 60},
              next_quest_id=None),

        Quest(id=4, name="약재 수집", quest_type="side", min_level=5,
              giver_npc_id=63,
              story_text="[의원] 요즘 마을에 열병이 돌고 있어. 내 처방에 꼭 필요한 회복약 재료가 떨어졌네. 산적들에게 약초꾼들이 산에 못 가는 바람에... 혹시 자네 인벤토리에 회복약이 있다면 3개만 나누어주게. 내가 직접 조제해서 아픈 사람들에게 나눠줄 테니.",
              accept_text="고맙네! 몬스터를 처치하다 보면 종종 드롭되곤 하지. 부탁하세.",
              complete_text="회복약 세 병이면 10명은 치료할 수 있어! 이건 내 비방으로 만든 특제 회복약일세. 자네도 혹시 모르니 챙겨두게. 강호 의원의 정성이 담긴 약이라네.",
              description="회복약 3개 수집",
              objectives={"type": "collect", "target": "회복약", "count": 3},
              rewards={"exp": 60, "gold": 20},
              next_quest_id=None),

        Quest(id=5, name="청람검문 입문시험", quest_type="faction", min_level=8,
              giver_npc_id=2,
              story_text="[청람문지기] 청람검문에 입문하고 싶다 이거지? 첫 관문은 간단하네. 우리 문파의 수련용 목인형 둘을 상대하게. 움직이지만 진짜 검이 아니라 다치진 않을 거야. 자네의 기본기를 평가하는 시험이라 생각하게. 부디... 실망시키지 말길.",
              accept_text="문파 입구로 올라오게. 수련장에 목인형이 대기 중이네.",
              complete_text="흠... 기본기는 나쁘지 않군. 하지만 이제 시작일세. 검문의 진정한 수련은 이제부터지. 이건 입문 기념으로 주는 검술 교본일세. 꾸준히 단련하게.",
              description="청람훈련인형 2마리 처치",
              objectives={"type": "kill", "target": "청람훈련인형", "count": 2},
              rewards={"exp": 150, "gold": 80},
              next_quest_id=None),

        Quest(id=6, name="주막의 비밀", quest_type="side", min_level=10,
              giver_npc_id=1,
              story_text="[주점주인] 손님, 술 한잔 하면서 내 얘기 좀 들어보시겠소? 저 건너편 혈랑곡 쪽에서 혈랑객 하나가 내 단골 손님을 해쳤소. 놈은 피에 미친 살인귀라오. 나 같은 평범한 술장수는 복수할 힘도 없고... 부탁이오. 그 미치광이를 처치해주시오. 사례는 반드시 하리다.",
              accept_text="감사하오! 만독림 쪽에 은신처가 있다는 제보가 있었소. 부디 조심하시오.",
              complete_text="복수했소! 고인의 명복을 빌며... 이것은 내가 평생 모은 비상금 중 일부요. 적지만 받아주시오. 그리고 오늘 밤은 내가 최고급 죽엽청주를 대접하리다.",
              description="혈랑객 1마리 처치",
              objectives={"type": "kill", "target": "혈랑객", "count": 1},
              rewards={"exp": 200, "gold": 100},
              next_quest_id=None),

        Quest(id=7, name="독버섯 채취", quest_type="side", min_level=12,
              giver_npc_id=30,
              story_text="[강호약사] 만독림에는 맹독성 버섯요괴들이 살고 있어요. 대부분 위험하지만... 그중 특별한 녀석의 포자는 강력한 해독제의 원료가 됩니다. 제가 늙어서 직접 갈 순 없고... 당신이라면 충분히 상대할 수 있겠죠. 2마리의 요괴에게서 포자를 채취해주세요. 대신 부탁드려요.",
              accept_text="포자는 버섯요괴를 처치하면 저절로 수집됩니다. 만독림의 독기를 주의하세요!",
              complete_text="완벽한 포자군요! 이걸로 수백 명을 독에서 구할 수 있어요. 이건 제 특제 해독제와 수고비입니다. 만독림에서 조난당한 사람들을 도울 수 있게 해줘서 정말 고마워요.",
              description="독버섯요괴 2마리 처치",
              objectives={"type": "kill", "target": "독버섯요괴", "count": 2},
              rewards={"exp": 180, "gold": 70},
              next_quest_id=None),

        Quest(id=8, name="만독림 생존", quest_type="main", min_level=15,
              giver_npc_id=30,
              story_text="[강호약사] 만독림 더 깊은 곳에 더 위험한 생명체가 있어요. 맹독전갈과 습지악어... 이 둘은 영역다툼을 하며 생태계를 파괴하고 있어요. 당신이 균형을 되찾아주지 않으면 이 숲 전체가 위험해질 거예요. 각각 한 마리씩만 처치해도 생태계는 회복될 수 있어요. 부탁이에요.",
              accept_text="전갈은 사막 지대, 악어는 늪지대에 있어요. 독에 저항할 약을 챙겨가세요.",
              complete_text="숲이 숨을 쉬기 시작했어요. 이제 다시 약초들이 자랄 공간이 생겼네요. 이걸로 당신에게도 약간의 보답을... 강호 최고의 약사가 만든 특별 보약이에요.",
              description="맹독전갈+습지악어 각1마리 처치",
              objectives={"type": "kill", "target": "맹독전갈", "count": 1},
              rewards={"exp": 350, "gold": 150},
              next_quest_id=None),

        Quest(id=9, name="혈뢰협곡의 비밀", quest_type="main", min_level=18,
              giver_npc_id=24,
              story_text="[무당진인] 혈뢰협곡에 뇌전석인이라는 이물이 출몰했소. 자연의 기운이 왜곡되어 생겨난 존재라오. 내공이 깊은 자만이 그 전격을 견딜 수 있지. 자네의 현재 경지라면 한 번 도전해볼 만하오. 이것은 단순한 전투가 아니라 기의 흐름을 이해하는 수련이 될 것이오.",
              accept_text="협곡 깊은 곳에서 번개가 치는 곳을 찾으시오. 현명하게 접근하길.",
              complete_text="훌륭하오! 자네 내공에 청명한 기운이 흐르는군. 이것은 내가 직접 써 내려간 내공 심법의 일부요. 수련하면 반드시 도움이 될 것이오.",
              description="뇌전석인 1마리 처치",
              objectives={"type": "kill", "target": "뇌전석인", "count": 1},
              rewards={"exp": 400, "gold": 200},
              next_quest_id=None),

        Quest(id=10, name="빙하의 수호자", quest_type="side", min_level=22,
              giver_npc_id=25,
              story_text="[소림방장] 빙하비궁에 얼음골렘이라는 수호자가 있소. 본디 사악한 것은 아니지만 지나칠 정도로 냉정해 방문객을 위협하고 있소. 자네 검술로 녀석을 제압할 수 있겠소? 명상과 전투의 조화를... 깨닫게 될 것이오.",
              accept_text="나무아미타불. 비궁 입구의 결계를 열어줄 염주를 빌려드리겠소. 지혜롭게 행동하시오.",
              complete_text="수호자가 잠들었구먼. 비궁은 이제 진정한 수련의 장소가 될 것이오. 이것은 소림사 달마원에서 내려오는 기공법이오. 자네의 내공을 한 단계 끌어올려줄 것이오.",
              description="얼음골렘 1마리 처치",
              objectives={"type": "kill", "target": "얼음골렘", "count": 1},
              rewards={"exp": 500, "gold": 250},
              next_quest_id=None),

        Quest(id=11, name="마황의 그림자", quest_type="main", min_level=28,
              giver_npc_id=25,
              story_text="[소림방장] 마황동굴에서 마기가 새어나오고 있소. 마수새끼와 마화된모험가... 이들은 과거 마황에게 희생된 이들의 잔영이오. 이대로 두면 언젠가 마황이 부활할지도 모르오. 자네가 동굴에 들어가 두 종류의 마물을 각각 정화해주시오. 이것이 무인의 사명이오.",
              accept_text="동굴 안에서는 마기가 자네의 마음을 유혹할 것이오. 명상으로 마음을 굳건히 하시오.",
              complete_text="동굴에서 마기가 약해지고 있소. 위대한 공덕이오. 소림사에서는 자네를 '호법무인'으로 기억할 것이오. 이 기공은 어둠을 밝히는 빛의 내공이오.",
              description="마수새끼+마화된모험가 각1킬",
              objectives={"type": "kill", "target": "마수새끼", "count": 1},
              rewards={"exp": 700, "gold": 350},
              next_quest_id=None),

        Quest(id=12, name="폭포의 전설", quest_type="side", min_level=35,
              giver_npc_id=24,
              story_text="[무당진인] 용문폭포에 용비늘뱀이 출몰했소. 전설에 따르면 용문을 오르던 잉어가 용이 되지 못한 한을 품은 존재라오. 깊은 원한의 마음을 가졌기에 강하기도 하지. 자네 검술로 이 한을 풀어줄 수 있겠소? 마음의 수련도 함께 될 터.",
              accept_text="폭포 꼭대기, 물안개 속에 숨어 있소. 명상으로 마음을 고요히 한 뒤 도전하시오.",
              complete_text="뱀의 원한이 폭포수와 함께 흘러내렸소. 수고했소. 이건 무당산 비전의 태극권보요. 부드러움이 강함을 이긴다는 진리를 담고 있소이다.",
              description="용비늘뱀 1마리 처치",
              objectives={"type": "kill", "target": "용비늘뱀", "count": 1},
              rewards={"exp": 900, "gold": 450},
              next_quest_id=None),

        Quest(id=13, name="귀곡촌 원혼 달래기", quest_type="main", min_level=40,
              giver_npc_id=52,
              story_text="[신비한노파] 귀곡촌... 저주받은 마을이야. 원귀와 백골병사가 밤마다 울부짖으며 산 자를 괴롭히고 있지. 그들의 한은 '살아서도 못 한 사랑'과 '죽어서도 지키지 못한 약속'에 맺혀있어. 자네가 그들을 각각 한 명씩 해방시켜준다면... 마을에 평화가 돌아올 거야.",
              accept_text="이 영단을 가지고 가게나. 귀신을 성불시키는 데 도움이 될 거야. 한밤중에만 활발히 움직이니 서둘러야 해.",
              complete_text="마을에 안개가 걷히는군... 주민들의 얼굴에 생기가 돌아왔어. 이건 그 마을 마지막 생존자에게서 받은 유품이야. 강호의 복운을 빌며... 받아주렴.",
              description="원귀+백골병사 각1마리 처치",
              objectives={"type": "kill", "target": "원귀", "count": 1},
              rewards={"exp": 1200, "gold": 600},
              next_quest_id=None),

        Quest(id=14, name="봉황의 시험", quest_type="side", min_level=45,
              giver_npc_id=55,
              story_text="[봉황사자] 봉황단애에 온 것을 환영하오. 하지만 신성한 이 땅을 밟으려면 봉황의 시험을 통과해야 하오. 봉황그림자와 현무거북을 각각 한 번씩 상대하시오. 봉황은 공격성을, 현무는 방어의 정수를 시험할 것이오. 신수들의 축복 없이는 강호를 구할 수 없소.",
              accept_text="단애 꼭대기에서 신수들이 기다리고 있소. 마음의 준비를 철저히 하시오.",
              complete_text="당신은 봉황의 축복을 받았소! 이제 봉황의 권능 일부를 사용할 자격이 주어졌소. 이것은 봉황의 깃털로 만든 부적이오. 위급할 때 힘이 되어줄 거요.",
              description="봉황그림자+현무거북 각1킬",
              objectives={"type": "kill", "target": "봉황그림자", "count": 1},
              rewards={"exp": 1500, "gold": 750},
              next_quest_id=None),

        Quest(id=15, name="설산의 침입자", quest_type="side", min_level=50,
              giver_npc_id=56,
              story_text="[설인족장] 외부인은 환영하지 않소. 하지만... 지금은 예외요. 빙마 한 마리가 우리 사냥터를 휩쓸었소. 부족 용사 다섯이 당하고 말았지. 당신이라면 그 놈을 처치할 수 있을 거요. 부탁이오... 천산 아이들의 미래를 지켜주오.",
              accept_text="설봉 남쪽 기슭, 빙하 협곡 쪽에 있어요. 부디... 복수해주오.",
              complete_text="빙마가 사라졌다고? 기쁜 소식이오! 부족의 원수 갚았소. 이건 천산에서 나는 희귀한 만년빙 결정이오. 강화할 때 아주 유용할 거요. 우리 부족은 당신을 영원히 기억하겠소.",
              description="빙마 1마리 처치",
              objectives={"type": "kill", "target": "빙마", "count": 1},
              rewards={"exp": 1800, "gold": 900},
              next_quest_id=None),

        Quest(id=16, name="황성의 음모", quest_type="main", min_level=60,
              giver_npc_id=42,
              story_text="[내시총관] 황성 지하에 근위병의 망령이 출몰하고 있소. 선대 황제 때 모반죄로 몰려 죽은 이들의 원혼이지. 황실로서는 부끄운 과거지만... 이제는 이 망령들을 달래려 하오. 2기의 망령을 성불시켜주시오. 황실은 반드시 은혜를 갚을 것이오.",
              accept_text="지하 감옥 쪽의 으스스한 기운에서 찾으시오. 하지만 조심하시오. 황실의 음모가 당신에게도 뻗칠 수 있소.",
              complete_text="망령들이 조용해졌소. 황실도 이제 이 죄를 인정할 수밖에. 이건 황실 금고에 보관되어 있던 보물이오. 받아주시오. 황제 폐하의 감사도 전하리다.",
              description="근위병망령 2마리 처치",
              objectives={"type": "kill", "target": "근위병망령", "count": 2},
              rewards={"exp": 2500, "gold": 1200},
              next_quest_id=None),

        Quest(id=17, name="귀화천의 밀정", quest_type="main", min_level=70,
              giver_npc_id=27,
              story_text="[비연각주] 내 정보망에 귀화천의 밀정 하나가 포착됐소. 암살길드에서조차 신원을 파악하지 못한 위험인물. 검은 밀복 속에 중요한 정보를 가졌을 거요. 당신이 자객이라면... 제거하시오. 단, 그의 품 속 문서는 살아서 가져와야 하오. 보수는 후하게 쳐주리다.",
              accept_text="녀석은 암시장 근처에 은신처가 있소. 주변에 접근할 땐 은밀하게.",
              complete_text="문서를 확보했소. 그리고 녀석을 제거해줘서 감사하오. 이 문서는 강호의 세력 판도를 바꿀 비밀을 담고 있소. 보수와 함께... 자객 길드의 명예로운 동료 증표를 수여하리다.",
              description="귀화천밀정 1마리 처치",
              objectives={"type": "kill", "target": "귀화천밀정", "count": 1},
              rewards={"exp": 3000, "gold": 1500},
              next_quest_id=None),

        Quest(id=18, name="타락한 성기사", quest_type="side", min_level=100,
              giver_npc_id=26,
              story_text="[혈마노괴] 허허, 타락한성기사라... 한때 신성했던 기사가 마물이 되었지. 꽤 재밌는 상대야. 정의감에 불타는 젊은이라면 도전해봐. 죽으면? 그건 실력 없는 거야. 안 죽고 이기면... 흐흐, 내가 희귀한 걸 하나 줄게. 어때, 할 거야 말 거야?",
              accept_text="흐흐, 가서 부딪혀봐. 녀석은 고대유적 근처에 있을 거야. 죽더라도 내 탓은 마라!",
              complete_text="오! 진짜 이겼다고? 놀랍군... 약속은 지켜야지. 내가 수백 년 수집한 비급 한 권 주마. 하지만 다음엔 더 강한 상대를 붙여줄 테니 각오해.",
              description="타락한성기사 1마리 처치",
              objectives={"type": "kill", "target": "타락한성기사", "count": 1},
              rewards={"exp": 5000, "gold": 2500},
              next_quest_id=None),

        Quest(id=19, name="마룡의 피", quest_type="main", min_level=160,
              giver_npc_id=26,
              story_text="[혈마노괴] 마룡혈족... 용의 피를 이은 반인반수야. 인간을 벌레 취급하지. 내가 젊었을 때 한 번 싸웠다가... 이 한쪽 팔을 잃었어. 지금의 나라면 이길 자신 있지만... 네가 한 번 해볼래? 지면 내 원수만 하나 더 늘어나는 거고, 이기면 내 평생 모은 보물 반을 주마.",
              accept_text="녀석은 '인간 따위가...' 하면서 덤벼들 거야. 용살검이 아니면 데미지가 안 박힐 수도 있어. 마음 단단히 먹어!",
              complete_text="내... 원수를 갚았군. 수백 년 만이다. 너 이 녀석... 정말 대단한 놈이야. 자, 약속한 보물이다. 이제 이 늙은이는 편히 죽을 수 있겠어. 고맙다.",
              description="마룡혈족 1마리 처치",
              objectives={"type": "kill", "target": "마룡혈족", "count": 1},
              rewards={"exp": 8000, "gold": 4000},
              next_quest_id=None),

        Quest(id=20, name="최후의 시련", quest_type="main", min_level=200,
              giver_npc_id=53,
              story_text="[무명무사] *망토 속에서 낮고 굵은 목소리가 들려온다* ...칠흑의기사. 무림에서 가장 위험한 마검사지. 본 적도, 이긴 자도 없어. 네 검술과 내공이 최고 경지에 이르렀다면... 한 번 도전해봐. 이 시련을 넘으면 너는 더 이상 인간이 아니야. 무림의... 전설이 되는 거야.",
              accept_text="녀석은 지금 마법탑 최상층에 있어. 이 부적을 가지고 가... 한 번만 네 생명을 구해줄 거야.",
              complete_text="해냈군... 500년 만에 나온 진정한 무인이야. 이걸로 나는... 더 이상 강호를 지키지 않아도 돼. 모든 걸 너에게 물려주마. 무공으로도, 마음으로도... 너야말로 진정한 무림지존이다.",
              description="칠흑의기사 1마리 처치",
              objectives={"type": "kill", "target": "칠흑의기사", "count": 1},
              rewards={"exp": 12000, "gold": 6000},
              next_quest_id=None),
    ]

    for q in quests:
        db.add(q)
    db.commit()
    db.close()
    print(f"Seeded {len(quests)} quests!")

if __name__ == "__main__":
    seed()
