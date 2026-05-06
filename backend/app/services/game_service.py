"""게임 명령어 처리 서비스 (길드, 인벤토리, 판매/분해, 레벨 999, 영어/한글 병행)"""
import random
import math
from typing import Optional
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.room import Room
from ..models.npc import NPC
from ..models.monster import Monster
from ..models.martial_art import MartialArt
from ..models.character_martial_art import CharacterMartialArt
from ..models.item import Item as ItemModel
from ..models.inventory import Inventory
from ..models.quest import Quest
from ..models.character_quest import CharacterQuest
from ..models.affection import Affection
from ..models.shop import Shop
from ..models.faction import Faction
from ..models.character_faction import CharacterFaction
from ..models.user import User
from .combat_service import attack_monster, cast_martial_art, meditate as meditate_service, check_stage_up
from .enchant_service import upgrade_item
from .admin_service import is_admin, admin_set_stat, admin_teleport, admin_give_item, get_all_users, get_all_characters, admin_list_rooms, admin_list_items, admin_get_item, admin_give_item_by_code
from .guild_service import create_guild, join_guild, approve_application, leave_guild, kick_member, change_rank, get_guild_info, add_reputation, add_guild_gold, withdraw_guild_gold, deposit_to_storage, withdraw_from_storage, get_storage_contents
from .inventory_service import sell_item, dismantle_item, discard_item, equip_status, unequip, equip_item, unequip_item
from .return_service import set_return_point, use_return_scroll, use_town_scroll


def parse_command(cmd):
    p = cmd.strip().split(maxsplit=1)
    return (p[0].lower() if p else "", p[1] if len(p)>1 else "")


def normalize_verb(v, r):
    m={
        "l":"look","look":"look","주변":"look","보기":"look","살펴보다":"look",
        "n":"north","north":"north","북":"north","북쪽":"north",
        "s":"south","south":"south","남":"south","남쪽":"south",
        "e":"east","east":"east","동":"east","동쪽":"east",
        "w":"west","west":"west","서":"west","서쪽":"west",
        "u":"up","up":"up","위":"up","올라가다":"up",
        "d":"down","down":"down","아래":"down","내려가다":"down",
        "enter":"enter","in":"enter","들어가다":"enter","입장":"enter",
        "out":"out","exit":"out","나가다":"out","퇴장":"out",
        "go":"go","이동":"go","가다":"go",
        "attack":"attack","공격":"attack","공":"attack","때리다":"attack",
        "cast":"cast","무공":"cast","시전":"cast",
        "meditate":"meditate","명상":"meditate","수련":"meditate","운기":"meditate",
        "talk":"talk","대화":"talk","말":"talk","말걸기":"talk","이야기":"talk",
        "status":"status","stat":"status","상태":"status","스탯":"status","정보":"status",
        "inv":"inv","inventory":"inv","가방":"inv","인벤":"inv","소지품":"inv","아이템":"inv",
        "arts":"arts","skills":"arts","무공목록":"arts","배운무공":"arts",
        "equip":"equip","장착":"equip","착용":"equip",
        "unequip":"unequip","해제":"unequip","장착해제":"unequip","벗다":"unequip",
        "use":"use","사용하기":"use","먹다":"use",
        "sell":"sell","판매":"sell","팔다":"sell",
        "dismantle":"dismantle","분해":"dismantle",
        "discard":"discard","drop":"discard","버리다":"discard","버리기":"discard",
        "shop":"shop","상점":"shop","물품":"shop","상인":"shop",
        "buy":"buy","구매":"buy","사다":"buy",
        "enchant":"enchant","upgrade":"enchant","강화":"enchant","인챈트":"enchant","강화하기":"enchant",
        "quest":"quest","퀘스트":"quest","의뢰":"quest","임무":"quest",
        "gold":"gold","money":"gold","돈":"gold","은전":"gold","소지금":"gold",
        "eq":"eq","equipment":"eq","장비":"eq","장비창":"eq",
        "save":"save","저장":"save","기록":"save",
        "help":"help","도움":"help","도움말":"help","?":"help","명령":"help","명령어":"help",
        "guild_create":"guild_create","길드생성":"guild_create","문파생성":"guild_create",
        "guild_join":"guild_join","길드가입":"guild_join","문파가입":"guild_join",
        "guild_approve":"guild_approve","승인":"guild_approve","가입승인":"guild_approve",
        "guild_leave":"guild_leave","길드탈퇴":"guild_leave","문파탈퇴":"guild_leave","탈퇴":"guild_leave",
        "guild_kick":"guild_kick","추방":"guild_kick","길드추방":"guild_kick",
        "guild_rank":"guild_rank","계급":"guild_rank","계급변경":"guild_rank",
        "guild_info":"guild_info","guild":"guild_info","길드":"guild_info","길드정보":"guild_info","문파":"guild_info",
        "guild_storage":"guild_storage","gstash":"guild_storage","길드창고":"guild_storage","문파창고":"guild_storage",
        "guild_deposit":"guild_deposit","gdep":"guild_deposit","창고보관":"guild_deposit","보관":"guild_deposit",
        "guild_withdraw":"guild_withdraw","gwdr":"guild_withdraw","창고인출":"guild_withdraw","인출":"guild_withdraw",
        "guild_gold_add":"guild_gold_add","입금":"guild_gold_add","길드입금":"guild_gold_add",
        "guild_gold_out":"guild_gold_out","출금":"guild_gold_out","길드출금":"guild_gold_out",
        "admin_set":"admin_set","관리자설정":"admin_set",
        "admin_tp":"admin_tp","tp":"admin_tp","순간이동":"admin_tp",
        "admin_give":"admin_give","give":"admin_give","아이템지급":"admin_give",
        "admin_users":"admin_users","users":"admin_users","유저목록":"admin_users",
        "admin_chars":"admin_chars","chars":"admin_chars","캐릭터목록":"admin_chars",
        "admin_rooms":"admin_rooms","rooms":"admin_rooms","방목록":"admin_rooms",
        "admin_items":"admin_items","aitems":"admin_items","관리자아이템":"admin_items","아이템목록":"admin_items",
        "admin_item_info":"admin_item_info","aitem":"admin_item_info","아이템정보":"admin_item_info",
        "admin_give_code":"admin_give_code","gcode":"admin_give_code","아이템코드지급":"admin_give_code",
        "return_set":"return_set","rset":"return_set","귀환지정":"return_set",
        "return_go":"return_go","rgo":"return_go","귀환":"return_go",
        "admin_god":"admin_god","god":"admin_god","무적":"admin_god",
    }
    return (m.get(v.lower(), v), r)


