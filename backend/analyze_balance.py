#!/usr/bin/env python3
"""게임 밸런스 분석 스크립트 - nakhwa.db 통계 추출 및 보고서 생성"""
import sqlite3
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "nakhwa.db")
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GAME_BALANCE_REPORT.md")

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def analyze_rooms(conn):
    rows = conn.execute("SELECT * FROM rooms").fetchall()
    total = len(rows)
    regions = Counter(r["region"] for r in rows)
    safe_count = sum(1 for r in rows if r["is_safe"])
    inn_count = sum(1 for r in rows if r["is_inn"])
    return {
        "total": total,
        "regions": dict(regions),
        "safe_count": safe_count,
        "inn_count": inn_count,
    }

def analyze_items(conn):
    rows = conn.execute("SELECT * FROM items").fetchall()
    total = len(rows)
    type_counts = Counter(r["item_type"] for r in rows)
    slot_counts = Counter(r["slot"] for r in rows if r["slot"])
    rarity_counts = Counter(r["rarity"] for r in rows if r["rarity"] is not None)

    prices = [r["price"] for r in rows if r["price"] is not None and r["price"] > 0]
    price_ranges = {
        "0~100": 0, "101~500": 0, "501~1000": 0, "1001~5000": 0,
        "5001~10000": 0, "10001~50000": 0, "50001+": 0
    }
    for p in prices:
        if p <= 100: price_ranges["0~100"] += 1
        elif p <= 500: price_ranges["101~500"] += 1
        elif p <= 1000: price_ranges["501~1000"] += 1
        elif p <= 5000: price_ranges["1001~5000"] += 1
        elif p <= 10000: price_ranges["5001~10000"] += 1
        elif p <= 50000: price_ranges["10001~50000"] += 1
        else: price_ranges["50001+"] += 1

    return {
        "total": total,
        "type_counts": dict(type_counts),
        "slot_counts": dict(slot_counts),
        "rarity_counts": dict(rarity_counts),
        "price_stats": {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "avg": round(sum(prices)/len(prices), 1) if prices else 0,
            "median": sorted(prices)[len(prices)//2] if prices else 0,
        },
        "price_ranges": price_ranges,
    }

def analyze_monsters(conn):
    rows = conn.execute("SELECT * FROM monsters").fetchall()
    total = len(rows)

    level_dist = defaultdict(int)
    for r in rows:
        ml = r["min_level"] or 0
        bracket = (ml // 20) * 20
        level_dist[f"{bracket}~{bracket+19}"] += 1

    has_drop = sum(1 for r in rows if r["drop_table"] and r["drop_table"] not in ("null", "[]", "{}", ""))
    exps = [r["exp_reward"] or 0 for r in rows]
    golds = [r["gold_reward"] or 0 for r in rows]
    boss_count = sum(1 for r in rows if r["is_boss"])
    hp_list = [(r["hp"] or 0, r["max_hp"] or 0) for r in rows]
    atk_list = [r["attack"] or 0 for r in rows]
    defense_list = [r["defense"] or 0 for r in rows]
    avg_hp = round(sum(max(h, m) for h, m in hp_list) / max(len(hp_list), 1), 1)

    return {
        "total": total,
        "boss_count": boss_count,
        "level_distribution": dict(sorted(level_dist.items(), key=lambda x: int(x[0].split("~")[0]))),
        "has_drop_table": has_drop,
        "no_drop_table": total - has_drop,
        "exp_reward": {
            "min": min(exps) if exps else 0,
            "max": max(exps) if exps else 0,
            "avg": round(sum(exps)/len(exps), 1) if exps else 0,
        },
        "gold_reward": {
            "min": min(golds) if golds else 0,
            "max": max(golds) if golds else 0,
            "avg": round(sum(golds)/len(golds), 1) if golds else 0,
        },
        "avg_hp": avg_hp,
        "avg_attack": round(sum(atk_list)/max(len(atk_list), 1), 1),
        "avg_defense": round(sum(defense_list)/max(len(defense_list), 1), 1),
    }

def analyze_weapons(conn):
    rows = conn.execute("SELECT * FROM items WHERE item_type = 'weapon'").fetchall()
    total = len(rows)
    slot_counts = Counter(r["slot"] for r in rows if r["slot"])
    type_counts = Counter(r["weapon_type"] for r in rows if r["weapon_type"])

    attacks = []
    prices = []
    rarities = Counter()
    for r in rows:
        rarities[r["rarity"]] += 1
        if r["stats"]:
            try:
                stats = json.loads(r["stats"]) if isinstance(r["stats"], str) else r["stats"]
                if isinstance(stats, dict):
                    atk = stats.get("attack") or stats.get("min_attack") or stats.get("damage") or 0
                    attacks.append(atk)
            except (json.JSONDecodeError, TypeError):
                pass
        if r["price"]:
            prices.append(r["price"])

    # min_level requirement distribution
    level_req = []
    for r in rows:
        if r["stats"]:
            try:
                stats = json.loads(r["stats"]) if isinstance(r["stats"], str) else r["stats"]
                if isinstance(stats, dict):
                    lr = stats.get("min_level") or stats.get("required_level") or stats.get("level") or 0
                    level_req.append(lr)
            except (json.JSONDecodeError, TypeError):
                level_req.append(0)

    level_brackets = defaultdict(int)
    for l in level_req:
        b = (l // 20) * 20
        level_brackets[f"{b}~{b+19}"] += 1

    return {
        "total": total,
        "slot_counts": dict(slot_counts),
        "weapon_type_counts": dict(type_counts),
        "rarity_counts": dict(rarities),
        "avg_attack": round(sum(attacks)/max(len(attacks), 1), 1),
        "min_attack": min(attacks) if attacks else 0,
        "max_attack": max(attacks) if attacks else 0,
        "avg_price": round(sum(prices)/max(len(prices), 1), 1),
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "level_distribution": dict(sorted(level_brackets.items(), key=lambda x: int(x[0].split("~")[0]))),
    }

def analyze_armors(conn):
    rows = conn.execute("SELECT * FROM items WHERE item_type = 'armor'").fetchall()
    total = len(rows)
    slot_counts = Counter(r["slot"] for r in rows if r["slot"])

    defenses = []
    prices = []
    rarities = Counter()
    for r in rows:
        rarities[r["rarity"]] += 1
        if r["stats"]:
            try:
                stats = json.loads(r["stats"]) if isinstance(r["stats"], str) else r["stats"]
                if isinstance(stats, dict):
                    defense = stats.get("defense") or stats.get("armor") or stats.get("def") or 0
                    defenses.append(defense)
            except (json.JSONDecodeError, TypeError):
                pass
        if r["price"]:
            prices.append(r["price"])

    return {
        "total": total,
        "slot_counts": dict(slot_counts),
        "rarity_counts": dict(rarities),
        "avg_defense": round(sum(defenses)/max(len(defenses), 1), 1),
        "min_defense": min(defenses) if defenses else 0,
        "max_defense": max(defenses) if defenses else 0,
        "avg_price": round(sum(prices)/max(len(prices), 1), 1),
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
    }

def analyze_consumables(conn):
    rows = conn.execute("SELECT * FROM items WHERE item_type = 'consumable'").fetchall()
    total = len(rows)
    heal_amounts = []
    return_items = []

    for r in rows:
        if r["effects"]:
            try:
                effects = json.loads(r["effects"]) if isinstance(r["effects"], str) else r["effects"]
                if isinstance(effects, dict):
                    heal = effects.get("heal") or effects.get("heal_amount") or effects.get("hp_restore") or effects.get("restore_hp") or 0
                    heal_amounts.append(heal)
            except (json.JSONDecodeError, TypeError):
                pass
        # Check for return scrolls / teleport items
        name = (r["name"] or "").lower()
        desc = (r["description"] or "").lower()
        code = (r["code"] or "").lower()
        if any(kw in name or kw in desc or kw in code for kw in ["귀환", "return", "teleport", "귀환서", "순간이동"]):
            return_items.append(r["name"])

    prices = [r["price"] or 0 for r in rows]
    heal_dist = {"0~50": 0, "51~100": 0, "101~200": 0, "201~500": 0, "501~1000": 0, "1001+": 0}
    for h in heal_amounts:
        if h <= 50: heal_dist["0~50"] += 1
        elif h <= 100: heal_dist["51~100"] += 1
        elif h <= 200: heal_dist["101~200"] += 1
        elif h <= 500: heal_dist["201~500"] += 1
        elif h <= 1000: heal_dist["501~1000"] += 1
        else: heal_dist["1001+"] += 1

    return {
        "total": total,
        "heal_distribution": heal_dist,
        "return_items": return_items,
        "avg_price": round(sum(prices)/max(len(prices), 1), 1),
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
    }

def analyze_drop_tables(conn):
    """Analyze all drop tables from monsters"""
    rows = conn.execute("SELECT id, name, min_level, drop_table FROM monsters WHERE drop_table IS NOT NULL AND drop_table NOT IN ('null','[]','{}','')").fetchall()

    drop_rates = []  # list of (monster_name, item_code, rate)
    for r in rows:
        try:
            dt = json.loads(r["drop_table"]) if isinstance(r["drop_table"], str) else r["drop_table"]
            if isinstance(dt, list):
                for entry in dt:
                    if isinstance(entry, dict):
                        rate = entry.get("rate") or entry.get("chance") or entry.get("probability") or 0
                        item = entry.get("item") or entry.get("item_code") or entry.get("code") or "unknown"
                        drop_rates.append((r["name"], item, float(rate)))
        except (json.JSONDecodeError, TypeError):
            pass

    if not drop_rates:
        return {"total_with_drops": 0, "avg_rate": 0, "low_rates": 0, "high_rates": 0}

    rates = [d[2] for d in drop_rates]
    return {
        "total_with_drops": len(rows),
        "total_drop_entries": len(drop_rates),
        "avg_rate": round(sum(rates)/len(rates), 3),
        "min_rate": min(rates),
        "max_rate": max(rates),
        "low_rate_count": sum(1 for r in rates if r < 0.01),
        "high_rate_count": sum(1 for r in rates if r > 0.5),
    }

def analyze_equipment_level_coverage(conn):
    """Check if weapons/armors cover all level ranges properly"""
    items = conn.execute("SELECT * FROM items WHERE item_type IN ('weapon', 'armor')").fetchall()

    level_items = defaultdict(lambda: {"weapon": 0, "armor": 0})
    for r in items:
        try:
            stats = json.loads(r["stats"]) if isinstance(r["stats"], str) else r["stats"]
            if isinstance(stats, dict):
                lv = stats.get("min_level") or stats.get("required_level") or stats.get("level") or 0
                b = (lv // 50) * 50
                if r["item_type"] == "weapon":
                    level_items[f"{b}~{b+49}"]["weapon"] += 1
                else:
                    level_items[f"{b}~{b+49}"]["armor"] += 1
        except (json.JSONDecodeError, TypeError):
            pass

    return dict(sorted(level_items.items(), key=lambda x: int(x[0].split("~")[0])))

def check_balance_gaps(rooms_stats, items_stats, monsters_stats, weapons_stats, armors_stats, consumables_stats, drop_stats, equip_coverage):
    """Generate balance assessment"""
    issues = []
    warnings = []
    goods = []

    # 1. Monster level distribution check
    monster_levels = monsters_stats["level_distribution"]
    total_monsters = monsters_stats["total"]
    has_low = any(int(k.split("~")[0]) < 50 for k in monster_levels.keys())
    has_mid = any(50 <= int(k.split("~")[0]) < 200 for k in monster_levels.keys())
    has_high = any(int(k.split("~")[0]) >= 200 for k in monster_levels.keys())
    if not has_low:
        issues.append("⚠️ **저레벨(1~49) 구간 몬스터 부재**: 초보자용 몬스터가 전혀 없습니다.")
    if not has_high:
        issues.append("⚠️ **고레벨(200+) 구간 몬스터 부재**: 고레벨 플레이어를 위한 사냥터가 없습니다.")

    # Check level gaps > 100 levels
    sorted_levels = sorted([int(k.split("~")[0]) for k in monster_levels.keys()])
    for i in range(len(sorted_levels)-1):
        gap = sorted_levels[i+1] - sorted_levels[i]
        if gap > 100:
            warnings.append(f"⚠️ 레벨 {sorted_levels[i]}~{sorted_levels[i+1]} 사이에 {gap}레벨 공백 구간이 있습니다.")

    # 2. Equipment coverage
    if equip_coverage:
        covered = [int(k.split("~")[0]) for k in equip_coverage.keys()]
        max_covered = max(covered) if covered else 0
        if max_covered < 200:
            issues.append(f"⚠️ **장비 커버리지 부족**: 장비의 최고 요구 레벨이 {max_covered}레벨에 불과합니다. 고레벨 장비가 필요합니다.")

    # 3. Drop rate check
    if drop_stats["total_with_drops"] > 0:
        drop_rate = drop_stats["avg_rate"]
        if drop_rate < 0.01:
            warnings.append(f"⚠️ **평균 드랍률이 매우 낮음**: 평균 {drop_rate:.2%}로, 플레이어가 아이템을 거의 획득하지 못할 수 있습니다.")
        elif drop_rate > 0.30:
            warnings.append(f"⚠️ **평균 드랍률이 높음**: 평균 {drop_rate:.2%}로, 아이템 가치가 하락할 수 있습니다.")

        if drop_stats["high_rate_count"] > 3:
            warnings.append(f"⚠️ 드랍률 50% 이상인 아이템이 {drop_stats['high_rate_count']}개 있습니다.")
    else:
        issues.append("⚠️ **드랍 테이블 전무**: 몬스터가 아이템을 드랍하지 않습니다. 사냥 동기부여를 위해 드랍 테이블 추가가 필요합니다.")

    # 4. Item total check
    if items_stats["total"] < 20:
        issues.append(f"⚠️ **아이템 부족**: 전체 아이템이 {items_stats['total']}개로 너무 적습니다. 최소 50개 이상 권장합니다.")
    elif items_stats["total"] < 50:
        warnings.append(f"⚠️ 아이템이 {items_stats['total']}개로 다소 부족합니다.")

    # 5. Consumable price check
    if consumables_stats["avg_price"] > 5000:
        warnings.append(f"⚠️ 소모품 평균 가격이 {consumables_stats['avg_price']:.0f}원으로 높습니다.")
    elif consumables_stats["avg_price"] > 10000:
        issues.append(f"⚠️ **소모품 가격 과다**: 평균 {consumables_stats['avg_price']:.0f}원으로 신규 플레이어 접근이 어렵습니다.")

    # 6. Inn / Safe zone check
    if rooms_stats["safe_count"] < 2:
        warnings.append(f"⚠️ 안전지역이 {rooms_stats['safe_count']}개로 적습니다. 최소 시작 마을 + 1곳 이상 권장합니다.")
    if rooms_stats["inn_count"] < 1:
        issues.append("⚠️ **여관 부재**: 휴식/회복이 가능한 여관이 없습니다.")

    # 7. Equipment slot coverage check
    for slot_type in ["weapon", "armor"]:
        slot_data = weapons_stats if slot_type == "weapon" else armors_stats
        if slot_data["total"] < 5:
            warnings.append(f"⚠️ {slot_type} 아이템이 {slot_data['total']}개로 부족합니다.")

    # Positive findings
    if total_monsters >= 10:
        goods.append(f"✅ 몬스터 {total_monsters}종 보유 - 다양성 확보")
    if items_stats["total"] >= 30:
        goods.append(f"✅ 아이템 {items_stats['total']}종 보유 - 기본 아이템 체계 구축")
    if rooms_stats["total"] >= 5:
        goods.append(f"✅ 방 {rooms_stats['total']}개 - 기본 맵 구성 완료")
    if consumables_stats["total"] > 0:
        goods.append(f"✅ 소모품 {consumables_stats['total']}종 - 회복 체계 존재")
    if monsters_stats["boss_count"] > 0:
        goods.append(f"✅ 보스 몬스터 {monsters_stats['boss_count']}종 - 도전 콘텐츠 존재")
    if rooms_stats["regions"]:
        goods.append(f"✅ 지역 {len(rooms_stats['regions'])}곳 - 지역별 콘텐츠 구분")

    return {"issues": issues, "warnings": warnings, "goods": goods}


def generate_report():
    conn = connect()

    print("분석 중: rooms...")
    rooms_stats = analyze_rooms(conn)
    print("분석 중: items...")
    items_stats = analyze_items(conn)
    print("분석 중: monsters...")
    monsters_stats = analyze_monsters(conn)
    print("분석 중: weapons...")
    weapons_stats = analyze_weapons(conn)
    print("분석 중: armors...")
    armors_stats = analyze_armors(conn)
    print("분석 중: consumables...")
    consumables_stats = analyze_consumables(conn)
    print("분석 중: drop tables...")
    drop_stats = analyze_drop_tables(conn)
    print("분석 중: equipment level coverage...")
    equip_coverage = analyze_equipment_level_coverage(conn)

    conn.close()

    print("밸런스 진단 중...")
    balance = check_balance_gaps(
        rooms_stats, items_stats, monsters_stats,
        weapons_stats, armors_stats, consumables_stats,
        drop_stats, equip_coverage
    )

    # Overall grade
    issue_count = len(balance["issues"])
    warning_count = len(balance["warnings"])
    if issue_count == 0 and warning_count <= 2:
        overall = "😊 **양호** - 게임 진행에 큰 무리가 없는 상태입니다."
    elif issue_count <= 1 and warning_count <= 4:
        overall = "😐 **보통** - 몇 가지 개선이 필요한 부분이 있습니다."
    elif issue_count <= 3:
        overall = "😟 **주의** - 밸런스에 상당한 문제가 있어 수정이 필요합니다."
    else:
        overall = "🚨 **심각** - 기초적인 게임 밸런스가 붕괴된 상태입니다. 광범위한 수정이 필요합니다."

    # --- BUILD REPORT ---
    report = f"""# 🎮 게임 밸런스 분석 보고서

> **생성일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **DB 파일**: `data/nakhwa.db`
> **분석 도구**: `analyze_balance.py`

---

## 📊 종합 진단

**종합 상태**: {overall}

### 주요 문제점 ({issue_count}건)
"""
    for i, iss in enumerate(balance["issues"], 1):
        report += f"{i}. {iss}\n"

    report += f"""### 주의 사항 ({warning_count}건)
"""
    for i, w in enumerate(balance["warnings"], 1):
        report += f"{i}. {w}\n"

    report += f"""### 긍정적 요소 ({len(balance['goods'])}건)
"""
    for i, g in enumerate(balance["goods"], 1):
        report += f"{i}. {g}\n"

    # --- 1. Rooms ---
    report += f"""
---

## 1. 🏠 방 (Rooms)

| 항목 | 값 |
|------|-----|
| 총 방 개수 | **{rooms_stats['total']}** 개 |
| 안전지역 개수 | **{rooms_stats['safe_count']}** 개 |
| 여관 개수 | **{rooms_stats['inn_count']}** 개 |
"""

    if rooms_stats["regions"]:
        report += "\n### 지역별 분포\n\n"
        for region, count in sorted(rooms_stats["regions"].items(), key=lambda x: -x[1]):
            report += f"- **{region}**: {count}개\n"
    else:
        report += "\n> 지역 정보가 설정되지 않았습니다.\n"

    # --- 2. Items ---
    report += f"""
---

## 2. 📦 아이템 (Items)

| 항목 | 값 |
|------|-----|
| 총 아이템 개수 | **{items_stats['total']}** 개 |

### 타입별 분포

| 타입 | 개수 |
|------|------|
"""
    for t, c in sorted(items_stats["type_counts"].items(), key=lambda x: -x[1]):
        report += f"| {t} | **{c}** 개 |\n"

    if items_stats["slot_counts"]:
        report += "\n### 슬롯별 분포\n\n"
        for s, c in sorted(items_stats["slot_counts"].items(), key=lambda x: -x[1]):
            report += f"- **{s}**: {c}개\n"

    if items_stats["rarity_counts"]:
        report += "\n### 레어도별 분포\n\n"
        rarity_names = {1: "일반", 2: "고급", 3: "희귀", 4: "영웅", 5: "전설", 6: "신화", 7: "유니크"}
        for r, c in sorted(items_stats["rarity_counts"].items()):
            rname = rarity_names.get(r, f"R{r}")
            report += f"- **{rname}** (R{r}): {c}개\n"

    report += f"""
### 가격 통계

- 최소 가격: **{items_stats['price_stats']['min']:,}** 원
- 최대 가격: **{items_stats['price_stats']['max']:,}** 원
- 평균 가격: **{items_stats['price_stats']['avg']:,.1f}** 원
- 중간값: **{items_stats['price_stats']['median']:,}** 원

### 가격대 분포

"""
    for prange, cnt in items_stats["price_ranges"].items():
        bar = "█" * max(1, cnt)
        report += f"- {prange}원: {cnt}개 {bar}\n"

    # --- 3. Monsters ---
    report += f"""
---

## 3. 👹 몬스터 (Monsters)

| 항목 | 값 |
|------|-----|
| 총 몬스터 수 | **{monsters_stats['total']}** 마리 |
| 보스 몬스터 수 | **{monsters_stats['boss_count']}** 마리 |
| 드랍테이블 보유 | **{monsters_stats['has_drop_table']}** 마리 |
| 드랍테이블 없음 | **{monsters_stats['no_drop_table']}** 마리 |

### 전투 스탯 평균

- 평균 HP: **{monsters_stats['avg_hp']:,}**
- 평균 공격력: **{monsters_stats['avg_attack']:,}**
- 평균 방어력: **{monsters_stats['avg_defense']:,}**

### 보상 통계

- 경험치: 최소 **{monsters_stats['exp_reward']['min']:,}** / 최대 **{monsters_stats['exp_reward']['max']:,}** / 평균 **{monsters_stats['exp_reward']['avg']:,.1f}**
- 골드: 최소 **{monsters_stats['gold_reward']['min']:,}** / 최대 **{monsters_stats['gold_reward']['max']:,}** / 평균 **{monsters_stats['gold_reward']['avg']:,.1f}**

### 레벨대별 분포

"""
    for bracket, count in monsters_stats["level_distribution"].items():
        bar = "█" * max(1, count)
        report += f"- **{bracket}** 레벨: {count}마리 {bar}\n"

    # --- 4. Weapons ---
    report += f"""
---

## 4. ⚔️ 무기 (Weapons)

| 항목 | 값 |
|------|-----|
| 총 무기 개수 | **{weapons_stats['total']}** 개 |

### 슬롯별

"""
    for s, c in sorted(weapons_stats["slot_counts"].items(), key=lambda x: -x[1]):
        report += f"- **{s}**: {c}개\n"

    if weapons_stats["weapon_type_counts"]:
        report += "\n### 무기 유형별\n\n"
        for t, c in sorted(weapons_stats["weapon_type_counts"].items(), key=lambda x: -x[1]):
            report += f"- **{t}**: {c}개\n"

    report += f"""
### 공격력 통계

- 최소: **{weapons_stats['min_attack']}** / 최대: **{weapons_stats['max_attack']}** / 평균: **{weapons_stats['avg_attack']}**

### 가격 통계

- 최소: **{weapons_stats['min_price']:,}** 원 / 최대: **{weapons_stats['max_price']:,}** 원 / 평균: **{weapons_stats['avg_price']:,.1f}** 원

### 레어도별 분포

"""
    for r, c in sorted(weapons_stats["rarity_counts"].items()):
        rname = rarity_names.get(r, f"R{r}")
        report += f"- **{rname}**: {c}개\n"

    if weapons_stats["level_distribution"]:
        report += "\n### 요구 레벨대별 분포\n\n"
        for bracket, count in weapons_stats["level_distribution"].items():
            report += f"- **{bracket}**: {count}개\n"

    # --- 5. Armors ---
    report += f"""
---

## 5. 🛡️ 방어구 (Armors)

| 항목 | 값 |
|------|-----|
| 총 방어구 개수 | **{armors_stats['total']}** 개 |

### 슬롯별

"""
    for s, c in sorted(armors_stats["slot_counts"].items(), key=lambda x: -x[1]):
        report += f"- **{s}**: {c}개\n"

    report += f"""
### 방어력 통계

- 최소: **{armors_stats['min_defense']}** / 최대: **{armors_stats['max_defense']}** / 평균: **{armors_stats['avg_defense']}**

### 가격 통계

- 최소: **{armors_stats['min_price']:,}** 원 / 최대: **{armors_stats['max_price']:,}** 원 / 평균: **{armors_stats['avg_price']:,.1f}** 원

### 레어도별 분포

"""
    for r, c in sorted(armors_stats["rarity_counts"].items()):
        rname = rarity_names.get(r, f"R{r}")
        report += f"- **{rname}**: {c}개\n"

    # --- 6. Consumables ---
    report += f"""
---

## 6. 🧪 소모품 (Consumables)

| 항목 | 값 |
|------|-----|
| 총 소모품 개수 | **{consumables_stats['total']}** 개 |

### 가격 통계

- 최소: **{consumables_stats['min_price']:,}** 원 / 최대: **{consumables_stats['max_price']:,}** 원 / 평균: **{consumables_stats['avg_price']:,.1f}** 원

### 회복량 분포

"""
    for hrange, cnt in consumables_stats["heal_distribution"].items():
        bar = "█" * max(1, cnt)
        report += f"- {hrange}: {cnt}개 {bar}\n"

    if consumables_stats["return_items"]:
        report += "\n### 귀환/이동 관련 아이템\n\n"
        for item in consumables_stats["return_items"]:
            report += f"- **{item}**\n"
    else:
        report += "\n> 귀환서/이동 관련 아이템이 발견되지 않았습니다.\n"

    # --- 7. Drop Table ---
    report += f"""
---

## 7. 🎲 드랍 테이블 분석

| 항목 | 값 |
|------|-----|
| 드랍테이블 보유 몬스터 | **{drop_stats['total_with_drops']}** 마리 |
| 전체 드랍 항목 수 | **{drop_stats['total_drop_entries']}** 개 |
| 평균 드랍률 | **{drop_stats['avg_rate']:.3f}** ({drop_stats['avg_rate']:.1%}) |
| 최소 드랍률 | **{drop_stats['min_rate']:.4f}** |
| 최대 드랍률 | **{drop_stats['max_rate']:.2f}** |
| 1% 미만 드랍 항목 | **{drop_stats['low_rate_count']}** 개 |
| 50% 이상 드랍 항목 | **{drop_stats['high_rate_count']}** 개 |
"""

    # --- 8. Equipment Coverage ---
    report += f"""
---

## 8. 📐 장비 레벨 커버리지

"""
    if equip_coverage:
        for bracket, counts in equip_coverage.items():
            w = counts["weapon"]
            a = counts["armor"]
            report += f"- **{bracket}**: 무기 {w}개 / 방어구 {a}개\n"
    else:
        report += "> 장비에 레벨 요구사항이 설정되지 않았습니다.\n"

    # --- 9. Recommendations ---
    report += """
---

## 9. 🔧 개선 권장사항

"""
    recs = []

    if monsters_stats["total"] < 5:
        recs.append("1. **몬스터 추가**: 최소 20종 이상 몬스터를 레벨대별로 균등하게 배치하세요.")
    else:
        recs.append("1. **몬스터 레벨 분포 조정**: 1~999레벨 구간을 약 15~20개 구간으로 나누고 각 구간에 최소 2종 이상 배치하세요.")

    if monsters_stats["no_drop_table"] > 0:
        recs.append("2. **드랍 테이블 보강**: 모든 몬스터에 최소 1개 이상의 드랍 아이템을 설정하세요. 드랍률은 0.05~0.30 (5%~30%) 범위를 권장합니다.")

    if items_stats["total"] < 30:
        recs.append(f"3. **아이템 확충**: 현재 {items_stats['total']}개에서 최소 50개 이상으로 확대하세요. 각 타입별로 균형 있게 추가해야 합니다.")

    if weapons_stats["total"] < 10:
        recs.append("4. **무기 다양화**: 각 슬롯(mainhand, offhand, twohand)별로 최소 3종 이상, 레벨대별로 점진적인 성능 향상이 있도록 설계하세요.")

    if armors_stats["total"] < 10:
        recs.append("5. **방어구 다양화**: 각 슬롯(head, chest, legs, feet 등)별로 최소 2종 이상 필요합니다.")

    if consumables_stats["total"] < 3:
        recs.append("6. **소모품 확충**: HP 회복, MP 회복, 상태이상 치료 등 최소 5종 이상의 소모품이 필요합니다.")

    if not consumables_stats["return_items"]:
        recs.append("7. **귀환서 추가**: 마을 귀환, 특정 지역 이동 등 편의성 아이템을 추가하세요.")

    recs.append("8. **가격 곡선 설계**: 레벨이 오를수록 장비 가격이 기하급수적으로 증가하는 곡선을 설정하세요. (예: 1레벨 100원 → 100레벨 10,000원 → 500레벨 500,000원)")
    recs.append("9. **경험치 곡선 검토**: 몬스터 레벨과 exp_reward가 비례 관계를 가지는지 확인하세요. 너무 평탄하면 동기부여가 떨어집니다.")
    recs.append("10. **보스 몬스터 보강**: 각 레벨 구간마다 보스 몬스터를 1종씩 배치하여 도전 요소를 제공하세요.")

    for rec in recs:
        report += rec + "\n\n"

    # --- Footer ---
    report += """---

> *본 보고서는 자동 생성되었습니다. 게임 기획 의도에 따라 조정이 필요할 수 있습니다.*
"""

    return report


if __name__ == "__main__":
    print("게임 밸런스 분석 시작...")
    report = generate_report()
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"보고서 생성 완료: {REPORT_PATH}")
    print(f"보고서 크기: {len(report):,} bytes")
