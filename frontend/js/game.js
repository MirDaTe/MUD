/* 낙화검심 - Client logic */
const API = 'http://localhost:8000/api';
const WS_BASE = 'ws://localhost:8000/ws';
let token = '';
let username = '';
let currentCharId = null;
let chatWs = null;

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
    document.getElementById('game-ui').style.display = 'flex';
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
    document.getElementById('game-ui').style.display = 'flex';
    loadChars();
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
        </div>`
    ).join('');
}

async function createChar() {
    const name = document.getElementById('char-name').value.trim();
    if (!name || name.length < 2) return alert('이름을 입력하세요');
    const data = {
        name, origin: document.getElementById('char-origin').value,
        physique: +document.getElementById('physique').value,
        ki: +document.getElementById('ki').value,
        agility: +document.getElementById('agility').value,
        insight: +document.getElementById('insight').value,
        charm: +document.getElementById('charm').value,
        luck: +document.getElementById('luck').value
    };
    const r = await fetch(`${API}/characters/`, {
        method:'POST', headers:{'Authorization':`Bearer ${token}`, 'Content-Type':'application/json'},
        body: JSON.stringify(data)
    });
    if (!r.ok) return alert('생성 실패');
    const c = await r.json();
    selectChar(c.id);
}

function showNewChar() {
    document.getElementById('new-char-form').style.display = 'block';
}

async function selectChar(id) {
    currentCharId = id;
    document.getElementById('char-select').style.display = 'none';
    document.getElementById('game-ui').style.display = 'flex';
    await sendCmd('look');
    connectChat();
}

// ─── GAME ───
async function sendCmd(cmd) {
    if (!currentCharId) return;
    if (!cmd) {
        cmd = document.getElementById('command-input').value;
        document.getElementById('command-input').value = '';
        if (!cmd.trim()) return;
    }
    addLog({type:'system', content:`▸ ${cmd}`, style:'system'});
    const r = await fetch(`${API}/game/cmd?char_id=${currentCharId}`, {
        method:'POST', headers:{'Authorization':`Bearer ${token}`, 'Content-Type':'application/json'},
        body: JSON.stringify({command: cmd})
    });
    if (!r.ok) return;
    const msgs = await r.json();
    for (const m of msgs) addLog(m);
    updateStats();
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

// ─── KEY HANDLER ───
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('command-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendCmd();
    });
    document.getElementById('chat-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendChat();
    });
});
