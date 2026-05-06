"""
낙화검심 v0.6 - 방 100개 추가 (총 202개)
신규 지역: 황룡산맥, 폭풍해안, 지하수로, 비취정원, 마법탑, 고대유적, 암흑숲, 운룡협곡
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from app.core.database import SessionLocal, engine, Base
from app.models import Room

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Room).filter(Room.id == 103).count() > 0:
        print("v6 rooms already seeded!"); db.close(); return

    # 기존 방들 업데이트 (마을은 안전지역+여관)
    safe_inn = list(range(1, 23))  # 입문마을 1~22
    for rid in safe_inn:
        r = db.query(Room).filter(Room.id == rid).first()
        if r:
            r.is_safe = True
            r.is_inn = (rid in [1, 2, 11, 12])  # 중심지/여관들
    db.commit()

    rooms = [
    {
      "id": 103,
      "name": "황룡산맥 - 험준한 바위산맥이 하늘을 찌르는 황룡산맥의 입구",
      "region": "황룡산맥",
      "description": "험준한 바위산맥이 하늘을 찌르는 황룡산맥의 입구. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"north": 104}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 104,
      "name": "황룡산맥 - 용의 등뼈처럼 솟은 산등성이",
      "region": "황룡산맥",
      "description": "용의 등뼈처럼 솟은 산등성이. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 103, "north": 105}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 105,
      "name": "황룡산맥 - 깎아지른 절벽 아래 협곡",
      "region": "황룡산맥",
      "description": "깎아지른 절벽 아래 협곡. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 104, "north": 106}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 106,
      "name": "황룡산맥 - 폭포수가 쏟아지는 계곡",
      "region": "황룡산맥",
      "description": "폭포수가 쏟아지는 계곡. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 105, "north": 107}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 107,
      "name": "황룡산맥 - 황룡굴 입구 - 어둠 속에서 금빛 눈동자가 반짝인다",
      "region": "황룡산맥",
      "description": "황룡굴 입구 - 어둠 속에서 금빛 눈동자가 반짝인다. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 106, "north": 108}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 108,
      "name": "황룡산맥 - 협곡 바닥의 안개 낀 습지",
      "region": "황룡산맥",
      "description": "협곡 바닥의 안개 낀 습지. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 107, "north": 109}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 109,
      "name": "황룡산맥 - 버려진 산적 소굴",
      "region": "황룡산맥",
      "description": "버려진 산적 소굴. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 108, "north": 110}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 110,
      "name": "황룡산맥 - 고목이 우거진 산허리",
      "region": "황룡산맥",
      "description": "고목이 우거진 산허리. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 109, "north": 111}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 111,
      "name": "황룡산맥 - 천둥새 둥지가 있는 절벽",
      "region": "황룡산맥",
      "description": "천둥새 둥지가 있는 절벽. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 110, "north": 112}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 112,
      "name": "황룡산맥 - 산정상으로 향하는 협로",
      "region": "황룡산맥",
      "description": "산정상으로 향하는 협로. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 111, "north": 113}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 113,
      "name": "황룡산맥 - 황룡봉 정상 - 구름 위의 세계",
      "region": "황룡산맥",
      "description": "황룡봉 정상 - 구름 위의 세계. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 112, "north": 114}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 114,
      "name": "황룡산맥 - 산신령의 사당",
      "region": "황룡산맥",
      "description": "산신령의 사당. 황룡산맥의 중심으로 향하는 길목.",
      "exits": '{"south": 113}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 115,
      "name": "폭풍해안 - 검은 모래사장이 펼쳐진 해안",
      "region": "폭풍해안",
      "description": "검은 모래사장이 펼쳐진 해안. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"north": 116}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 116,
      "name": "폭풍해안 - 파도가 부서지는 절벽 아래",
      "region": "폭풍해안",
      "description": "파도가 부서지는 절벽 아래. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 115, "north": 117}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 117,
      "name": "폭풍해안 - 버려진 어부의 오두막",
      "region": "폭풍해안",
      "description": "버려진 어부의 오두막. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 116, "north": 118}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 118,
      "name": "폭풍해안 - 해적선 잔해가 널린 해안",
      "region": "폭풍해안",
      "description": "해적선 잔해가 널린 해안. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 117, "north": 119}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 119,
      "name": "폭풍해안 - 폭풍우 속 등대섬으로 가는 배",
      "region": "폭풍해안",
      "description": "폭풍우 속 등대섬으로 가는 배. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 118, "north": 120}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 120,
      "name": "폭풍해안 - 등대섬 선착장",
      "region": "폭풍해안",
      "description": "등대섬 선착장. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 119, "north": 121}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 121,
      "name": "폭풍해안 - 버려진 등대 내부",
      "region": "폭풍해안",
      "description": "버려진 등대 내부. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 120, "north": 122}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 122,
      "name": "폭풍해안 - 산호초가 드러난 얕은 바다",
      "region": "폭풍해안",
      "description": "산호초가 드러난 얕은 바다. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 121, "north": 123}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 123,
      "name": "폭풍해안 - 해룡이 출몰한다는 심해구",
      "region": "폭풍해안",
      "description": "해룡이 출몰한다는 심해구. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 122, "north": 124}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 124,
      "name": "폭풍해안 - 바위굴 속 비밀 동굴",
      "region": "폭풍해안",
      "description": "바위굴 속 비밀 동굴. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 123, "north": 125}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 125,
      "name": "폭풍해안 - 폭풍 신전 유적",
      "region": "폭풍해안",
      "description": "폭풍 신전 유적. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 124, "north": 126}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 126,
      "name": "폭풍해안 - 난파선 내부 갑판",
      "region": "폭풍해안",
      "description": "난파선 내부 갑판. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 125, "north": 127}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 127,
      "name": "폭풍해안 - 선장의 방",
      "region": "폭풍해안",
      "description": "선장의 방. 폭풍해안의 중심으로 향하는 길목.",
      "exits": '{"south": 126}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 128,
      "name": "지하수로 - 녹슨 철문 너머의 지하수로 입구",
      "region": "지하수로",
      "description": "녹슨 철문 너머의 지하수로 입구. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"north": 129}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 129,
      "name": "지하수로 - 고인 물이 반짝이는 넓은 수로",
      "region": "지하수로",
      "description": "고인 물이 반짝이는 넓은 수로. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 128, "north": 130}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 130,
      "name": "지하수로 - 벽면에서 물이 흐르는 좁은 통로",
      "region": "지하수로",
      "description": "벽면에서 물이 흐르는 좁은 통로. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 129, "north": 131}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 131,
      "name": "지하수로 - 버섯이 자라는 지하 동굴",
      "region": "지하수로",
      "description": "버섯이 자라는 지하 동굴. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 130, "north": 132}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 132,
      "name": "지하수로 - 지하 폭포 아래 연못",
      "region": "지하수로",
      "description": "지하 폭포 아래 연못. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 131, "north": 133}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 133,
      "name": "지하수로 - 고대 문명의 흔적이 남은 회랑",
      "region": "지하수로",
      "description": "고대 문명의 흔적이 남은 회랑. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 132, "north": 134}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 134,
      "name": "지하수로 - 녹색 형광 이끼로 뒤덮인 천장",
      "region": "지하수로",
      "description": "녹색 형광 이끼로 뒤덮인 천장. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 133, "north": 135}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 135,
      "name": "지하수로 - 지하 호수 - 물속에 무언가 있다",
      "region": "지하수로",
      "description": "지하 호수 - 물속에 무언가 있다. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 134, "north": 136}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 136,
      "name": "지하수로 - 무너진 다리 옆 우회로",
      "region": "지하수로",
      "description": "무너진 다리 옆 우회로. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 135, "north": 137}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 137,
      "name": "지하수로 - 심연으로 이어지는 수직 갱도",
      "region": "지하수로",
      "description": "심연으로 이어지는 수직 갱도. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 136, "north": 138}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 138,
      "name": "지하수로 - 지하 도시 유적 입구",
      "region": "지하수로",
      "description": "지하 도시 유적 입구. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 137, "north": 139}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 139,
      "name": "지하수로 - 왕좌의 방 - 물에 잠긴 옥좌",
      "region": "지하수로",
      "description": "왕좌의 방 - 물에 잠긴 옥좌. 지하수로의 중심으로 향하는 길목.",
      "exits": '{"south": 138}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 140,
      "name": "비취정원 - 비취빛 꽃잎이 흩날리는 정원 입구",
      "region": "비취정원",
      "description": "비취빛 꽃잎이 흩날리는 정원 입구. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"north": 141}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 141,
      "name": "비취정원 - 영롱한 연꽃이 핀 연못",
      "region": "비취정원",
      "description": "영롱한 연꽃이 핀 연못. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 140, "north": 142}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 142,
      "name": "비취정원 - 대나무 숲 사이 오솔길",
      "region": "비취정원",
      "description": "대나무 숲 사이 오솔길. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 141, "north": 143}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 143,
      "name": "비취정원 - 선계로 통하는 달문",
      "region": "비취정원",
      "description": "선계로 통하는 달문. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 142, "north": 144}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 144,
      "name": "비취정원 - 폭포 옆 찻집",
      "region": "비취정원",
      "description": "폭포 옆 찻집. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 143, "north": 145}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 145,
      "name": "비취정원 - 비취 나비떼가 춤추는 공터",
      "region": "비취정원",
      "description": "비취 나비떼가 춤추는 공터. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 144, "north": 146}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 146,
      "name": "비취정원 - 약초밭과 선단로",
      "region": "비취정원",
      "description": "약초밭과 선단로. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 145, "north": 147}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 147,
      "name": "비취정원 - 돌다리가 놓인 계류",
      "region": "비취정원",
      "description": "돌다리가 놓인 계류. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 146, "north": 148}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 148,
      "name": "비취정원 - 하늘을 찌르는 영목",
      "region": "비취정원",
      "description": "하늘을 찌르는 영목. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 147, "north": 149}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 149,
      "name": "비취정원 - 숨겨진 비밀 화원",
      "region": "비취정원",
      "description": "숨겨진 비밀 화원. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 148, "north": 150}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 150,
      "name": "비취정원 - 선녀상이 있는 연못가",
      "region": "비취정원",
      "description": "선녀상이 있는 연못가. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 149, "north": 151}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 151,
      "name": "비취정원 - 비취궁 입구",
      "region": "비취정원",
      "description": "비취궁 입구. 비취정원의 중심으로 향하는 길목.",
      "exits": '{"south": 150}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 152,
      "name": "마법탑 - 마법탑 외부 - 하늘을 찌르는 첨탑",
      "region": "마법탑",
      "description": "마법탑 외부 - 하늘을 찌르는 첨탑. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"north": 153}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 153,
      "name": "마법탑 - 탑 1층 로비 - 떠도는 촛불들",
      "region": "마법탑",
      "description": "탑 1층 로비 - 떠도는 촛불들. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 152, "north": 154}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 154,
      "name": "마법탑 - 2층 서재 - 살아있는 책들",
      "region": "마법탑",
      "description": "2층 서재 - 살아있는 책들. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 153, "north": 155}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 155,
      "name": "마법탑 - 3층 연금술 실험실",
      "region": "마법탑",
      "description": "3층 연금술 실험실. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 154, "north": 156}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 156,
      "name": "마법탑 - 4층 소환의 방 - 차원문",
      "region": "마법탑",
      "description": "4층 소환의 방 - 차원문. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 155, "north": 157}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 157,
      "name": "마법탑 - 5층 마법진 연구실",
      "region": "마법탑",
      "description": "5층 마법진 연구실. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 156, "north": 158}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 158,
      "name": "마법탑 - 6층 원소의 방 - 불/얼음/번개",
      "region": "마법탑",
      "description": "6층 원소의 방 - 불/얼음/번개. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 157, "north": 159}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 159,
      "name": "마법탑 - 7층 환영의 복도",
      "region": "마법탑",
      "description": "7층 환영의 복도. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 158, "north": 160}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 160,
      "name": "마법탑 - 8층 마도서 보관실",
      "region": "마법탑",
      "description": "8층 마도서 보관실. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 159, "north": 161}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 161,
      "name": "마법탑 - 9층 시공간 왜곡실",
      "region": "마법탑",
      "description": "9층 시공간 왜곡실. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 160, "north": 162}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 162,
      "name": "마법탑 - 10층 대마법사의 서재",
      "region": "마법탑",
      "description": "10층 대마법사의 서재. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 161, "north": 163}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 163,
      "name": "마법탑 - 옥상 천문대",
      "region": "마법탑",
      "description": "옥상 천문대. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 162, "north": 164}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 164,
      "name": "마법탑 - 탑 지하 감옥",
      "region": "마법탑",
      "description": "탑 지하 감옥. 마법탑의 중심으로 향하는 길목.",
      "exits": '{"south": 163}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 165,
      "name": "고대유적 - 모래에 반쯤 묻힌 유적 입구",
      "region": "고대유적",
      "description": "모래에 반쯤 묻힌 유적 입구. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"north": 166}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 166,
      "name": "고대유적 - 거대 석상이 늘어선 회랑",
      "region": "고대유적",
      "description": "거대 석상이 늘어선 회랑. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 165, "north": 167}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 167,
      "name": "고대유적 - 태양 신전 중앙 광장",
      "region": "고대유적",
      "description": "태양 신전 중앙 광장. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 166, "north": 168}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 168,
      "name": "고대유적 - 봉인된 지하 무덤 입구",
      "region": "고대유적",
      "description": "봉인된 지하 무덤 입구. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 167, "north": 169}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 169,
      "name": "고대유적 - 뱀 문양이 새겨진 통로",
      "region": "고대유적",
      "description": "뱀 문양이 새겨진 통로. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 168, "north": 170}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 170,
      "name": "고대유적 - 희생 제단이 있는 방",
      "region": "고대유적",
      "description": "희생 제단이 있는 방. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 169, "north": 171}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 171,
      "name": "고대유적 - 미이라가 잠든 묘실",
      "region": "고대유적",
      "description": "미이라가 잠든 묘실. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 170, "north": 172}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 172,
      "name": "고대유적 - 고대 보물 창고",
      "region": "고대유적",
      "description": "고대 보물 창고. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 171, "north": 173}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 173,
      "name": "고대유적 - 저주받은 왕의 묘실",
      "region": "고대유적",
      "description": "저주받은 왕의 묘실. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 172, "north": 174}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 174,
      "name": "고대유적 - 태양석이 빛나는 중앙홀",
      "region": "고대유적",
      "description": "태양석이 빛나는 중앙홀. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 173, "north": 175}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 175,
      "name": "고대유적 - 붕괴 직전의 지하 통로",
      "region": "고대유적",
      "description": "붕괴 직전의 지하 통로. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 174, "north": 176}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 176,
      "name": "고대유적 - 고대 신의 조각상 앞",
      "region": "고대유적",
      "description": "고대 신의 조각상 앞. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 175, "north": 177}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 177,
      "name": "고대유적 - 유적最深部 - 금단의 방",
      "region": "고대유적",
      "description": "유적最深部 - 금단의 방. 고대유적의 중심으로 향하는 길목.",
      "exits": '{"south": 176}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 178,
      "name": "암흑숲 - 햇빛 한 점 들지 않는 숲 입구",
      "region": "암흑숲",
      "description": "햇빛 한 점 들지 않는 숲 입구. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"north": 179}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 179,
      "name": "암흑숲 - 뒤틀린 고목들 사이 길",
      "region": "암흑숲",
      "description": "뒤틀린 고목들 사이 길. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 178, "north": 180}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 180,
      "name": "암흑숲 - 형광 버섯이 자라는 늪지대",
      "region": "암흑숲",
      "description": "형광 버섯이 자라는 늪지대. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 179, "north": 181}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 181,
      "name": "암흑숲 - 저주받은 나무 - 얼굴이 보인다",
      "region": "암흑숲",
      "description": "저주받은 나무 - 얼굴이 보인다. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 180, "north": 182}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 182,
      "name": "암흑숲 - 버려진 마녀의 오두막",
      "region": "암흑숲",
      "description": "버려진 마녀의 오두막. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 181, "north": 183}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 183,
      "name": "암흑숲 - 안개 자욱한 숲속 공터",
      "region": "암흑숲",
      "description": "안개 자욱한 숲속 공터. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 182, "north": 184}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 184,
      "name": "암흑숲 - 피를 빨아먹는 덩굴 지대",
      "region": "암흑숲",
      "description": "피를 빨아먹는 덩굴 지대. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 183, "north": 185}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 185,
      "name": "암흑숲 - 숲속 호수 - 검은 물",
      "region": "암흑숲",
      "description": "숲속 호수 - 검은 물. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 184, "north": 186}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 186,
      "name": "암흑숲 - 유령이 출몰하는 옛 전장",
      "region": "암흑숲",
      "description": "유령이 출몰하는 옛 전장. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 185, "north": 187}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 187,
      "name": "암흑숲 - 고블린 소굴 입구",
      "region": "암흑숲",
      "description": "고블린 소굴 입구. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 186, "north": 188}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 188,
      "name": "암흑숲 - 숲의 심장부 - 거대 고목",
      "region": "암흑숲",
      "description": "숲의 심장부 - 거대 고목. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 187, "north": 189}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 189,
      "name": "암흑숲 - 암흑의 제단",
      "region": "암흑숲",
      "description": "암흑의 제단. 암흑숲의 중심으로 향하는 길목.",
      "exits": '{"south": 188}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 190,
      "name": "운룡협곡 - 구름이 발아래 펼쳐진 협곡 입구",
      "region": "운룡협곡",
      "description": "구름이 발아래 펼쳐진 협곡 입구. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"north": 191}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 191,
      "name": "운룡협곡 - 용 발톱 자국이 남은 바위",
      "region": "운룡협곡",
      "description": "용 발톱 자국이 남은 바위. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 190, "north": 192}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 192,
      "name": "운룡협곡 - 협곡을 가로지르는 구름다리",
      "region": "운룡협곡",
      "description": "협곡을 가로지르는 구름다리. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 191, "north": 193}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 193,
      "name": "운룡협곡 - 용의 둥지 - 거대 알껍질",
      "region": "운룡협곡",
      "description": "용의 둥지 - 거대 알껍질. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 192, "north": 194}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 194,
      "name": "운룡협곡 - 번개 맞은 고목 지대",
      "region": "운룡협곡",
      "description": "번개 맞은 고목 지대. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 193, "north": 195}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 195,
      "name": "운룡협곡 - 협곡 바닥의 안개 호수",
      "region": "운룡협곡",
      "description": "협곡 바닥의 안개 호수. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 194, "north": 196}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 196,
      "name": "운룡협곡 - 바람의 신전 유적",
      "region": "운룡협곡",
      "description": "바람의 신전 유적. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 195, "north": 197}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 197,
      "name": "운룡협곡 - 구름 속 떠도는 바위섬",
      "region": "운룡협곡",
      "description": "구름 속 떠도는 바위섬. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 196, "north": 198}',
      "is_safe": True,
      "is_inn": True
    },
    {
      "id": 198,
      "name": "운룡협곡 - 용비늘 동굴",
      "region": "운룡협곡",
      "description": "용비늘 동굴. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 197, "north": 199}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 199,
      "name": "운룡협곡 - 폭풍우 치는 협곡 중앙",
      "region": "운룡협곡",
      "description": "폭풍우 치는 협곡 중앙. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 198, "north": 200}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 200,
      "name": "운룡협곡 - 고대 용해골 앞",
      "region": "운룡협곡",
      "description": "고대 용해골 앞. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 199, "north": 201}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 201,
      "name": "운룡협곡 - 천둥새 서식지",
      "region": "운룡협곡",
      "description": "천둥새 서식지. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 200, "north": 202}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 202,
      "name": "운룡협곡 - 운룡봉 정상",
      "region": "운룡협곡",
      "description": "운룡봉 정상. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 201, "north": 203}',
      "is_safe": False,
      "is_inn": False
    },
    {
      "id": 203,
      "name": "운룡협곡 - 용신상이 모셔진 사당",
      "region": "운룡협곡",
      "description": "용신상이 모셔진 사당. 운룡협곡의 중심으로 향하는 길목.",
      "exits": '{"south": 202}',
      "is_safe": False,
      "is_inn": False
    }
  ]

    for rdata in rooms:
        db.add(Room(**rdata))
    db.commit()
    print(f"v6 rooms seeded: {len(rooms)} rooms added (total 202+)")

if __name__ == "__main__":
    seed()
