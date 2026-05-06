<p align="center">
  <img src="https://img.shields.io/badge/version-0.5.0-cherry?style=for-the-badge">
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge">
</p>

# 🌸 낙화검심(落花劍心) — 꽃은 지고, 검은 남는다

웹 브라우저에서 즐기는 **정통 무협 멀티플레이 MUD**. 김용풍 무협의 낭만과 비극미를 독자 세계관으로 구현한 온라인 RPG.

> **"문장을 읽는 순간 장면이 떠오르고, 명령을 입력하는 순간 운명이 갈리는 정통 무협 MUD"**

---

## 📊 v0.5.0 스펙

| 항목 | 수량 |
|------|------|
| 🏠 **지역/방** | 102개 방 / 15개 지역 |
| 👤 **NPC** | 70명+ (연애 대상 8명) |
| ⚔️ **무공** | 210종 / 12계열 / 9단계 경지 |
| 🐉 **몬스터** | 83종 + 보스 25종 |
| 🎒 **아이템** | 341종 |
| 💎 **인챈트** | +0~+15 강화 |
| 🏯 **문파(길드)** | 유저 생성 길드 시스템 |
| 🏪 **상점** | 13곳 |
| 📈 **레벨** | 999까지 확장 |

### 🆕 v0.5.0 신규 기능

| 기능 | 설명 |
|------|------|
| 🏯 **길드 시스템** | 문파 생성(5000은전+1000EXP), 가입/승인/탈퇴/추방/계급 |
| 🏆 **명성 & 버프** | 7단계 명성 마일스톤, 길드원 전원 영구버프 (최대 공+160) |
| 📦 **길드 창고** | 문파 공용 아이템 보관/인출 |
| 💰 **길드 금고** | 은전 입금/출금 |
| 🛒 **판매/분해** | 아이템 판매(반값)·분해(강화석)·버리기 |
| ⚙️ **장비 시스템** | 장착/해제/장비현황(`eq`) |
| 💵 **소지금** | `gold`/`돈` 명령어, 캐릭터당 은전 보유 |
| 🎒 **가방 제한** | 30칸 인벤토리 제한 |
| 📈 **레벨 999** | 지수함수 기반 EXP 공식 |

---

## 🏯 길드 시스템

### 문파 생성
```
guild_create <문파명> [설명]
길드생성 <문파명>
→ 5000은전 + 1000EXP 소모
```

### 길드 명령어 13종
| 명령어 (영/한) | 설명 | 권한 |
|----------------|------|------|
| `guild_join` / `길드가입` | 문파 가입 신청 | 누구나 |
| `guild_approve` / `승인` | 가입 승인 | 길드장 |
| `guild_leave` / `탈퇴` | 문파 탈퇴 | 길드원 |
| `guild_kick` / `추방` | 길드원 추방 | 길드장 |
| `guild_rank` / `계급변경` | 계급 변경 (신입/일반/정예/부길드장) | 길드장 |
| `guild_info` / `길드정보` | 문파 정보, 길드원 목록, 해금 버프 | 누구나 |
| `guild_storage` / `길드창고` | 창고 물품 조회 | 길드원 |
| `guild_deposit` / `보관` | 창고에 아이템 보관 | 길드원 |
| `guild_withdraw` / `인출` | 창고에서 인출 | 길드원 |
| `guild_gold_add` / `입금` | 문파 금고에 은전 입금 | 길드원 |
| `guild_gold_out` / `출금` | 금고에서 출금 | 부길드장↑ |

### 명성 마일스톤 & 버프 (영구 적용)

| 명성 | 칭호 | 공격 | 방어 | HP | MP | 속도 | 치명 |
|------|------|------|------|-----|-----|------|------|
| 100 | 초심자의 의지 | +2 | +1 | +20 | — | — | — |
| 500 | 단결된 무인 | +5 | +3 | +50 | +20 | — | — |
| 1,500 | 정예 문파 | +10 | +6 | +120 | +50 | +2 | — |
| 5,000 | 강호의 명문 | +20 | +12 | +300 | +120 | +5 | +3% |
| 15,000 | 천하제일문 | +40 | +25 | +800 | +300 | +10 | +7% |
| 50,000 | 전설의 문파 | +80 | +50 | +2,000 | +800 | +20 | +12% |
| 150,000 | 신화의 경지 | +160 | +100 | +5,000 | +2,000 | +40 | +20% |

> ⚠️ 버프는 해금 시점에 모든 길드원에게 영구 적용. 신규 가입자는 과거 해금 버프 자동 적용. 밸런스를 위해 최대 버프 합계는 공+160/방+100/HP+5000 수준으로 설계.

---

## 🎮 전체 명령어

| 분류 | 명령어 |
|------|--------|
| **기본** | `look`/`보기`, 이동(`북`/`남`/`동`/`서`/`위`/`아래`/`들어가다`/`나가다`), `go`/`이동` |
| **전투** | `attack`/`공격`, `cast`/`시전`/`무공`, `meditate`/`수련` |
| **대화** | `talk`/`대화` |
| **정보** | `status`/`상태`, `inv`/`가방`/`소지품`, `arts`/`무공목록`, `gold`/`돈`/`은전` |
| **장비** | `equip`/`장착`, `unequip`/`해제`, `eq`/`장비`, `use`/`사용` |
| **아이템** | `sell`/`판매`, `dismantle`/`분해`, `discard`/`버리기`, `shop`/`상점`, `buy`/`구매` |
| **강화** | `enchant`/`강화` (+1~+15, `-p`보호 `-a`고급) |
| **길드** | `guild_create`/`길드생성`, `guild_join`/`길드가입`, `guild_approve`/`승인`, `guild_leave`/`탈퇴`, `guild_kick`/`추방`, `guild_rank`/`계급변경`, `guild_info`/`길드정보`, `guild_storage`/`길드창고`, `guild_deposit`/`보관`, `guild_withdraw`/`인출`, `guild_gold_add`/`입금`, `guild_gold_out`/`출금` |
| **퀘스트** | `quest`/`퀘스트` |
| **저장** | `save`/`저장` |
| **관리자** | `admin_set`, `admin_tp`, `admin_give`, `admin_users`, `admin_chars`, `admin_rooms`, `admin_god`/`무적` |

---

## 🚀 설치

```bash
git clone https://github.com/MirDaTe/MUD.git && cd MUD
pip install -r requirements.txt
cd backend
# 12개 시드 실행
python3 seed.py && python3 seed_extended.py && python3 seed_martial_arts.py
python3 seed_items.py && python3 seed_factions.py && python3 seed_shops.py
python3 seed_mega_rooms.py && python3 seed_mega_npcs.py && python3 seed_mega_monsters.py
python3 seed_mega_items.py && python3 seed_mega_shops.py && python3 seed_v4_rooms.py
# 서버
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- 게임: `http://localhost:8080` (`cd frontend && python3 -m http.server 8080`)
- API: `http://localhost:8000/docs`

---

## 🔄 버전

| 버전 | 주요 변경 |
|------|-----------|
| **0.5.0** | 길드 시스템·소지금·장비·판매분해·레벨999 |
| 0.4.0 | 관리자·영한병행·레벨디자인·지역ID·신규30방 |
| 0.3.0 | Mega 확장 (인챈트·72방·25보스·341아이템) |
| 0.2.0 | 무공210종·경지·연애시스템 |
| 0.1.0 | MVP |

<p align="center"><sub>🌸 꽃은 지고, 검은 남는다 — 花落劍存 🌸</sub></p>
