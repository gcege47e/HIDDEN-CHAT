import os
import uuid
from flask import Flask, render_template_string, request, jsonify

app = Flask(name)

# ذخیره اطلاعات اتاق‌ها در حافظه موقت سرور
ROOMS = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تیک‌تاک‌تو نئونی خطی پیشرفته</title>
    <link href="https://cdn.jsdelivr.net/npm/vazirmatn@33.0.3/styles/font-face.css" rel="stylesheet" type="text/css" />
    <style>
        :root {
            --bg-color: #060610;
            --neon-cyan: #00f3ff;
            --neon-magenta: #ff0055;
            --neon-purple: #9d4edd;
            --text-color: #ffffff;
            --panel-bg: rgba(15, 15, 35, 0.7);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Vazirmatn', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
            background-image: radial-gradient(circle at 50% 50%, #120e2e 0%, #060610 100%);
        }

        .container {
            width: 100%;
            max-width: 450px;
            padding: 15px;
        }

        .card {
            background: var(--panel-bg);
            border: 1px solid rgba(157, 78, 221, 0.2);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 25px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
        }

        h1 {
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #fff;
            text-shadow: 0 0 10px var(--neon-purple), 0 0 20px var(--neon-purple);
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-size: 0.85rem;
            color: #aaa;
            text-align: right;
        }

        input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(157, 78, 221, 0.3);
            border-radius: 10px;
            color: #fff;
            font-size: 0.95rem;
            transition: all 0.3s;
            text-align: right;
        }

        input:focus {
            outline: none;
            border-color: var(--neon-cyan);
            box-shadow: 0 0 12px rgba(0, 243, 255, 0.3);
        }

        .btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .btn-cyan {
            background: transparent;
            color: var(--neon-cyan);
            border: 2px solid var(--neon-cyan);
        }

        .btn-cyan:hover {
            background: var(--neon-cyan);
            color: #000;
            box-shadow: 0 0 20px var(--neon-cyan);
        }

        .btn-magenta {
            background: transparent;
            color: var(--neon-magenta);
            border: 2px solid var(--neon-magenta);
        }

        .btn-magenta:hover {
            background: var(--neon-magenta);
            color: #fff;
            box-shadow: 0 0 20px var(--neon-magenta);
        }

        .hidden { display: none !important; }

        /* سیستم اعلان بالای لایوت */
        .notification-banner {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--neon-purple);
            box-shadow: 0 0 15px var(--neon-purple);

