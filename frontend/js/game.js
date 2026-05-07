/* 낙화검심 - Client logic */
const API_HOST = window.location.hostname;
const API = `http://${API_HOST}:8000/api`;
const WS_BASE = `ws://${API_HOST}:8000/ws`;
let token = '';
let username = '';
let currentCharId = null;
let chatWs = null;
let petalTimer = null;
const STAT_IDS = ['physique','ki','agility','insight','charm','luck'];
const MAX_PTS = 80;
const DEFAULT_VAL = 10;

// ─── AUTH ───
function toggleAuth() {
    document.getElementById('login-form').style.display =
        document.getElementById('login-form').style.display === 'none' ? 'block' : 'none';
    document.getElementById('signup-form').style.display =
        document.getElementById('signup-form').style.display === 'none' ? 'block' : 'none';
}

async function login() {
    const u = document.getElementById('login-user').value.trim();
    const p = document.getElementById('login-pass').value;
    if (!u || !p) return;
    const r = await fetch(`${API}/auth/login`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({username:u, password:p})
    });
    if (!r.ok) return alert('로그인 실패');
    const d = await r.json();
    token = d.access_token; username = d.username;
    document.getElementById('auth-overlay').style.display = 'none';
    loadChars();
}

async function signup() {
    const u = document.getElementById('signup-user').value.trim();
    const e = document.getElementById('signup-email').value.trim();
    const p = document.getElementById('signup-pass').value;
    if (!u || !p) return;
    const r = await fetch(`${API}/auth/signup`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({username:u, email:e, password:p})
    });
    if (!r.ok) return alert('회원가입 실패');
    const d = await r.json();
    token = d.access_token; username = d.username;
    document.getElementById('auth-overlay').style.display = 'none';
    loadChars();
}

function logout() {
    token = ''; username = ''; currentCharId = null;
    if (chatWs) { chatWs.close(); chatWs = null; }
    document.getElementById('game-ui').style.display = 'none';
    document.getElementById('char-select').style.display = 'none';
    document.getElementById('auth-overlay').style.display = 'flex';
    document.getElementById('login-user').value = '';
    document.getElementById('login-pass').value = '';
    const btn = document.getElementById('btn-logout');
    if (btn) btn.style.display = 'none';
    document.body.classList.remove('game-active');
    transitionToAuthPetals();
}

// ─── CHARACTERS ───
async function loadChars() {
    document.getElementById('char-select').style.display = 'flex';
    const r = await fetch(`${API}/characters/`, {
        headers:{'Authorization':`Bearer ${token}`}
    });
    const chars = await r.json();
    const list = document.getElementById('char-list');
    list.innerHTML = chars.map(c =>
        `<div class="char-card" onclick="selectChar(${c.id})">
            <span class="cname">${c.name}</span>
            <span class="cinfo">${c.origin} | Lv.${c.level} | ${c.martial_stage}</span>
            <button class="del-char-btn" onclick="event.stopPropagation();deleteChar(${c.id})" title="캐릭터 삭제">✕</button>
        </div>`
    ).join('');
}

async function createChar() {
    const name = document.getElementById('char-name').value.trim();
    if (!name || name.length < 2) return alert('이름을 입력하세요');
    // 스탯 총합 검증 (정확히 MAX_PTS)
    const total = STAT_IDS.reduce((sum, id) => sum + (+document.getElementById(id).value), 0);
    const remain = MAX_PTS - total;
    if (remain !== 0) return alert(`스탯 포인트를 모두 사용해주세요! (남은 포인트: ${remain})`);
    const data = {
        name, origin: document.getElementById('char-origin').value,
        physique: +document.getElementById('physique').value,
        ki: +document.getElementById('ki').value,
        agility: +document.getElementById('agility').value,
        insight: +document.getElementById('insight').value,
        charm: +document.getElementById('charm').value,
        luck: +document.getElementById('luck').value
    };const r = await fetch(`${API}/characters`, {
        method:'POST', headers:{'Authorization':`Bearer ${token}`, 'Content-Type':'application/json'},
        body: JSON.stringify(data)
    });
    if (!r.ok) return alert('생성 실패');
    const c = await r.json();
    selectChar(c.id);
}

