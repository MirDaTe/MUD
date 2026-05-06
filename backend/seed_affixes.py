"""어픽스 시드 데이터 — 무협 테마 접두/접미 60종

실행: python seed_affixes.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.models.item_affix import ItemAffix


def seed_affixes():
    """어픽스 시드 데이터를 DB에 삽입합니다. 이미 있으면 스킵."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(ItemAffix).count() > 0:
        print("Affixes already seeded!")
        db.close()
        return

    print("Seeding 60 affixes...")

    affixes = [
        # ═══════════════ 접두어 (prefix) 40종 ═══════════════
        # 등급1 (흔함)
        {"id": 1, "code": "AFF_PREFIX_RUSTY", "name": "녹슨", "affix_type": "prefix", "tier": 1,
         "apply_to": ["weapon", "armor"], "stats": {"attack": -2}, "description": "녹이 슨"},
        {"id": 2, "code": "AFF_PREFIX_OLD", "name": "낡은", "affix_type": "prefix", "tier": 1,
         "apply_to": ["armor"], "stats": {"defense": -1}, "description": "오래되어 낡은"},
        {"id": 3, "code": "AFF_PREFIX_CRACKED", "name": "금이 간", "affix_type": "prefix", "tier": 1,
         "apply_to": ["armor"], "stats": {"hp": -5}, "description": "금이 가 있다"},
        {"id": 4, "code": "AFF_PREFIX_DIRTY", "name": "때 묻은", "affix_type": "prefix", "tier": 1,
         "apply_to": ["weapon", "armor"], "stats": {"gold_reward": 0.05}, "description": "때가 묻어있다"},
        {"id": 5, "code": "AFF_PREFIX_DULL", "name": "무딘", "affix_type": "prefix", "tier": 1,
         "apply_to": ["weapon"], "stats": {"attack": -3, "speed": 2}, "description": "날이 무디다"},

        # 등급2 (일반)
        {"id": 6, "code": "AFF_PREFIX_TEMPERED", "name": "단련된", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 3}, "description": "단련된"},
        {"id": 7, "code": "AFF_PREFIX_SHARP", "name": "예리한", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 5}, "description": "예리하게 벼려진"},
        {"id": 8, "code": "AFF_PREFIX_HEAVY", "name": "묵직한", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 4, "speed": -2}, "description": "무겁고 묵직한"},
        {"id": 9, "code": "AFF_PREFIX_KEEN", "name": "날카로운", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 5, "crit_rate": 0.02}, "description": "날카롭다"},
        {"id": 10, "code": "AFF_PREFIX_PRECISE", "name": "정교한", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 3, "speed": 3}, "description": "정교하게 만들어진"},
        {"id": 11, "code": "AFF_PREFIX_STEEL", "name": "강철", "affix_type": "prefix", "tier": 2,
         "apply_to": ["armor", "weapon"], "stats": {"defense": 5}, "description": "강철로 된"},
        {"id": 12, "code": "AFF_PREFIX_BRONZE", "name": "청동", "affix_type": "prefix", "tier": 2,
         "apply_to": ["armor", "weapon"], "stats": {"attack": 3, "defense": 2}, "description": "청동으로 된"},
        {"id": 13, "code": "AFF_PREFIX_TRAINEE", "name": "수련자의", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 4, "hp": 10}, "description": "수련자가 사용하던"},

        # 등급3 (고급)
        {"id": 14, "code": "AFF_PREFIX_DAGGER", "name": "비수의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 8, "crit_rate": 0.03}, "description": "비수처럼 날카로운"},
        {"id": 15, "code": "AFF_PREFIX_FIERCE_TIGER", "name": "맹호의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 10, "hp": 15}, "description": "맹호의 기운이 깃든"},
        {"id": 16, "code": "AFF_PREFIX_STORM", "name": "폭풍의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 7, "speed": 5}, "description": "폭풍을 머금은"},
        {"id": 17, "code": "AFF_PREFIX_BLOOD_WOLF", "name": "혈랑의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 12, "defense": -3}, "description": "피에 굶주린"},
        {"id": 18, "code": "AFF_PREFIX_THUNDER", "name": "뇌전의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 10, "crit_rate": 0.04}, "description": "번개를 품은"},
        {"id": 19, "code": "AFF_PREFIX_FIRE_DRAGON", "name": "화룡의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 9, "defense": 5}, "description": "화룡의 기운이 깃든"},
        {"id": 20, "code": "AFF_PREFIX_ICE", "name": "한빙의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 6, "speed": 3}, "description": "얼음처럼 차가운"},
        {"id": 21, "code": "AFF_PREFIX_DARK", "name": "암흑의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 11}, "description": "어둠을 머금은"},
        {"id": 22, "code": "AFF_PREFIX_WHITE_TIGER", "name": "백호의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 8, "speed": 4}, "description": "백호의 힘이 깃든"},
        {"id": 23, "code": "AFF_PREFIX_VERMILION", "name": "주작의", "affix_type": "prefix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 7, "crit_rate": 0.03, "hp": 20}, "description": "주작의 불꽃이 깃든"},

        # 등급4 (희귀)
        {"id": 24, "code": "AFF_PREFIX_RUIN", "name": "파멸의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 18, "crit_rate": 0.05}, "description": "파멸을 부르는"},
        {"id": 25, "code": "AFF_PREFIX_DESTROY", "name": "멸망의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 20}, "description": "모든 것을 멸하는"},
        {"id": 26, "code": "AFF_PREFIX_SKY_THUNDER", "name": "천둥의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 16, "speed": 6}, "description": "하늘의 천둥을 담은"},
        {"id": 27, "code": "AFF_PREFIX_HELL", "name": "지옥의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 15, "hp": 30}, "description": "지옥에서 온"},
        {"id": 28, "code": "AFF_PREFIX_HOLY", "name": "신성한", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 10, "defense": 10, "hp": 25}, "description": "신성한 힘이 깃든"},
        {"id": 29, "code": "AFF_PREFIX_LEGENDARY", "name": "전설의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 17, "speed": 4, "crit_rate": 0.04}, "description": "전설로 전해지는"},
        {"id": 30, "code": "AFF_PREFIX_CHAOS", "name": "혼돈의", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 15, "defense": 5, "speed": 3}, "description": "혼돈을 품은"},
        {"id": 31, "code": "AFF_PREFIX_SEALED", "name": "봉인된", "affix_type": "prefix", "tier": 4,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 13, "defense": 8}, "description": "봉인이 풀리지 않은"},

        # 등급5 (전설)
        {"id": 32, "code": "AFF_PREFIX_EXTINCT", "name": "절멸의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon"], "stats": {"attack": 25, "crit_rate": 0.07}, "description": "모든 것을 절멸시키는"},
        {"id": 33, "code": "AFF_PREFIX_DIVINE_BEAST", "name": "신수의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 22, "defense": 10, "hp": 40}, "description": "신수의 힘이 깃든"},
        {"id": 34, "code": "AFF_PREFIX_DEMON_EMPEROR", "name": "마황의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon"], "stats": {"attack": 30, "defense": -5}, "description": "마황이 사용하던"},
        {"id": 35, "code": "AFF_PREFIX_HEAVENLY_DEMON", "name": "천마의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon"], "stats": {"attack": 28, "speed": 8}, "description": "천마의 힘이 깃든"},
        {"id": 36, "code": "AFF_PREFIX_GHOST_FIRE", "name": "귀화의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 25, "defense": 12, "speed": 5}, "description": "귀신의 불꽃이 깃든"},
        {"id": 37, "code": "AFF_PREFIX_SOUL", "name": "영혼의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 20, "hp": 50, "mp": 30}, "description": "영혼이 깃든"},
        {"id": 38, "code": "AFF_PREFIX_IMMORTAL", "name": "불멸의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 18, "defense": 15, "hp": 60}, "description": "영원히 사라지지 않는"},
        {"id": 39, "code": "AFF_PREFIX_APOCALYPSE", "name": "종말의", "affix_type": "prefix", "tier": 5,
         "apply_to": ["weapon"], "stats": {"attack": 35}, "description": "종말을 가져오는"},
        {"id": 40, "code": "AFF_PREFIX_OBSIDIAN", "name": "흑요석", "affix_type": "prefix", "tier": 2,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 2, "defense": 3}, "description": "흑요석으로 된"},

        # ═══════════════ 접미사 (suffix) 20종 ═══════════════
        # 등급1
        {"id": 41, "code": "AFF_SUFFIX_TRAVELER", "name": "[여행자]", "affix_type": "suffix", "tier": 1,
         "apply_to": ["weapon", "armor"], "stats": {"speed": 2}, "description": "여행자의 흔적"},
        {"id": 42, "code": "AFF_SUFFIX_MERCHANT", "name": "[행상인]", "affix_type": "suffix", "tier": 1,
         "apply_to": ["weapon", "armor"], "stats": {"gold_reward": 0.10}, "description": "행상인의 물건"},
        {"id": 43, "code": "AFF_SUFFIX_ORPHAN", "name": "[고아]", "affix_type": "suffix", "tier": 1,
         "apply_to": ["weapon", "armor"], "stats": {"charm": 2}, "description": "고아의 유품"},

        # 등급2
        {"id": 44, "code": "AFF_SUFFIX_WARRIOR", "name": "[무인]", "affix_type": "suffix", "tier": 2,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 3, "defense": 2}, "description": "무인의 혼이 담긴"},
        {"id": 45, "code": "AFF_SUFFIX_STUDENT", "name": "[수련생]", "affix_type": "suffix", "tier": 2,
         "apply_to": ["weapon", "armor"], "stats": {"hp": 10, "mp": 5}, "description": "수련생의 노력"},
        {"id": 46, "code": "AFF_SUFFIX_WANDERER", "name": "[방랑자]", "affix_type": "suffix", "tier": 2,
         "apply_to": ["weapon", "armor"], "stats": {"speed": 4}, "description": "방랑자의 벗"},
        {"id": 47, "code": "AFF_SUFFIX_HUNTER", "name": "[사냥꾼]", "affix_type": "suffix", "tier": 2,
         "apply_to": ["weapon"], "stats": {"attack": 4}, "description": "사냥꾼의 도구"},

        # 등급3
        {"id": 48, "code": "AFF_SUFFIX_ELITE", "name": "[정예]", "affix_type": "suffix", "tier": 3,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 6, "defense": 4}, "description": "정예의 장비"},
        {"id": 49, "code": "AFF_SUFFIX_HERO", "name": "[용사]", "affix_type": "suffix", "tier": 3,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 8, "hp": 20}, "description": "용사의 유산"},
        {"id": 50, "code": "AFF_SUFFIX_SAGE", "name": "[현자]", "affix_type": "suffix", "tier": 3,
         "apply_to": ["weapon", "armor"], "stats": {"mp": 15, "insight": 3}, "description": "현자의 지혜"},
        {"id": 51, "code": "AFF_SUFFIX_ASSASSIN", "name": "[암살자]", "affix_type": "suffix", "tier": 3,
         "apply_to": ["weapon"], "stats": {"attack": 8, "speed": 6, "defense": -3}, "description": "암살자의 도구"},
        {"id": 52, "code": "AFF_SUFFIX_GUARDIAN", "name": "[수호자]", "affix_type": "suffix", "tier": 3,
         "apply_to": ["weapon", "armor"], "stats": {"defense": 10, "hp": 25}, "description": "수호자의 의지"},

        # 등급4
        {"id": 53, "code": "AFF_SUFFIX_MASTER", "name": "[고수]", "affix_type": "suffix", "tier": 4,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 12, "defense": 8, "speed": 3}, "description": "고수의 혼"},
        {"id": 54, "code": "AFF_SUFFIX_SWORD_IMMORTAL", "name": "[검선]", "affix_type": "suffix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 18, "speed": 5, "crit_rate": 0.03}, "description": "검선의 검"},
        {"id": 55, "code": "AFF_SUFFIX_SLAYER", "name": "[살수]", "affix_type": "suffix", "tier": 4,
         "apply_to": ["weapon"], "stats": {"attack": 16, "speed": 8, "crit_rate": 0.04}, "description": "살수의 칼날"},
        {"id": 56, "code": "AFF_SUFFIX_LORD", "name": "[군주]", "affix_type": "suffix", "tier": 4,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 15, "defense": 10, "hp": 30}, "description": "군주의 위엄"},

        # 등급5
        {"id": 57, "code": "AFF_SUFFIX_BEST_UNDER_HEAVEN", "name": "[천하제일]", "affix_type": "suffix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 25, "defense": 15, "speed": 5}, "description": "천하제일의 증표"},
        {"id": 58, "code": "AFF_SUFFIX_MURIM_SUPREME", "name": "[무림지존]", "affix_type": "suffix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 30, "crit_rate": 0.05, "hp": 50}, "description": "무림지존의 상징"},
        {"id": 59, "code": "AFF_SUFFIX_IMMORTAL_BEING", "name": "[신선]", "affix_type": "suffix", "tier": 5,
         "apply_to": ["weapon", "armor"], "stats": {"attack": 20, "defense": 12, "mp": 40, "speed": 6}, "description": "신선의 도구"},
        {"id": 60, "code": "AFF_SUFFIX_DEMON_KING", "name": "[마왕]", "affix_type": "suffix", "tier": 5,
         "apply_to": ["weapon"], "stats": {"attack": 35, "hp": 60, "defense": -10}, "description": "마왕의 유물"},
    ]

    for a in affixes:
        db.add(ItemAffix(**a))
    db.commit()
    print(f"Seeded {len(affixes)} affixes!")
    db.close()


if __name__ == "__main__":
    seed_affixes()