color: #fff;
            padding: 10px 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 15px;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.4s ease;
            font-size: 0.95rem;
        }

        .notification-banner.show {
            opacity: 1;
            transform: translateY(0);
        }

        /* بخش کپی لینک در فرم اول زیر دکمه */
        .link-section {
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
            border: 1px dashed var(--neon-cyan);
            text-align: center;
        }
        .link-text {
            font-size: 0.8rem;
            color: var(--neon-cyan);
            word-break: break-all;
            margin-bottom: 10px;
            display: block;
        }

        .scoreboard {
            display: flex;
            justify-content: space-between;
            background: rgba(0,0,0,0.3);
            padding: 12px;
            border-radius: 14px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .player-score { text-align: center; flex: 1; }
        .score-num { font-size: 1.6rem; font-weight: 800; color: var(--neon-cyan); }

        /* طراحی جدول به صورت خط کشی نئونی بنفش */
        .board-container {
            position: relative;
            margin: 0 auto 20px auto;
            width: 280px;
            height: 280px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, 1fr);
            width: 100%;
            height: 100%;
            position: relative;
        }

        .cell {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2.6rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        /* اعمال خط‌کشی‌های داخلی بنفش نئونی */
        .cell:nth-child(1), .cell:nth-child(2), .cell:nth-child(4), .cell:nth-child(5) {
            border-bottom: 3px solid var(--neon-purple);
            border-left: 3px solid var(--neon-purple);
            box-shadow: -1px 1px 5px rgba(157, 78, 221, 0.4);
        }
        .cell:nth-child(3), .cell:nth-child(6) {
            border-bottom: 3px solid var(--neon-purple);
            box-shadow: 0px 1px 5px rgba(157, 78, 221, 0.4);
        }
        .cell:nth-child(7), .cell:nth-child(8) {
            border-left: 3px solid var(--neon-purple);
            box-shadow: -1px 0px 5px rgba(157, 78, 221, 0.4);
        }

        .cell.cell-x { color: var(--neon-cyan); text-shadow: 0 0 12px var(--neon-cyan); }
        .cell.cell-o { color: var(--neon-magenta); text-shadow: 0 0 12px var(--neon-magenta); }

        .win-line {
            position: absolute;
            background: #fff;
            box-shadow: 0 0 15px #fff, 0 0 25px var(--neon-cyan);
            border-radius: 4px;
            z-index: 10;
            display: none;
        }

        .status-bar {
            text-align: center;
            font-size: 1.1rem;
            padding: 10px;
            background: rgba(0,0,0,0.4);
            border-radius: 10px;
            border-bottom: 2px solid var(--neon-purple);
            margin-bottom: 15px;
        }

        /* پاپ آپ تمام صفحه انتخاب علامت هوشمند راندها */
        .overlay-choice {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(6, 6, 16, 0.96);
            border-radius: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
            padding: 20px;
            text-align: center;
        }

.choice-container { display: flex; gap: 20px; margin-top: 20px; }
        .choice-btn {
            width: 75px; height: 75px; border-radius: 50%;
            border: 3px solid #fff; font-size: 2.2rem; font-weight: bold;
            cursor: pointer; background: transparent; transition: all 0.3s;
        }
        .btn-x-choice { color: var(--neon-cyan); border-color: var(--neon-cyan); }
        .btn-x-choice:hover { background: var(--neon-cyan); color: #000; box-shadow: 0 0 20px var(--neon-cyan); }
        .btn-o-choice { color: var(--neon-magenta); border-color: var(--neon-magenta); }
        .btn-o-choice:hover { background: var(--neon-magenta); color: #fff; box-shadow: 0 0 20px var(--neon-magenta); }
    </style>
</head>
<body>

<div class="container">
    
    <div id="auth-panel" class="card">
        <h1 id="auth-title">ایجاد اتاق بازی</h1>
        <div class="form-group">
            <label>نام کاربری شما</label>
            <input type="text" id="username" placeholder="نام خود را وارد کنید...">
        </div>
        <div class="form-group">
            <label>رمز عبور اتاق</label>
            <input type="password" id="password" placeholder="یک رمز عبور دلخواه...">
        </div>
        
        <button class="btn btn-cyan" id="btn-submit" onclick="joinOrCreateRoom()">ساخت اتاق بازی</button>

        <div id="setup-link-box" class="link-section hidden">
            <span class="link-text" id="setup-link-str"></span>
            <button class="btn btn-cyan" style="padding: 6px; margin: 0; font-size: 0.85rem;" onclick="copySetupLink()">کپی کردن لینک دعوت</button>
        </div>
    </div>

    <div id="game-panel" class="card hidden">
        <div id="toast-notification" class="notification-banner"></div>

        <div class="scoreboard">
            <div class="player-score">
                <div id="p1-name" style="color: var(--neon-cyan)">بازیکن ۱ (-)</div>
                <div id="p1-score" class="score-num">0</div>
            </div>
            <div style="align-self: center; font-weight: bold; color: #444; margin: 0 10px;">VS</div>
            <div class="player-score">
                <div id="p2-name" style="color: var(--neon-magenta)">بازیکن ۲ (-)</div>
                <div id="p2-score" class="score-num">0</div>
            </div>
        </div>

        <div class="board-container">
            <div id="winning-line" class="win-line"></div>
            
            <div id="choice-overlay" class="overlay-choice hidden">
                <div id="choice-msg-text" style="font-size: 1.2rem; font-weight: bold; line-height: 1.6;">در انتظار ورود حریف...</div>
                <div id="choice-buttons" class="choice-container hidden">
                    <button class="choice-btn btn-x-choice" onclick="chooseSign('X')">X</button>
                    <button class="choice-btn btn-o-choice" onclick="chooseSign('O')">O</button>
                </div>
            </div>

            <div class="grid" id="board">
                <div class="cell" onclick="makeMove(0)"></div>
                <div class="cell" onclick="makeMove(1)"></div>
                <div class="cell" onclick="makeMove(2)"></div>
                <div class="cell" onclick="makeMove(3)"></div>
                <div class="cell" onclick="makeMove(4)"></div>
                <div class="cell" onclick="makeMove(5)"></div>
                <div class="cell" onclick="makeMove(6)"></div>
                <div class="cell" onclick="makeMove(7)"></div>
                <div class="cell" onclick="makeMove(8)"></div>
            </div>
        </div>

        <div class="status-bar" id="turn-status">در انتظار حریف...</div>
        <button class="btn btn-magenta" onclick="leaveRoom()">خروج و بستن اتاق</button>
    </div>
</div>

<script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playSound(type) {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

if (type === 'click' || type === 'write') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(type === 'click' ? 450 : 250, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
            osc.start(); osc.stop(audioCtx.currentTime + 0.08);
        } else if (type === 'win') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(260, audioCtx.currentTime);
            osc.frequency.setValueAtTime(390, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(520, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        } else if (type === 'draw') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
            osc.start(); osc.stop(audioCtx.currentTime + 0.25);
        }
    }

    // تشخیص خودکار لینک مستقیم ورودی
    const urlParams = new URLSearchParams(window.location.search);
    let urlRoomId = urlParams.get('room');
    if(urlRoomId) {
        document.getElementById('auth-title').innerText = "ورود به اتاق بازی دعوت شده";
        document.getElementById('btn-submit').innerText = "ورود به اتاق بازی";
    }

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', () => playSound('write'));
    });

    let currentRoom = null;
    let myUser = "";
    let mySign = ""; 
    let pollingInterval = null;
    let localRoundNum = 0;

    function showToast(message, duration = 3000) {
        const toast = document.getElementById('toast-notification');
        toast.innerText = message;
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, duration);
    }

    function joinOrCreateRoom() {
        playSound('click');
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if(!username || !password) {
            alert('لطفاً نام و رمز عبور را وارد کنید.');
            return;
        }

        myUser = username;

        fetch('/api/join', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password, room_id: urlRoomId || ""})
        })
        .then(res => res.json())
        .then(data => {
            if(data.error) { alert(data.error); return; }
            currentRoom = data.room_id;
            
            // نمایش بخش لینک دعوت برای سازنده اصلی اتاق
            if(!urlRoomId) {
                const inviteUrl = window.location.origin + window.location.pathname + '?room=' + currentRoom;
                document.getElementById('setup-link-str').innerText = inviteUrl;
                document.getElementById('setup-link-box').classList.remove('hidden');
                showToast('اتاق ساخته شد! لینک را کپی کرده و وارد تب جدید یا بفرستید برای حریف.');
            } else {
                // مهمان مستقیما وارد بازی می‌شود
                document.getElementById('auth-panel').classList.add('hidden');
                document.getElementById('game-panel').classList.remove('hidden');
                pollingInterval = setInterval(updateGameState, 800);
            }
        });
    }

    function copySetupLink() {

playSound('click');
        const linkText = document.getElementById('setup-link-str').innerText;
        navigator.clipboard.writeText(linkText).then(() => {
            showToast('لینک اتاق کپی شد! اکنون می‌توانید آن را در تب جدید باز کنید.');
            // بعد از کپی لینک، سازنده را هم به لایوت بازی منتقل می‌کنیم تا منتظر بماند
            setTimeout(() => {
                document.getElementById('auth-panel').classList.add('hidden');
                document.getElementById('game-panel').classList.remove('hidden');
                pollingInterval = setInterval(updateGameState, 800);
            }, 1000);
        });
    }

    function updateGameState() {
        if (!currentRoom) return;

        fetch(/api/room/${currentRoom})
        .then(res => res.json())
        .then(room => {
            document.getElementById('p1-name').innerText = room.p1 + (room.p1_sign ?  (${room.p1_sign}) : '');
            document.getElementById('p1-score').innerText = room.scores[room.p1] || 0;
            
            if(room.p2) {
                document.getElementById('p2-name').innerText = room.p2 + (room.p2_sign ?  (${room.p2_sign}) : '');
                document.getElementById('p2-score').innerText = room.scores[room.p2] || 0;
            } else {
                document.getElementById('p2-name').innerText = "در انتظار حریف...";
                document.getElementById('p2-score').innerText = "0";
            }

            const choiceOverlay = document.getElementById('choice-overlay');
            const choiceMsgText = document.getElementById('choice-msg-text');
            const choiceButtons = document.getElementById('choice-buttons');

            if (!room.p2) {
                // بازیکن دوم هنوز نیامده است
                choiceOverlay.classList.remove('hidden');
                choiceMsgText.innerText = "منتظر ورود بازیکن دوم با لینک دعوت باشید...";
                choiceButtons.classList.add('hidden');
                return;
            }

            // فاز مدیریت چرخشی نوبت انتخاب علامت
            if (!room.signs_chosen) {
                choiceOverlay.classList.remove('hidden');
                
                if (myUser === room.chooser_turn) {
                    choiceMsgText.innerText = "شما انتخاب‌کننده علامت این راند هستید! انتخاب کنید:";
                    choiceButtons.classList.remove('hidden');
                } else {
                    choiceMsgText.innerText = در انتظار انتخاب علامت توسط حریف (${room.chooser_turn}) باشید...;
                    choiceButtons.classList.add('hidden');
                }
                return;
            }

            // نمایش پیام ست شدن علامت‌ها و محو شدن آن پس از انتخاب
            if (room.signs_chosen && localRoundNum !== room.round_count) {
                mySign = (myUser === room.p1) ? room.p1_sign : room.p2_sign;
                let oppSign = (mySign === 'X') ? 'O' : 'X';
                
                choiceMsgText.innerHTML = علامت‌ها مشخص شد!<br><span style="color:var(--neon-cyan)">شما: ${mySign}</span><br><span style="color:var(--neon-magenta)">حریف: ${oppSign}</span>;
                choiceButtons.classList.add('hidden');
                
                setTimeout(() => {
                    choiceOverlay.classList.add('hidden');
                    localRoundNum = room.round_count; 
                }, 2000);
                return;
            }

            mySign = (myUser === room.p1) ? room.p1_sign : room.p2_sign;

            // وضعیت زیر جدول نوبت‌ها
            const turnStatus = document.getElementById('turn-status');
            if(room.winner_status) {
                turnStatus.innerText = "پایان این راند - در حال بروزرسانی...";
            } else {
                if(room.current_turn === mySign) {
                    turnStatus.innerText = "نوبت شماست! یک خانه را خط بزنید.";

turnStatus.style.borderBottomColor = "var(--neon-cyan)";
                } else {
                    let oppName = (mySign === room.p1_sign) ? room.p2 : room.p1;
                    turnStatus.innerText = نوبت بازیکن ${oppName} (${room.current_turn});
                    turnStatus.style.borderBottomColor = "var(--neon-magenta)";
                }
            }

            // رندر کردن خانه‌ها
            const cells = document.querySelectorAll('.cell');
            room.board.forEach((val, index) => {
                cells[index].className = 'cell'; 
                if(val) {
                    cells[index].innerText = val;
                    cells[index].classList.add(val === 'X' ? 'cell-x' : 'cell-o');
                } else { cells[index].innerText = ''; }
            });

            if(room.winner_status && !room.local_notified) {
                handleRoundEnd(room);
            }
        });
    }

    function chooseSign(sign) {
        playSound('click');
        fetch('/api/choose_sign', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({room_id: currentRoom, username: myUser, sign: sign})
        }).then(() => updateGameState());
    }

    function makeMove(index) {
        if(!currentRoom || !mySign) return;
        playSound('click');
        fetch('/api/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({room_id: currentRoom, sign: mySign, index: index})
        }).then(() => updateGameState());
    }

    function handleRoundEnd(room) {
        room.local_notified = true;
        const winLine = document.getElementById('winning-line');
        
        if(room.winner_status === 'draw') {
            playSound('draw');
            showToast('راند مساوی شد! هیچکس امتیاز نگرفت.');
        } else {
            playSound('win');
            let winnerName = room.winner_status === room.p1_sign ? room.p1 : room.p2;
            showToast(بازیکن ${winnerName} (${room.winner_status}) این راند را برد! 🎉);
            if(room.win_pattern) drawNeonLine(room.win_pattern);
        }

        setTimeout(() => {
            winLine.style.display = 'none';
            updateGameState();
        }, 3000);
    }

    function drawNeonLine(pattern) {
        const winLine = document.getElementById('winning-line');
        winLine.style.display = 'block';
        
        // رفع باگ موقعیت خط‌کشی با مرتب‌سازی عددی صحیح خانه‌ها
        const sortedPattern = pattern.map(Number).sort((a, b) => a - b).join('');
        
        const positions = {
            '012': {top: '45px', left: '10px', width: '260px', height: '5px', transform: 'none'},
            '345': {top: '140px', left: '10px', width: '260px', height: '5px', transform: 'none'},
            '678': {top: '235px', left: '10px', width: '260px', height: '5px', transform: 'none'},
            '036': {top: '10px', left: '45px', width: '5px', height: '260px', transform: 'none'},
            '147': {top: '10px', left: '140px', width: '5px', height: '260px', transform: 'none'},
            '258': {top: '10px', left: '235px', width: '5px', height: '260px', transform: 'none'},
            '048': {top: '10px', left: '10px', width: '5px', height: '350px', transform: 'rotate(-45deg)', transformOrigin: 'top left'},
            '246': {top: '10px', left: '270px', width: '5px', height: '350px', transform: 'rotate(45deg)', transformOrigin: 'top right'}
        };
        const style = positions[sortedPattern];
        if(style) {
            winLine.style.top = style.top; winLine.style.left = style.left;
            winLine.style.width = style.width; winLine.style.height = style.height;
            winLine.style.transform = style.transform; winLine.style.transformOrigin = style.transformOrigin || 'unset';
        }
    }