def execute_command(db, char, cmd):
    msgs = []
    v, rest = parse_command(cmd)
    v, rest = normalize_verb(v, rest)
    room = db.query(Room).filter(Room.id == char.current_room_id).first()

    if v == "look":
        if not room: return [{"type":"system","content":"허공...","style":"normal"}]
        msgs.append({"type":"room_desc","content":f"[{room.name}] (#{room.id})","style":"room"})
        msgs.append({"type":"room_desc","content":room.description,"style":"room"})
        ex={k:vv for k,vv in (room.exits or {}).items() if vv}
        if ex:
            ko={"north":"북","south":"남","east":"동","west":"서","up":"위","down":"아래","enter":"입장","out":"퇴장","cross":"건너","deep":"깊은","escape":"도망","inner":"안","secret":"비밀","back":"뒤로","edge":"끝"}
            msgs.append({"type":"system","content":"갈수있는곳: "+", ".join(f"[{ko.get(k,k)}]" for k in ex),"style":"normal"})
        for nid in (room.npc_ids or []):
            npc=db.query(NPC).filter(NPC.id==nid).first()
            if npc: msgs.append({"type":"npc_present","content":f"{'⚔' if npc.is_hostile else ''} {npc.name}(이)가 있습니다.","style":"npc"})
        for mid in (room.monster_ids or []):
            mon=db.query(Monster).filter(Monster.id==mid).first()
            if mon: msgs.append({"type":"monster_present","content":f"위협적인 {mon.name}! (HP:{mon.hp}/{mon.max_hp})","style":"warning"})
        return msgs

    if v in ("north","south","east","west","up","down","enter","out","go"):
        if v=="go":
            d=rest.strip().lower()
            ds={"n":"north","s":"south","e":"east","w":"west","북":"north","남":"south","동":"east","서":"west","u":"up","d":"down"}.get(d,d)
        else: ds=v
        t=(room.exits or {}).get(ds) if room else None
        if t: char.current_room_id=t; db.commit(); return msgs+execute_command(db,char,"look")
        return [{"type":"system","content":"갈 수 없습니다.","style":"warning"}]

    if v == "attack":
        for mid in list(room.monster_ids or []):
            mon=db.query(Monster).filter(Monster.id==mid).first()
            if mon and mon.name.lower()==rest.lower():
                m=attack_monster(db,char,mon)
                if mon.hp<=0 and mid in (room.monster_ids or []):
                    room.monster_ids.remove(mid); db.delete(mon); db.commit()
                    add_reputation(db,char,10)
                if char.hp<=0: char.hp=char.max_hp; char.current_room_id=1; db.commit(); m.append({"type":"system","content":"마을에서 깨어납니다...","style":"warning"})
                _check_lv(db,char,m); return m
        return [{"type":"system","content":f"'{rest}' 없습니다.","style":"warning"}]

    if v == "cast":
        for mid in list(room.monster_ids or []):
            mon=db.query(Monster).filter(Monster.id==mid).first()
            if mon:
                m=cast_martial_art(db,char,rest,mon)
                if mon.hp<=0 and mid in (room.monster_ids or []):
                    room.monster_ids.remove(mid); db.delete(mon); db.commit()
                    add_reputation(db,char,15)
                _check_lv(db,char,m); return m
        return [{"type":"system","content":"적이 없습니다.","style":"warning"}]

    if v == "meditate": m=meditate_service(db,char); _check_lv(db,char,m); return m
    if v == "talk":
        for nid in (room.npc_ids or []):
            npc=db.query(NPC).filter(NPC.id==nid).first()
            if npc and npc.name.lower()==rest.lower(): return [{"type":"npc_dialogue","content":npc.dialogue or f"[{npc.name}]: ...","style":"npc"}]
        return [{"type":"system","content":"대화 상대 없음.","style":"warning"}]

    if v == "status":
        fac=db.query(CharacterFaction).filter(CharacterFaction.character_id==char.id).first()
        fn=db.query(Faction).filter(Faction.id==fac.faction_id).first().name if fac else "무소속"
        tn=_exp_for_level(char.level)
        buf=f" 버프:공{char.guild_buff_attack} 방{char.guild_buff_defense} HP{char.guild_buff_hp}" if char.guild_buff_attack else ""
        s=f"""══ {char.name} [{char.origin}] ══
 Lv.{char.level} ({char.exp}/{tn})  경지:{char.martial_stage}  은전:{char.gold}
 HP:{char.hp}/{char.max_hp} MP:{char.mp}/{char.max_mp}
 공격:{char.attack} 방어:{char.defense} 속도:{char.speed} 치명:{char.crit_rate:.1%}
 근골{char.physique} 기맥{char.ki} 신법{char.agility} 심안{char.insight} 매력{char.charm} 복운{char.luck}
 문파:{fn}  위치:#{char.current_room_id}{buf}"""
        return [{"type":"system","content":s,"style":"normal"}]

    if v == "gold": return [{"type":"system","content":f"소지금: {char.gold}은전","style":"normal"}]

    if v == "inv":
        invs=db.query(Inventory).filter(Inventory.character_id==char.id).all()
        cnt=sum(1 for i in invs if not i.equipped)
        if not invs: return [{"type":"system","content":f"소지품 없음. ({cnt}/{char.inventory_limit}칸)","style":"normal"}]
        lines=[f"[소지품] ({cnt}/{char.inventory_limit}칸)"]
        for i in invs:
            it=db.query(ItemModel).filter(ItemModel.id==i.item_id).first()
            eq=" [장착중]" if i.equipped else ""
            lines.append(f"  {it.name} x{i.quantity}{eq}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "arts":
        cmas=db.query(CharacterMartialArt).filter(CharacterMartialArt.character_id==char.id).all()
        if not cmas: return [{"type":"system","content":"무공 없음.","style":"normal"}]
        lines=["[무공]"]
        for c in cmas:
            a=db.query(MartialArt).filter(MartialArt.id==c.martial_art_id).first()
            lines.append(f"  {a.name} 숙련:{c.proficiency}/1000 MP:{a.mp_cost}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "equip":
        e = equip_item(db, char, rest)
        if e:
            return [{"type":"system","content":e,"style":"warning"}]
        return [{"type":"system","content":f"{rest} 장착 완료!","style":"normal"}]

    if v == "unequip":
        e = unequip_item(db, char, rest)
        return [{"type":"system","content":e if e else f"{rest} 해제 완료.","style":"warning" if e else "normal"}]

    if v == "eq":
        es = equip_status(db, char)
        lines = ["[장비현황]"]
        for sn, info in es["slots"].items():
            if info:
                sn_display = sn.replace("1","①").replace("2","②")
                s = info["stats"]
                stat_str = f" 공:{s.get('attack',0)} 방:{s.get('defense',0)} HP:{s.get('hp',0)} MP:{s.get('mp',0)} 속:{s.get('speed',0)}"
                lines.append(f"  {sn_display}: {info['name']}{stat_str}")
            else:
                lines.append(f"  {sn}: 빈칸")
        lines.append(f"  ────────────────────────")
        lines.append(f"  총합 공:{es['total_attack']} 방:{es['total_defense']} HP:{es['max_hp']} MP:{es['max_mp']} 속:{es['speed']} 치명:{es['crit_rate']:.0%}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "use":
        inv=db.query(Inventory).join(ItemModel).filter(Inventory.character_id==char.id,ItemModel.name.ilike(f"%{rest}%")).first()
        if not inv: return [{"type":"system","content":"아이템 없음.","style":"warning"}]
        it=db.query(ItemModel).filter(ItemModel.id==inv.item_id).first()
        if it.item_type!="consumable": return [{"type":"system","content":"사용 불가.","style":"warning"}]
        heal=(it.effects or {}).get("heal_amount",15)
        char.hp=min(char.hp+heal,char.max_hp); inv.quantity-=1
        if inv.quantity<=0: db.delete(inv)
        db.commit(); return [{"type":"battle_log","content":f"{it.name} 사용! HP+{heal}","style":"healing"}]

    if v == "sell":
        p=rest.split(); qty=int(p[-1]) if p[-1].isdigit() else 1
        nm=" ".join(p[:-1]) if p[-1].isdigit() else rest
        e=sell_item(db,char,nm,qty)
        return [{"type":"system","content":e if e else f"{nm} 판매 완료!","style":"warning" if e else "normal"}]

    if v == "dismantle": e=dismantle_item(db,char,rest); return [{"type":"system","content":e if e else f"{rest} 분해! 강화석 획득.","style":"warning" if e else "normal"}]

    if v == "discard":
        p=rest.split(); qty=int(p[-1]) if p[-1].isdigit() else 1
        nm=" ".join(p[:-1]) if p[-1].isdigit() else rest
        e=discard_item(db,char,nm,qty)
        return [{"type":"system","content":e if e else f"{nm} 버림.","style":"warning" if e else "normal"}]

    if v == "shop":
        shop=db.query(Shop).filter(Shop.room_id==char.current_room_id).first()
        if not shop: return [{"type":"system","content":"상점 없음.","style":"warning"}]
        lines=[f"[{shop.name}]"]
        for iid in (shop.item_ids or [])[:15]:
            it=db.query(ItemModel).filter(ItemModel.id==iid).first()
            if it: lines.append(f"  {it.name} — {it.price}은전")
        lines.append("'buy 아이템' / 'sell 아이템' / 'dismantle 아이템'")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "buy":
        shop=db.query(Shop).filter(Shop.room_id==char.current_room_id).first()
        if not shop: return [{"type":"system","content":"상점 없음.","style":"warning"}]
        it=db.query(ItemModel).filter(ItemModel.name.ilike(f"%{rest}%"),ItemModel.id.in_(shop.item_ids or [])).first()
        if not it: return [{"type":"system","content":"없는 물품.","style":"warning"}]
        if char.gold<(it.price or 10): return [{"type":"system","content":f"은전 부족. (필요:{it.price})","style":"warning"}]
        cnt=db.query(Inventory).filter(Inventory.character_id==char.id,Inventory.equipped==0).count()
        if cnt>=char.inventory_limit: return [{"type":"system","content":"가방 가득.","style":"warning"}]
        char.gold-=it.price; db.add(Inventory(character_id=char.id,item_id=it.id,quantity=1)); db.commit()
        return [{"type":"system","content":f"{it.name} 구매!","style":"normal"}]

    if v == "enchant":
        p=rest.split(); up="-p" in p or "보호" in p; ua="-a" in p or "고급" in p
        ip=" ".join(w for w in p if not w.startswith("-") and w not in ("보호","고급"))
        if not ip: return [{"type":"system","content":"사용법: enchant 아이템 [-p] [-a]","style":"warning"}]
        return upgrade_item(db,char,ip,up,ua)

    if v == "quest":
        cqs=db.query(CharacterQuest).filter(CharacterQuest.character_id==char.id,CharacterQuest.status=="active").all()
        if not cqs: return [{"type":"system","content":"의뢰 없음.","style":"normal"}]
        lines=["[의뢰]"]
        for cq in cqs:
            q=db.query(Quest).filter(Quest.id==cq.quest_id).first()
            if q: lines.append(f"  {q.name} ({cq.progress}/{q.objectives.get('count',1)})")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    # ── GUILD ──
    if v == "guild_create":
        p=rest.split(maxsplit=1); gn=p[0] if p else ""; desc=p[1] if len(p)>1 else ""
        if not gn: return [{"type":"system","content":"사용법: guild_create 문파명 [설명]","style":"warning"}]
        e=create_guild(db,char,gn,desc)
        return [{"type":"system","content":e if e else f"✦ '{gn}' 문파 창설! ✦\\n(5000은전+1000EXP 소모)","style":"critical" if not e else "warning"}]

    if v == "guild_join": e=join_guild(db,char,rest); return [{"type":"system","content":e if e else f"{rest} 가입 신청!","style":"warning" if e else "normal"}]
    if v == "guild_approve": e=approve_application(db,char,rest); return [{"type":"system","content":e if e else f"{rest} 승인!","style":"warning" if e else "normal"}]
    if v == "guild_leave": e=leave_guild(db,char); return [{"type":"system","content":e if e else "탈퇴 완료.","style":"warning" if e else "normal"}]
    if v == "guild_kick": e=kick_member(db,char,rest); return [{"type":"system","content":e if e else f"{rest} 추방.","style":"warning" if e else "normal"}]
    if v == "guild_rank":
        p=rest.split(maxsplit=1)
        if len(p)<2: return [{"type":"system","content":"사용법: guild_rank 이름 계급","style":"warning"}]
        e=change_rank(db,char,p[0],p[1]); return [{"type":"system","content":e if e else f"{p[0]}→{p[1]}","style":"warning" if e else "normal"}]

    if v == "guild_info":
        info=get_guild_info(db,char)
        if not info: return [{"type":"system","content":"소속 문파 없음.","style":"normal"}]
        nxt=info.get("next_milestone")
        nm=f"\\n  다음:{nxt['name']} (명성{nxt['reputation']})" if nxt else ""
        lines=[f"[{info['name']}] {info['description']}\n 명성:{info['reputation']} 금고:{info['gold']} 길드원:{info['member_count']}명\n 길드장:{info['leader']} 계급:{info['my_rank']} 기여:{info['my_contribution']}\n 해금버프:{len(info['buffs'])}개{nm}\n[길드원]"]
        for m in info["members"]: lines.append(f"  [{m['rank']}] {m['name']} (기여:{m['contribution']})")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "guild_storage":
        items=get_storage_contents(db,char)
        if items is None: return [{"type":"system","content":"소속 문파 없음.","style":"warning"}]
        if not items: return [{"type":"system","content":"창고 비었음.","style":"normal"}]
        lines=["[문파 창고]"]
        for it in items[:20]: lines.append(f"  {it['name']} x{it['quantity']}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "guild_deposit":
        p=rest.split(); qty=int(p[-1]) if p[-1].isdigit() else 1
        nm=" ".join(p[:-1]) if p[-1].isdigit() else rest
        if not nm: return [{"type":"system","content":"사용법: guild_deposit 아이템 [수량]","style":"warning"}]
        e=deposit_to_storage(db,char,nm,qty); return [{"type":"system","content":e if e else f"{nm} 보관!","style":"warning" if e else "normal"}]

    if v == "guild_withdraw":
        p=rest.split(); qty=int(p[-1]) if p[-1].isdigit() else 1
        nm=" ".join(p[:-1]) if p[-1].isdigit() else rest
        if not nm: return [{"type":"system","content":"사용법: guild_withdraw 아이템 [수량]","style":"warning"}]
        e=withdraw_from_storage(db,char,nm,qty); return [{"type":"system","content":e if e else f"{nm} 인출!","style":"warning" if e else "normal"}]

    if v == "guild_gold_add":
        p=rest.split()
        if not p: return [{"type":"system","content":"사용법: guild_gold_add 금액","style":"warning"}]
        try: amt=int(p[0])
        except: return [{"type":"system","content":"올바른 금액.","style":"warning"}]
        ok=add_guild_gold(db,char,amt); return [{"type":"system","content":"입금 완료!" if ok else "은전 부족.","style":"normal" if ok else "warning"}]

    if v == "guild_gold_out":
        p=rest.split()
        if not p: return [{"type":"system","content":"사용법: guild_gold_out 금액","style":"warning"}]
        try: amt=int(p[0])
        except: return [{"type":"system","content":"올바른 금액.","style":"warning"}]
        e=withdraw_guild_gold(db,char,amt); return [{"type":"system","content":e if e else f"{amt}은전 출금!","style":"warning" if e else "normal"}]

    # ── ADMIN ──
    if v == "admin_set":
        p=rest.split()
        if len(p)<3: return [{"type":"system","content":"admin_set 캐릭ID 필드 값","style":"warning"}]
        e=admin_set_stat(db,int(p[0]),p[1],int(p[2])); return [{"type":"system","content":e if e else f"#{p[0]}.{p[1]}={p[2]}","style":"warning" if e else "normal"}]

    if v == "admin_tp":
        p=rest.split()
        if len(p)<2: return [{"type":"system","content":"admin_tp 캐릭ID 방ID","style":"warning"}]
        e=admin_teleport(db,int(p[0]),int(p[1])); return [{"type":"system","content":e if e else f"#{p[0]}→#{p[1]}","style":"warning" if e else "normal"}]

    if v == "admin_give":
        p=rest.split()
        if len(p)<2: return [{"type":"system","content":"admin_give 캐릭ID 아이템ID [수량]","style":"warning"}]
        qty=int(p[2]) if len(p)>2 else 1
        e=admin_give_item(db,int(p[0]),int(p[1]),qty); return [{"type":"system","content":e if e else f"#{p[1]}x{qty} 지급","style":"warning" if e else "normal"}]

    if v == "admin_users":
        users=get_all_users(db); lines=["[유저]"]
        for u in users: lines.append(f"  #{u['id']} {u['username']}{' ★' if u['is_admin'] else ''}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "admin_chars":
        chars=get_all_characters(db); lines=["[캐릭터]"]
        for c in chars: lines.append(f"  #{c['id']} {c['name']} Lv{c['level']} {c['martial_stage']} (#{c['current_room_id']})")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "admin_rooms":
        rooms=admin_list_rooms(db); lines=["[방]"]
        for r in rooms[:30]:
            ex=", ".join(r["exits"].keys()) if r["exits"] else "X"
            safe="🛡안전" if r.get("is_safe") else ""
            inn="🏠여관" if r.get("is_inn") else ""
            tags=f" {safe}{inn}" if (safe or inn) else ""
            lines.append(f"  #{r['id']} {r['name']} ({r['region']})→{ex}{tags}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "admin_items":
        itype=rest if rest else None
        items=admin_list_items(db,search=itype)
        lines=[f"[관리자 아이템] ({len(items)}개)"]
        for it in items[:30]:
            lines.append(f"  #{it['id']} {it['name']} [{it['item_type']}] {it.get('slot','')} — {it['price']}은전 ({it.get('code','')})")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "admin_item_info":
        try: iid=int(rest); info=admin_get_item(db,iid)
        except: return [{"type":"system","content":"사용법: admin_item_info 아이템ID","style":"warning"}]
        if not info: return [{"type":"system","content":"아이템 없음.","style":"warning"}]
        lines=[f"[아이템 정보] #{info['id']}"]
        for k in ["name","code","item_type","sub_type","slot","weapon_type","description","rarity","price","stack_limit"]:
            lines.append(f"  {k}: {info.get(k,'')}")
        lines.append(f"  stats: {info.get('stats',{})}")
        lines.append(f"  effects: {info.get('effects',{})}")
        return [{"type":"system","content":"\n".join(lines),"style":"normal"}]

    if v == "admin_give_code":
        p=rest.split()
        if len(p)<2: return [{"type":"system","content":"사용법: admin_give_code 캐릭ID 아이템코드 [수량]","style":"warning"}]
        try: cid=int(p[0])
        except: return [{"type":"system","content":"캐릭터ID는 숫자.","style":"warning"}]
        code=p[1]; qty=int(p[2]) if len(p)>2 else 1
        e=admin_give_item_by_code(db,cid,code,qty)
        return [{"type":"system","content":e if e else f"#{code}x{qty} 지급 완료!","style":"warning" if e else "normal"}]

    if v == "return_set":
        e=set_return_point(db,char,char.current_room_id)
        return [{"type":"system","content":e if e else f"✦ 귀환장소 지정: [{room.name}] ✦","style":"critical"}]

    if v == "return_go":
        e=use_return_scroll(db,char)
        if e: return [{"type":"system","content":e,"style":"warning"}]
        return execute_command(db,char,"look")

    if v == "admin_god": char.hp=char.max_hp=999999; char.attack=char.defense=9999; db.commit(); return [{"type":"system","content":"⚡무적!","style":"critical"}]

    if v == "help":
        admin = is_admin(db, char.user_id)
        help_text = _build_help(admin)
        return [{"type":"system","content":help_text,"style":"normal"}]

    if v == "save": db.commit(); return [{"type":"system","content":"저장 완료.","style":"normal"}]
    return [{"type":"system","content":f"'{cmd}'? 알수없음. help 확인.","style":"warning"}]


# ═══════════════ HELP SYSTEM ═══════════════
def _build_help(is_admin_user: bool) -> str:
    """관리자 여부에 따라 다른 도움말을 구성합니다."""
    basic = """[기본]
• look / 보기 / 주변 — 현재 방의 정보를 확인합니다.
  예) look → 「마을 광장」 주변을 둘러봅니다.

• 북 / 남 / 동 / 서 / 위 / 아래 / n / s / e / w / u / d — 해당 방향으로 이동합니다.
  예) 북 → 북쪽으로 이동합니다.

• go 방향 — 지정한 방향으로 이동합니다.
  예) go 북 → 북쪽으로 이동합니다.

• status / 상태 / 스탯 / 정보 — 캐릭터의 능력치를 표시합니다.
  예) status → 레벨, HP, 공격력, 스탯 등 표시

• inv / 가방 / 인벤 / 소지품 — 소지 중인 아이템을 확인합니다.
  예) inv → 가방 속 아이템 목록 표시"""

    battle = """
[전투]
• attack 대상 / 공격 대상 — 대상을 기본 공격합니다.
  예) attack 도적 → 도적을 공격합니다.

• cast 무공명 / 시전 무공명 / 무공 무공명 — 배운 무공을 시전합니다.
  예) cast 벽력검법 → 벽력검법으로 적을 공격합니다.

• meditate / 명상 / 수련 / 운기 — 명상으로 HP와 MP를 회복합니다.
  예) 명상 → 명상을 통해 기운을 회복합니다.

• arts / 무공목록 / 배운무공 — 배운 무공 목록을 확인합니다.
  예) arts → 보유한 무공과 숙련도 표시"""

    equipment = """
[장비]
• equip 아이템 / 장착 아이템 — 아이템을 해당 슬롯에 장착합니다.
  예) equip 철검 → 철검을 mainhand 슬롯에 장착합니다.

• unequip 아이템 / 해제 아이템 — 장착 중인 아이템을 해제합니다.
  예) unequip 철검 → 철검 장착을 해제합니다.

• eq / 장비 / 장비창 — 현재 장비 현황과 총합 스탯을 확인합니다.
  예) eq → 장착 중인 장비와 스탯 합계 표시"""

    items = """
[아이템/소모품]
• use 아이템 / 사용 아이템 / 먹다 아이템 — 소모품을 사용합니다.
  예) use 회복약 → 회복약을 사용해 HP를 회복합니다.

• sell 아이템 [수량] / 판매 아이템 — 아이템을 상점에 판매합니다.
  예) sell 철검 2 → 철검 2개를 판매합니다.

• buy 아이템 / 구매 아이템 — 상점에서 아이템을 구매합니다.
  예) buy 회복약 → 상점에서 회복약을 구매합니다.

• shop / 상점 / 물품 — 현재 방의 상점 상품 목록을 확인합니다.
  예) shop → 상점 판매 물품 확인

• dismantle 아이템 / 분해 아이템 — 장비를 분해하여 강화석을 얻습니다.
  예) dismantle 낡은검 → 낡은검을 분해합니다.

• discard 아이템 [수량] / 버리기 아이템 — 아이템을 버립니다.
  예) discard 부러진창 → 부러진창을 버립니다.

• gold / 돈 / 은전 / 소지금 — 현재 소지금을 확인합니다.
  예) gold → 보유 은전 확인"""

    enchant = """
[강화]
• enchant 아이템 [-p] [-a] / 강화 아이템 [-보호] [-고급] — 아이템을 강화합니다.
  예) enchant 철검 → 철검을 +1 강화 시도합니다.
  예) enchant 철검 -p → 보호석을 사용하여 실패 시 하락을 방지합니다.
  예) enchant 철검 -a → 고급 강화석으로 더 높은 확률로 강화합니다."""

    return_cmd = """
[귀환]
• return_set / 귀환지정 / rset — 현재 위치를 귀환 지점으로 지정합니다.
  예) 귀환지정 → 이곳을 귀환 지점으로 등록합니다.

• return_go / 귀환 / rgo — 지정한 귀환 지점으로 이동합니다. (귀환부 필요)
  예) 귀환 → 등록된 귀환 지점으로 순간 이동합니다."""

    guild = """
[길드/문파]
• guild_create 문파명 [설명] / 길드생성 문파명 — 새 문파를 창설합니다. (5000은전 + 1000EXP 소모)
  예) guild_create 천하제일문 최고의 문파 → 천하제일문을 창설합니다.

• guild_join 문파명 / 길드가입 문파명 — 해당 문파에 가입 신청합니다.
  예) guild_join 천하제일문 → 천하제일문 가입을 신청합니다.

• guild_approve 캐릭명 / 승인 캐릭명 / 가입승인 — 가입 신청자를 승인합니다. (문파 운영진 전용)
  예) 승인 홍길동 → 홍길동의 가입을 승인합니다.

• guild_leave / 길드탈퇴 / 탈퇴 — 현재 소속된 문파에서 탈퇴합니다.
  예) 탈퇴 → 문파에서 탈퇴합니다.

• guild_kick 캐릭명 / 추방 캐릭명 — 문파원을 추방합니다. (문파 운영진 전용)
  예) 추방 홍길동 → 홍길동을 문파에서 추방합니다.

• guild_rank 캐릭명 계급 / 계급변경 — 문파원의 계급을 변경합니다. (문파주 전용)
  예) guild_rank 홍길동 부문주 → 홍길동을 부문주로 임명합니다.

• guild_info / guild / 길드 / 문파 / 길드정보 — 문파 상세 정보를 확인합니다.
  예) 길드정보 → 문파 명성, 금고, 길드원 목록 표시

• guild_storage / 길드창고 / 문파창고 — 문파 창고 보관품을 확인합니다.
  예) 길드창고 → 창고에 보관된 아이템 목록 표시

• guild_deposit 아이템 [수량] / 보관 아이템 — 아이템을 문파 창고에 보관합니다.
  예) 보관 철검 2 → 철검 2개를 문파 창고에 보관합니다.

• guild_withdraw 아이템 [수량] / 인출 아이템 — 문파 창고에서 아이템을 찾습니다.
  예) 인출 철검 → 문파 창고에서 철검을 인출합니다.

• guild_gold_add 금액 / 입금 금액 — 문파 금고에 은전을 입금합니다.
  예) 입금 1000 → 문파 금고에 1000은전을 입금합니다.

• guild_gold_out 금액 / 출금 금액 — 문파 금고에서 은전을 출금합니다. (운영진 전용)
  예) 출금 500 → 문파 금고에서 500은전을 출금합니다."""

    etc = """
[기타]
• talk 대상 / 대화 대상 / 말걸기 대상 — NPC와 대화합니다.
  예) talk 촌장 → 촌장과 대화를 시도합니다.

• quest / 퀘스트 / 의뢰 / 임무 — 진행 중인 퀘스트를 확인합니다.
  예) 퀘스트 → 현재 수행 중인 의뢰 목록 표시

• save / 저장 — 현재 상태를 저장합니다.
  예) 저장 → 진행 상황을 저장합니다.

• help / 도움말 / ? — 이 도움말을 출력합니다.
  예) 도움말 → 명령어 도움말을 확인합니다."""

    if not is_admin_user:
        sections = [basic, battle, equipment, items, enchant, return_cmd, guild, etc]
        return "━━━ *도움말* ━━━\n" + "\n".join(sections)

    # 관리자 전용 명령어
    admin_cmds = """
[관리자]
• admin_set 캐릭ID 필드 값 / 관리자설정 — 캐릭터 스탯을 직접 수정합니다.
  예) admin_set 1 attack 100 → 1번 캐릭터의 공격력을 100으로 설정합니다.

• admin_tp 캐릭ID 방ID / tp / 순간이동 — 대상 캐릭터를 지정 방으로 이동시킵니다.
  예) admin_tp 1 5 → 1번 캐릭터를 5번 방으로 이동시킵니다.

• admin_give 캐릭ID 아이템ID [수량] / give / 아이템지급 — 아이템 ID로 지급합니다.
  예) admin_give 1 101 3 → 1번 캐릭터에게 101번 아이템 3개를 지급합니다.

• admin_give_code 캐릭ID 아이템코드 [수량] / gcode / 아이템코드지급 — 아이템 코드로 지급합니다.
  예) admin_give_code 1 WPN_SWORD_IRON_01 → 1번 캐릭터에게 철검을 지급합니다.

• admin_users / users / 유저목록 — 등록된 모든 유저를 조회합니다.
  예) 유저목록 → 전체 유저 목록 표시

• admin_chars / chars / 캐릭터목록 — 생성된 모든 캐릭터를 조회합니다.
  예) 캐릭터목록 → 모든 캐릭터 목록 표시

• admin_rooms / rooms / 방목록 — 모든 방 정보를 조회합니다.
  예) 방목록 → 지역별 방 목록 표시

• admin_items [검색어] / aitems / 아이템목록 — 아이템을 검색하거나 전체 목록을 확인합니다.
  예) admin_items 검 → '검'이 포함된 아이템 검색 결과를 표시합니다.

• admin_item_info 아이템ID / aitem / 아이템정보 — 특정 아이템의 상세 정보를 확인합니다.
  예) admin_item_info 101 → 101번 아이템의 스탯과 효과를 상세히 표시합니다.

• admin_god / god / 무적 — 캐릭터를 무적 상태로 만듭니다. (HP/공격/방어 999999)
  예) 무적 → 무적 상태가 됩니다."""

    sections = [basic, battle, equipment, items, enchant, return_cmd, guild, admin_cmds, etc]
    return "━━━ *도움말* (관리자) ━━━\n" + "\n".join(sections)
def _exp_for_level(lv):
    if lv<=1: return 0
    if lv<=50:
        t=[0,50,120,220,350,520,740,1000,1320,1700,2150,2680,3300,4000,4800,5700,6700,7800,9000,10400,12000,13800,15800,18000,20500,23300,26400,29800,33500,37600,42200,47300,53000,59400,66600,74600,83500,93400,104400,116500,130000,145000,162000,181000,202000,225000,251000,280000,312000,350000]
        if lv<=len(t): return t[lv-1]
    return int(350000*math.pow(1.025,lv-50)+(lv-50)*2000)

def _check_lv(db,char,msgs):
    while char.level<999 and char.exp>=_exp_for_level(char.level+1):
        char.level+=1; char.max_hp+=12; char.hp=char.max_hp; char.max_mp+=6; char.mp=char.max_mp
        char.attack+=2; char.defense+=1; char.speed+=1
        msgs.append({"type":"system","content":f"── Lv.{char.level}!! ──","style":"critical"})
        db.commit()
