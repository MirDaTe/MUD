<!-- 낙화검심 README -->
<p align="center">
  <img src="https://img.shields.io/badge/version-0.4.0-cherry?style=for-the-badge" alt="version">
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge" alt="python">
  <img src="https://img.shields.io/badge/fastapi-0.115-green?style=for-the-badge" alt="fastapi">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge" alt="license">
</p>

---

## 🌸 낙화검심(落花劍心) — 꽃은 지고, 검은 남는다

웹 브라우저에서 즐기는 **정통 무협 멀티플레이 MUD**. 김용풍 무협의 낭만과 비극미를 독자 세계관으로 구현한 온라인 RPG입니다.

> **"문장을 읽는 순간 장면이 떠오르고, 명령을 입력하는 순간 운명이 갈리는 정통 무협 MUD"**

---

## 📊 v0.4.0 스펙

| 항목 | 수량 |
|------|------|
| 🏠 **지역/방** | **102개+ 방** / 15개 지역 |
| 🗺 **지역 분류** | 입문마을·청람산·낙화곡·암시장·황성·만독림·혈뢰협곡·빙하비궁·마황동굴·용문폭포·귀곡촌·봉황단애·천산설봉·동해해변·석회동굴·녹림채·대사막·흑풍산맥·밀림·천곡협곡 |
| 👤 **NPC** | **70명+** (연애 대상 8명) |
| ⚔️ **무공** | **210종** / 12계열 / 9단계 경지 |
| 🐉 **몬스터** | **83종** |
| 💀 **보스** | **25종** |
| 🎒 **아이템** | **341종** |
| 💎 **인챈트** | +0 ~ +15 강화 시스템 |
| 🏯 **문파** | **10개** |
| 🏪 **상점** | **13곳** |
| 🛡️ **관리자** | 유저/캐릭터 관리, 순간이동, 아이템 생성, 무적모드 |

### 🆕 v0.4.0 신규 기능
- 🔤 **영어/한글 병행 명령어** — `attack`=`공격`, `north`=`북`, `talk`=`대화` 등
- 🛡️ **관리자 시스템** — `is_admin` 권한, `admin_set`/`admin_tp`/`admin_give` 등
- 📈 **레벨 디자인 최적화** — 50레벨 EXP 테이블 + 스탯 성장 공식
- 🗺 **지역 ID 체계** — 규칙적인 ID로 각 지역 식별 (1~102+)
- 🏖️ **신규 지역 5곳** — 동해해변·석회동굴·녹림채(도둑소굴)·대사막·밀림·천곡협곡·흑풍산맥

---

## 🛡️ 관리자 시스템

### 관리자 권한 부여
```bash
# API 방식
POST /api/admin/promote/{username}  (관리자만 호출 가능)

# 또는 DB 직접 수정
UPDATE users SET is_admin=1 WHERE username='원하는계정';
```

### 관리자 명령어 (인게임)
| 명령어 | 설명 |
|--------|------|
| `admin_set <캐릭터ID> <필드> <값>` | 캐릭터 스탯 직접 수정 |
| `admin_tp <캐릭터ID> <방ID>` | 캐릭터 지정 방으로 순간이동 |
| `admin_give <캐릭터ID> <아이템ID> [수량]` | 아이템 지급 |
| `admin_users` / `유저목록` | 전체 유저 조회 |
| `admin_chars` / `캐릭터목록` | 전체 캐릭터 조회 |
| `admin_rooms` / `방목록` | 모든 방 목록 (ID, 출구 포함) |
| `admin_god` / `무적` | HP 999999 / 공격 9999 무적 모드 |

### 관리자 API 엔드포인트
| 엔드포인트 | 메서드 | 설명 |
|------------|--------|------|
| `/api/admin/check` | GET | 관리자 여부 확인 |
| `/api/admin/promote/{name}` | POST | 관리자 승급 |
| `/api/admin/users` | GET | 유저 목록 |
| `/api/admin/characters` | GET | 캐릭터 목록 |
| `/api/admin/rooms` | GET | 방 목록 |
| `/api/admin/char/{id}/set` | POST | 스탯 수정 |
| `/api/admin/char/{id}/teleport` | POST | 순간이동 |
| `/api/admin/char/{id}/giveitem` | POST | 아이템 지급 |

---

## 🗺 지역 ID 체계

