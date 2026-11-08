import os
import sys
import re
import glob
import time
import html
import uuid
import shutil
import random
import sqlite3
import traceback
import threading
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, send_file
import telebot
from telebot import types
import yt_dlp
import requests

# ==========================================
# 1. FLASK WEB SERVER & CONFIGURATION
# ==========================================
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = [5140546628, 7728010216, 8967715315]
PRIMARY_ADMIN = 5140546628
REQUIRED_CHANNEL = "@mrghost_121"
CHANNEL_URL = "https://t.me/mrghost_121"

if not BOT_TOKEN:
    print("❌ CRITICAL ERROR: BOT_TOKEN is missing in Environment Variables!", flush=True)

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between font-sans">
    <div class="max-w-3xl mx-auto w-full px-4 py-12 flex-grow flex flex-col justify-center">
        <div class="text-center mb-8">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/20 mb-4">
                <i class="fa-solid fa-cloud-arrow-down text-2xl text-white"></i>
            </div>
            <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight text-white">
                Universal <span class="text-cyan-400">Downloader</span>
            </h1>
            <p class="text-slate-400 mt-2 text-sm md:text-base">
                YouTube, Facebook, TikTok, Instagram, Pinterest সহ যেকোনো ভিডিও সহজে ডাউনলোড করুন
            </p>
        </div>

        <div class="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl backdrop-blur-xl">
            <form id="downloadForm" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">ভিডিও লিংক পেস্ট করুন</label>
                    <div class="relative">
                        <input type="url" id="videoUrl" required placeholder="https://..." 
                            class="w-full bg-slate-950 border border-slate-700/80 rounded-2xl py-3.5 pl-4 pr-12 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all">
                        <button type="button" onclick="pasteClipboard()" class="absolute right-3.5 top-3.5 text-slate-400 hover:text-cyan-400 transition-colors" title="Paste">
                            <i class="fa-regular fa-paste text-lg"></i>
                        </button>
                    </div>
                </div>

                <button type="submit" id="submitBtn" 
                    class="w-full py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold text-sm shadow-lg shadow-cyan-500/25 transition-all flex items-center justify-center gap-2">
                    <i class="fa-solid fa-bolt"></i>
                    <span>ডাউনলোড শুরু করুন</span>
                </button>
            </form>

            <div id="statusBox" class="hidden mt-6 text-center">
                <div class="inline-flex items-center gap-3 px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-cyan-400">
                    <svg class="animate-spin h-4 w-4 text-cyan-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                    <span id="statusText">ভিডিও সংগ্রহ ও প্রসেস হচ্ছে...</span>
                </div>
            </div>

            <div id="resultBox" class="hidden mt-6 p-4 rounded-2xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="truncate w-full sm:w-auto">
                    <p id="videoTitle" class="text-sm font-medium text-slate-200 truncate max-w-sm"></p>
                    <p class="text-xs text-emerald-400 mt-0.5"><i class="fa-solid fa-circle-check mr-1"></i>ভিডিও প্রস্তুত হয়েছে!</p>
                </div>
                <a id="downloadLink" href="#" download class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-white text-xs font-semibold text-center transition-all flex items-center justify-center gap-2">
                    <i class="fa-solid fa-arrow-down"></i>
                    <span>Save Video</span>
                </a>
            </div>
        </div>

        <div class="mt-8 text-center">
            <a href="https://t.me/mrghost_121" target="_blank" class="inline-flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-cyan-400 transition-colors">
                <i class="fa-brands fa-telegram text-base text-cyan-400"></i>
                <span>টেলিগ্রাম বটের সাথে যুক্ত হন (@mrghost_121)</span>
            </a>
        </div>
    </div>

    <footer class="py-4 text-center text-xs text-slate-600 border-t border-slate-900">
        Powered by Mr Ghost | Universal Video Engine
    </footer>

    <script>
        async function pasteClipboard() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('videoUrl').value = text;
            } catch (err) {}
        }

        document.getElementById('downloadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('videoUrl').value.trim();
            if (!url) return;

            const submitBtn = document.getElementById('submitBtn');
            const statusBox = document.getElementById('statusBox');
            const resultBox = document.getElementById('resultBox');
            const statusText = document.getElementById('statusText');

            submitBtn.disabled = true;
            statusBox.classList.remove('hidden');
            resultBox.classList.add('hidden');
            statusText.innerText = "ভিডিও সংগ্রহ ও প্রসেস হচ্ছে, অপেক্ষা করুন...";

            try {
                const response = await fetch('/api/web-download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();
                if (data.success) {
                    statusBox.classList.add('hidden');
                    resultBox.classList.remove('hidden');
                    document.getElementById('videoTitle').innerText = data.title;
                    document.getElementById('downloadLink').href = data.download_url;
                } else {
                    alert('⚠️ ' + data.error);
                    statusBox.classList.add('hidden');
                }
            } catch (err) {
                alert('⚠️ সার্ভার রেসপন্স করতে পারেনি। পুনরায় চেষ্টা করুন।');
                statusBox.classList.add('hidden');
            } finally {
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

def resolve_url(url):
    try:
        res = requests.head(url, allow_redirects=True, timeout=12)
        return res.url
    except Exception:
        return url

FFMPEG_DIR = os.path.abspath("ffmpeg_bin") if os.path.exists("ffmpeg_bin") else None

def get_ydl_options(output_path):
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    if FFMPEG_DIR:
        opts['ffmpeg_location'] = FFMPEG_DIR
    if os.path.exists("cookies.txt"):
        opts['cookiefile'] = "cookies.txt"
    return opts

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/web-download', methods=['POST'])
def web_download_api():
    data = request.get_json() or {}
    raw_url = data.get('url', '').strip()
    if not raw_url:
        return jsonify({'success': False, 'error': 'কোনো ভিডিও URL দেওয়া হয়নি'}), 400

    url = resolve_url(raw_url)
    temp_id = f"web_{int(time.time() * 1000)}"
    output_dir = f"downloads/{temp_id}"
    os.makedirs(output_dir, exist_ok=True)
    out_template = f'{output_dir}/video.%(ext)s'
    ydl_opts = get_ydl_options(out_template)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title') or "Video"

        files = [f for f in glob.glob(f"{output_dir}/*") if not f.endswith(('.temp', '.part', '.ytdl'))]
        if not files:
            return jsonify({'success': False, 'error': 'ভিডিও পাওয়া যায়নি বা ডাউনলোড ব্যর্থ হয়েছে'}), 400

        filename = os.path.basename(files[0])
        return jsonify({
            'success': True,
            'title': title,
            'download_url': f'/get-file/{temp_id}/{filename}'
        })
    except Exception as e:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)
        return jsonify({'success': False, 'error': f'ত্রুটি: {str(e)[:120]}'}), 500

@app.route('/get-file/<folder>/<filename>')
def serve_downloaded_file(folder, filename):
    file_path = os.path.join("downloads", folder, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File Not Found", 404

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"[*] Starting Web Server on port {port}...", flush=True)
    app.run(host="0.0.0.0", port=port, use_reloader=False, threaded=True)


# ==========================================
# 2. SQLITE DATABASE (NO COIN SYSTEM)
# ==========================================
DB_PATH = "bot_database.db"
db_mutex = threading.Lock()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout = 30000;")
    return conn

def init_db():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                is_banned INTEGER DEFAULT 0,
                total_uploads INTEGER DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_code TEXT PRIMARY KEY,
                file_id TEXT,
                file_type TEXT,
                file_name TEXT,
                caption TEXT,
                uploader_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_data TEXT UNIQUE
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance_mode', '0')")
        conn.commit()
        conn.close()

def register_user(user):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user.id,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                (user.id, user.username or "N/A", user.first_name or "User")
            )
        else:
            cursor.execute(
                "UPDATE users SET username = ?, first_name = ? WHERE user_id = ?",
                (user.username or "N/A", user.first_name or "User", user.id)
            )
        conn.commit()
        conn.close()
        return not bool(exists)

def is_banned(user_id):
    if user_id in ADMIN_IDS:
        return False
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return bool(row and row[0] == 1)

def set_ban_status(user_id, status):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, 'N/A', 'User')", (user_id,))
        cursor.execute("UPDATE users SET is_banned = ? WHERE user_id = ?", (1 if status else 0, user_id))
        conn.commit()
        conn.close()

