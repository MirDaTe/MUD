# 📖 낙화검심 — 전체 게임 기록

> **최종 업데이트**: 2026년 5월 6일 v0.8.1  
> **개발자**: 류원석 (MirDaTe)  
> **GitHub**: https://github.com/MirDaTe/MUD

---

## 📊 게임 통계 (v0.8.1 기준)

### 🗺️ 월드
| 항목 | 수치 |
|------|------|
| 전체 방 | **203** 개 |
| 지역 | **23** 개 |
| 안전지역 | **8** 개 |
| 여관 (귀환 가능) | **8** 개 |

### 📦 아이템
| 항목 | 수치 |
|------|------|
| 전체 아이템 | **531** 종 |
| 무기 | **160** 종 (공격력 8~72, 평균 29) |
| 방어구 | **130** 종 (방어력 평균 21, 최대 41) |
| 소모품 | **116** 종 (귀환서 3종 포함) |
| 가격대 | 18 ~ 65,000 은전 |

### 👹 몬스터
| 항목 | 수치 |
|------|------|
| 전체 몬스터 | **108** 종 |
| 드롭테이블 보유 | **88** 종 (100%) |
| 평균 HP | 1,054 |
| 평균 공격력 | 50 |
| 평균 방어력 | 23 |
| 평균 경험치 보상 | 2,480 |
| 평균 금화 보상 | 271 |

### 🎭 기타 시스템
| 항목 | 수치 |
|------|------|
| 무공 | **210** 종 |
| 세력 | **10** 종 |
| 상점 | **13** 개 |
| NPC | **70**+ 종 |
| 어픽스 | **60** 종 (접두 40 + 접미 20) |
| 퀘스트 | **20** 종 |
| 명령어 자동완성 | **50** 종 |

---

## 🏗️ 시스템 아키텍처

```
backend/
├── app/
│   ├── main.py              # FastAPI 애플리케이션 (v0.8.1, 리스폰 템플릿 등록)
│   ├── api/endpoints/        # REST API 엔드포인트
│   │   ├── auth.py           # 인증 (회원가입/로그인)
│   │   ├── characters.py     # 캐릭터 CRUD
│   │   ├── game.py           # 게임 명령어 처리 + 대상 자동완성 API
│   │   └── admin.py          # 관리자 API
│   ├── core/
│   │   ├── config.py         # 환경 설정
│   │   ├── database.py       # SQLAlchemy 세션
│   │   └── security.py       # JWT 인증
│   ├── models/               # DB 모델 (18종)
│   │   ├── character.py      # 캐릭터 (13슬롯 장비 스탯 포함)
│   │   ├── item.py           # 아이템 (code/slot/stack_limit/level_required)
│   │   ├── inventory.py      # 인벤토리 (slot/instance_id/affix_data)
│   │   ├── room.py           # 방 (is_safe/is_inn)
│   │   ├── monster.py        # 몬스터 (drop_table/is_aggro/respawn_*/ambient_lines)
│   │   ├── npc.py            # NPC (occupation/shop_id/dialogue_options/quest_giver)
│   │   ├── martial_art.py    # 무공
│   │   ├── item_affix.py     # 어픽스 (접두/접미)
│   │   ├── quest.py          # 퀘스트 (story_text/accept_text/complete_text)
│   │   ├── character_quest.py
│   │   ├── enchantment.py    # 인챈트 (enchant_level/bonus_value)
│   │   ├── faction.py        # 세력
│   │   ├── shop.py           # 상점
│   │   ├── guild.py          # 길드(문파)
│   │   ├── guild_member.py
│   │   ├── guild_storage.py
│   │   ├── guild_buff.py
│   │   └── guild_application.py
│   ├── services/             # 비즈니스 로직
│   │   ├── game_service.py   # 메인 명령어 처리 (attack/flee/map/귀환/help 등)
│   │   ├── combat_service.py # 자동 전투(틱 기반)·무공·드롭·어픽스·경지
│   │   ├── inventory_service.py # 13슬롯 장비 시스템 + 레벨 체크 + 인챈트 적용
│   │   ├── enchant_service.py   # 강화(+15) 시스템 (Enchantment 기반)
│   │   ├── affix_service.py     # 접두/접미 랜덤 부여
│   │   ├── respawn_service.py   # 몬스터 리스폰 (threading.Timer)
│   │   ├── return_service.py    # 귀환 시스템 (BFS 여관 탐색)
│   │   ├── admin_service.py     # 관리자 기능
│   │   ├── guild_service.py     # 길드 관리
│   │   └── character_service.py # 캐릭터 관리
│   └── ws/chat.py           # WebSocket
├── seed.py                   # 기본 시드 (방/몬스터/아이템)
├── seed_items.py             # 아이템 시드
├── seed_martial_arts.py      # 무공 210종
├── seed_factions.py          # 세력 10종
├── seed_affixes.py           # 어픽스 60종
├── seed_quests.py            # 퀘스트 20종
├── seed_*.py                 # 각종 시드 스크립트
└── data/nakhwa.db            # SQLite 데이터베이스

frontend/
├── index.html                # 게임 UI (로그인·캐릭터선택·게임)
├── images/login-bg.jpg       # 로그인 배경 이미지
├── css/style.css             # 무협 다크테마 + 애니메이션 + 자동완성
└── js/game.js                # 클라이언트 로직 (자동완성·벚꽃·웹소켓)

launch.sh                     # 서버 런처 (screen 분리 실행)
README.md                     # 프로젝트 소개
GAME_RECORD.md                # 이 파일
GAME_BALANCE_REPORT.md        # 밸런스 분석 보고서
```

