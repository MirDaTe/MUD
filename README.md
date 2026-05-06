<p align="center">
  <img src="https://img.shields.io/badge/version-0.6.2-cherry?style=for-the-badge">
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge">
</p>

# 🌸 낙화검심(落花劍心) — 꽃은 지고, 검은 남는다

웹 브라우저에서 즐기는 **정통 무협 멀티플레이 MUD**. 13슬롯 WoW 스타일 장비·귀환·레벨제 경제를 갖춘 온라인 RPG.

> **"문장을 읽는 순간 장면이 떠오르고, 명령을 입력하는 순간 운명이 갈리는 정통 무협 MUD"**

---

## 📊 v0.6.2 스펙

| 항목 | 수량 |
|------|------|
| 🏠 **지역/방** | 156개 방 / 23개 지역 |
| 👤 **NPC** | 70명+ |
| ⚔️ **무공** | 210종 / 12계열 / 9단계 경지 |
| 👹 **몬스터** | 108종 (80-210 구간 13종 신규) |
| 🎒 **아이템** | 531종 (고유 코드 + 인스턴스 UUID) |
| 🔒 **레벨제 장비** | 무기 90종 + 방어구 80종 (Lv.1~800) |
| 💰 **가격** | 200 ~ 65,000은전 (현실화) |
| 🏠 **귀환** | 여관 지정 + 귀환서 3종 |
| 🏯 **문파(길드)** | 유저 생성 길드 시스템 |
| 🏪 **상점** | 13곳 |
| 📈 **레벨** | 999까지 확장 |

### 🆕 v0.6.0~0.6.2 신규 기능

| 기능 | 설명 |
|------|------|
| 🎒 **13슬롯 장비** | WoW 스타일 (head/chest/legs/feet/hands/cloak/necklace/ring×2/underwear/trinket×2/mainhand/offhand) |
| ⚔️ **양손무기** | 장착 시 offhand 자동 해제 |
| 🔒 **레벨 제한** | `level_required` 필드 — 장착 시 `"Lv.X 이상만 장착 가능"` |
| 🏠 **귀환 시스템** | 여관 지정 → 귀환서/마을귀환서/고급귀환서 사용 |
| 💰 **돈 상한** | 9,999,999,999 은전 / 가방 30칸 |
| 👹 **몬스터 보강** | 80~210 구간 13종 추가 (암흑마법사·강철골렘·칠흑의기사 등) |
| 💎 **인챈트 재료** | 강화석/보호석/고급강화석 — 모든 몬스터 드랍 (레벨↑ 확률↑) |
| 🛡️ **관리자 강화** | 아이템 검색/코드지급/방 필터링(안전/여관) |

### 🔒 장비 레벨 제한 예시

| 요구 레벨 | 무기 예시 | 방어구 예시 | 가격대 |
|:--------:|----------|------------|------:|
| Lv.1 | 철검, 목방패 | 삼베속옷, 천망토 | 200~300 |
| Lv.20 | 청룡검, 강철창 | 철갑옷, 은반지 | 2,000~3,000 |
| Lv.60 | 벽력검, 참마도 | 강철갑옷, 마력목걸이 | 5,000~8,000 |
| Lv.130 | 신검, 파멸대검 | 용비늘갑, 수호반지 | 12,000~18,000 |
| Lv.300 | 혼돈검, 신의대검 | 마계갑옷, 신의목걸이 | 28,000~38,000 |
| Lv.800 | 뇌전검 | 신의갑옷, 봉황관 | 50,000~65,000 |

---

## 🗺️ 신규 지역 (v0.6.0)

운룡협곡(14) · 폭풍해안(13) · 마법탑(13) · 고대유적(13) · 황룡산맥(12) · 지하수로(12) · 암흑숲(12) · 비취정원(12)  
+ 만독림(6) · 마황동굴(5) · 귀곡촌(5) · 혈뢰협곡(4) · 빙하비궁(4) · 용문폭포(4) · 황성(4) 등 총 23지역