function leaveRoom() {
        playSound('click');
        if(currentRoom) {
            fetch('/api/leave', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({room_id: currentRoom})
            });
        }
        clearInterval(pollingInterval);
        currentRoom = null;
        window.location.search = ""; 
    }
</script>
</body>
</html>
"""

@app.route('/api/join', methods=['POST'])
def join_room():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    room_id = data.get('room_id')

    if not room_id:
        room_id = str(uuid.uuid4())[:8]
        ROOMS[room_id] = {
            'p1': username, 'password': password, 'p1_sign': None,
            'p2': None, 'p2_sign': None,
            'signs_chosen': False,
            'chooser_turn': username, 
            'round_count': 1,
            'board': ["" for _ in range(9)],
            'current_turn': 'X',
            'first_turn_next_round': 'O',
            'scores': {username: 0},
            'winner_status': None,
            'win_pattern': None
        }
        return jsonify({'room_id': room_id})
    else:
        if room_id not in ROOMS:
            return jsonify({'error': 'اتاق معتبر نیست!'}), 404
        
        room = ROOMS[room_id]
        if room['password'] != password:
            return jsonify({'error': 'رمز عبور اشتباه است!'}), 400

        if room['p1'] != username and room['p2'] is None:
            room['p2'] = username
            room['scores'][username] = 0

        return jsonify({'room_id': room_id})

@app.route('/api/choose_sign', methods=['POST'])
def choose_sign():
    data = request.json
    room_id = data.get('room_id')
    username = data.get('username')
    sign = data.get('sign')

    room = ROOMS.get(room_id)
    if room and not room['signs_chosen']:
        opp_sign = 'O' if sign == 'X' else 'X'
        if room['p1'] == username:
            room['p1_sign'] = sign
            room['p2_sign'] = opp_sign
        else:
            room['p2_sign'] = sign
            room['p1_sign'] = opp_sign
        room['signs_chosen'] = True
    return jsonify({'success': True})

@app.route('/api/room/<room_id>', methods=['GET'])
def get_room(room_id):
    if room_id in ROOMS:
        return jsonify(ROOMS[room_id])
    return jsonify({'error': 'اتاق یافت نشد'}), 404

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    room_id = data.get('room_id')
    sign = data.get('sign')
    index = int(data.get('index'))

    room = ROOMS.get(room_id)
    if not room or room['winner_status'] or not room['signs_chosen']:
        return jsonify({'error': 'غیرمجاز'}), 400

    if room['current_turn'] != sign or room['board'][index] != "":
        return jsonify({'error': 'حرکت اشتباه'}), 400

    room['board'][index] = sign
    
    win_conditions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    won = False
    for condition in win_conditions:
        if room['board'][condition[0]] == room['board'][condition[1]] == room['board'][condition[2]] == sign:
            won = True
            room['winner_status'] = sign
            room['win_pattern'] = condition
            winner_name = room['p1'] if room['p1_sign'] == sign else room['p2']
            room['scores'][winner_name] += 1
            break

    if not won and "" not in room['board']:
        room['winner_status'] = 'draw'

    if room['winner_status']:
        import threading, time
        def reset_board():
            time.sleep(3)
            room['board'] = ["" for _ in range(9)]
            room['winner_status'] = None
            room['win_pattern'] = None
            room['signs_chosen'] = False 
            room['round_count'] += 1

room['chooser_turn'] = room['p2'] if room['chooser_turn'] == room['p1'] else room['p1']
            
            room['current_turn'] = room['first_turn_next_round']
            room['first_turn_next_round'] = 'O' if room['first_turn_next_round'] == 'X' else 'X'
            
        threading.Thread(target=reset_board).start()
    else:
        room['current_turn'] = 'O' if sign == 'X' else 'X'

    return jsonify(room)

@app.route('/api/leave', methods=['POST'])
def leave_room():
    data = request.json
    room_id = data.get('room_id')
    if room_id in ROOMS: del ROOMS[room_id]
    return jsonify({'success': True})

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if name == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