function updatePts(changedId) {
    const total = STAT_IDS.reduce((sum, id) => sum + (+document.getElementById(id).value), 0);
    const remain = MAX_PTS - total;
    document.getElementById('remain-pts').textContent = remain;
    if (remain < 0) {
        document.getElementById('remain-pts').style.color = '#ff6b6b';
        document.getElementById(changedId).value = +document.getElementById(changedId).value + remain;
        document.getElementById(changedId[0]+'v').textContent = document.getElementById(changedId).value;
        document.getElementById('remain-pts').textContent = '0';
    } else {
        document.getElementById('remain-pts').style.color = '#e892a8';
    }
    document.getElementById(changedId[0]+'v').textContent = document.getElementById(changedId).value;
}

function showNewChar() {
    document.getElementById('new-char-form').style.display = 'block';
    // reset all to defaults
    STAT_IDS.forEach(id => {
        document.getElementById(id).value = DEFAULT_VAL;
        document.getElementById(id[0]+'v').textContent = DEFAULT_VAL;
    });
    document.getElementById('remain-pts').textContent = MAX_PTS - DEFAULT_VAL * 6;
}

async function deleteChar(id) {
    if (!confirm('정말 이 캐릭터를 삭제하시겠습니까?\n삭제 후에는 복구할 수 없습니다.')) return;
    const r = await fetch(`${API}/characters/${id}`, {
        method: 'DELETE', headers: {'Authorization': `Bearer ${token}`}
    });
    if (!r.ok) return alert('삭제 실패');
    loadChars();  // 목록 갱신
}

async function selectChar(id) {
    currentCharId = id;
    document.getElementById('char-select').style.display = 'none';
    document.getElementById('game-ui').style.display = 'flex';
    // topbar에 캐릭터명 표시
    const r = await fetch(`${API}/characters/`, {headers:{'Authorization':`Bearer ${token}`}});
    const chars = await r.json();
    const c = chars.find(x => x.id === id);
    if (c) {
        document.getElementById('top-char').textContent = c.name;
        document.getElementById('top-region').textContent = '';  // look에서 업데이트
    }
    const btn = document.getElementById('btn-logout');
    if (btn) btn.style.display = 'inline-block';
    document.body.classList.add('game-active');
    transitionToGamePetals();
    await sendCmd('look');
    connectChat();
    // 명령 입력창에 자동 포커스
    setTimeout(() => {
        const cmdInput = document.getElementById('command-input');
        if (cmdInput) cmdInput.focus();
    }, 500);
}

// ─── GAME ───
let _sending = false;
async function sendCmd(cmd) {
    if (!currentCharId || _sending) return;
    if (!cmd) {
        cmd = document.getElementById('command-input').value;
        if (cmd.trim()) {
            cmdHistory.push(cmd.trim());
            if (cmdHistory.length > 50) cmdHistory.shift();
            cmdHistoryIdx = cmdHistory.length;
        }
        document.getElementById('command-input').value = '';
        if (!cmd.trim()) return;
    }
    _sending = true;
    addLog({type:'system', content:`▸ ${cmd}`, style:'system'});
    let msgs;
    try {
        const r = await fetch(`${API}/game/cmd?char_id=${currentCharId}`, {
            method:'POST', headers:{'Authorization':`Bearer ${token}`, 'Content-Type':'application/json'},
            body: JSON.stringify({command: cmd})
        });
        if (!r.ok) { _sending = false; return; }
        msgs = await r.json();
    } catch(e) {
        addLog({type:'system', content:'⚠️ 연결이 끊겼습니다. 잠시 후 다시 시도해주세요.', style:'warning'});
        _sending = false;
        return;
    }

    // 전투 틱은 1초 간격으로, 나머지는 즉시 표시
    let i = 0;
    function showNext() {
        if (i >= msgs.length) {
            updateStats();
            _sending = false;
            // 대상 캐시 초기화 (방 이동/전투 후 대상 변경 가능)
            if (typeof _targetCache !== 'undefined') { _targetCache.loaded = false; }
            const cmdInput = document.getElementById('command-input');
            if (cmdInput) { cmdInput.value = ''; cmdInput.focus(); }
            return;
        }
        const m = msgs[i];
        i++;
        if (m.type === 'map_data') {
            // 지도 데이터 → 시각적 모달 렌더링
            try {
                const mapData = JSON.parse(m.content);
                renderMapModal(mapData);
            } catch(e) { addLog({type:'system', content:m.content, style:'normal'}); }
            showNext();
        } else if (m.type === 'battle_log') {
            // 전투 로그: 2초 딜레이
            addLog(m);
            setTimeout(showNext, 2000);
        } else {
            // 시스템 메시지 등은 즉시 모두 표시
            addLog(m);
            showNext();  // 재귀, 다음 배틀 로그 전까지 즉시
        }
    }
    showNext();
}