---

## 💎 인챈트 재료 드랍 시스템

- **강화석** (`CONS_ENCHANT_STONE`): 모든 몬스터 드랍. Lv.10=6% → Lv.250=30%(상한)
- **보호석** (`CONS_PROTECT_STONE`): 실패 시 강화 레벨 보호. Lv.10=1.5% → Lv.500=15%(상한)
- **고급강화석** (`CONS_ADVANCED_STONE`): 성공률 +20%. Lv.10=0.3% → Lv.500=8%(상한)

---

## 📜 버전 기록

| 버전 | 시기 | 내용 |
|------|------|------|
| **v0.1.0** | 2026.04 | JWT 인증, 캐릭터 생성(6종 출신), 방 이동(8방향), NPC 대화, 기본 전투 |
| **v0.2.0** | 2026.04 | 무공 210종(데미지/회복/버프/디버프/DOT), 경지 9단계 시스템, 퀘스트 |
| **v0.3.0** | 2026.04 | 세력(10종), 호감도, 강화 시스템(+15), 상점(구매/판매), 아이템 인벤토리 |
| **v0.4.0** | 2026.05 | 방 102개 대확장(만독림/혈뢰협곡 등 8지역), 아이템 350종+, 몬스터 145종+, NPC 70종+ |
| **v0.5.0** | 2026.05 | 길드(문파) 시스템(생성/가입/승인/추방/계급), 명성 버프 7단계, 창고/금고, 판매/분해/버리기, 레벨 999(지수함수 EXP) |
| **v0.6.0** | 2026.05 | 13슬롯 장비(WoW 스타일), 귀환 시스템(여관+귀환서3종), 방 151개(8신규지역), 아이템 531종, 몬스터 레벨제 드롭테이블, 인챈트 재료 전 몬스터 드랍, 관리자 강화 |
| **v0.6.2** | 2026.05 | 장비 레벨 제한(level_required), 가격 현실화(65,000은전), 몬스터 80~210 구간 13종 보강, bcrypt 4.0.1 호환 |
| **v0.6.3** | 2026.05 | 자동 전투(틱 기반)·무공 전투·도망 시스템(flee/도망), 전투 결과 요약 |
| **v0.6.4** | 2026.05 | 로그인 배경 이미지·타이틀 애니메이션·서버 8000 통합·벚꽃 입자·인게임 테마·지도(map)·캐릭터 스탯 80 자유분배·캐릭터 선택 UI·로그아웃·로그인 crash 버그 수정 |
| **v0.7.0** | 2026.05 | 선공 몬스터(is_aggro 57종)·리스폰 시스템(threading.Timer)·명령어 자동완성(50종+Tab+↑↓)·NPC 개성화(70명 직업/dialogue_options)·상점 NPC 연동·맵 이동 풍부화·배경 스토리·드롭 개선 |
| **v0.8.0** | 2026.05 | 디아블로2 접두/접미 시스템(60종)·와우식 퀘스트(20종+story/accept/complete)·대상 자동완성·지도 시각화·네트워크 오류 방어·로그인 Enter·WebSocket 복구·CSS/JS 대확장 |
| **v0.8.1** | 2026.05 | 🔍 **5개 버그 수정** (리스폰 미작동·인챈트 스탯 공유·JS 문법 오류 2건·talk 중복 쿼리)·🔄 리스폰 활성화·📦 인챈트 Enchantment 분리·🌐 장비 슬롯명 전면 한글화·⌨️ 입력창 자동 초기화 |

---

## 🎯 향후 계획

- [ ] PvP 시스템 (캐릭터 간 대결)
- [ ] 제작/채집 시스템
- [ ] 파티/공격대 시스템
- [ ] 보스 레이드 (인스턴스 던전)
- [ ] 퀘스트 시스템 확장

---

> *"무림의 역사는 한 줄기 낙화에서 시작되었다."*  
> — 낙화검심 개발팀, 2026년 5월