def get_banned_users():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, first_name FROM users WHERE is_banned = 1")
        rows = cursor.fetchall()
        conn.close()
        return rows

def is_maintenance():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'maintenance_mode'")
        row = cursor.fetchone()
        conn.close()
        return bool(row and row[0] == '1')

def set_maintenance(state):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET value = ? WHERE key = 'maintenance_mode'", ('1' if state else '0',))
        conn.commit()
        conn.close()

def get_all_user_ids():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = [r[0] for r in cursor.fetchall()]
        conn.close()
        return rows

def get_user_stats(user_id):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0] or 0
        cursor.execute("SELECT total_uploads FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        user_uploads = row[0] if row else 0
        cursor.execute("SELECT COUNT(*) FROM files")
        total_files = cursor.fetchone()[0] or 0
        conn.close()
        return total_users, user_uploads, total_files

def save_shared_file(file_code, file_id, file_type, file_name, caption, uploader_id):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO files (file_code, file_id, file_type, file_name, caption, uploader_id) VALUES (?, ?, ?, ?, ?, ?)",
            (file_code, file_id, file_type, file_name, caption, uploader_id)
        )
        cursor.execute("UPDATE users SET total_uploads = total_uploads + 1 WHERE user_id = ?", (uploader_id,))
        conn.commit()
        conn.close()

def get_shared_file(file_code):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT file_id, file_type, file_name, caption FROM files WHERE file_code = ?", (file_code,))
        row = cursor.fetchone()
        conn.close()
        return row

def add_bulk_cards_db(cards_list):
    added = 0
    duplicate = 0
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        for c in cards_list:
            try:
                cursor.execute("INSERT INTO cards (card_data) VALUES (?)", (c,))
                added += 1
            except sqlite3.IntegrityError:
                duplicate += 1
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM cards")
        total = cursor.fetchone()[0] or 0
        conn.close()
    return added, duplicate, total

def pop_card_db():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, card_data FROM cards ORDER BY id ASC LIMIT 1")
        row = cursor.fetchone()
        if row:
            cursor.execute("DELETE FROM cards WHERE id = ?", (row[0],))
            conn.commit()
        conn.close()
        return row[1] if row else None

def count_cards_db():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cards")
        total = cursor.fetchone()[0] or 0
        conn.close()
        return total

def clear_cards_db():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cards")
        conn.commit()
        conn.close()


# ==========================================
# 3. FORCE JOIN & ACCESS VERIFICATION
# ==========================================
def check_channel_joined(user_id):
    if user_id in ADMIN_IDS:
        return True
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        print(f"[!] Channel verify warning: {e}", flush=True)
        return True

def send_join_prompt(chat_id, callback_action="verify_home"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 Join Official Channel (@mrghost_121)", url=CHANNEL_URL),
        types.InlineKeyboardButton("✅ Joined / Verify Now", callback_data=callback_action)
    )
    text = (
        "⛔ <b>Access Denied!</b>\n\n"
        "❌ বটের সকল টুলস ও ফাইল সম্পূর্ণ ফ্রিতে ব্যবহার করতে আগে আমাদের অফিসিয়াল চ্যানেলে জয়েন করতে হবে।\n"
        "❌ You must join our channel first!\n\n"
        f"👉 <b>Join:</b> {REQUIRED_CHANNEL}\n"
        "জয়েন করার পর নিচের <b>Joined / Verify Now</b> বাটনে ক্লিক করুন।"
    )
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

def verify_user_access(message, action_tag="verify_home"):
    user = message.from_user
    register_user(user)

    if is_banned(user.id):
        bot.send_message(
            message.chat.id,
            "🚫 <b>Access Denied!</b>\n\nতুমি এই বট থেকে ব্যান করা আছো! Unban করতে এডমিনের সাথে যোগাযোগ করো।",
            parse_mode="HTML"
        )
        return False

    if is_maintenance() and user.id not in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            "🚧 <b>Bot Under Maintenance!</b>\n\n🔧 সিস্টেম আপগ্রেড চলছে...\n⏳ অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।",
            parse_mode="HTML"
        )
        return False

    if not check_channel_joined(user.id):
        send_join_prompt(message.chat.id, action_tag)
        return False

    return True

def notify_admin_log(user, tool_name):
    if not bot:
        return
    try:
        name = html.escape(user.first_name or "Unknown")
        username = f"@{user.username}" if user.username else "N/A"
        log_text = (
            f"🚀 <b>{html.escape(tool_name)}</b>\n\n"
            f"👤 <b>User:</b> <a href='tg://user?id={user.id}'>{name}</a>\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"🔗 <b>Username:</b> {username}"
        )
        bot.send_message(PRIMARY_ADMIN, log_text, parse_mode="HTML")
    except Exception:
        pass


# ==========================================
# 4. KEYBOARD MENUS (NO APK / NO COINS)
# ==========================================
def get_main_reply_keyboard(user_id=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(types.KeyboardButton("📂 File Sharing Bot"))
    markup.row(
        types.KeyboardButton("🎥 YouTube Downloader"),
        types.KeyboardButton("📹 Facebook Download")
    )
    markup.row(
        types.KeyboardButton("🎵 TikTok Download"),
        types.KeyboardButton("🖼️ Thumbnail Downloader")
    )
    markup.row(
        types.KeyboardButton("📝 Yt Title Tags Extract"),
        types.KeyboardButton("📝 TikTok Title Extract")
    )
    markup.row(
        types.KeyboardButton("📞 Number to Info"),
        types.KeyboardButton("🔳 Qr Maker")
    )
    markup.row(
        types.KeyboardButton("🖼️ Background Remover"),
        types.KeyboardButton("🔐 Encode & Decode")
    )
    markup.row(
        types.KeyboardButton("🛡️ Link Checker"),
        types.KeyboardButton("📊 YouTube Watchtime")
    )
    markup.row(
        types.KeyboardButton("🌍 IP Tracker"),
        types.KeyboardButton("💫 Whatsapp Opener")
    )
    markup.row(
        types.KeyboardButton("🪪 Visa / Master Card Maker"),
        types.KeyboardButton("🆔 BD NID Tools")
    )
    markup.row(
        types.KeyboardButton("🪪 Aadhaar Tools"),
        types.KeyboardButton("⚠️ SMS BOMBER")
    )
    markup.row(
        types.KeyboardButton("😫 Google Photos"),
        types.KeyboardButton("🎓 Tutorials Hub")
    )
    markup.row(
        types.KeyboardButton("📊 Stats"),
        types.KeyboardButton("ℹ️ Help")
    )
    if user_id in ADMIN_IDS:
        markup.row(types.KeyboardButton("⚙️ Admin Panel"))
    return markup

def get_file_sharing_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton("📤 Upload File"),
        types.KeyboardButton("📊 Stats")
    )
    markup.row(types.KeyboardButton("🏠 Home"))
    return markup

def get_visa_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton("💳 CC Generator"),
        types.KeyboardButton("💳 Get Free Card")
    )
    markup.row(types.KeyboardButton("🏠 Home"))
    return markup

def get_admin_keyboard():
    maint = is_maintenance()
    maint_btn = "🔴 Maintenance OFF" if maint else "🟢 Maintenance ON"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton("📢 Broadcast"),
        types.KeyboardButton("👥 Total Users")
    )
    markup.row(
        types.KeyboardButton("➕ Add Bulk Cards"),
        types.KeyboardButton("💳 Card Stock")
    )
    markup.row(
        types.KeyboardButton("🗑️ Delete Stock"),
        types.KeyboardButton("🚫 Ban User")
    )
    markup.row(
        types.KeyboardButton("✅ Unban User"),
        types.KeyboardButton("☠️ Ban List")
    )
    markup.row(
        types.KeyboardButton(maint_btn),
        types.KeyboardButton("🏠 Home")
    )
    return markup