function addLog(msg) {
    const container = document.getElementById('log-container');
    const div = document.createElement('div');
    const now = new Date();
    const ts = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
    div.className = `log-line ${msg.style || 'system'}`;
    let content = msg.content || '';
    // if chat, add sender info
    if (msg.type === 'chat' && msg.sender) {
        content = `<span class="timestamp">${ts}</span><span class="sender">${msg.sender}</span>: ${content}`;
    }
    div.innerHTML = content;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

async function updateStats() {
    // we'll fetch fresh char data every time. For now, just toggle based on what we know.
    // Better: fetch from /api/characters/ directly.
    const r = await fetch(`${API}/characters/`, {headers:{'Authorization':`Bearer ${token}`}});
    const chars = await r.json();
    const c = chars.find(x => x.id === currentCharId);
    if (!c) return;
    document.getElementById('stat-hp').textContent = `${c.hp}/${c.max_hp}`;
    document.getElementById('stat-mp').textContent = `${c.mp}/${c.max_mp}`;
    document.getElementById('hp-bar').style.width = `${(c.hp / c.max_hp * 100).toFixed(0)}%`;
    document.getElementById('mp-bar').style.width = `${(c.mp / c.max_mp * 100).toFixed(0)}%`;
    document.getElementById('stat-stage').textContent = c.martial_stage;
    document.getElementById('stat-level').textContent = c.level;
    document.getElementById('stat-exp').textContent = c.exp;
    document.getElementById('attr-grid').innerHTML = `
        <span>근골</span><span>${c.physique}</span>
        <span>기맥</span><span>${c.ki}</span>
        <span>신법</span><span>${c.agility}</span>
        <span>심안</span><span>${c.insight}</span>
        <span>매력</span><span>${c.charm}</span>
        <span>복운</span><span>${c.luck}</span>`;
    document.getElementById('top-char').textContent = c.name;
}

// ─── CHAT (WebSocket) ───
function connectChat() {
    if (chatWs) chatWs.close();
    chatWs = new WebSocket(`${WS_BASE}/chat/${username}`);
    chatWs.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        if (msg.type === 'chat') {
            const chatArea = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.style.cssText = 'font-size:12px; color:var(--text-secondary)';
            div.innerHTML = `<span style="color:var(--gold)">${msg.sender}</span>: ${msg.content}`;
            chatArea.appendChild(div);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        if (msg.type === 'system') {
            const chatArea = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.style.cssText = 'font-size:11px; color:var(--text-dim); font-style:italic';
            div.textContent = msg.content;
            chatArea.appendChild(div);
        }
    };
    chatWs.onerror = () => {
        console.log('[WS] Connection error, will retry in 5s...');
        chatWs = null;
        setTimeout(connectChat, 5000);
    };
    chatWs.onclose = (e) => {
        console.log('[WS] Disconnected (code:', e.code, '), retrying in 5s...');
        chatWs = null;
        if (currentCharId) setTimeout(connectChat, 5000);
    };
}

function sendChat() {
    const input = document.getElementById('chat-input');
    const content = input.value.trim();
    if (!content) return;
    if (chatWs && chatWs.readyState === WebSocket.OPEN) {
        chatWs.send(content);
        input.value = '';
    }
}

function switchTab(tab) {
    document.querySelectorAll('#right-tabs button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(`panel-${tab}`).classList.add('active');
}

// ─── PETALS (벚꽃 입자 애니메이션) ───
function spawnPetals(cls = '') {
    const PETALS = 50;
    const chars = ['🌸','💮','🌺','🏵','✿','❀'];
    const container = document.body;
    for (let i = 0; i < PETALS; i++) {
        const el = document.createElement('span');
        el.className = 'petal' + (cls ? ' ' + cls : '');
        el.textContent = chars[i % chars.length];
        el.style.left = Math.random() * 100 + '%';
        el.style.setProperty('--drift', (Math.random() - 0.5) * 300 + 'px');
        el.style.animationDelay = Math.random() * 8 + 's';
        el.style.animationDuration = (8 + Math.random() * 12) + 's';
        container.appendChild(el);
    }
}

function clearPetals() {
    document.querySelectorAll('.petal').forEach(el => el.remove());
}

function transitionToGamePetals() {
    // 인게임에서는 벚꽃 OFF
    clearPetals();
}

function transitionToAuthPetals() {
    // 인게임 페탈 → auth 페탈로 전환
    clearPetals();
    spawnPetals('');
}

// ─── AUTOCOMPLETE ───
const COMMANDS = [
    'look', '보기', '주변', '살펴보다',
    'north', 'south', 'east', 'west', 'up', 'down',
    '북', '남', '동', '서', '위', '아래',
    'attack', '공격', '공', '때리다',
    'talk', '대화', '말걸기', '이야기',
    'shop', '상점', '물품',
    'buy', '구매', '사다',
    'sell', '판매', '팔다',
    'status', '상태', '정보', '스탯',
    'inv', '가방', '인벤', '소지품',
    'eq', '장비', '장비창',
    'equip', '장착', '착용',
    'unequip', '해제', '장착해제',
    'use', '사용하기', '먹다',
    'enchant', '강화', '인챈트',
    'cast', '무공', '시전',
    'meditate', '명상', '수련', '운기',
    'flee', '도망', '도망치다',
    'map', '지도',
    'help', '도움말', '?',
    'save', '저장',
    'dismantle', '분해',
    'discard', '버리기', '버리다',
    'gold', '돈', '은전', '소지금',
    'quest', '퀘스트', '의뢰',
    'return_set', '귀환지정', 'rset',
    'return_go', '귀환', 'rgo',
    'arts', '무공목록', '배운무공',
    'go', '이동', '가다',
    'quest_accept', '수락',
    'quest_complete', '완료',
];

let cmdHistory = [];
let cmdHistoryIdx = -1;
let autocompleteVisible = false;

function setupAutocomplete() {
    const input = document.getElementById('command-input');
    if (!input) return;
    
    // 자동완성 드롭다운 컨테이너
    let dropdown = document.getElementById('cmd-autocomplete');
    if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.id = 'cmd-autocomplete';
        dropdown.style.cssText = 'position:absolute; bottom:100%; left:0; right:0; background:#1a1220; border:1px solid rgba(232,146,168,0.3); border-radius:6px; max-height:200px; overflow-y:auto; display:none; z-index:100;';
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(dropdown);
    }
    
    // oninput으로 직접 설정 (중복 등록 방지) — 명령어 + 대상 자동완성
    input.oninput = function() {
        const val = this.value.trim();
        const lowerVal = val.toLowerCase();
        const parts = val.split(' ');
        
        // 명령어 자동완성 (첫 단어, 공백 없음)
        if (!val || parts.length === 1) {
            const matches = COMMANDS.filter(c => c.startsWith(lowerVal) && c !== lowerVal);
            if (matches.length === 0) {
                dropdown.style.display = 'none';
                autocompleteVisible = false;
                return;
            }
            dropdown.innerHTML = matches.map(c => `<div class="ac-item" data-cmd="${c}">${c}</div>`).join('');
            dropdown.style.display = 'block';
            autocompleteVisible = true;
            dropdown.querySelectorAll('.ac-item').forEach(el => {
                el.onclick = function() {
                    input.value = this.dataset.cmd + ' ';
                    dropdown.style.display = 'none';
                    autocompleteVisible = false;
                    input.focus();
                    // 대상 명령어면 대상 목록 자동 로드
                    loadTargetAutocomplete(this.dataset.cmd);
                };
            });
            return;
        }
        
        // 대상 자동완성 (명령어 입력 후 스페이스 + 대상명)
        const cmd = parts[0].toLowerCase();
        const targetVerbs = ['attack','공격','공','때리다','talk','대화','말','말걸기','이야기','cast','무공','시전','buy','구매','사다','sell','판매','팔다'];
        const isTargetVerb = targetVerbs.includes(cmd);
        
        if (!isTargetVerb) {
            dropdown.style.display = 'none';
            autocompleteVisible = false;
            return;
        }
        
        // 대상명 부분 (첫 공백 이후)
        const targetPart = parts.slice(1).join(' ').toLowerCase();
        if (!targetPart) {
            // 스페이스만 누름 → 모든 대상 표시
            loadTargetAutocomplete(cmd);
            return;
        }
        
        // 부분 필터링
        loadTargetAutocomplete(cmd, targetPart);
    };
    
    // 대상 목록 로드 (백엔드 API 호출)
    let _targetCache = {npcs: [], monsters: [], loaded: false};
    async function loadTargetAutocomplete(cmd, filterText = '') {
        if (!_targetCache.loaded) {
            try {
                const r = await fetch(`${API}/game/targets?char_id=${currentCharId}`, {
                    headers: {'Authorization': `Bearer ${token}`}
                });
                if (r.ok) {
                    _targetCache = await r.json();
                    _targetCache.loaded = true;
                }
            } catch(e) {
                dropdown.style.display = 'none';
                autocompleteVisible = false;
                return;
            }
        }
        
        let targets = [];
        // 공격 계열: 몬스터만
        if (['attack','공격','공','때리다','cast','무공','시전'].includes(cmd)) {
            targets = _targetCache.monsters;
        }
        // 대화 계열: NPC만
        else if (['talk','대화','말','말걸기','이야기'].includes(cmd)) {
            targets = _targetCache.npcs;
        }
        // 상점 계열: NPC만
        else if (['buy','구매','사다','sell','판매','팔다'].includes(cmd)) {
            targets = _targetCache.npcs.filter(n => n.occupation === '상인');
        }

        if (filterText) {
            targets = targets.filter(t => t.name.toLowerCase().startsWith(filterText));
        }
        
        if (targets.length === 0) {
            dropdown.style.display = 'none';
            autocompleteVisible = false;
            return;
        }
        
        dropdown.innerHTML = targets.map(t => {
            const label = t.display || t.name;
            return `<div class="ac-item" data-target="${t.name}">🎯 ${label}</div>`;
        }).join('');
        dropdown.style.display = 'block';
        autocompleteVisible = true;
        
        dropdown.querySelectorAll('.ac-item').forEach(el => {
            el.onclick = function() {
                const cmd = input.value.split(' ')[0];
                input.value = cmd + ' ' + this.dataset.target;
                dropdown.style.display = 'none';
                autocompleteVisible = false;
                input.focus();
            };
        });
    };
    
    // onkeydown으로 직접 설정 (중복 등록 방지) — Tab 자동완성 + Enter 실행 + ↑↓ 히스토리
    input.onkeydown = function(e) {
        if (e.key === 'Tab' && autocompleteVisible) {
            e.preventDefault();
            const first = dropdown.querySelector('.ac-item');
            if (first) {
                // 명령어 자동완성 (data-cmd 있음)
                if (first.dataset.cmd) {
                    this.value = first.dataset.cmd + ' ';
                    dropdown.style.display = 'none';
                    autocompleteVisible = false;
                    // 대상 명령어면 대상 목록 자동 로드
                    setTimeout(() => loadTargetAutocomplete(first.dataset.cmd), 100);
                }
                // 대상 자동완성 (data-target 있음)
                else if (first.dataset.target) {
                    const cmd = this.value.split(' ')[0];
                    this.value = cmd + ' ' + first.dataset.target;
                    dropdown.style.display = 'none';
                    autocompleteVisible = false;
                }
            }
            return;
        }
        
        if (e.key === 'Enter') {
            e.preventDefault();
            sendCmd();
            return;
        }

        // 명령어 기록 (위/아래 화살표)
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (cmdHistory.length > 0) {
                cmdHistoryIdx = Math.max(0, cmdHistoryIdx - 1);
                this.value = cmdHistory[cmdHistoryIdx];
            }
        }
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (cmdHistory.length > 0 && cmdHistoryIdx < cmdHistory.length - 1) {
                cmdHistoryIdx++;
                this.value = cmdHistory[cmdHistoryIdx];
            } else {
                cmdHistoryIdx = cmdHistory.length;
                this.value = '';
            }
        }
    };
    
    // onblur로 직접 설정 (중복 등록 방지)
    input.onblur = function() {
        setTimeout(() => {
            dropdown.style.display = 'none';
            autocompleteVisible = false;
        }, 200);
    };
}