| ID 범위 | 지역명 | 방 수 |
|---------|--------|-------|
| 1~5 | 입문마을 | 5 |
| 6~10 | 입문마을 확장 | 4 |
| 11~14 | 청람산 | 4 |
| 15~16 | 낙화곡 | 2 |
| 17~19 | 암시장 | 3 |
| 20~22 | 황성 | 3 |
| 23~28 | 만독림 | 6 |
| 29~32 | 혈뢰협곡 | 4 |
| 33~36 | 빙하비궁 | 4 |
| 37~41 | 마황동굴 | 5 |
| 42~45 | 용문폭포 | 4 |
| 46~50 | 귀곡촌 | 5 |
| 51~53 | 봉황단애 | 3 |
| 54~56 | 천산설봉 | 3 |
| 57~58 | 청람산 확장 | 2 |
| 59~62 | 황성 확장 | 4 |
| 63~64 | 암시장 확장 | 2 |
| 65~66 | 낙화곡 확장 | 2 |
| 67~72 | 비밀지역/중원 | 6 |
| 73~76 | 동해해변 | 4 |
| 77~80 | 석회동굴 | 4 |
| 81~84 | 녹림채(도둑소굴) | 4 |
| 85~89 | 대사막 | 5 |
| 90~93 | 흑풍산맥 | 4 |
| 94~96 | 밀림 | 3 |
| 97~99 | 천곡협곡 | 3 |
| 100~102 | 연결 브리지 | 3 |

---

## 🎮 명령어 (영어/한글 병행)

| 영어 | 한글 | 동작 |
|------|------|------|
| `look` / `l` | `보기` / `주변` | 현재 위치 살펴보기 |
| `north` / `south` / `east` / `west` | `북` / `남` / `동` / `서` | 기본 이동 |
| `up` / `down` / `enter` / `out` | `위` / `아래` / `들어가다` / `나가다` | 특수 이동 |
| `go <방향>` | `이동 <방향>` | 방향 이동 |
| `attack <대상>` | `공격 <대상>` | 기본 공격 |
| `cast <무공명>` | `시전 <무공명>` | 무공 발동 |
| `meditate` | `수련` / `명상` | 내공 운행 |
| `talk <대상>` | `대화 <대상>` | NPC와 대화 |
| `status` | `상태` / `정보` | 캐릭터 정보 |
| `inv` | `가방` / `소지품` | 인벤토리 |
| `equip <아이템>` | `장착 <아이템>` | 장비 착용 |
| `use <아이템>` | `사용 <아이템>` | 소모품 사용 |
| `arts` | `무공목록` | 배운 무공 |
| `quest` | `퀘스트` / `의뢰` | 진행중 의뢰 |
| `shop` | `상점` | 상점 보기 |
| `buy <아이템>` | `구매 <아이템>` | 아이템 구매 |
| `enchant <아이템>` | `강화 <아이템>` | 아이템 강화 (+1~+15) |
| `save` | `저장` | 수동 저장 |
| `help` | `도움` / `도움말` | 명령어 도움말 |

---

## 📈 레벨 디자인

- **최대 레벨:** 50
- **레벨업 보상:** 공격+2, 방어+1, HP+12, MP+6, 속도+1
- **EXP 테이블:** 0(Lv.1) → 50(2) → 350(5) → 1,700(10) → 10,400(20) → 130,000(41) → 350,000(50)

---

## 🚀 설치 및 구동

```bash
git clone https://github.com/MirDaTe/MUD.git && cd MUD
pip install -r requirements.txt
cd backend

# 시드 실행 (11개)
python3 seed.py && python3 seed_extended.py && python3 seed_martial_arts.py
python3 seed_items.py && python3 seed_factions.py && python3 seed_shops.py
python3 seed_mega_rooms.py && python3 seed_mega_npcs.py && python3 seed_mega_monsters.py
python3 seed_mega_items.py && python3 seed_mega_shops.py && python3 seed_v4_rooms.py

# 서버 실행
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 프론트엔드 (새 터미널)
cd ../frontend && python3 -m http.server 8080
```

접속: **http://localhost:8080** · API문서: **http://localhost:8000/docs**

---

## 🔄 버전

| 버전 | 주요 변경 |
|------|-----------|
| **0.4.0** | 관리자 시스템·영어/한글 병행·레벨 디자인·지역 ID·신규 30방 |
| 0.3.0 | Mega 확장 (인챈트·72방·70NPC·25보스·341아이템) |
| 0.2.0 | 무공 210종·경지·22방·연애시스템 |
| 0.1.0 | MVP |

<p align="center"><sub>🌸 꽃은 지고, 검은 남는다 — 花落劍存 🌸</sub></p>