# ==========================================
# 5. CORE DOWNLOADER & TOOL HELPERS
# ==========================================
USER_STATES = {}

def set_state(user_id, state):
    USER_STATES[user_id] = state

def get_state(user_id):
    return USER_STATES.get(user_id)

def clear_state(user_id):
    USER_STATES.pop(user_id, None)

def send_shared_file_by_code(chat_id, file_code):
    row = get_shared_file(file_code)
    if not row:
        bot.send_message(
            chat_id,
            "❌ <b>ফাইল পাওয়া যায়নি!</b>\nফাইলটি মুছে ফেলা হয়েছে অথবা লিংকটি মেয়াদোত্তীর্ণ।",
            parse_mode="HTML"
        )
        return

    file_id, file_type, file_name, caption = row
    bot.send_message(chat_id, "⏳ আপনার ফাইল পাঠানো হচ্ছে...")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Main Channel", url=CHANNEL_URL))

    try:
        if file_type == "video":
            bot.send_video(chat_id, file_id, caption=caption or "", reply_markup=markup)
        elif file_type == "photo":
            bot.send_photo(chat_id, file_id, caption=caption or "", reply_markup=markup)
        else:
            bot.send_document(chat_id, file_id, caption=caption or file_name or "", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"❌ ফাইল পাঠাতে সমস্যা হয়েছে: {str(e)[:100]}")

def download_and_send_universal_video(user_id, raw_url):
    if not bot:
        return
    status_msg = bot.send_message(user_id, "⏳ <b>ভিডিও সংগ্রহ ও প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...</b>", parse_mode="HTML")
    target_url = resolve_url(raw_url)
    output_dir = f"downloads/{user_id}_{int(time.time())}"
    os.makedirs(output_dir, exist_ok=True)
    out_template = f'{output_dir}/%(id)s.%(ext)s'
    ydl_opts = get_ydl_options(out_template)

    try:
        video_title = "Social Video"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=True)
            if info:
                video_title = info.get('title') or info.get('description') or "Social Video"
                if len(video_title) > 200:
                    video_title = video_title[:200] + "..."

        files = [f for f in glob.glob(f"{output_dir}/*") if not f.endswith(('.temp', '.part', '.ytdl'))]
        if not files:
            bot.edit_message_text("❌ ভিডিও ডাউনলোড করা সম্ভব হয়নি।", user_id, status_msg.message_id)
            return

        file_path = files[0]
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

        if file_size_mb > 49.5:
            bot.edit_message_text("❌ ভিডিও সাইজ ৫০MB-এর বেশি হওয়ায় টেলিগ্রামে সরাসরি পাঠানো সম্ভব নয়।", user_id, status_msg.message_id)
        else:
            escaped_title = html.escape(video_title)
            caption_text = (
                f"✅ <b>ডাউনলোড সফল হয়েছে! (১০০% ফ্রি)</b>\n\n"
                f"📝 <b>ক্যাপশন (ক্লিক করলে কপি হবে):</b>\n"
                f"<code>{escaped_title}</code>\n\n"
                f'⚡ Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
            )
            with open(file_path, 'rb') as vf:
                bot.send_video(user_id, vf, caption=caption_text, parse_mode="HTML", supports_streaming=True)
            try:
                bot.delete_message(user_id, status_msg.message_id)
            except Exception:
                pass

    except Exception as e:
        err_str = str(e)
        if "tiktok.com" in target_url:
            if fallback_tiktok_download(user_id, target_url, status_msg.message_id):
                return
        try:
            bot.edit_message_text(f"⚠️ ডাউনলোড ব্যর্থ হয়েছে: {err_str[:120]}", user_id, status_msg.message_id)
        except Exception:
            pass
    finally:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)

def fallback_tiktok_download(user_id, link, status_msg_id=None):
    apis = [
        f"https://www.tikwm.com/api/?url={urllib.parse.quote(link)}",
        f"https://api.tiklydown.eu.org/api/download?url={urllib.parse.quote(link)}"
    ]
    for api_url in apis:
        try:
            r = requests.get(api_url, timeout=12).json()
            video_url = None
            title = "TikTok Video"
            if r.get("data") and r["data"].get("play"):
                video_url = r["data"]["play"]
                title = r["data"].get("title") or title
            elif r.get("video"):
                video_url = r["video"].get("noWatermark") or r["video"].get("watermark")
                title = r.get("title") or title
            if video_url:
                bot.send_video(
                    user_id,
                    video_url,
                    caption=f"🎵 <b>TikTok Video Downloaded</b>\n\n📌 <code>{html.escape(title[:180])}</code>",
                    parse_mode="HTML"
                )
                if status_msg_id:
                    try:
                        bot.delete_message(user_id, status_msg_id)
                    except Exception:
                        pass
                return True
        except Exception:
            continue
    return False