---

## 🎮 전체 명령어

| 분류 | 명령어 |
|------|--------|
| **기본** | `look`/`보기`, 이동(`북`/`남`/`동`/`서`/`위`/`아래`), `go`/`이동` |
| **전투** | `attack`/`공격`, `cast`/`무공`, `meditate`/`수련` |
| **정보** | `status`/`상태`, `inv`/`가방`, `arts`/`무공목록`, `gold`/`돈` |
| **장비** 🔒 | `equip`/`장착`, `unequip`/`해제`, `eq`/`장비`, `use`/`사용` |
| **아이템** | `sell`/`판매`, `dismantle`/`분해`, `discard`/`버리기`, `shop`/`상점`, `buy`/`구매` |
| **귀환** 🏠 | `return_set`/`귀환지정`, `return_go`/`귀환` |
| **강화** | `enchant`/`강화` (+1~+15, `-p`보호 `-a`고급) |
| **문파** | `guild_create`/`길드생성`, `guild_join`/`길드가입`, `guild_approve`/`승인`, `guild_leave`/`탈퇴`, `guild_kick`/`추방`, `guild_rank`/`계급`, `guild_info`/`길드정보`, `guild_storage`/`길드창고`, `guild_deposit`/`보관`, `guild_withdraw`/`인출`, `guild_gold_add`/`입금`, `guild_gold_out`/`출금` |
| **관리자** 🛡️ | `admin_set`, `admin_tp`, `admin_give`, `admin_give_code`, `admin_users`, `admin_chars`, `admin_rooms`, `admin_items`, `admin_item_info`, `admin_god` |

---

## 💎 인챈트 재료 드랍 확률

| 몬스터 레벨 | 강화석 | 보호석 | 고급강화석 |
|:----------:|:------:|:------:|:----------:|
| 10 | 6.0% | 1.5% | 0.3% |
| 50 | 10.0% | 3.5% | 1.5% |
| 100 | 15.0% | 6.0% | 3.0% |
| 200 | 25.0% | 11.0% | 6.0% |
| 250+ | 30.0% | 13.5% | 7.5% |
| 500+ | 30.0% | 15.0% | 8.0% |

---

## 🚀 설치

```bash
git clone https://github.com/MirDaTe/MUD.git && cd MUD/backend
pip install -r requirements.txt

# 시드 실행
python3 seed.py && python3 seed_martial_arts.py && python3 seed_items.py
python3 seed_factions.py && python3 seed_shops.py
python3 seed_mega_rooms.py && python3 seed_v6_rooms.py
python3 seed_mega_items.py && python3 seed_v6_weapons.py
python3 seed_v6_armors.py && python3 seed_v6_consumables.py
python3 seed_mega_monsters.py && python3 seed_v6_monsters.py
python3 seed_mega_shops.py && python3 seed_mega_npcs.py

# 서버
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- 게임: `http://localhost:8080` (`cd frontend && python3 -m http.server 8080`)
- API 문서: `http://localhost:8000/docs`

---

## 🔄 버전

| 버전 | 주요 변경 |
|------|-----------|
| **v0.6.2** | 🔒 레벨제 장비·💰 가격 현실화·👹 몬스터 80-210 구간 13종 보강 |
| v0.6.0 | 13슬롯 장비·귀환·방 151개·드롭테이블·관리자 강화 |
| v0.5.0 | 길드 시스템·소지금·장비·판매분해·레벨999 |
| v0.4.0 | 대규모 확장 (방 102개·아이템 350+·몬스터 145+) |
| v0.3.0 | 인챈트·상점·세력·호감도 |
| v0.2.0 | 무공 210종·경지·연애시스템 |
| v0.1.0 | MVP |

<p align="center"><sub>🌸 꽃은 지고, 검은 남는다 — 花落劍存 🌸</sub></p>