// ─── MAP MODAL ───
function renderMapModal(mapData) {
    // 기존 모달 제거
    const existing = document.getElementById('map-modal-overlay');
    if (existing) existing.remove();
    
    const overlay = document.createElement('div');
    overlay.id = 'map-modal-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:1000;display:flex;align-items:center;justify-content:center;';
    
    const modal = document.createElement('div');
    modal.style.cssText = 'background:linear-gradient(135deg,#1a1220,#0f0b12);border:1px solid rgba(232,146,168,0.3);border-radius:12px;padding:24px;max-width:700px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,0.6);';
    
    let html = `<h2 style="color:var(--cherry);margin:0 0 4px 0;font-size:22px;">🗺 ${mapData.region} 지도</h2>`;
    html += `<div style="color:var(--text-dim);font-size:13px;margin-bottom:16px;">전체 ${mapData.rooms.length}개 방 · ★ = 현재 위치</div>`;
    html += '<div style="display:flex;flex-wrap:wrap;gap:6px;">';
    
    for (const room of mapData.rooms) {
        const marker = room.is_current ? '★' : '·';
        const bg = room.is_current ? 'rgba(232,146,168,0.15)' : 'rgba(26,18,32,0.6)';
        const border = room.is_current ? '1px solid rgba(232,146,168,0.5)' : '1px solid rgba(232,146,168,0.1)';
        const color = room.is_current ? 'var(--cherry)' : 'var(--text-secondary)';
        let icons = '';
        if (room.has_npc) icons += ` 👤${room.npc_count||''}`;
        if (room.has_monster) icons += ` ⚔${room.monster_count||''}`;
        
        html += `<div style="background:${bg};border:${border};border-radius:8px;padding:8px 12px;min-width:140px;flex:1;cursor:pointer;"
            onclick="document.getElementById('command-input').value='go ${room.name}';sendCmd('go ${room.name}');document.getElementById('map-modal-overlay').remove();"
            title="클릭하여 이동: ${room.name}">
            <div style="color:${color};font-weight:700;font-size:14px;">${marker} ${room.name}</div>
            <div style="color:var(--text-dim);font-size:11px;margin:2px 0;">#${room.id}${icons}</div>
            <div style="color:var(--text-dim);font-size:10px;">${room.exits || '출구 없음'}</div>
        </div>`;
    }
    html += '</div>';
    html += '<div style="margin-top:16px;text-align:center;"><button onclick="closeMapModal()" style="background:var(--cherry);border:none;color:#fff;padding:8px 24px;border-radius:6px;cursor:pointer;font-size:14px;">닫기 (ESC)</button></div>';
    
    modal.innerHTML = html;
    overlay.appendChild(modal);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
    document.body.appendChild(overlay);
    
    // ESC 키 닫기
    document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
            const el = document.getElementById('map-modal-overlay');
            if (el) el.remove();
            document.removeEventListener('keydown', escHandler);
        }
    });
}

function closeMapModal() {
    const el = document.getElementById('map-modal-overlay');
    if (el) el.remove();
}

// ─── KEY HANDLER ───
document.addEventListener('DOMContentLoaded', () => {
    spawnPetals('');
    setupAutocomplete();
    document.getElementById('chat-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChat();
    });
});