# ==========================================
# 6. BOT HANDLERS (COMMANDS & TOOLS)
# ==========================================
if bot:
    @bot.message_handler(commands=['start', 'home', 'menu'])
    def handle_start(message):
        user = message.from_user
        clear_state(user.id)
        is_new = register_user(user)

        if is_banned(user.id):
            bot.send_message(message.chat.id, "🚫 তুমি এই বট থেকে ব্যান করা আছো!")
            return

        parts = message.text.split(maxsplit=1)
        payload = parts[1].strip() if len(parts) > 1 else ""

        if payload.startswith("file_") or payload.startswith("f_"):
            if not check_channel_joined(user.id):
                send_join_prompt(message.chat.id, f"verify_file|{payload}")
                return
            send_shared_file_by_code(message.chat.id, payload)
            return

        if is_maintenance() and user.id not in ADMIN_IDS:
            bot.send_message(
                message.chat.id,
                "⚠️ <b>BOT UNDER MAINTENANCE</b>\n\nবটটি বর্তমানে মেইনটেইন্যান্সে রয়েছে। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।",
                parse_mode="HTML"
            )
            return

        if is_new:
            notify_admin_log(user, "MR GHOST BOT STARTED (New User)")

        if not check_channel_joined(user.id):
            send_join_prompt(message.chat.id, "verify_home")
            return

        welcome_text = (
            "👋 <b>WELCOME TO MR GHOST BOT!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🌐 আমাদের বটটি একটি <b>100% Free Public Utility & Video Downloader Bot</b>।\n"
            "কোনো কয়েন ছাড়াই সকল টুলস এবং ডাউনলোডার আনলিমিটেড ব্যবহার করতে পারবেন!\n\n"
            "✨ <b>ডিরেক্ট ভিডিও ডাউনলোডার:</b>\n"
            "যেকোনো ভিডিওর (YouTube, Facebook, TikTok, Instagram) লিংক সরাসরি চ্যাটে পাঠালেই বট অটোমেটিক ডাউনলোড করে দেবে।\n\n"
            "⚠️ <b>IMPORTANT NOTICE | গুরুত্বপূর্ণ সতর্কবার্তা</b>\n"
            "✅ বটটি বৈধ ও দায়িত্বশীল কাজে ব্যবহার করুন।\n"
            "❌ প্রতারণা, স্প্যাম বা অন্যের ক্ষতি হয় এমন কাজে বট ব্যবহার করবেন না।\n\n"
            "🛡️ <b>USE RESPONSIBLY • STAY SAFE</b>\n"
            "👨‍💻 Powered by <b>Mr Ghost</b> (@mrghost_121)"
        )
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode="HTML",
            reply_markup=get_main_reply_keyboard(user.id)
        )

    @bot.message_handler(commands=['help', 'about'])
    def handle_help(message):
        help_text = (
            "🛡️ <b>MR GHOST — Cyber Security & Utility Bot</b>\n\n"
            "<b>Available Free Tools:</b>\n"
            "• Universal Video Downloader (YT, FB, TikTok, IG)\n"
            "• File Sharing & Cloud Link Generator\n"
            "• YouTube Thumbnail & Title/Tags Extractor\n"
            "• TikTok Video & Title Extractor\n"
            "• Phone Number to Info & IP Location Tracker\n"
            "• Direct WhatsApp Chat Opener\n"
            "• QR Code Generator & CC/BIN Generator\n"
            "• Background Remover, Encode/Decode & Link Checker\n"
            "• NID / Aadhaar & Cyber Tutorials Hub\n\n"
            "<b>Commands:</b>\n"
            "/start - Start or restart the bot\n"
            "/help - Show this help menu\n"
            "/banlist - View banned users\n"
            "/admin - Admin Control Panel\n\n"
            "<b>Channel Rule:</b>\n"
            "আমাদের অফিসিয়াল চ্যানেলে (@mrghost_121) অবশ্যই Join থাকতে হবে।"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL),
            types.InlineKeyboardButton("💬 Contact Support", url="https://t.me/helpghotsteam")
        )
        bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)

    @bot.message_handler(commands=['banlist'])
    def handle_banlist_cmd(message):
        rows = get_banned_users()
        if not rows:
            bot.reply_to(message, "✅ No banned users.")
            return
        txt = "☠️ <b>Channel Rule Break / Banned List:</b>\n\n"
        for idx, (uid, fname) in enumerate(rows, 1):
            txt += f"{idx}. <code>{uid}</code> → <a href='tg://user?id={uid}'>{html.escape(fname or 'User')}</a>\n"
        bot.reply_to(message, txt, parse_mode="HTML")

    @bot.message_handler(commands=['unban'])
    def handle_unban_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            bot.reply_to(message, "⚠️ ফরম্যাট: <code>/unban 123456789</code>", parse_mode="HTML")
            return
        set_ban_status(int(parts[1]), False)
        bot.reply_to(message, f"✅ User <code>{parts[1]}</code> unbanned successfully!", parse_mode="HTML")

    @bot.message_handler(commands=['ban'])
    def handle_ban_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            bot.reply_to(message, "⚠️ ফরম্যাট: <code>/ban 123456789</code>", parse_mode="HTML")
            return
        set_ban_status(int(parts[1]), True)
        bot.reply_to(message, f"🚫 User <code>{parts[1]}</code> banned successfully!", parse_mode="HTML")

    @bot.message_handler(commands=['admin', 'ad'])
    def handle_admin_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            bot.reply_to(message, "❌ আপনি এই বটের এডমিন নন।")
            return
        clear_state(message.from_user.id)
        maint = is_maintenance()
        txt = (
            "⚙️ <b>ADMIN CONTROL PANEL</b>\n\n"
            f"🔧 <b>Maintenance Status:</b> {'🟢 ON' if maint else '🔴 OFF'}\n"
            f"👥 <b>Total Users:</b> <code>{len(get_all_user_ids())}</code>\n"
            f"💳 <b>Card Stock:</b> <code>{count_cards_db()}</code>"
        )
        bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=get_admin_keyboard())

    # ==========================================
    # 7. FILE UPLOAD HANDLER (DOCUMENT / VIDEO / PHOTO)
    # ==========================================
    @bot.message_handler(content_types=['document', 'video', 'photo'])
    def handle_media_upload(message):
        if not verify_user_access(message, "verify_upload"):
            return

        file_id = None
        file_type = None
        file_name = "Shared File"
        caption = message.caption or ""

        if message.document:
            file_id = message.document.file_id
            file_type = "document"
            file_name = message.document.file_name or "Document"
        elif message.video:
            file_id = message.video.file_id
            file_type = "video"
            file_name = "Video"
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_type = "photo"
            file_name = "Photo"

        if not file_id:
            return

        unique_code = "file_" + uuid.uuid4().hex[:8]
        save_shared_file(unique_code, file_id, file_type, file_name, caption, message.from_user.id)
        clear_state(message.from_user.id)

        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start={unique_code}"

        msg = (
            "✅ <b>ফাইল সফলভাবে আপলোড হয়েছে!</b>\n\n"
            f"📁 <b>নাম:</b> <code>{html.escape(file_name)}</code>\n"
            f"📂 <b>File Code:</b> <code>{unique_code}</code>\n\n"
            f"🔗 <b>শেয়ার লিংক:</b>\n{share_link}\n\n"
            "<i>এই লিংকে ক্লিক করলে চ্যানেলে জয়েন ভেরিফাই করে যে কেউ ফাইলটি পেয়ে যাবে।</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 আরও আপলোড করুন", callback_data="act_upload"))
        markup.add(types.InlineKeyboardButton("🏠 মেইন মেনু", callback_data="verify_home"))
        bot.reply_to(message, msg, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)

    # ==========================================
    # 8. CALLBACK QUERY HANDLERS
    # ==========================================
    @bot.callback_query_handler(func=lambda call: True)
    def handle_all_callbacks(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        data = call.data

        if data.startswith("verify_"):
            if not check_channel_joined(user_id):
                bot.answer_callback_query(call.id, "❌ আপনি এখনো @mrghost_121 চ্যানেলে জয়েন করেননি! আগে জয়েন করে আবার চেষ্টা করুন।", show_alert=True)
                return

            bot.answer_callback_query(call.id, "✅ জয়েন ভেরিফিকেশন সফল হয়েছে!")
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except Exception:
                pass

            if data.startswith("verify_file|"):
                file_code = data.split("|", 1)[1]
                send_shared_file_by_code(chat_id, file_code)
            else:
                bot.send_message(
                    chat_id,
                    "✅ <b>ভেরিফিকেশন সফল হয়েছে!</b>\nনিচের মেনু থেকে যেকোনো টুলস সম্পূর্ণ ফ্রিতে ব্যবহার করুন 👇",
                    parse_mode="HTML",
                    reply_markup=get_main_reply_keyboard(user_id)
                )
            return

        if not check_channel_joined(user_id):
            bot.answer_callback_query(call.id, "⚠️ আগে @mrghost_121 চ্যানেলে জয়েন করুন!", show_alert=True)
            send_join_prompt(chat_id, "verify_home")
            return

        if data == "act_upload":
            bot.answer_callback_query(call.id)
            set_state(user_id, "awaiting_file_upload")
            bot.send_message(
                chat_id,
                "📤 <b>যেকোনো ফাইল পাঠান:</b>\n\nআপনি Document, Video বা Photo পাঠাতে পারেন। বট স্বয়ংক্রিয়ভাবে একটি ইউনিক শেয়ার লিংক বানিয়ে দেবে।",
                parse_mode="HTML"
            )
            return

        tutorial_links = {
            "tut_bot": ("🤖 BOT Create", "https://youtu.be/Ws6N7RNv1Eg"),
            "tut_file": ("📂 File Share Bot Make", "https://youtu.be/xvqdMxIHVIM?si=GMFuUcFvfBtkvkOb"),
            "tut_aitrend": ("🤖 AI Trend", "https://youtu.be/kTWoiAhXMv0?si=qtENai2-PPd-gpUV"),
            "tut_follower": ("📈 Unlimited Follower", "https://youtu.be/JfFPO9GfI8A?si=5OujH-7Z8koavma3"),
            "tut_cyber": ("🌐 Cyber Website Make", "https://youtu.be/Cqy6CWkp2do?si=c9mRN5qxVyXh-qfJ"),
            "tut_vpn": ("🎮 VPN / Game Crack", "https://youtu.be/Nx1rmTSJ0Q8"),
            "tut_chatgpt": ("💎 ChatGPT Plus", "https://youtu.be/WhiBrtwqDPY"),
            "tut_hosting": ("🔥 Free Hosting + Giveaway", "https://youtu.be/3h_NiJoqx2E?si=thMaPm6M0aUcuqaB"),
        }
        if data in tutorial_links:
            bot.answer_callback_query(call.id)
            title, link = tutorial_links[data]
            notify_admin_log(call.from_user, f"Tutorial: {title}")
            bot.send_message(chat_id, f"🎬 <b>{title} Tutorial:</b>\n\n👉 {link}", parse_mode="HTML")
            return

    # ==========================================
    # 9. TEXT MESSAGE & MENU ROUTER
    # ==========================================
    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        user = message.from_user
        text = message.text.strip()
        chat_id = message.chat.id

        if text in ["🏠 Home", "🏠 Main Menu", "🔙 Back to Main Menu", "🔙 মেইন মেনু"]:
            clear_state(user.id)
            handle_start(message)
            return

        if user.id in ADMIN_IDS:
            if text in ["⚙️ Admin Panel", "🔙 Back to Admin"]:
                clear_state(user.id)
                handle_admin_cmd(message)
                return
            elif text == "🟢 Maintenance ON":
                set_maintenance(True)
                bot.send_message(chat_id, "🛑 Maintenance Mode turned ON!", reply_markup=get_admin_keyboard())
                return
            elif text == "🔴 Maintenance OFF":
                set_maintenance(False)
                bot.send_message(chat_id, "✅ Maintenance Mode turned OFF!", reply_markup=get_admin_keyboard())
                return
            elif text == "👥 Total Users":
                total_u, _, total_f = get_user_stats(user.id)
                bot.send_message(
                    chat_id,
                    f"📊 <b>Bot Statistics</b>\n\n🟢 Status: Alive\n👥 <b>Total Users:</b> <code>{total_u}</code>\n📂 <b>Total Stored Files:</b> <code>{total_f}</code>",
                    parse_mode="HTML"
                )
                return
            elif text == "📢 Broadcast":
                set_state(user.id, "admin_broadcast")
                bot.send_message(chat_id, "📢 বটের সকল ইউজারকে যে নোটিফিকেশন বা মেসেজটি পাঠাতে চান তা লিখে পাঠান (বাতিল করতে 🏠 Home চাপুন):")
                return
            elif text == "➕ Add Bulk Cards":
                set_state(user.id, "admin_add_cards")
                bot.send_message(
                    chat_id,
                    "📝 আপনার কার্ডগুলো নিচের ফরম্যাটে একটার নিচে একটা দিয়ে পেস্ট করুন:\n\n<code>5598880395051834|08|2030|038</code>\n<code>5598880395051834|08|2030|039</code>",
                    parse_mode="HTML"
                )
                return
            elif text == "💳 Card Stock":
                bot.send_message(chat_id, f"📦 <b>Current Stock Info:</b>\n\n💵 মোট উপলব্ধ কার্ড আছে: <code>{count_cards_db()}</code> টি।", parse_mode="HTML")
                return
            elif text == "🗑️ Delete Stock":
                clear_cards_db()
                bot.send_message(chat_id, "🗑️ <b>স্টক সফলভাবে খালি করা হয়েছে!</b>", parse_mode="HTML")
                return
            elif text == "🚫 Ban User":
                set_state(user.id, "admin_ban_user")
                bot.send_message(chat_id, "🚫 যাকে ব্যান করতে চান তার <b>Telegram User ID</b> পাঠান:", parse_mode="HTML")
                return
            elif text == "✅ Unban User":
                set_state(user.id, "admin_unban_user")
                bot.send_message(chat_id, "✅ যাকে আনব্যান করতে চান তার <b>Telegram User ID</b> পাঠান:", parse_mode="HTML")
                return
            elif text == "☠️ Ban List":
                handle_banlist_cmd(message)
                return

        if not verify_user_access(message, "verify_home"):
            return

        menu_buttons = {
            "📂 File Sharing Bot", "📤 Upload File", "📊 Stats", "ℹ️ Help",
            "🎥 YouTube Downloader", "📹 Facebook Download", "🎵 TikTok Download",
            "🖼️ Thumbnail Downloader", "📝 Yt Title Tags Extract", "📝 TikTok Title Extract",
            "📞 Number to Info", "🔳 Qr Maker", "🖼️ Background Remover",
            "🔐 Encode & Decode", "🛡️ Link Checker", "📊 YouTube Watchtime",
            "🌍 IP Tracker", "💫 Whatsapp Opener", "🪪 Visa / Master Card Maker",
            "💳 CC Generator", "💳 Get Free Card", "🆔 BD NID Tools",
            "🪪 Aadhaar Tools", "⚠️ SMS BOMBER", "😫 Google Photos", "🎓 Tutorials Hub"
        }

        if text in menu_buttons:
            clear_state(user.id)

            if text == "📂 File Sharing Bot":
                panel_txt = (
                    "📂 <b>FILE SHARING SYSTEM — MR GHOST</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    "⚡ এখানে আপনি যেকোনো Document, Photo বা Video আপলোড করে শেয়ার লিংক বানাতে পারবেন (১০০% ফ্রি)।\n\n"
                    "👇 নিচের বাটন থেকে নির্বাচন করুন অথবা সরাসরি ফাইল পাঠান:"
                )
                bot.send_message(chat_id, panel_txt, parse_mode="HTML", reply_markup=get_file_sharing_keyboard())
                return

            elif text == "📤 Upload File":
                set_state(user.id, "awaiting_file_upload")
                bot.send_message(
                    chat_id,
                    "📤 <b>যেকোনো ফাইল পাঠান:</b>\n\nআপনি Document, Video বা Photo পাঠাতে পারেন। বট স্বয়ংক্রিয়ভাবে একটি ইউনিক শেয়ার লিংক বানিয়ে দেবে।",
                    parse_mode="HTML"
                )
                return

            elif text == "📊 Stats":
                total_u, user_up, total_f = get_user_stats(user.id)
                stats_msg = (
                    "📊 <b>MR GHOST BOT — পরিসংখ্যান</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    "👤 <b>ব্যবহারকারীর তথ্য:</b>\n"
                    f"• নাম: {html.escape(user.first_name or 'User')}\n"
                    f"• আইডি: <code>{user.id}</code>\n"
                    f"• ইউজারনেম: @{user.username or 'N/A'}\n\n"
                    "📈 <b>অ্যাক্টিভিটি:</b>\n"
                    "• অ্যাকাউন্ট স্ট্যাটাস: <b>Free Unlimited</b> ⚡\n"
                    f"• আপনার মোট ফাইল আপলোড: <b>{user_up}</b> টি\n"
                    f"• বটের মোট ব্যবহারকারী: <b>{total_u}</b> জন\n\n"
                    "👨‍💻 <b>Powered by Mr Ghost</b>"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("📢 Join Main Channel", url=CHANNEL_URL))
                markup.add(types.InlineKeyboardButton("📤 Upload New File", callback_data="act_upload"))
                bot.send_message(chat_id, stats_msg, parse_mode="HTML", reply_markup=markup)
                return

            elif text == "ℹ️ Help":
                handle_help(message)
                return

            elif text == "🎥 YouTube Downloader":
                notify_admin_log(user, "YouTube Downloader")
                set_state(user.id, "awaiting_video_url")
                bot.send_message(chat_id, "🎥 <b>YouTube Video Downloader</b>\n\nআপনার কাঙ্ক্ষিত ইউটিউব ভিডিও বা শর্টস লিংকটি পাঠান 👇", parse_mode="HTML")
                return

            elif text == "📹 Facebook Download":
                notify_admin_log(user, "Facebook Downloader")
                set_state(user.id, "awaiting_video_url")
                bot.send_message(chat_id, "📥 <b>Facebook Video & Reels Downloader</b>\n\nআপনার ফেসবুক ভিডিও বা রিলস (Reel) লিংকটি পাঠান 👇", parse_mode="HTML")
                return

            elif text == "🎵 TikTok Download":
                notify_admin_log(user, "TikTok Downloader")
                set_state(user.id, "awaiting_video_url")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🌐 Open TikTok Downloader Web", url="https://mrghost.ct.ws/tiktok.html"))
                bot.send_message(
                    chat_id,
                    "🎵 <b>TikTok Video Downloader (No Watermark)</b>\n\nসরাসরি চ্যাটে TikTok ভিডিওর লিংক পাঠান অথবা নিচের ওয়েব টুল ব্যবহার করুন 👇",
                    parse_mode="HTML",
                    reply_markup=markup
                )
                return

            elif text == "🖼️ Thumbnail Downloader":
                notify_admin_log(user, "Thumbnail Downloader")
                set_state(user.id, "awaiting_yt_thumb")
                bot.send_message(
                    chat_id,
                    "🖼️ <b>YouTube Thumbnail Downloader</b>\n\nদয়া করে আপনার কাঙ্ক্ষিত ইউটিউব ভিডিওর লিংকটি এখানে পাঠান:\n<i>উদাহরণ: https://youtu.be/xxxxxx</i>",
                    parse_mode="HTML"
                )
                return

            elif text == "📝 Yt Title Tags Extract":
                notify_admin_log(user, "YT Title/Tags Extractor")
                set_state(user.id, "awaiting_yt_extract")
                bot.send_message(
                    chat_id,
                    "🎥 <b>YouTube Data Extractor</b>\n\nযে ভিডিওর Title, Description ও Tags চান, তার লিংকটি পাঠান 👇",
                    parse_mode="HTML"
                )
                return

            elif text == "📝 TikTok Title Extract":
                notify_admin_log(user, "TikTok Title Extractor")
                set_state(user.id, "awaiting_tik_title")
                bot.send_message(
                    chat_id,
                    "🎵 <b>TikTok Title Extractor</b>\n\nটিকিটক ভিডিওর টাইটেল বা ক্যাপশন এক্সট্রাক্ট করতে লিংক পাঠান 👇",
                    parse_mode="HTML"
                )
                return

            elif text == "📞 Number to Info":
                notify_admin_log(user, "Number to Info")
                set_state(user.id, "awaiting_num_info")
                bot.send_message(
                    chat_id,
                    "📞 <b>Number to Info Feature</b>\n\nযেকোনো নাম্বারের ডিটেইলস জানতে কান্ট্রি কোডসহ নাম্বারটি লিখে পাঠান।\nযেমন: <code>+88017XXXXXXXX</code> বা <code>+14158586273</code>",
                    parse_mode="HTML"
                )
                return

            elif text == "🔳 Qr Maker":
                notify_admin_log(user, "QR Maker")
                set_state(user.id, "awaiting_qr_text")
                bot.send_message(chat_id, "🔳 <b>QR Code Maker</b>\n\nQR Code বানাতে নিচে যেকোনো Text বা Link পাঠান 👇", parse_mode="HTML")
                return

            elif text == "🖼️ Background Remover":
                notify_admin_log(user, "Background Remover")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🌐 Open Background Remover", url="https://mboxofficial.vercel.app/"))
                markup.add(types.InlineKeyboardButton("✨ Alternative Mirror", url="https://itsmuttakin.pages.dev/bgremove"))
                bot.send_message(chat_id, "👇 <b>Click the button below to remove image background instantly:</b>", parse_mode="HTML", reply_markup=markup)
                return

            elif text == "🔐 Encode & Decode":
                notify_admin_log(user, "Encode & Decode Tool")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔐 Open Encode Tool", url="https://itsmuttakin.pages.dev/encode"))
                markup.add(types.InlineKeyboardButton("🌐 Mirror 2", url="https://mrghost.ct.ws/encode.html"))
                bot.send_message(chat_id, "⬇️ <b>Click the button below to use the Encode & Decode Tool instantly:</b>", parse_mode="HTML", reply_markup=markup)
                return

            elif text == "🛡️ Link Checker":
                notify_admin_log(user, "Link Checker Tool")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔗 Open Link Checker Tool", url="https://itsmuttakin.pages.dev/linkchek"))
                bot.send_message(chat_id, "⬇️ <b>Click the button below to check your link safely:</b>", parse_mode="HTML", reply_markup=markup)
                return

            elif text == "📊 YouTube Watchtime":
                notify_admin_log(user, "YouTube Watchtime Tool")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("⏱️ Open Watch Time Tool", url="https://itsmuttakin.pages.dev/wachtime"))
                bot.send_message(chat_id, "⬇️ <b>Click the button below to access the YouTube Watch Time Tool:</b>", parse_mode="HTML", reply_markup=markup)
                return

            elif text == "🌍 IP Tracker":
                notify_admin_log(user, "IP Tracker")
                set_state(user.id, "awaiting_ip")
                bot.send_message(chat_id, "🌍 <b>IP Tracker</b>\n\n👉 Send IP Address To Get IP Information With Location! (e.g. <code>8.8.8.8</code>)", parse_mode="HTML")
                return

            elif text == "💫 Whatsapp Opener":
                notify_admin_log(user, "WhatsApp Opener")
                set_state(user.id, "awaiting_wa_num")
                wa_msg = (
                    "📱 <b>Direct WhatsApp Chat Opener</b>\n\n"
                    "🌍 All country supported (Contact save করা লাগবে না)\n\n"
                    "<b>Examples:</b>\n"
                    "• 017XXXXXXXX (BD)\n"
                    "• +919876543210 (India)\n"
                    "• 1234567890 (USA)\n\n"
                    "📥 <b>Enter your WhatsApp number now 👇</b>"
                )
                bot.send_message(chat_id, wa_msg, parse_mode="HTML")
                return

            elif text == "🪪 Visa / Master Card Maker":
                notify_admin_log(user, "Visa / Master Card Hub")
                bot.send_message(
                    chat_id,
                    "💳 <b>Visa / Master Card Tools</b>\n\nনিচের বাটন থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন 👇",
                    parse_mode="HTML",
                    reply_markup=get_visa_menu_keyboard()
                )
                return

            elif text == "💳 CC Generator":
                notify_admin_log(user, "CC Generator")
                set_state(user.id, "awaiting_cc_bin")
                bot.send_message(
                    chat_id,
                    "💳 <b>Credit Card Generator (50 Cards)</b>\n\nআপনার কাঙ্ক্ষিত BIN টি দিন (৬ থেকে ৮ ডিজিট)।\n👇 এখন BIN টি লিখে পাঠান:",
                    parse_mode="HTML"
                )
                return

            elif text == "💳 Get Free Card":
                card = pop_card_db()
                if not card:
                    bot.send_message(chat_id, "😢 দুঃখিত! এই মুহূর্তে কোনো কার্ড স্টকে নেই। এডমিনকে জানান।")
                else:
                    random_zip = random.randint(10000, 99999)
                    bot.send_message(
                        chat_id,
                        f"🎁 <b>আপনার কার্ড:</b>\n<code>{html.escape(card)}</code>\n\n📌 <b>Random US ZIP:</b> <code>{random_zip}</code>\n\n<i>(কার্ড ও জিপ কোডের ওপর ক্লিক করলেই কপি হয়ে যাবে)</i>",
                        parse_mode="HTML"
                    )
                return

            elif text == "🆔 BD NID Tools":
                notify_admin_log(user, "BD NID Tools")
                bot.send_message(
                    chat_id,
                    "🆔 <b>BD NID Tools Resources:</b>\n\n👉 https://t.me/mrghostdataserver/15\n👉 https://t.me/mrghostdataserver/16",
                    parse_mode="HTML"
                )
                return

            elif text == "🪪 Aadhaar Tools":
                notify_admin_log(user, "Aadhaar Tools")
                bot.send_message(
                    chat_id,
                    "🪪 <b>Aadhaar Tools Resource:</b>\n\n👉 https://t.me/mrghostdataserver/14",
                    parse_mode="HTML"
                )
                return

            elif text == "⚠️ SMS BOMBER":
                notify_admin_log(user, "SMS Bomber")
                bot.send_message(
                    chat_id,
                    "⚠️ <b>SMS Bomber Resource:</b>\n\n👉 https://t.me/mrghostdataserver/43",
                    parse_mode="HTML"
                )
                return

            elif text == "😫 Google Photos":
                notify_admin_log(user, "Google Photos Unlimited")
                bot.send_message(
                    chat_id,
                    "😫 <b>Google Photos Unlimited Backup:</b>\n\n👉 https://youtu.be/P2KV2fradZs?si=Q1H-zXt0SXZyuQ6_\n🔒 <i>The File Is Password Protected (Password In This Video)</i>",
                    parse_mode="HTML"
                )
                return

            elif text == "🎓 Tutorials Hub":
                notify_admin_log(user, "Tutorials Hub")
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton("🤖 BOT Create", callback_data="tut_bot"),
                    types.InlineKeyboardButton("📂 File Share Bot Make", callback_data="tut_file"),
                    types.InlineKeyboardButton("🤖 AI Trend", callback_data="tut_aitrend"),
                    types.InlineKeyboardButton("📈 Unlimited Follower", callback_data="tut_follower"),
                    types.InlineKeyboardButton("🌐 Cyber Website Make", callback_data="tut_cyber"),
                    types.InlineKeyboardButton("🎮 VPN / Game Crack", callback_data="tut_vpn"),
                    types.InlineKeyboardButton("💎 ChatGPT Plus", callback_data="tut_chatgpt"),
                    types.InlineKeyboardButton("🔥 Free Hosting + Giveaway", callback_data="tut_hosting")
                )
                bot.send_message(
                    chat_id,
                    "🎓 <b>Welcome to Tutorials Hub!</b>\n📚 এখানে সব প্রিমিয়াম টিউটোরিয়াল ভিডিও ফ্রিতে পাবা 👇",
                    parse_mode="HTML",
                    reply_markup=markup
                )
                return

        # ==========================================
        # 10. STATE-BASED INPUT PROCESSING
        # ==========================================
        state = get_state(user.id)

        if state == "admin_broadcast" and user.id in ADMIN_IDS:
            clear_state(user.id)
            all_users = get_all_user_ids()
            sent_count = 0
            status_m = bot.send_message(chat_id, f"⏳ {len(all_users)} জন ইউজারের কাছে ব্রডকাস্ট পাঠানো হচ্ছে...")
            for uid in all_users:
                try:
                    bot.send_message(uid, f"📢 <b>Important Notice:</b>\n\n{html.escape(text)}", parse_mode="HTML")
                    sent_count += 1
                except Exception:
                    pass
            bot.edit_message_text(f"✅ সফলভাবে {sent_count} জন ইউজারের ইনবক্সে ব্রডকাস্ট মেসেজ পাঠানো হয়েছে।", chat_id, status_m.message_id)
            return

        elif state == "admin_add_cards" and user.id in ADMIN_IDS:
            clear_state(user.id)
            cards = [c.strip() for c in re.split(r'[\r\n,\s]+', text) if c.strip()]
            added, dup, total = add_bulk_cards_db(cards)
            bot.send_message(
                chat_id,
                f"✅ <b>Cards Added Successfully!</b>\n\n➕ Added: <code>{added}</code>\n♻️ Duplicate: <code>{dup}</code>\n💳 Total Card Stock: <code>{total}</code>",
                parse_mode="HTML"
            )
            return

        elif state == "admin_ban_user" and user.id in ADMIN_IDS:
            clear_state(user.id)
            if text.isdigit():
                set_ban_status(int(text), True)
                bot.send_message(chat_id, f"🚫 User <code>{text}</code> কে ব্যান করা হয়েছে।", parse_mode="HTML")
            else:
                bot.send_message(chat_id, "❌ সঠিক সংখ্যাবাচক User ID দিন।")
            return

        elif state == "admin_unban_user" and user.id in ADMIN_IDS:
            clear_state(user.id)
            if text.isdigit():
                set_ban_status(int(text), False)
                bot.send_message(chat_id, f"✅ User <code>{text}</code> কে আনব্যান করা হয়েছে।", parse_mode="HTML")
            else:
                bot.send_message(chat_id, "❌ সঠিক সংখ্যাবাচক User ID দিন।")
            return

        if state == "awaiting_yt_thumb":
            clear_state(user.id)
            video_id = ""
            if "shorts/" in text:
                video_id = re.split(r'[?#&]', text.split("shorts/")[1])[0]
            elif "youtu.be/" in text:
                video_id = re.split(r'[?#&]', text.split("youtu.be/")[1])[0]
            elif "watch?v=" in text:
                video_id = text.split("watch?v=")[1].split("&")[0]
            elif "embed/" in text:
                video_id = re.split(r'[?#&]', text.split("embed/")[1])[0]

            if len(video_id) == 11:
                thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                bot.send_photo(
                    chat_id,
                    thumb_url,
                    caption="🎯 <b>আপনার ইউটিউব ভিডিওর থাম্বনেইল!</b>\n🔥 <i>Quality: Ultra HD (Max Resolution)</i>",
                    parse_mode="HTML"
                )
            else:
                bot.send_message(chat_id, "❌ এটি সঠিক ইউটিউব লিংক নয়! দয়া করে সঠিক লিংক পাঠান।")
            return

        elif state == "awaiting_yt_extract":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, "⏳ <b>Extracting Data from YouTube...</b>", parse_mode="HTML")
            try:
                ydl_opts = get_ydl_options('%(id)s.%(ext)s')
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(text, download=False)
                title = info.get("title") or "No Title Found"
                desc = info.get("description") or "No Description Provided"
                tags_list = info.get("tags") or []
                tags = ", ".join(tags_list) if isinstance(tags_list, list) and tags_list else "No Tags Found"
                if len(desc) > 2000:
                    desc = desc[:2000] + "... (Truncated)"

                res_text = (
                    "🎯 <b>YouTube Data Extracted Successfully!</b>\n\n"
                    f"📌 <b>Title:</b>\n<code>{html.escape(title)}</code>\n\n"
                    f"📝 <b>Description:</b>\n<pre>{html.escape(desc)}</pre>\n\n"
                    f"🏷️ <b>Tags / Keywords:</b>\n<code>{html.escape(tags)}</code>"
                )
                bot.edit_message_text(res_text, chat_id, wait_m.message_id, parse_mode="HTML")
            except Exception:
                try:
                    r = requests.get("https://yt-vid.hazex.workers.dev/?url=" + urllib.parse.quote(text), timeout=10).json()
                    title = r.get("title") or "No Title Found"
                    desc = (r.get("description") or "No Description")[:2000]
                    tags_raw = r.get("tags")
                    tags = ", ".join(tags_raw) if isinstance(tags_raw, list) else (tags_raw or "No Tags Found")
                    res_text = (
                        "🎯 <b>YouTube Data Extracted Successfully!</b>\n\n"
                        f"📌 <b>Title:</b>\n<code>{html.escape(title)}</code>\n\n"
                        f"📝 <b>Description:</b>\n<pre>{html.escape(desc)}</pre>\n\n"
                        f"🏷️ <b>Tags / Keywords:</b>\n<code>{html.escape(str(tags))}</code>"
                    )
                    bot.edit_message_text(res_text, chat_id, wait_m.message_id, parse_mode="HTML")
                except Exception:
                    bot.edit_message_text("❌ এই লিংক থেকে ডাটা বের করা যায়নি! সঠিক ইউটিউব লিংক দিন।", chat_id, wait_m.message_id)
            return

        elif state == "awaiting_tik_title":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, "⏳ <b>Extracting TikTok Title...</b>", parse_mode="HTML")
            try:
                r = requests.get("https://www.tikwm.com/api/?url=" + urllib.parse.quote(text), timeout=12).json()
                if r.get("data"):
                    title = r["data"].get("title") or "No Title Found!"
                    bot.edit_message_text(
                        f"🎵 <b>TikTok Video Title Extracted Successfully!</b>\n\n📝 <b>Title:</b>\n<code>{html.escape(title)}</code>",
                        chat_id,
                        wait_m.message_id,
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text("❌ Failed to fetch TikTok video data!", chat_id, wait_m.message_id)
            except Exception:
                bot.edit_message_text("❌ সার্ভার রেসপন্স করছে না, কিছুক্ষণ পর চেষ্টা করুন।", chat_id, wait_m.message_id)
            return

        elif state == "awaiting_num_info":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, "⏳ <b>তথ্য খোঁজা হচ্ছে, দয়া করে অপেক্ষা করুন...</b>", parse_mode="HTML")
            api_keys = [
                "num_live_mneEFIScOsKerA8d3hXBMPHiF4HkZ3dEFqtIvHFv",
                "num_live_nTrhy606oIdTtY38in7aAqRgEJNKgKBqwTlhbtEE"
            ]
            selected_key = random.choice(api_keys)
            api_url = "https://api.numlookupapi.com/v1/validate/" + urllib.parse.quote(text)
            try:
                r = requests.get(api_url, headers={"apikey": selected_key}, timeout=12).json()
                if r.get("message"):
                    bot.edit_message_text("⚠️ API লিমিট শেষ হয়েছে, দয়া করে একটু পর চেষ্টা করুন।", chat_id, wait_m.message_id)
                    return
                if not r.get("valid"):
                    bot.edit_message_text("❌ নাম্বারটি সঠিক নয়! কান্ট্রি কোডসহ (যেমন: +880...) নাম্বার দিন।", chat_id, wait_m.message_id)
                    return

                num = r.get("number") or text
                fname = r.get("first_name") or ""
                lname = r.get("last_name") or ""
                full_name = (fname + " " + lname).strip() or "Not Found/N/A"
                country = r.get("country_name") or "N/A"
                ccode = r.get("country_code") or "N/A"
                city = r.get("location") or "Not Found"
                carrier = r.get("carrier") or "N/A"
                ltype = r.get("line_type") or "N/A"
                clean_num = re.sub(r'[^0-9]', '', num)
                wa_link = f"https://wa.me/{clean_num}"

                info_txt = (
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📞 <b>NUMBER INFORMATION</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"👤 <b>Owner Name    :</b> <code>{html.escape(full_name)}</code>\n"
                    f"🔹 <b>Phone Number  :</b> <code>{html.escape(num)}</code>\n"
                    f"🌍 <b>Country Name  :</b> <code>{html.escape(country)}</code>\n"
                    f"🆔 <b>Country Code  :</b> <code>{html.escape(ccode)}</code>\n"
                    f"🏙️ <b>City / Region :</b> <code>{html.escape(city)}</code>\n"
                    f"📡 <b>Sim Company   :</b> <code>{html.escape(carrier)}</code>\n"
                    f"📱 <b>Line Type     :</b> <code>{html.escape(ltype)}</code>\n\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕵️‍♂️ <b>SOCIAL MEDIA TRACK:</b>\n💬 <a href='{wa_link}'>Direct WhatsApp Chat</a>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "✅ <i>Search Completed Successfully!</i>"
                )
                bot.edit_message_text(info_txt, chat_id, wait_m.message_id, parse_mode="HTML", disable_web_page_preview=True)
            except Exception:
                bot.edit_message_text("❌ সার্ভার থেকে তথ্য আনা সম্ভব হয়নি।", chat_id, wait_m.message_id)
            return

        elif state == "awaiting_qr_text":
            clear_state(user.id)
            qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + urllib.parse.quote(text)
            bot.send_photo(
                chat_id,
                qr_url,
                caption=f"✅ <b>QR Code Ready!</b>\n\n📌 <b>Data:</b> <code>{html.escape(text)}</code>",
                parse_mode="HTML"
            )
            return

        elif state == "awaiting_ip":
            clear_state(user.id)
            if "." not in text:
                bot.send_message(chat_id, "❌ দয়া করে একটি সঠিক IP Address পাঠান (যেমন: 8.8.8.8)")
                return
            try:
                r = requests.get(f"http://ip-api.com/json/{urllib.parse.quote(text)}", timeout=10).json()
                if r.get("status") == "fail":
                    bot.send_message(chat_id, f"❌ <b>Error:</b> {html.escape(r.get('message', 'Invalid IP'))}", parse_mode="HTML")
                    return
                txt = "🔻 <b>IP Information Extracted</b>\n\n"
                for k, v in r.items():
                    txt += f"<b>{html.escape(str(k))}</b> : <code>{html.escape(str(v))}</code>\n"
                bot.send_message(chat_id, txt, parse_mode="HTML")
                if r.get("lat") and r.get("lon"):
                    bot.send_location(chat_id, r["lat"], r["lon"])
            except Exception:
                bot.send_message(chat_id, "❌ IP তথ্য খুঁজে পাওয়া যায়নি।")
            return

        elif state == "awaiting_wa_num":
            clear_state(user.id)
            number = re.sub(r'[^0-9]', '', text)
            if number.startswith("01") and len(number) == 11:
                number = "880" + number[1:]
            elif len(number) == 10 and number[0] in ["6", "7", "8", "9"]:
                number = "91" + number
            elif len(number) == 10:
                number = "1" + number

            if len(number) < 10 or len(number) > 15:
                bot.send_message(chat_id, "❌ Invalid number!\nSend a valid WhatsApp number with country code.")
                return

            link = f"https://wa.me/{number}"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("💬 Open WhatsApp Chat", url=link))
            bot.send_message(chat_id, "🌍 <b>Ready for all countries!</b>\nClick below to start chat 👇", parse_mode="HTML", reply_markup=markup)
            return

        elif state == "awaiting_cc_bin":
            clear_state(user.id)
            bin_str = re.sub(r'[^0-9]', '', text)
            if len(bin_str) < 6:
                bot.send_message(chat_id, "❌ ভুল BIN ফরম্যাট! দয়া করে অন্তত ৬ ডিজিটের সঠিক সংখ্যা পাঠান।")
                return
            bin_str = bin_str[:8]
            cards_out = []
            for _ in range(50):
                cc_num = bin_str
                while len(cc_num) < 15:
                    cc_num += str(random.randint(0, 9))
                s = 0
                double = True
                for i in range(len(cc_num) - 1, -1, -1):
                    d = int(cc_num[i])
                    if double:
                        d *= 2
                        if d > 9:
                            d -= 9
                    s += d
                    double = not double
                check_digit = (10 - (s % 10)) % 10
                cc_num += str(check_digit)
                month = f"{random.randint(1, 12):02d}"
                year = random.randint(2026, 2031)
                cvc = random.randint(100, 999)
                cards_out.append(f"{cc_num}|{month}|{year}|{cvc}")

            cards_block = "\n".join(cards_out)
            resp = (
                f"💳 <b>Generated 50 Cards for BIN:</b> <code>{bin_str}</code>\n\n"
                f"<pre>{cards_block}</pre>\n"
                "👇 ওপরের বক্সে ক্লিক করলেই <b>সবগুলো কার্ড একসাথে কপি</b> হয়ে যাবে।"
            )
            bot.send_message(chat_id, resp, parse_mode="HTML")
            return

        # ==========================================
        # 11. AUTOMATIC UNIVERSAL VIDEO URL HANDLER
        # ==========================================
        if text.startswith("http://") or text.startswith("https://"):
            clear_state(user.id)
            threading.Thread(
                target=download_and_send_universal_video,
                args=(chat_id, text),
                daemon=True
            ).start()
            return

        bot.reply_to(
            message,
            "⚠️ দয়া করে নিচের মেনু থেকে যেকোনো একটি টুল সিলেক্ট করুন অথবা ভিডিও ডাউনলোড করতে সরাসরি <b>Video URL</b> পাঠান 👇",
            parse_mode="HTML",
            reply_markup=get_main_reply_keyboard(user.id)
        )


# ==========================================
# 12. APPLICATION ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    try:
        init_db()
        t = threading.Thread(target=run_web_server, daemon=True)
        t.start()

        if not bot:
            print("⚠️ Bot polling skipped because BOT_TOKEN is not configured. Web server running.", flush=True)
            while True:
                time.sleep(3600)

        try:
            bot.remove_webhook()
            time.sleep(1)
        except Exception:
            pass

        print("🚀 Merged All-Tools & Universal Downloader Bot is LIVE!", flush=True)

        while True:
            try:
                bot.polling(none_stop=True, interval=1, timeout=20)
            except telebot.apihelper.ApiTelegramException as e:
                print(f"[!] Telegram API Exception: {e}", flush=True)
                time.sleep(5 if e.error_code == 409 else 3)
            except Exception as e:
                print(f"[!] Polling Error: {e}", flush=True)
                time.sleep(3)

    except Exception:
        print("❌ CRITICAL STARTUP ERROR:", flush=True)
        traceback.print_exc()
        sys.stdout.flush()
        time.sleep(600)
