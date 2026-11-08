import os
import sys
import re
import io
import glob
import time
import html
import uuid
import shutil
import random
import socket
import base64
import codecs
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
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# ==========================================
# 1. FLASK WEB SERVER & CONFIGURATION
# ==========================================
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = [5140546628, 7728010216, 8967715315]
PRIMARY_ADMIN = 5140546628
REQUIRED_CHANNEL = "@mrghost_121"
CHANNEL_URL = "https://t.me/mrghost_121"
REQUIRED_CHANNEL_2_URL = "https://t.me/+RlwOoen4k05kMDg9"
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "").strip()

START_PHOTO_PATH = "start_photo.jpg"
APK_BANNER_PATH = "apk_banner.jpg"
APK_API_URL = "https://app-creator-x.ueu.workers.dev/api/v1/build"

MAX_HTML_SIZE = 10 * 1024 * 1024
MAX_ZIP_SIZE = 10 * 1024 * 1024
MAX_ICON_SIZE = 6 * 1024 * 1024
MAX_ICON_PIXELS = 4_000_000
MAX_TOTAL_BODY = 16_842_752
MAX_TOTAL_FILES = MAX_TOTAL_BODY - 64 * 1024
MAX_APP_NAME_UTF16 = 80
MAX_APP_NAME_UTF8 = 120

APK_SESSIONS = {}

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
                'player_client': ['ios', 'android', 'mweb'],
                'player_skip': ['webpage', 'configs']
            }
        }
    }
    if FFMPEG_DIR:
        opts['ffmpeg_location'] = FFMPEG_DIR
    if os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 0:
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
# 2. SQLITE DATABASE
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
                coins INTEGER DEFAULT 0,
                last_daily_bonus TEXT DEFAULT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("PRAGMA table_info(users)")
        cols = [c[1] for c in cursor.fetchall()]
        if "coins" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN coins INTEGER DEFAULT 0")
        if "last_daily_bonus" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN last_daily_bonus TEXT DEFAULT NULL")

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
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('start_photo_protection', '1')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('daily_bonus_amount', '5')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('card_cost', '5')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('required_channel_2_id', '')")
        conn.commit()
        conn.close()

def get_setting(key, default=""):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row and row[0] is not None else default

def set_setting(key, value):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()

def get_user_coins(user_id):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?, 'N/A', 'User', 0)", (user_id,))
        conn.commit()
        cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row and row[0] is not None else 0

def add_user_coins(user_id, amount):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?, 'N/A', 'User', 0)", (user_id,))
        cursor.execute("UPDATE users SET coins = COALESCE(coins, 0) + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

def deduct_user_coins(user_id, amount):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?, 'N/A', 'User', 0)", (user_id,))
        cursor.execute("UPDATE users SET coins = MAX(0, COALESCE(coins, 0) - ?) WHERE user_id = ?", (amount, user_id))
        conn.commit()
        cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

def set_user_coins(user_id, amount):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?, 'N/A', 'User', 0)", (user_id,))
        cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (max(0, amount), user_id))
        conn.commit()
        conn.close()

def get_daily_bonus_amount():
    val = get_setting("daily_bonus_amount", "5")
    try:
        return int(val)
    except Exception:
        return 5

def set_daily_bonus_amount(amount: int):
    set_setting("daily_bonus_amount", str(max(1, amount)))

def get_card_cost():
    val = get_setting("card_cost", "5")
    try:
        return int(val)
    except Exception:
        return 5

def can_claim_daily_bonus(user_id):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT last_daily_bonus FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

    if not row or not row[0]:
        return True, 0, 0

    try:
        last_time = datetime.fromisoformat(row[0])
        diff = datetime.now() - last_time
        seconds_left = 86400 - int(diff.total_seconds())
        if seconds_left <= 0:
            return True, 0, 0
        else:
            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            return False, hours, minutes
    except Exception:
        return True, 0, 0

def claim_daily_bonus(user_id):
    can_claim, hours, mins = can_claim_daily_bonus(user_id)
    if not can_claim:
        return False, hours, mins, get_user_coins(user_id)

    bonus_pts = get_daily_bonus_amount()
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, coins) VALUES (?, 'N/A', 'User', 0)", (user_id,))
        now_str = datetime.now().isoformat()
        cursor.execute(
            "UPDATE users SET coins = COALESCE(coins, 0) + ?, last_daily_bonus = ? WHERE user_id = ?",
            (bonus_pts, now_str, user_id)
        )
        conn.commit()
        cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        new_balance = row[0] if row else bonus_pts
        conn.close()
    return True, bonus_pts, 0, new_balance

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

def is_photo_protection_enabled():
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'start_photo_protection'")
        row = cursor.fetchone()
        conn.close()
        return bool(not row or row[0] == '1')

def set_photo_protection(state: bool):
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('start_photo_protection', ?)", ('1' if state else '0',))
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

    # 1. Verify Channel 1 (@mrghost_121)
    try:
        member1 = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member1.status not in ["member", "administrator", "creator"]:
            return False
    except Exception as e:
        print(f"[!] Channel 1 verify warning: {e}", flush=True)

    # 2. Verify Channel 2 (VIP Channel)
    ch2_id = get_setting("required_channel_2_id") or os.getenv("REQUIRED_CHANNEL_2_ID", "").strip()
    if ch2_id:
        try:
            target_id = int(ch2_id) if (ch2_id.startswith("-") or ch2_id.isdigit()) else ch2_id
            member2 = bot.get_chat_member(target_id, user_id)
            if member2.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"[!] Channel 2 verify warning: {e}", flush=True)

    return True

def send_join_prompt(chat_id, callback_action="verify_home"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 ১. Join Main Channel (@mrghost_121)", url=CHANNEL_URL),
        types.InlineKeyboardButton("📢 ২. Join VIP Channel 2", url=REQUIRED_CHANNEL_2_URL),
        types.InlineKeyboardButton("✅ Joined Both / Verify Now", callback_data=callback_action)
    )
    text = (
        "⛔ <b>Access Denied! | প্রবেশাধিকার সংরক্ষিত</b>\n"
        "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
        "❌ বটের যেকোনো টুলস ও ফিচার ব্যবহার করতে হলে আপনাকে <b>উভয় চ্যানেলে</b> অবশ্যই জয়েন থাকতে হবে:\n\n"
        f"👉 <b>চ্যানেল ১:</b> {REQUIRED_CHANNEL}\n"
        f"👉 <b>চ্যানেল ২:</b> <a href='{REQUIRED_CHANNEL_2_URL}'>VIP Private Channel</a>\n\n"
        "উভয় চ্যানেলে জয়েন করার পর নিচের <b>✅ Joined Both / Verify Now</b> বাটনে ক্লিক করুন।"
    )
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)

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
# 4. KEYBOARD MENUS (COLORED BUTTONS)
# ==========================================
def get_main_reply_keyboard(user_id=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Row 1: File Sharing (Green / Success)
    markup.row(
        types.KeyboardButton("📂 File Sharing Bot", style="success")
    )
    # Row 2: Website to APK (Blue / Primary)
    markup.row(
        types.KeyboardButton("📱 Website to APK", style="primary")
    )
    # Row 3: YouTube (Red / Danger) | Facebook (Blue / Primary)
    markup.row(
        types.KeyboardButton("🎥 YouTube Downloader", style="danger"),
        types.KeyboardButton("📹 Facebook Download", style="primary")
    )
    # Row 3: TikTok (Blue / Primary) | Instagram (Red / Danger)
    markup.row(
        types.KeyboardButton("🎵 TikTok Download", style="primary"),
        types.KeyboardButton("📸 Instagram Download", style="danger")
    )
    # Row 4: Pinterest (Red / Danger) | Thumbnail (Green / Success)
    markup.row(
        types.KeyboardButton("📌 Pinterest Download", style="danger"),
        types.KeyboardButton("🖼️ Thumbnail Downloader", style="success")
    )
    # Row 5: Image to Link (Blue / Primary) | Live TV (Green / Success)
    markup.row(
        types.KeyboardButton("🖼️ Image to Link", style="primary"),
        types.KeyboardButton("📺 Live TV", style="success")
    )
    # Row 6: Number to Info (Green / Success) | QR Maker (Blue / Primary)
    markup.row(
        types.KeyboardButton("📞 Number to Info", style="success"),
        types.KeyboardButton("🔳 Qr Maker", style="primary")
    )
    # Row 7: Encode & Decode (Red / Danger) | Link Checker (Green / Success)
    markup.row(
        types.KeyboardButton("🔐 Encode & Decode", style="danger"),
        types.KeyboardButton("🛡️ Link Checker", style="success")
    )
    # Row 8: Title/Tags Extract (Red / Danger) | TikTok Title Extract (Blue / Primary)
    markup.row(
        types.KeyboardButton("📝 Yt Title Tags Extract", style="danger"),
        types.KeyboardButton("📝 TikTok Title Extract", style="primary")
    )
    # Row 9: IP Tracker (Blue / Primary) | WhatsApp (Green / Success)
    markup.row(
        types.KeyboardButton("🌍 IP Tracker", style="primary"),
        types.KeyboardButton("💫 Whatsapp Opener", style="success")
    )
    # Row 10: Card Maker (Blue / Primary) | NID Tools (Red / Danger)
    markup.row(
        types.KeyboardButton("🪪 Visa / Master Card Maker", style="primary"),
        types.KeyboardButton("🆔 BD NID Tools", style="danger")
    )
    # Row 11: Aadhaar Tools (Blue / Primary) | SMS Bomber (Red / Danger)
    markup.row(
        types.KeyboardButton("🪪 Aadhaar Tools", style="primary"),
        types.KeyboardButton("⚠️ SMS BOMBER", style="danger")
    )
    # Row 12: Stats (Blue / Primary) | Help (Green / Success)
    markup.row(
        types.KeyboardButton("📊 Stats", style="primary"),
        types.KeyboardButton("ℹ️ Help", style="success")
    )
    return markup

def get_file_sharing_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton("📤 Upload File", style="primary"),
        types.KeyboardButton("📊 Stats", style="success")
    )
    markup.row(types.KeyboardButton("🏠 Home", style="danger"))
    return markup

def get_visa_menu_keyboard():
    cost = get_card_cost()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton(f"💳 Get Card ({cost} Coins)", style="success"),
        types.KeyboardButton("💳 CC Generator", style="primary")
    )
    markup.row(
        types.KeyboardButton("🎁 Daily Bonus", style="primary"),
        types.KeyboardButton("💰 My Balance", style="success")
    )
    markup.row(types.KeyboardButton("🏠 Home", style="danger"))
    return markup

def get_admin_keyboard():
    maint = is_maintenance()
    maint_btn = "🔴 Maintenance OFF" if maint else "🟢 Maintenance ON"
    protect = is_photo_protection_enabled()
    protect_btn = "🔒 Photo Protect: ON" if protect else "🔓 Photo Protect: OFF"
    has_cookie = os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 0
    cookie_btn = "🍪 Cookie: ACTIVE" if has_cookie else "🍪 Upload Cookie"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton("📢 Broadcast", style="primary"),
        types.KeyboardButton("👥 Total Users", style="success")
    )
    markup.row(
        types.KeyboardButton("💰 User Coin (+/-)", style="success"),
        types.KeyboardButton("🎁 Set Daily Bonus", style="primary")
    )
    markup.row(
        types.KeyboardButton("➕ Add Bulk Cards", style="primary"),
        types.KeyboardButton("💳 Card Stock", style="success")
    )
    markup.row(
        types.KeyboardButton("🗑️ Delete Stock", style="danger"),
        types.KeyboardButton(cookie_btn, style="primary")
    )
    markup.row(
        types.KeyboardButton("🚫 Ban User", style="danger"),
        types.KeyboardButton("✅ Unban User", style="success")
    )
    markup.row(
        types.KeyboardButton("☠️ Ban List", style="danger"),
        types.KeyboardButton("📢 Channel 2 ID", style="primary")
    )
    markup.row(
        types.KeyboardButton(protect_btn, style="success" if protect else "danger"),
        types.KeyboardButton(maint_btn, style="danger" if maint else "success")
    )
    markup.row(
        types.KeyboardButton("🏠 Home", style="primary")
    )
    return markup

def get_encode_decode_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton("🔒 Base64 Encode", callback_data="op_enc_b64"),
        types.InlineKeyboardButton("🔓 Base64 Decode", callback_data="op_dec_b64")
    )
    markup.row(
        types.InlineKeyboardButton("🌐 URL Encode", callback_data="op_enc_url"),
        types.InlineKeyboardButton("🔄 URL Decode", callback_data="op_dec_url")
    )
    markup.row(
        types.InlineKeyboardButton("🔢 Hex Encode", callback_data="op_enc_hex"),
        types.InlineKeyboardButton("🔤 Hex Decode", callback_data="op_dec_hex")
    )
    markup.row(
        types.InlineKeyboardButton("0️⃣1️⃣ Binary Encode", callback_data="op_enc_bin"),
        types.InlineKeyboardButton("🔠 Binary Decode", callback_data="op_dec_bin")
    )
    markup.row(
        types.InlineKeyboardButton("🔄 ROT13 Cipher", callback_data="op_enc_rot13"),
        types.InlineKeyboardButton("🔃 Reverse Text", callback_data="op_text_rev")
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
    bot.send_message(chat_id, "⏳ <b>আপনার ফাইল পাঠানো হচ্ছে...</b>", parse_mode="HTML")

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

def fallback_cobalt_download(user_id, url, status_msg_id=None):
    cobalt_instances = [
        "https://api.cobalt.tools/api/json",
        "https://cobalt-api.kwiatekm.pl/api/json",
        "https://api.wuk.sh/api/json"
    ]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {"url": url}
    for c_url in cobalt_instances:
        try:
            res = requests.post(c_url, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                media_url = data.get("url")
                if media_url:
                    bot.send_video(
                        user_id,
                        media_url,
                        caption="🎬 <b>Video Downloaded Successfully!</b>\n\n⚡ <i>Fast Cloud Stream</i>\n👨‍💻 Powered by @mrghost_121",
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

def download_and_send_tiktok(user_id, raw_url):
    if not bot:
        return
    status_msg = bot.send_message(user_id, "⏳ <b>TikTok ভিডিও সংগ্রহ ও প্রসেস করা হচ্ছে...</b>", parse_mode="HTML")
    url = resolve_url(raw_url)

    # Method 1: TikWM (No Watermark HD)
    try:
        r = requests.get(f"https://www.tikwm.com/api/?url={urllib.parse.quote(url)}", timeout=15).json()
        if r.get("code") == 0 and r.get("data"):
            data = r["data"]
            video_url = data.get("play") or data.get("wmplay")
            title = data.get("title") or "TikTok Video"
            author = (data.get("author") or {}).get("nickname") or "Creator"
            music = (data.get("music_info") or {}).get("title") or ""

            caption = (
                "🎵 <b>𝐓𝐈𝐊𝐓𝐎𝐊 𝐕𝐈𝐃𝐄𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"👤 <b>Author:</b> <code>{html.escape(author)}</code>\n"
                f"📝 <b>Caption:</b>\n<code>{html.escape(title[:250])}</code>\n\n"
            )
            if music:
                caption += f"🎶 <b>Music:</b> <code>{html.escape(music[:80])}</code>\n\n"
            caption += (
                "⚡ <i>Downloaded without Watermark in HD</i>\n"
                '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
            )

            if video_url:
                v_res = requests.get(video_url, timeout=30, stream=True)
                if v_res.status_code == 200:
                    temp_file = f"downloads/tiktok_{user_id}_{int(time.time())}.mp4"
                    os.makedirs("downloads", exist_ok=True)
                    with open(temp_file, "wb") as f:
                        for chunk in v_res.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)

                    if os.path.exists(temp_file):
                        with open(temp_file, "rb") as vf:
                            bot.send_video(user_id, vf, caption=caption, parse_mode="HTML", supports_streaming=True)
                        os.remove(temp_file)
                        try:
                            bot.delete_message(user_id, status_msg.message_id)
                        except Exception:
                            pass
                        return
    except Exception as e:
        print(f"[!] TikWM error: {e}", flush=True)

    # Method 2: Tiklydown API
    try:
        r2 = requests.get(f"https://api.tiklydown.eu.org/api/download?url={urllib.parse.quote(url)}", timeout=15).json()
        video_url = None
        title = "TikTok Video"
        if r2.get("video"):
            video_url = r2["video"].get("noWatermark") or r2["video"].get("watermark")
            title = r2.get("title") or title
        if video_url:
            bot.send_video(
                user_id,
                video_url,
                caption=f"🎵 <b>TikTok Video Downloaded</b>\n\n📝 <code>{html.escape(title[:180])}</code>\n⚡ <i>No Watermark</i>\n👨‍💻 Powered by @mrghost_121",
                parse_mode="HTML"
            )
            try:
                bot.delete_message(user_id, status_msg.message_id)
            except Exception:
                pass
            return
    except Exception as e:
        print(f"[!] Tiklydown error: {e}", flush=True)

    # Method 3: Universal Downloader
    download_and_send_universal_video(user_id, raw_url, status_msg_id=status_msg.message_id)

def download_and_send_instagram(user_id, raw_url):
    if not bot:
        return
    status_msg = bot.send_message(user_id, "⏳ <b>Instagram রিলস/পোস্ট সংগ্রহ ও প্রসেস করা হচ্ছে...</b>", parse_mode="HTML")
    url = resolve_url(raw_url)

    # Method 1: Public IG API
    try:
        api_url = f"https://api.vkrdown.com/web/app/instagram.php?url={urllib.parse.quote(url)}"
        r = requests.get(api_url, timeout=15).json()
        data = r.get("data") or {}
        media_url = data.get("download_url") or data.get("url") or (r.get("media") or [{}])[0].get("url")
        if media_url:
            caption = (
                "📸 <b>𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "✅ <i>HD Quality Video / Photo</i>\n"
                '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
            )
            if ".mp4" in media_url or "video" in str(data.get("type", "")).lower():
                bot.send_video(user_id, media_url, caption=caption, parse_mode="HTML")
            else:
                bot.send_photo(user_id, media_url, caption=caption, parse_mode="HTML")
            try:
                bot.delete_message(user_id, status_msg.message_id)
            except Exception:
                pass
            return
    except Exception as e:
        print(f"[!] Instagram API fallback: {e}", flush=True)

    # Method 2: Cobalt fallback
    if fallback_cobalt_download(user_id, url, status_msg.message_id):
        return

    # Method 3: Universal Downloader
    download_and_send_universal_video(user_id, raw_url, status_msg_id=status_msg.message_id)

def download_and_send_pinterest(user_id, raw_url):
    if not bot:
        return
    status_msg = bot.send_message(user_id, "⏳ <b>Pinterest মিডিয়া সংগ্রহ করা হচ্ছে...</b>", parse_mode="HTML")
    url = resolve_url(raw_url)

    caption = (
        "📌 <b>𝐏𝐈𝐍𝐓𝐄𝐑𝐄𝐒𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ <i>Ultra HD Quality Media</i>\n"
        '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
    )

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        resp = requests.get(url, headers=headers, timeout=15)
        html_text = resp.text

        video_match = re.search(r'https://v\.pinimg\.com/videos/[^"\']+\.mp4', html_text) or re.search(r'https://v\.pinimg\.com/[^"\']+\.mp4', html_text)
        if video_match:
            v_url = video_match.group(0)
            bot.send_video(user_id, v_url, caption=caption, parse_mode="HTML")
            try:
                bot.delete_message(user_id, status_msg.message_id)
            except Exception:
                pass
            return

        img_match = re.search(r'https://i\.pinimg\.com/originals/[^"\']+\.(?:jpg|png|jpeg|gif)', html_text)
        if not img_match:
            img_match = re.search(r'https://i\.pinimg\.com/736x/[^"\']+\.(?:jpg|png|jpeg|gif)', html_text)
        if img_match:
            img_url = img_match.group(0)
            bot.send_photo(user_id, img_url, caption=caption, parse_mode="HTML")
            try:
                bot.delete_message(user_id, status_msg.message_id)
            except Exception:
                pass
            return
    except Exception as e:
        print(f"[!] Pinterest direct scraper error: {e}", flush=True)

    # Method 2: Cobalt fallback
    if fallback_cobalt_download(user_id, url, status_msg.message_id):
        return

    # Method 3: Universal Downloader
    download_and_send_universal_video(user_id, raw_url, status_msg_id=status_msg.message_id)

def download_and_send_universal_video(user_id, raw_url, status_msg_id=None):
    if not bot:
        return
    if status_msg_id:
        msg_id = status_msg_id
    else:
        status_msg = bot.send_message(user_id, "⏳ <b>ভিডিও সংগ্রহ ও প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...</b>", parse_mode="HTML")
        msg_id = status_msg.message_id

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
            # Fallback to cobalt
            if fallback_cobalt_download(user_id, target_url, msg_id):
                return
            bot.edit_message_text("❌ ভিডিও ডাউনলোড করা সম্ভব হয়নি।", user_id, msg_id)
            return

        file_path = files[0]
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

        if file_size_mb > 49.5:
            bot.edit_message_text("❌ ভিডিও সাইজ ৫০MB-এর বেশি হওয়ায় টেলিগ্রামে সরাসরি পাঠানো সম্ভব নয়।", user_id, msg_id)
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
                bot.delete_message(user_id, msg_id)
            except Exception:
                pass

    except Exception as e:
        err_str = str(e)
        if "tiktok.com" in target_url:
            download_and_send_tiktok(user_id, target_url)
            return
        # Try Cobalt fallback for YouTube / general
        if fallback_cobalt_download(user_id, target_url, msg_id):
            return

        if "confirm you're not a bot" in err_str.lower() or "sign in" in err_str.lower():
            err_msg = (
                "⚠️ <b>YouTube Bot Detection Error:</b>\n\n"
                "ইউটিউব বর্তমানে এই ভিডিওর জন্য কুকিজ ভেরিফিকেশন দাবি করছে।\n"
                "এডমিনকে <code>cookies.txt</code> ফাইল কনফিগার করার অনুরোধ করা হয়েছে।"
            )
        else:
            err_msg = f"⚠️ ডাউনলোড ব্যর্থ হয়েছে: {err_str[:120]}"

        try:
            bot.edit_message_text(err_msg, user_id, msg_id, parse_mode="HTML")
        except Exception:
            pass
    finally:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)

# Helper: Number to Info
def resolve_phone_info(number_text):
    clean_text = number_text.strip()
    if not clean_text.startswith("+"):
        clean_text = "+" + clean_text

    clean_digits = re.sub(r'[^0-9]', '', clean_text)

    res = {
        "valid": False,
        "possible": False,
        "country": "Unknown",
        "carrier": "Standard Mobile/Telco",
        "timezone": "Unknown",
        "type": "Mobile / Telco",
        "intl_format": clean_text,
        "nat_format": clean_text,
        "owner_name": "Not Publicly Indexed",
        "clean_digits": clean_digits
    }

    try:
        parsed = phonenumbers.parse(clean_text, None)
        res["valid"] = phonenumbers.is_valid_number(parsed)
        res["possible"] = phonenumbers.is_possible_number(parsed)
        res["country"] = geocoder.description_for_number(parsed, "en") or "International"
        res["carrier"] = carrier.name_for_number(parsed, "en") or "Standard Mobile/Telco"
        tz_list = timezone.time_zones_for_number(parsed)
        res["timezone"] = ", ".join(tz_list) if tz_list else "Unknown"

        ntype = phonenumbers.number_type(parsed)
        type_map = {
            0: "Fixed Line (Landline)",
            1: "Mobile",
            2: "Fixed Line or Mobile",
            3: "Toll-Free",
            4: "Premium Rate",
            5: "Shared Cost",
            6: "VoIP",
            7: "Personal Number",
            8: "Pager",
            9: "UAN",
            10: "Voicemail"
        }
        res["type"] = type_map.get(ntype, "Mobile / Telco")
        res["intl_format"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        res["nat_format"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    except Exception as e:
        print(f"[!] phonenumbers parse error: {e}", flush=True)

    api_keys = [
        "num_live_mneEFIScOsKerA8d3hXBMPHiF4HkZ3dEFqtIvHFv",
        "num_live_nTrhy606oIdTtY38in7aAqRgEJNKgKBqwTlhbtEE"
    ]
    for k in api_keys:
        try:
            r = requests.get(
                "https://api.numlookupapi.com/v1/validate/" + urllib.parse.quote(clean_text),
                headers={"apikey": k},
                timeout=5
            ).json()
            if r.get("valid"):
                fn = r.get("first_name") or ""
                ln = r.get("last_name") or ""
                name = (fn + " " + ln).strip()
                if name:
                    res["owner_name"] = name
                if r.get("carrier") and res["carrier"] in ["Unknown", "Standard Mobile/Telco"]:
                    res["carrier"] = r.get("carrier")
                if r.get("country_name"):
                    res["country"] = r.get("country_name")
                break
        except Exception:
            continue

    return res

# Helper: Link Safety Analyzer
def analyze_link_safety(raw_url):
    url = raw_url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    report = {
        "url": url,
        "is_up": False,
        "status_code": "N/A",
        "final_url": url,
        "redirect_count": 0,
        "redirect_chain": [],
        "ip": "Unknown",
        "server": "Unknown",
        "response_time_ms": 0,
        "ssl_secure": url.startswith("https://"),
        "safety_level": "🟢 SAFE",
        "flags": []
    }

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""

    try:
        ip = socket.gethostbyname(hostname)
        report["ip"] = ip
    except Exception:
        report["flags"].append("⚠️ Domain DNS IP could not be resolved")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    start_t = time.time()
    try:
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True, stream=True)
        report["response_time_ms"] = int((time.time() - start_t) * 1000)
        report["is_up"] = True
        report["status_code"] = f"{res.status_code} {res.reason}"
        report["final_url"] = res.url
        report["server"] = res.headers.get("Server", "Cloudflare / Protected")

        if res.history:
            report["redirect_count"] = len(res.history)
            report["redirect_chain"] = [r.url for r in res.history] + [res.url]
    except requests.exceptions.SSLError:
        report["flags"].append("❌ Invalid SSL Certificate (Insecure)")
        report["safety_level"] = "🔴 DANGEROUS"
    except Exception as e:
        report["flags"].append(f"❌ Connection Failed: {str(e)[:50]}")
        report["safety_level"] = "🔴 UNREACHABLE"
        return report

    suspicious_tlds = [".xyz", ".top", ".buzz", ".fit", ".tk", ".ml", ".ga", ".cf", ".gq", ".work", ".click", ".surf", ".rest"]
    phishing_keywords = ["login", "signin", "verify", "secure", "update", "bank", "account-check", "free-gift", "giveaway", "free-claim"]

    final_host = urllib.parse.urlparse(report["final_url"]).hostname or ""

    if re.match(r'^\d+\.\d+\.\d+\.\d+$', final_host):
        report["flags"].append("⚠️ Uses raw IP address as host (Phishing Risk)")
        report["safety_level"] = "🟡 SUSPICIOUS"

    for tld in suspicious_tlds:
        if final_host.endswith(tld):
            report["flags"].append(f"⚠️ High-risk TLD ({tld})")
            report["safety_level"] = "🟡 SUSPICIOUS"
            break

    for kw in phishing_keywords:
        if kw in report["final_url"].lower():
            report["flags"].append(f"⚠️ Contains sensitive keyword: '{kw}'")
            if report["safety_level"] != "🔴 DANGEROUS":
                report["safety_level"] = "🟡 SUSPICIOUS"
            break

    if report["redirect_count"] >= 3:
        report["flags"].append(f"⚠️ High number of redirects ({report['redirect_count']} hops)")

    if not report["final_url"].startswith("https://"):
        report["flags"].append("⚠️ Insecure connection (HTTP without SSL)")
        if report["safety_level"] == "🟢 SAFE":
            report["safety_level"] = "🟡 UNENCRYPTED"

    if not report["flags"]:
        report["flags"].append("✅ No known security threats detected")

    return report

# Helper: Encode / Decode
def run_encode_decode(op_code, text):
    try:
        if op_code == "op_enc_b64":
            return base64.b64encode(text.encode('utf-8')).decode('utf-8')
        elif op_code == "op_dec_b64":
            return base64.b64decode(text.encode('utf-8')).decode('utf-8', errors='replace')
        elif op_code == "op_enc_url":
            return urllib.parse.quote(text)
        elif op_code == "op_dec_url":
            return urllib.parse.unquote(text)
        elif op_code == "op_enc_hex":
            return text.encode('utf-8').hex()
        elif op_code == "op_dec_hex":
            clean_hex = text.strip().replace(" ", "").replace("0x", "")
            return bytes.fromhex(clean_hex).decode('utf-8', errors='replace')
        elif op_code == "op_enc_bin":
            return ' '.join(format(ord(c), '08b') for c in text)
        elif op_code == "op_dec_bin":
            clean_bin = [b for b in text.strip().split() if len(b) == 8]
            return ''.join(chr(int(b, 2)) for b in clean_bin)
        elif op_code == "op_enc_rot13":
            return codecs.encode(text, 'rot_13')
        elif op_code == "op_text_rev":
            return text[::-1]
    except Exception as e:
        return f"Conversion Error: {e}"
    return "Unknown operation"

# Helper: ImgBB Upload
def upload_image_to_imgbb(file_bytes):
    api_key = os.getenv("IMGBB_API_KEY", "").strip() or IMGBB_API_KEY
    if not api_key:
        return {"success": False, "error": "IMGBB_API_KEY is not configured in environment variables!"}

    b64_image = base64.b64encode(file_bytes).decode('utf-8')
    try:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": api_key,
                "image": b64_image
            },
            timeout=30
        ).json()
        if res.get("success") and res.get("data"):
            return {
                "success": True,
                "url": res["data"].get("url"),
                "display_url": res["data"].get("display_url"),
                "delete_url": res["data"].get("delete_url"),
                "size": round(res["data"].get("size", 0) / 1024, 2)
            }
        else:
            err = (res.get("error") or {}).get("message") or "Upload failed"
            return {"success": False, "error": err}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==========================================
# APK BUILDER (WEBSITE TO APK) HELPERS
# ==========================================
def validate_app_name(value):
    value = (value or "").strip()
    if not value:
        return "দয়া করে একটি সঠিক অ্যাপ নাম লিখুন।"
    utf16_units = len(value.encode("utf-16-le")) // 2
    utf8_bytes = len(value.encode("utf-8"))
    if utf16_units > MAX_APP_NAME_UTF16:
        return f"অ্যাপ নাম অনেক বড় ({utf16_units}/80 UTF-16 units)।"
    if utf8_bytes > MAX_APP_NAME_UTF8:
        return f"অ্যাপ নাম সাইজে বড় ({utf8_bytes}/120 UTF-8 bytes)।"
    if any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value):
        return "অ্যাপ নামে কোনো ইনভ্যালিড কন্ট্রোল ক্যারেক্টার থাকতে পারবে না।"
    return None

def validate_icon(content):
    if not content:
        return "আইকন ফাইলটি খালি।"
    try:
        with Image.open(io.BytesIO(content)) as image:
            if image.format not in ("PNG", "JPEG"):
                return "শুধুমাত্র PNG এবং JPEG ফরম্যাটের আইকন গ্রহণযোগ্য।"
            width, height = image.size
            if width * height > MAX_ICON_PIXELS:
                return "আইকন ছবির সাইজ অনেক বড় (সর্বোচ্চ 4 Megapixels অনুমোদিত)।"
            if image.format == "PNG" and image.info.get("interlace"):
                return "Interlaced PNG আইকন কাজ করবে না। সাধারণ Standard PNG ছবি দিন।"
    except Exception:
        return "ফাইলটি কোনো বৈধ PNG বা JPEG ছবি নয়।"
    return None

def send_apk_home(chat_id, user_id=None):
    if user_id:
        clear_state(user_id)
        APK_SESSIONS.pop(user_id, None)

    caption = (
        "📱 <b>𝐀𝐏𝐊 𝐂𝐎𝐍𝐕𝐄𝐑𝐓𝐄𝐑 𝐒𝐓𝐔𝐃𝐈𝐎 — 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓</b>\n"
        "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
        "🌐 <b>Website to Android APK</b>\n\n"
        "আপনার যেকোনো HTML ওয়েবসাইট বা ZIP প্রজেক্টকে সরাসরি অ্যান্ড্রয়েড অ্যাপ্লিকেশনে (APK) রূপান্তর করুন।\n\n"
        "⚡ <i>Fast • Secure • Real Android APK</i>\n"
        '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Create APK", callback_data="apk:new"),
        types.InlineKeyboardButton("📘 How it works", callback_data="apk:help")
    )

    if os.path.exists(APK_BANNER_PATH):
        try:
            with open(APK_BANNER_PATH, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=caption, parse_mode="HTML", reply_markup=markup)
                return
        except Exception as e:
            print(f"[!] Error sending APK banner: {e}", flush=True)

    bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=markup)

def send_apk_confirmation(chat_id, user_id):
    session = APK_SESSIONS.get(user_id)
    if not session or "html" not in session or "icon" not in session:
        bot.send_message(chat_id, "❌ সেশন পাওয়া যায়নি। অনুগ্রহ করে আবার শুরু করুন।", reply_markup=get_main_reply_keyboard(user_id))
        return
    app_name = session.get("app_name", "My App")
    html_name, html_bytes = session["html"]
    icon_name, icon_bytes = session["icon"]

    summary_text = (
        "<b>Step 4/5 — Review & Confirmation</b>\n"
        "✅  ✅  ✅  🔵  ⚪\n\n"
        "📋 <b>সবকিছু প্রস্তুত! কনফার্মেশন দিন:</b>\n"
        "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n"
        f"📛 <b>App Name:</b> <b>{html.escape(app_name)}</b>\n"
        f"📄 <b>Website:</b> <code>{html.escape(html_name)}</code> ({round(len(html_bytes)/1024, 1)} KB)\n"
        f"🖼️ <b>Icon:</b> <code>{html.escape(icon_name)}</code> ({round(len(icon_bytes)/1024, 1)} KB)\n"
        "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
        "সব তথ্য সঠিক থাকলে <b>Build APK</b> বাটনে চাপুন:"
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✅ Build APK", callback_data="apk:build"),
        types.InlineKeyboardButton("✏️ Rename", callback_data="apk:rename")
    )
    markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
    bot.send_message(chat_id, summary_text, parse_mode="HTML", reply_markup=markup)

def animate_apk_build(chat_id, message_id, stop_event):
    frames = ["◐", "◓", "◑", "◒"]
    stages = [
        ("Uploading website files", "📤", 25),
        ("Preparing Android WebView", "🧩", 50),
        ("Compiling Android package", "⚙️", 75),
        ("Finalizing & Packing APK", "🔐", 95),
    ]
    index = 0
    while not stop_event.is_set():
        label, icon, percent = stages[index % len(stages)]
        filled = max(1, percent // 10)
        bar = "🟦" * filled + "▫️" * (10 - filled)
        text = (
            f"<b>{frames[index % len(frames)]} 𝐀𝐏𝐊 𝐁𝐔𝐈𝐋𝐃 𝐈𝐍 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            f"{icon} <b>{label}...</b>\n"
            f"{bar} <b>{percent}%</b>\n\n"
            "☕ অনুগ্রহ করে ১–২ মিনিট অপেক্ষা করুন...\n"
            "<i>আপনার ফাইলগুলো নিরাপদে প্রসেস হচ্ছে।</i>"
        )
        try:
            bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML")
        except Exception:
            pass
        index += 1
        stop_event.wait(2.0)

def build_apk_task(chat_id, user_id, status_message_id=None):
    session = APK_SESSIONS.get(user_id)
    if not session or "html" not in session or "icon" not in session:
        bot.send_message(chat_id, "❌ সেশনের মেয়াদ শেষ হয়েছে। দয়া করে আবার শুরু করুন।", reply_markup=get_main_reply_keyboard(user_id))
        return

    stop_event = threading.Event()
    anim_thread = None
    if status_message_id:
        anim_thread = threading.Thread(target=animate_apk_build, args=(chat_id, status_message_id, stop_event), daemon=True)
        anim_thread.start()
    else:
        try:
            m = bot.send_message(chat_id, "⚙️ <b>Preparing your APK build...</b>", parse_mode="HTML")
            status_message_id = m.message_id
            anim_thread = threading.Thread(target=animate_apk_build, args=(chat_id, status_message_id, stop_event), daemon=True)
            anim_thread.start()
        except Exception:
            pass

    app_name = session["app_name"]
    html_name, html_bytes = session["html"]
    icon_name, icon_bytes = session["icon"]

    html_mime = "application/zip" if html_name.lower().endswith(".zip") else "text/html"
    icon_mime = "image/png" if icon_name.lower().endswith("png") else "image/jpeg"
    files = {
        "html": (html_name, html_bytes, html_mime),
        "icon": (icon_name, icon_bytes, icon_mime)
    }

    try:
        resp = requests.post(
            APK_API_URL,
            data={"app_name": app_name},
            files=files,
            timeout=150
        )
        stop_event.set()
        if anim_thread:
            anim_thread.join(timeout=2.0)

        content_type = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "application/vnd.android.package-archive" in content_type:
            if status_message_id:
                try:
                    bot.edit_message_text("✅ <b>APK তৈরি সম্পন্ন হয়েছে!</b>\n📦 ফাইল আপনার চ্যাটে পাঠানো হচ্ছে...", chat_id, status_message_id, parse_mode="HTML")
                except Exception:
                    pass

            disposition = resp.headers.get("Content-Disposition", "")
            match = re.search(r'filename=(?:"([^"]+)"|([^;]+))', disposition)
            apk_name = (match.group(1) or match.group(2)).strip() if match else f"{app_name}.apk"
            if not apk_name.lower().endswith(".apk"):
                apk_name += ".apk"

            clean_caption = (
                "🎉 <b>𝐀𝐏𝐊 𝐁𝐔𝐈𝐋𝐃 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄!</b>\n"
                "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                f"📦 <b>App Name:</b> <code>{html.escape(apk_name)}</code>\n"
                "⚡ <b>Status:</b> Ready to install\n\n"
                '👨‍💻 <b>Powered by</b> <a href="https://t.me/mrghost_121">Mr Ghost</a>'
            )
            bot.send_document(
                chat_id,
                (apk_name, resp.content),
                caption=clean_caption,
                parse_mode="HTML",
                reply_markup=get_main_reply_keyboard(user_id)
            )
        else:
            err_msg = ""
            try:
                err_payload = resp.json()
                err_msg = err_payload.get("error", resp.text)
            except Exception:
                err_msg = resp.text or f"HTTP {resp.status_code}"

            fail_txt = (
                f"❌ <b>APK তৈরি ব্যর্থ হয়েছে!</b> (Status: {resp.status_code})\n"
                "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                f"⚠️ কারণ: <code>{html.escape(str(err_msg)[:300])}</code>\n\n"
                "দয়া করে ফাইল সাইজ ও কনফিগারেশন চেক করে আবার চেষ্টা করুন।"
            )
            if status_message_id:
                try:
                    bot.edit_message_text(fail_txt, chat_id, status_message_id, parse_mode="HTML")
                except Exception:
                    bot.send_message(chat_id, fail_txt, parse_mode="HTML", reply_markup=get_main_reply_keyboard(user_id))
            else:
                bot.send_message(chat_id, fail_txt, parse_mode="HTML", reply_markup=get_main_reply_keyboard(user_id))

    except Exception as exc:
        stop_event.set()
        if anim_thread:
            anim_thread.join(timeout=2.0)
        err_txt = f"❌ <b>সার্ভারে সমস্যা হয়েছে:</b>\n<code>{html.escape(str(exc)[:200])}</code>\nঅনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।"
        if status_message_id:
            try:
                bot.edit_message_text(err_txt, chat_id, status_message_id, parse_mode="HTML")
            except Exception:
                bot.send_message(chat_id, err_txt, parse_mode="HTML", reply_markup=get_main_reply_keyboard(user_id))
        else:
            bot.send_message(chat_id, err_txt, parse_mode="HTML", reply_markup=get_main_reply_keyboard(user_id))
    finally:
        stop_event.set()
        clear_state(user_id)
        APK_SESSIONS.pop(user_id, None)


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

        # 1. Send Start Photo First (Protected content based on Admin setting, not forwarded)
        if os.path.exists(START_PHOTO_PATH):
            try:
                protect = is_photo_protection_enabled()
                with open(START_PHOTO_PATH, 'rb') as pf:
                    bot.send_photo(message.chat.id, pf, protect_content=protect)
            except Exception as e:
                print(f"[!] Start photo send error: {e}", flush=True)

        # 2. Send Stylish Welcome Message
        welcome_text = (
            "👋 <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 𝐔𝐓𝐈𝐋𝐈𝐓𝐘 𝐁𝐎𝐓!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "🌐 আমাদের বটটি একটি <b>100% Free Public Utility & Video Downloader Bot</b>।\n"
            "কোনো লিমিট বা চার্জ ছাড়াই সকল টুলস এবং ডাউনলোডার আনলিমিটেড ব্যবহার করুন!\n\n"
            "⚡ <b>অটোমেটিক ভিডিও ডাউনলোডার:</b>\n"
            "যেকোনো ভিডিও লিংক (YouTube, Facebook, TikTok, Instagram, Pinterest) সরাসরি চ্যাটে পেস্ট করলেই বট স্বয়ংক্রিয়ভাবে ডাউনলোড করে দেবে।\n\n"
            "✨ <b>জনপ্রিয় ফিচারসমূহ:</b>\n"
            "• 🎬 Universal Downloader (YT, FB, TikTok, Insta, Pin)\n"
            "• 🖼️ Image to Direct Link (ImgBB Hosting)\n"
            "• 📺 Live TV Streaming Hub\n"
            "• 🔐 Encode & Decode Suite (Base64, URL, Hex, Binary)\n"
            "• 🛡️ Real-time Link & Phishing Checker\n"
            "• 📞 Phone Number to Information Lookup\n\n"
            "⚠️ <b>জরুরী নোটিশ:</b> বটটি সম্পূর্ণ বৈধ ও গঠনমূলক কাজে ব্যবহার করুন।\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
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
            "🛡️ <b>𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 — 𝐂𝐲𝐛𝐞𝐫 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 & 𝐔𝐭𝐢𝐥𝐢𝐭𝐲 𝐒𝐮𝐢𝐭𝐞</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "<b>Available Free Tools:</b>\n"
            "• 📥 Universal Video Downloader (YT, FB, TikTok, IG, Pinterest)\n"
            "• 🖼️ Image to Link (ImgBB Direct Hosting)\n"
            "• 📺 Live TV Streaming Player\n"
            "• 📂 File Sharing & Cloud Link Generator\n"
            "• 🖼️ YouTube Thumbnail & Title/Tags Extractor\n"
            "• 🎵 TikTok Video & Title Extractor (No Watermark)\n"
            "• 📞 Phone Number to Info & IP Location Tracker\n"
            "• 💫 Direct WhatsApp Chat Opener\n"
            "• 🔳 QR Code Generator & CC/BIN Generator\n"
            "• 🔐 Built-in Encode/Decode & Link Security Checker\n"
            "• 🆔 BD NID & Aadhaar Resources\n\n"
            "<b>Bot Commands:</b>\n"
            "/start - Start or restart the bot\n"
            "/help - View this help menu\n"
            "/ad - Admin Control Panel (Admins Only)\n\n"
            "<b>Channel Requirement:</b>\n"
            "আমাদের অফিসিয়াল চ্যানেলে (@mrghost_121) যুক্ত থাকতে হবে।"
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
        txt = "☠️ <b>Banned Users List:</b>\n\n"
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
        protect = is_photo_protection_enabled()
        has_cookie = os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 0
        daily_b = get_daily_bonus_amount()
        c2_id = get_setting("required_channel_2_id") or "Not Configured"
        txt = (
            "⚙️ <b>𝐀𝐃𝐌𝐈𝐍 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            f"🔧 <b>Maintenance Mode:</b> {'🟢 ON' if maint else '🔴 OFF'}\n"
            f"🔒 <b>Start Photo Download Protect:</b> {'🟢 ON (Protected)' if protect else '🔴 OFF (Downloadable)'}\n"
            f"🎁 <b>Daily Bonus Amount:</b> <code>{daily_b} Coins</code>\n"
            f"📢 <b>VIP Channel 2 ID:</b> <code>{c2_id}</code>\n"
            f"🍪 <b>YouTube Cookies:</b> {'🟢 Active (cookies.txt)' if has_cookie else '🔴 Not Uploaded'}\n"
            f"👥 <b>Total Users:</b> <code>{len(get_all_user_ids())}</code>\n"
            f"💳 <b>Card Stock:</b> <code>{count_cards_db()}</code>"
        )
        bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=get_admin_keyboard())

    @bot.message_handler(commands=['newapk'])
    def handle_newapk_cmd(message):
        if not verify_user_access(message, "verify_apk"):
            return
        notify_admin_log(message.from_user, "Website to APK Studio")
        send_apk_home(message.chat.id, message.from_user.id)

    # ==========================================
    # 7. MEDIA UPLOAD HANDLER
    # ==========================================
    @bot.message_handler(content_types=['document', 'video', 'photo'])
    def handle_media_upload(message):
        user_id = message.from_user.id
        state = get_state(user_id)

        # Admin uploading cookies.txt
        if user_id in ADMIN_IDS and message.document and (state == "admin_upload_cookie" or message.document.file_name == "cookies.txt"):
            clear_state(user_id)
            try:
                file_info = bot.get_file(message.document.file_id)
                downloaded = bot.download_file(file_info.file_path)
                with open("cookies.txt", "wb") as f:
                    f.write(downloaded)
                bot.reply_to(message, "✅ <b>cookies.txt সফলভাবে আপডেট করা হয়েছে!</b>\nএখন ইউটিউব ডাউনলোড কুকিজ সক্রিয় থাকবে।", parse_mode="HTML")
            except Exception as e:
                bot.reply_to(message, f"❌ কুকিজ ফাইল সেভ করতে ব্যর্থ: {e}")
            return

        # Image to Link State
        if state == "awaiting_imgbb_photo" and message.photo:
            clear_state(user_id)
            wait_m = bot.send_message(message.chat.id, "⏳ <b>ImgBB সার্ভারে ছবি আপলোড করা হচ্ছে...</b>", parse_mode="HTML")
            try:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_bytes = bot.download_file(file_info.file_path)
                res = upload_image_to_imgbb(file_bytes)
                if res.get("success"):
                    direct_url = res["url"]
                    display_url = res["display_url"]
                    delete_url = res["delete_url"]
                    size_kb = res["size"]

                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("🌐 Open Direct Image", url=direct_url))

                    out_txt = (
                        "✅ <b>𝐈𝐌𝐀𝐆𝐄 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘!</b>\n"
                        "━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🔗 <b>Direct Link (ক্লিক করলেই কপি হবে):</b>\n"
                        f"<code>{direct_url}</code>\n\n"
                        f"👁️ <b>Viewer URL:</b>\n"
                        f"<code>{display_url}</code>\n\n"
                        f"📦 <b>File Size:</b> {size_kb} KB\n"
                        "━━━━━━━━━━━━━━━━━━━━\n"
                        "⚡ <i>Hosted permanently on ImgBB</i>\n"
                        '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
                    )
                    bot.edit_message_text(out_txt, message.chat.id, wait_m.message_id, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=False)
                else:
                    bot.edit_message_text(f"❌ <b>আপলোড ব্যর্থ হয়েছে:</b> {res.get('error')}", message.chat.id, wait_m.message_id, parse_mode="HTML")
            except Exception as e:
                bot.edit_message_text(f"❌ ছবি প্রসেস করতে সমস্যা হয়েছে: {e}", message.chat.id, wait_m.message_id)
            return

        # APK Builder - Step 2: HTML / ZIP Document
        if state == "apk_step_html":
            if not message.document:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.reply_to(message, "⚠️ <b>ফাইল প্রয়োজন:</b> দয়া করে <code>.html</code>, <code>.htm</code> অথবা <code>.zip</code> ফাইলটি ডকুমেন্ট (Document/File) হিসেবে পাঠান:", parse_mode="HTML", reply_markup=markup)
                return

            doc = message.document
            filename = doc.file_name or "index.html"
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if ext not in ["html", "htm", "zip"]:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.reply_to(message, "⚠️ <b>ফরম্যাট গ্রহণযোগ্য নয়!</b> শুধুমাত্র <code>.html</code>, <code>.htm</code> অথবা <code>.zip</code> ফাইল পাঠান:", parse_mode="HTML", reply_markup=markup)
                return

            limit = MAX_ZIP_SIZE if ext == "zip" else MAX_HTML_SIZE
            if doc.file_size and doc.file_size > limit:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.reply_to(message, f"⚠️ <b>ফাইল অনেক বড়!</b> সর্বোচ্চ {round(limit / (1024*1024))} MB পর্যন্ত অনুমোদিত। ছোট ফাইল পাঠান:", parse_mode="HTML", reply_markup=markup)
                return

            wait_m = bot.send_message(message.chat.id, "⏳ <b>ওয়েবসাইট ফাইল ডাউনলোড ও প্রসেস করা হচ্ছে...</b>", parse_mode="HTML")
            try:
                file_info = bot.get_file(doc.file_id)
                content = bot.download_file(file_info.file_path)
            except Exception as e:
                bot.edit_message_text(f"❌ ফাইল ডাউনলোড করতে ব্যর্থ: {e}", message.chat.id, wait_m.message_id)
                return

            session = APK_SESSIONS.setdefault(user_id, {})
            session["html"] = (filename, content)
            set_state(user_id, "apk_step_icon")
            try:
                bot.delete_message(message.chat.id, wait_m.message_id)
            except Exception:
                pass

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
            next_txt = (
                "<b>Step 3/5 — App Icon</b>\n"
                "✅  ✅  🔵  ⚪  ⚪\n\n"
                f"✅ ওয়েবসাইট ফাইল গৃহীত: <code>{html.escape(filename)}</code> ({round(len(content)/1024, 1)} KB)\n\n"
                "🖼️ <b>আপনার অ্যাপের আইকন (App Icon) পাঠান:</b>\n"
                "একটি স্ট্যান্ডার্ড PNG বা JPEG ছবি পাঠান (Photo বা Document হিসেবে, সর্বোচ্চ 6 MB, 4 Megapixels)।"
            )
            bot.send_message(message.chat.id, next_txt, parse_mode="HTML", reply_markup=markup)
            return

        # APK Builder - Step 3: Icon File
        if state == "apk_step_icon":
            filename = "icon.png"
            file_id = None
            if message.document:
                doc = message.document
                filename = doc.file_name or "icon.png"
                ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
                if ext not in ["png", "jpg", "jpeg"]:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                    bot.reply_to(message, "⚠️ শুধুমাত্র <b>PNG</b> অথবা <b>JPEG</b> ফরম্যাটের ছবি পাঠান:", parse_mode="HTML", reply_markup=markup)
                    return
                if doc.file_size and doc.file_size > MAX_ICON_SIZE:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                    bot.reply_to(message, "⚠️ আইকন ফাইলের সাইজ অনেক বড় (সর্বোচ্চ 6 MB অনুমোদিত):", parse_mode="HTML", reply_markup=markup)
                    return
                file_id = doc.file_id
            elif message.photo:
                file_id = message.photo[-1].file_id
                filename = "icon.jpg"
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.reply_to(message, "⚠️ অ্যাপ আইকন হিসেবে একটি PNG বা JPEG ছবি পাঠান (ফটো বা ফাইল):", parse_mode="HTML", reply_markup=markup)
                return

            wait_m = bot.send_message(message.chat.id, "⏳ <b>আইকন ভেরিফাই করা হচ্ছে...</b>", parse_mode="HTML")
            try:
                file_info = bot.get_file(file_id)
                content = bot.download_file(file_info.file_path)
            except Exception as e:
                bot.edit_message_text(f"❌ আইকন ডাউনলোড করতে ব্যর্থ: {e}", message.chat.id, wait_m.message_id)
                return

            if len(content) > MAX_ICON_SIZE:
                bot.edit_message_text("⚠️ আইকন ফাইলের সাইজ অনেক বড় (সর্বোচ্চ 6 MB অনুমোদিত)। ছোট ছবি দিন।", message.chat.id, wait_m.message_id)
                return

            icon_err = validate_icon(content)
            if icon_err:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.edit_message_text(f"⚠️ <b>আইকন গ্রহণযোগ্য নয়:</b>\n{html.escape(icon_err)}\n\nদয়া করে স্ট্যান্ডার্ড PNG বা JPEG ছবি পাঠান:", message.chat.id, wait_m.message_id, parse_mode="HTML", reply_markup=markup)
                return

            session = APK_SESSIONS.get(user_id)
            if not session or "html" not in session:
                clear_state(user_id)
                bot.edit_message_text("❌ সেশনের মেয়াদ শেষ হয়েছে! আবার শুরু করুন।", message.chat.id, wait_m.message_id)
                return

            if len(session["html"][1]) + len(content) > MAX_TOTAL_FILES:
                clear_state(user_id)
                APK_SESSIONS.pop(user_id, None)
                bot.edit_message_text("⚠️ ওয়েবসাইট ফাইল ও আইকন একসাথে রিকুয়েস্ট লিমিট অতিক্রম করেছে। ছোট ফাইল দিয়ে আবার চেষ্টা করুন।", message.chat.id, wait_m.message_id)
                return

            session["icon"] = (filename, content)
            clear_state(user_id)
            try:
                bot.delete_message(message.chat.id, wait_m.message_id)
            except Exception:
                pass

            send_apk_confirmation(message.chat.id, user_id)
            return

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
                bot.answer_callback_query(call.id, "❌ আপনি এখনো উভয় চ্যানেলে জয়েন করেননি! আগে দুটি চ্যানেলেই জয়েন করে আবার চেষ্টা করুন।", show_alert=True)
                return

            bot.answer_callback_query(call.id, "✅ উভয় চ্যানেলে জয়েন ভেরিফিকেশন সফল হয়েছে!")
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except Exception:
                pass

            if data.startswith("verify_file|"):
                file_code = data.split("|", 1)[1]
                send_shared_file_by_code(chat_id, file_code)
            elif data == "verify_apk":
                send_apk_home(chat_id, user_id)
            else:
                bot.send_message(
                    chat_id,
                    "✅ <b>ভেরিফিকেশন সফল হয়েছে!</b>\nনিচের মেনু থেকে যেকোনো টুলস ব্যবহার করুন 👇",
                    parse_mode="HTML",
                    reply_markup=get_main_reply_keyboard(user_id)
                )
            return

        if not check_channel_joined(user_id):
            bot.answer_callback_query(call.id, "⚠️ আগে উভয় চ্যানেলে জয়েন করুন!", show_alert=True)
            send_join_prompt(chat_id, "verify_home")
            return

        # APK Builder Callbacks
        if data.startswith("apk:"):
            if data == "apk:new":
                bot.answer_callback_query(call.id)
                APK_SESSIONS[user_id] = {}
                set_state(user_id, "apk_step_name")
                prompt_txt = (
                    "<b>Step 1/5 — App Name</b>\n"
                    "🔵  ⚪  ⚪  ⚪  ⚪\n\n"
                    "📛 <b>আপনার অ্যাপটির নাম কী হবে?</b>\n\n"
                    "অ্যাপের নাম লিখে পাঠান (১ থেকে ৮০ অক্ষরের মধ্যে):"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.send_message(chat_id, prompt_txt, parse_mode="HTML", reply_markup=markup)
                return

            elif data == "apk:help":
                bot.answer_callback_query(call.id)
                apk_help = (
                    "<b>📘 How it works — Website to APK</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    "<b>১.</b> <b>Create APK</b> বাটনে চাপুন।\n"
                    "<b>২.</b> অ্যাপের নাম (App Name) লিখে পাঠান (১–৮০ অক্ষর)।\n"
                    "<b>৩.</b> ওয়েবসাইটের ফাইল <code>.html</code>, <code>.htm</code> অথবা <code>.zip</code> ডকুমেন্ট হিসেবে পাঠান (সর্বোচ্চ 10 MB)।\n"
                    "<b>৪.</b> অ্যাপের আইকন হিসেবে PNG বা JPEG ছবি পাঠান (সর্বোচ্চ 6 MB, 4 MP)।\n"
                    "<b>৫.</b> রিভিউ দেখে <b>Build APK</b> বাটনে চাপুন।\n\n"
                    "⚡ কিছুক্ষণের মধ্যেই আপনার কাঙ্ক্ষিত অ্যান্ড্রয়েড APK ফাইল তৈরি হয়ে চ্যাটে চলে আসবে!"
                )
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    types.InlineKeyboardButton("🚀 Create APK", callback_data="apk:new"),
                    types.InlineKeyboardButton("⬅️ Back to Studio", callback_data="apk:home")
                )
                try:
                    if call.message.content_type == "photo":
                        bot.edit_message_caption(apk_help, chat_id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
                    else:
                        bot.edit_message_text(apk_help, chat_id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
                except Exception:
                    bot.send_message(chat_id, apk_help, parse_mode="HTML", reply_markup=markup)
                return

            elif data == "apk:home":
                bot.answer_callback_query(call.id)
                try:
                    bot.delete_message(chat_id, call.message.message_id)
                except Exception:
                    pass
                send_apk_home(chat_id, user_id)
                return

            elif data == "apk:cancel":
                bot.answer_callback_query(call.id, "বাতিল করা হয়েছে")
                clear_state(user_id)
                APK_SESSIONS.pop(user_id, None)
                try:
                    bot.edit_message_text("✖️ <b>APK তৈরি বাতিল করা হয়েছে।</b>", chat_id, call.message.message_id, parse_mode="HTML")
                except Exception:
                    bot.send_message(chat_id, "✖️ <b>APK তৈরি বাতিল করা হয়েছে।</b>", parse_mode="HTML", reply_markup=get_main_reply_keyboard(user_id))
                return

            elif data == "apk:rename":
                session = APK_SESSIONS.get(user_id)
                if not session:
                    bot.answer_callback_query(call.id, "Session expired. Start again.", show_alert=True)
                    return
                bot.answer_callback_query(call.id)
                set_state(user_id, "apk_step_name_rename")
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.send_message(
                    chat_id,
                    "<b>Step 1/5 — Rename App</b>\n"
                    "🔵  ⚪  ⚪  ⚪  ⚪\n\n"
                    "📛 <b>নতুন অ্যাপের নাম লিখে পাঠান (১-৮০ অক্ষর):</b>",
                    parse_mode="HTML",
                    reply_markup=markup
                )
                return

            elif data == "apk:build":
                session = APK_SESSIONS.get(user_id)
                if not session or "html" not in session or "icon" not in session:
                    bot.answer_callback_query(call.id, "Session expired. Start again.", show_alert=True)
                    return
                bot.answer_callback_query(call.id, "Build started")
                try:
                    bot.edit_message_text("⚙️ <b>Preparing your APK build...</b>\n<i>This may take up to two minutes.</i>", chat_id, call.message.message_id, parse_mode="HTML")
                except Exception:
                    pass
                threading.Thread(target=build_apk_task, args=(chat_id, user_id, call.message.message_id), daemon=True).start()
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

        # Encode / Decode Callbacks
        if data.startswith("op_"):
            bot.answer_callback_query(call.id)
            op_titles = {
                "op_enc_b64": "Base64 Encode",
                "op_dec_b64": "Base64 Decode",
                "op_enc_url": "URL Encode",
                "op_dec_url": "URL Decode",
                "op_enc_hex": "Hex Encode",
                "op_dec_hex": "Hex Decode",
                "op_enc_bin": "Binary Encode",
                "op_dec_bin": "Binary Decode",
                "op_enc_rot13": "ROT13 Cipher",
                "op_text_rev": "Reverse Text"
            }
            title = op_titles.get(data, "Encode/Decode")
            set_state(user_id, f"run_op|{data}")
            bot.send_message(
                chat_id,
                f"📝 <b>Selected: {title}</b>\n\nযে টেক্সটটিকে কনভার্ট করতে চান তা নিচে লিখে পাঠান 👇",
                parse_mode="HTML"
            )
            return

        if data == "open_enc_menu":
            bot.answer_callback_query(call.id)
            bot.send_message(
                chat_id,
                "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐌𝐄𝐍𝐔</b>\nনিচের অপশন থেকে সিলেক্ট করুন 👇",
                parse_mode="HTML",
                reply_markup=get_encode_decode_keyboard()
            )
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

        # Admin Actions
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
            elif text == "🔒 Photo Protect: ON":
                set_photo_protection(False)
                bot.send_message(chat_id, "🔓 Start Photo Download Protection turned OFF! (ইউজাররা এখন ছবি ডাউনলোড করতে পারবে)", reply_markup=get_admin_keyboard())
                return
            elif text == "🔓 Photo Protect: OFF":
                set_photo_protection(True)
                bot.send_message(chat_id, "🔒 Start Photo Download Protection turned ON! (ছবি ডাউনলোড ও ফরওয়ার্ড বন্ধ করা হয়েছে)", reply_markup=get_admin_keyboard())
                return
            elif text in ["🍪 Upload Cookie", "🍪 Cookie: ACTIVE"]:
                set_state(user.id, "admin_upload_cookie")
                bot.send_message(
                    chat_id,
                    "🍪 <b>YouTube Cookie Management:</b>\n\n"
                    "আপনার <code>cookies.txt</code> ফাইলটি সরাসরি এখানে ডকুমেন্ট আকারে পাঠান অথবা কুকিজের টেক্সট পেস্ট করুন:\n"
                    "(বাতিল করতে 🏠 Home চাপুন)",
                    parse_mode="HTML"
                )
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
            elif text == "💰 User Coin (+/-)":
                set_state(user.id, "admin_manage_coins")
                msg = (
                    "💰 <b>ইউজারের কয়েন নিয়ন্ত্রণ (Add / Deduct)</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    "কয়েন যোগ বা বিয়োগ করতে নিচের ফরম্যাটে পাঠান:\n"
                    "• কয়েন যোগ করতে: <code>USER_ID +AMOUNT</code> (যেমন: <code>5140546628 +20</code>)\n"
                    "• কয়েন কাটতে: <code>USER_ID -AMOUNT</code> (যেমন: <code>5140546628 -10</code>)\n"
                    "• ব্যালেন্স নির্দিষ্ট করতে: <code>USER_ID AMOUNT</code> (যেমন: <code>5140546628 50</code>)\n\n"
                    "👇 <b>এখন ইউজার আইডি ও অ্যামাউন্ট লিখে পাঠান:</b>\n"
                    "(বাতিল করতে 🏠 Home চাপুন)"
                )
                bot.send_message(chat_id, msg, parse_mode="HTML")
                return
            elif text == "🎁 Set Daily Bonus":
                set_state(user.id, "admin_set_daily_bonus")
                curr = get_daily_bonus_amount()
                msg = (
                    "🎁 <b>কাস্টম ডেইলি বোনাস সেটিং</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    f"বর্তমান ডেইলি বোনাস: <b>{curr} Coins</b>\n\n"
                    "ইউজারদের প্রতিদিন কত কয়েন বোনাস দিতে চান তা সংখ্যায় লিখে পাঠান (যেমন: 5, 10, 20):\n"
                    "(বাতিল করতে 🏠 Home চাপুন)"
                )
                bot.send_message(chat_id, msg, parse_mode="HTML")
                return
            elif text == "📢 Channel 2 ID":
                set_state(user.id, "admin_set_channel2")
                c2 = get_setting("required_channel_2_id") or "Not Configured"
                msg = (
                    "📢 <b>VIP CHANNEL 2 CONFIGURATION</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    f"🔗 <b>Invite Link:</b> {REQUIRED_CHANNEL_2_URL}\n"
                    f"🆔 <b>Current Channel ID:</b> <code>{c2}</code>\n\n"
                    "👉 চ্যানেলটির Numeric ID সেট করতে সরাসরি আইডি লিখে পাঠান (যেমন: <code>-1001234567890</code>) অথবা ওই চ্যানেল থেকে যেকোনো একটি পোস্ট/মেসেজ বটকে Forward করুন!\n"
                    "(বাতিল করতে 🏠 Home চাপুন)"
                )
                bot.send_message(chat_id, msg, parse_mode="HTML")
                return

            if message.forward_from_chat and message.forward_from_chat.type in ["channel", "supergroup"]:
                f_chat = message.forward_from_chat
                set_setting("required_channel_2_id", str(f_chat.id))
                bot.reply_to(message, f"✅ <b>Channel 2 ID স্বয়ংক্রিয়ভাবে ডিটেক্ট ও সেভ হয়েছে!</b>\n\n📢 <b>Title:</b> {html.escape(f_chat.title or '')}\n🆔 <b>Chat ID:</b> <code>{f_chat.id}</code>", parse_mode="HTML")
                clear_state(user.id)
                return

        if not verify_user_access(message, "verify_home"):
            return

        menu_buttons = {
            "📂 File Sharing Bot", "📱 Website to APK", "📤 Upload File", "📊 Stats", "ℹ️ Help",
            "🎥 YouTube Downloader", "📹 Facebook Download", "🎵 TikTok Download",
            "📸 Instagram Download", "📌 Pinterest Download",
            "🖼️ Thumbnail Downloader", "📝 Yt Title Tags Extract", "📝 TikTok Title Extract",
            "🖼️ Image to Link", "📺 Live TV",
            "📞 Number to Info", "🔳 Qr Maker",
            "🔐 Encode & Decode", "🛡️ Link Checker",
            "🌍 IP Tracker", "💫 Whatsapp Opener", "🪪 Visa / Master Card Maker",
            "💳 CC Generator", "💳 Get Free Card", "🎁 Daily Bonus", "💰 My Balance",
            "🆔 BD NID Tools", "🪪 Aadhaar Tools", "⚠️ SMS BOMBER"
        }

        if text in menu_buttons or text.startswith("💳 Get Card"):
            clear_state(user.id)

            if text == "📂 File Sharing Bot":
                panel_txt = (
                    "📂 <b>𝐅𝐈𝐋𝐄 𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐒𝐘𝐒𝐓𝐄𝐌 — 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "⚡ এখানে আপনি যেকোনো Document, Photo বা Video আপলোড করে শেয়ার লিংক বানাতে পারবেন (১০০% ফ্রি)।\n\n"
                    "👇 নিচের বাটন থেকে নির্বাচন করুন অথবা সরাসরি ফাইল পাঠান:"
                )
                bot.send_message(chat_id, panel_txt, parse_mode="HTML", reply_markup=get_file_sharing_keyboard())
                return

            elif text == "📱 Website to APK":
                notify_admin_log(user, "Website to APK Studio")
                send_apk_home(chat_id, user.id)
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
                _, user_up, total_f = get_user_stats(user.id)
                user_coins = get_user_coins(user.id)
                stats_msg = (
                    "📊 <b>𝐔𝐒𝐄𝐑 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "👤 <b>ব্যবহারকারীর তথ্য:</b>\n"
                    f"• নাম: <b>{html.escape(user.first_name or 'User')}</b>\n"
                    f"• আইডি: <code>{user.id}</code>\n"
                    f"• ইউজারনেম: @{user.username or 'N/A'}\n\n"
                    "📈 <b>অ্যাক্টিভিটি ও স্ট্যাটাস:</b>\n"
                    "• সাবস্ক্রিপশন: <b>Free Lifetime Access ⚡</b>\n"
                    f"• আপনার আপলোডকৃত ফাইল: <b>{user_up}</b> টি\n"
                    f"• আপনার কয়েন ব্যালেন্স: <b>{user_coins} Coins 💰</b>\n"
                    "• ক্লাউড স্টোরেজ: <b>Unlimited Storage</b>\n\n"
                    "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("📢 Join Main Channel", url=CHANNEL_URL))
                markup.add(types.InlineKeyboardButton("📢 Join VIP Channel 2", url=REQUIRED_CHANNEL_2_URL))
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
                bot.send_message(chat_id, "📹 <b>Facebook Video & Reels Downloader</b>\n\nআপনার ফেসবুক ভিডিও বা রিলস (Reels) লিংকটি পাঠান 👇", parse_mode="HTML")
                return

            elif text == "🎵 TikTok Download":
                notify_admin_log(user, "TikTok Downloader")
                set_state(user.id, "awaiting_tiktok_url")
                bot.send_message(
                    chat_id,
                    "🎵 <b>TikTok Video Downloader (No Watermark)</b>\n\nসরাসরি চ্যাটে আপনার কাঙ্ক্ষিত TikTok ভিডিওর লিংক পাঠান 👇",
                    parse_mode="HTML"
                )
                return

            elif text == "📸 Instagram Download":
                notify_admin_log(user, "Instagram Downloader")
                set_state(user.id, "awaiting_insta_url")
                bot.send_message(
                    chat_id,
                    "📸 <b>Instagram Video & Reels Downloader</b>\n\nআপনার ইনস্টাগ্রাম রিলস, ভিডিও বা পোস্টের লিংক পাঠান 👇",
                    parse_mode="HTML"
                )
                return

            elif text == "📌 Pinterest Download":
                notify_admin_log(user, "Pinterest Downloader")
                set_state(user.id, "awaiting_pin_url")
                bot.send_message(
                    chat_id,
                    "📌 <b>Pinterest Video & Image Downloader</b>\n\nআপনার Pinterest পিন বা ভিডিওর লিংক পাঠান 👇",
                    parse_mode="HTML"
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

            elif text == "🖼️ Image to Link":
                notify_admin_log(user, "Image to Link")
                set_state(user.id, "awaiting_imgbb_photo")
                bot.send_message(
                    chat_id,
                    "🖼️ <b>𝐈𝐌𝐀𝐆𝐄 𝐓𝐎 𝐔𝐑𝐋 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 (𝐈𝐦𝐠𝐁𝐁)</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📸 <b>আপনার ছবিটি এখানে পাঠান (Photo হিসেবে):</b>\n\n"
                    "⚡ বট সরাসরি ImgBB সার্ভারে আপলোড করে আপনাকে পার্মানেন্ট <b>Direct Image Link</b> বানিয়ে দেবে।\n"
                    "━━━━━━━━━━━━━━━━━━━━",
                    parse_mode="HTML"
                )
                return

            elif text == "📺 Live TV":
                notify_admin_log(user, "Live TV")
                tv_text = (
                    "📺 <b>𝐋𝐈𝐕𝐄 𝐓𝐕 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐔𝐁</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🌐 <b>অনলাইন লাইভ টিভি লিংক:</b>\n"
                    "👉 https://mboxofficial.vercel.app/\n\n"
                    "⚠️ <b>দৃষ্টি আকর্ষণ / জরুরী নোটিশ:</b>\n"
                    "এই লিংকটি অনলাইনে সরাসরি যেকোনো ব্রাউজারে ব্যবহার করা যায়, তবে অ্যাপ ছাড়া অনেকগুলো টিভি চ্যানেল কাজ নাও করতে পারে। তাই নিরবচ্ছিন্ন বিনোদনের জন্য তাদের অফিসিয়াল <b>App ব্যবহার করুন</b>।\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("🌐 Open Live TV", url="https://mboxofficial.vercel.app/"),
                    types.InlineKeyboardButton("📢 Official Channel", url=CHANNEL_URL)
                )
                bot.send_message(chat_id, tv_text, parse_mode="HTML", reply_markup=markup)
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

            elif text == "🔐 Encode & Decode":
                notify_admin_log(user, "Encode & Decode Tool")
                bot.send_message(
                    chat_id,
                    "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐒𝐔𝐈𝐓𝐄 (১০০% ইন-বট)</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "নিচের যেকোনো অ্যালগরিদম বেছে নিন:\n"
                    "• Base64 Encode / Decode\n"
                    "• URL Encode / Decode\n"
                    "• Hex (Hexadecimal) Encode / Decode\n"
                    "• Binary (0101) Encode / Decode\n"
                    "• ROT13 Cipher & Text Reverse\n\n"
                    "👇 <b>নিচের মেনু থেকে আপনার পছন্দ সিলেক্ট করুন:</b>",
                    parse_mode="HTML",
                    reply_markup=get_encode_decode_keyboard()
                )
                return

            elif text == "🛡️ Link Checker":
                notify_admin_log(user, "Link Checker Tool")
                set_state(user.id, "awaiting_link_check")
                bot.send_message(
                    chat_id,
                    "🛡️ <b>𝐋𝐈𝐍𝐊 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 & 𝐑𝐄𝐃𝐈𝐑𝐄𝐂𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🔍 <b>যেকোনো URL বা লিংক এখানে পাঠান:</b>\n"
                    "বট পরীক্ষা করবে:\n"
                    "• লিংকটি সচল ও নিরাপদ কিনা\n"
                    "• আসল ডেস্টিনেশন URL (Unshorten Link)\n"
                    "• রিডাইরেক্ট চেইন (Redirect Chain)\n"
                    "• আইপি ও সার্ভার ইনফরমেশন\n"
                    "• ফিশিং বা ক্ষতিকারক TLD ওয়ার্নিং\n\n"
                    "👇 <b>এখন লিংকটি লিখে বা পেস্ট করে পাঠান:</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━",
                    parse_mode="HTML"
                )
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
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                daily_b = get_daily_bonus_amount()
                msg = (
                    "💳 <b>𝐕𝐈𝐒𝐀 / 𝐌𝐀𝐒𝐓𝐄𝐑 𝐂𝐀𝐑𝐃 𝐇𝐔𝐁</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    "⚡ <b>কয়েন সিস্টেম তথ্য:</b>\n"
                    f"• ১টি প্রিমিয়াম কার্ড নিতে <b>{cost} Coins</b> প্রয়োজন।\n"
                    f"• আপনার বর্তমান ব্যালেন্স: <b>{user_coins} Coins 💰</b>\n"
                    f"• প্রতিদিন ফ্রি <b>{daily_b} Coins</b> পেতে <b>🎁 Daily Bonus</b> এ ক্লিক করুন!\n\n"
                    "👇 <b>নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন:</b>"
                )
                bot.send_message(
                    chat_id,
                    msg,
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

            elif text.startswith("💳 Get Card") or text == "💳 Get Free Card":
                notify_admin_log(user, "Card Purchase")
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                if user_coins < cost:
                    msg = (
                        "❌ <b>কয়েন অপর্যাপ্ত! | Insufficient Coins</b>\n"
                        "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                        f"💳 ১টি প্রিমিয়াম কার্ড নিতে <b>{cost} Coins</b> প্রয়োজন।\n"
                        f"💰 আপনার বর্তমান ব্যালেন্স: <b>{user_coins} Coins</b>\n\n"
                        "👉 ফ্রিতে কয়েন পেতে নিচের <b>🎁 Daily Bonus</b> বাটনে চাপ দিন অথবা এডমিনের সাথে যোগাযোগ করুন।"
                    )
                    bot.send_message(chat_id, msg, parse_mode="HTML")
                    return

                card = pop_card_db()
                if not card:
                    bot.send_message(chat_id, "😢 দুঃখিত! এই মুহূর্তে কোনো কার্ড স্টকে নেই। এডমিনকে জানান।")
                else:
                    new_bal = deduct_user_coins(user.id, cost)
                    random_zip = random.randint(10000, 99999)
                    bot.send_message(
                        chat_id,
                        f"🎁 <b>আপনার প্রিমিয়াম কার্ড:</b>\n"
                        f"<code>{html.escape(card)}</code>\n\n"
                        f"📌 <b>Random US ZIP:</b> <code>{random_zip}</code>\n"
                        f"💰 <b>কাটা হয়েছে:</b> -{cost} Coins\n"
                        f"💵 <b>অবশিষ্ট ব্যালেন্স:</b> <code>{new_bal}</code> Coins\n\n"
                        f"<i>(কার্ড ও জিপ কোডের ওপর ক্লিক করলেই কপি হয়ে যাবে)</i>",
                        parse_mode="HTML"
                    )
                return

            elif text == "🎁 Daily Bonus":
                notify_admin_log(user, "Daily Bonus Claim")
                claimed, bonus_or_hours, mins, new_bal = claim_daily_bonus(user.id)
                if claimed:
                    bot.send_message(
                        chat_id,
                        f"🎉 <b>𝐃𝐀𝐈𝐋𝐘 𝐁𝐎𝐍𝐔𝐒 𝐂𝐋𝐀𝐈𝐌𝐄𝐃!</b>\n"
                        f"✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                        f"✅ আপনি আজকের ডেইলি বোনাস হিসেবে <b>+{bonus_or_hours} Coins</b> পেয়েছেন!\n"
                        f"💰 আপনার বর্তমান ব্যালেন্স: <b>{new_bal} Coins</b>\n\n"
                        f"⏰ পরবর্তী বোনাস ২৪ ঘণ্টা পর আবার সংগ্রহ করতে পারবেন।",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"⏳ <b>বোনাস ইতিমধ্যে সংগ্রহ করা হয়েছে!</b>\n"
                        f"✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                        f"❌ আপনি আজকের ডেইলি বোনাস ইতিমধ্যে সংগ্রহ করেছেন।\n"
                        f"🕒 পরবর্তী বোনাস পাওয়া যাবে: <b>{bonus_or_hours} ঘণ্টা {mins} মিনিট</b> পর।\n\n"
                        f"💰 আপনার বর্তমান ব্যালেন্স: <b>{new_bal} Coins</b>",
                        parse_mode="HTML"
                    )
                return

            elif text == "💰 My Balance":
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                daily_b = get_daily_bonus_amount()
                bot.send_message(
                    chat_id,
                    f"💰 <b>𝐘𝐎𝐔𝐑 𝐖𝐀𝐋𝐋𝐄𝐓 𝐁𝐀𝐋𝐀𝐍𝐂𝐄</b>\n"
                    f"✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    f"👤 <b>User:</b> {html.escape(user.first_name or 'User')}\n"
                    f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
                    f"💎 <b>কয়েন ব্যালেন্স:</b> <b>{user_coins} Coins</b>\n\n"
                    f"💳 প্রতি কার্ডের মূল্য: <b>{cost} Coins</b>\n"
                    f"🎁 দৈনিক ফ্রি বোনাস: <b>{daily_b} Coins</b>\n\n"
                    f"⚡ <i>(শুধুমাত্র Visa / Master Card কিনতে কয়েন ব্যবহৃত হয়, বাকি সব টুলস ফ্রি!)</i>",
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

        # ==========================================
        # 10. STATE-BASED INPUT PROCESSING
        # ==========================================
        state = get_state(user.id)

        # APK Builder States
        if state in ["apk_step_name", "apk_step_name_rename"]:
            if text in ["✖️ Cancel", "/cancel"]:
                clear_state(user.id)
                APK_SESSIONS.pop(user.id, None)
                bot.send_message(chat_id, "✖️ <b>APK তৈরি বাতিল করা হয়েছে।</b>", parse_mode="HTML", reply_markup=get_main_reply_keyboard(user.id))
                return

            name_err = validate_app_name(text)
            if name_err:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
                bot.send_message(chat_id, f"⚠️ <b>ভুল অ্যাপ নাম:</b> {html.escape(name_err)}\n\nদয়া করে সঠিক নাম পাঠান (১-৮০ অক্ষর):", parse_mode="HTML", reply_markup=markup)
                return

            if state == "apk_step_name_rename":
                session = APK_SESSIONS.get(user.id)
                if session:
                    session["app_name"] = text
                    clear_state(user.id)
                    send_apk_confirmation(chat_id, user.id)
                else:
                    clear_state(user.id)
                    bot.send_message(chat_id, "❌ সেশনের মেয়াদ শেষ হয়েছে! আবার শুরু করুন।", reply_markup=get_main_reply_keyboard(user.id))
                return

            APK_SESSIONS[user.id] = {"app_name": text}
            set_state(user.id, "apk_step_html")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
            bot.send_message(
                chat_id,
                "<b>Step 2/5 — Website Files</b>\n"
                "✅  🔵  ⚪  ⚪  ⚪\n\n"
                f"✅ সংরক্ষিত নাম: <b>{html.escape(text)}</b>\n\n"
                "📄 <b>আপনার ওয়েবসাইটের ফাইল আপলোড করুন:</b>\n"
                "একটি <code>.html</code>, <code>.htm</code> অথবা <code>.zip</code> ফাইল ডকুমেন্ট (Document) হিসেবে পাঠান (সর্বোচ্চ 10 MB)।",
                parse_mode="HTML",
                reply_markup=markup
            )
            return

        elif state == "apk_step_html":
            if text in ["✖️ Cancel", "/cancel"]:
                clear_state(user.id)
                APK_SESSIONS.pop(user.id, None)
                bot.send_message(chat_id, "✖️ <b>APK তৈরি বাতিল করা হয়েছে।</b>", parse_mode="HTML", reply_markup=get_main_reply_keyboard(user.id))
                return
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
            bot.send_message(
                chat_id,
                "⚠️ <b>ডকুমেন্ট ফাইল প্রয়োজন:</b>\n\nদয়া করে আপনার ওয়েবসাইট ফাইলটি ডকুমেন্ট (Document/File) হিসেবে পাঠান (যেমন: <code>index.html</code> অথবা <code>project.zip</code>) বা বাতিল করতে ✖️ Cancel চাপুন।",
                parse_mode="HTML",
                reply_markup=markup
            )
            return

        elif state == "apk_step_icon":
            if text in ["✖️ Cancel", "/cancel"]:
                clear_state(user.id)
                APK_SESSIONS.pop(user.id, None)
                bot.send_message(chat_id, "✖️ <b>APK তৈরি বাতিল করা হয়েছে।</b>", parse_mode="HTML", reply_markup=get_main_reply_keyboard(user.id))
                return
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✖️ Cancel", callback_data="apk:cancel"))
            bot.send_message(
                chat_id,
                "⚠️ <b>ছবি/আইকন প্রয়োজন:</b>\n\nদয়া করে আপনার অ্যাপ আইকনটি ফটো বা ডকুমেন্ট (PNG/JPEG) হিসেবে পাঠান বা বাতিল করতে ✖️ Cancel চাপুন।",
                parse_mode="HTML",
                reply_markup=markup
            )
            return

        elif state == "admin_upload_cookie" and user.id in ADMIN_IDS:
            clear_state(user.id)
            with open("cookies.txt", "w", encoding="utf-8") as f:
                f.write(text)
            bot.send_message(chat_id, "✅ <b>cookies.txt সফলভাবে সেভ করা হয়েছে!</b>", parse_mode="HTML")
            return

        elif state == "admin_broadcast" and user.id in ADMIN_IDS:
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

        elif state == "admin_manage_coins" and user.id in ADMIN_IDS:
            clear_state(user.id)
            parts = text.split()
            if len(parts) >= 2 and (parts[0].isdigit() or (parts[0].startswith("-") and parts[0][1:].isdigit())):
                target_uid = int(parts[0])
                amt_str = parts[1]
                diff_text = ""
                if amt_str.startswith("+") and amt_str[1:].isdigit():
                    amt = int(amt_str[1:])
                    new_b = add_user_coins(target_uid, amt)
                    diff_text = f"+{amt}"
                elif amt_str.startswith("-") and amt_str[1:].isdigit():
                    amt = int(amt_str[1:])
                    new_b = deduct_user_coins(target_uid, amt)
                    diff_text = f"-{amt}"
                elif amt_str.isdigit():
                    amt = int(amt_str)
                    set_user_coins(target_uid, amt)
                    new_b = amt
                    diff_text = f"Set to {amt}"
                else:
                    bot.send_message(chat_id, "❌ ভুল ফরম্যাট! উদাহরণ: <code>12345678 +20</code> বা <code>12345678 -10</code>", parse_mode="HTML")
                    return

                bot.send_message(
                    chat_id,
                    f"✅ <b>ইউজার ব্যালেন্স সফলভাবে আপডেট হয়েছে!</b>\n\n"
                    f"👤 <b>User ID:</b> <code>{target_uid}</code>\n"
                    f"📊 <b>পরিবর্তন:</b> <code>{diff_text}</code> Coins\n"
                    f"💰 <b>বর্তমান ব্যালেন্স:</b> <b>{new_b} Coins</b>",
                    parse_mode="HTML"
                )
                try:
                    bot.send_message(
                        target_uid,
                        f"🔔 <b>আপনার ওয়ালেট ব্যালেন্স আপডেট হয়েছে!</b>\n\n"
                        f"এডমিন আপনার অ্যাকাউন্টে <b>{diff_text} Coins</b> আপডেট করেছেন।\n"
                        f"💰 বর্তমান ব্যালেন্স: <b>{new_b} Coins</b>",
                        parse_mode="HTML"
                    )
                except Exception:
                    pass
            else:
                bot.send_message(chat_id, "❌ ফরম্যাট সঠিক নয়! উদাহরণ: <code>12345678 +20</code>", parse_mode="HTML")
            return

        elif state == "admin_set_daily_bonus" and user.id in ADMIN_IDS:
            clear_state(user.id)
            if text.isdigit() and int(text) > 0:
                new_amt = int(text)
                set_daily_bonus_amount(new_amt)
                bot.send_message(chat_id, f"✅ <b>ডেইলি বোনাস সফলভাবে {new_amt} Coins এ সেট করা হয়েছে!</b>", parse_mode="HTML")
            else:
                bot.send_message(chat_id, "❌ দয়া করে একটি সঠিক ধনাত্মক সংখ্যা দিন (যেমন: 5, 10, 20)।", parse_mode="HTML")
            return

        elif state == "admin_set_channel2" and user.id in ADMIN_IDS:
            clear_state(user.id)
            raw_id = text.strip()
            set_setting("required_channel_2_id", raw_id)
            bot.send_message(chat_id, f"✅ <b>Channel 2 ID সফলভাবে সেট করা হয়েছে:</b> <code>{html.escape(raw_id)}</code>", parse_mode="HTML")
            return

        # Encode / Decode State Execution
        if state and state.startswith("run_op|"):
            op_code = state.split("|", 1)[1]
            clear_state(user.id)
            result = run_encode_decode(op_code, text)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Another Operation", callback_data="open_enc_menu"))

            resp_txt = (
                "🎯 <b>𝐄𝐍𝐂𝐎𝐃𝐄 / 𝐃𝐄𝐂𝐎𝐃𝐄 𝐑𝐄𝐒𝐔𝐋𝐓:</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"<pre>{html.escape(result)}</pre>\n\n"
                "👆 <i>ক্লিক করলেই সম্পূর্ণ ফলাফল একসাথে কপি হয়ে যাবে।</i>"
            )
            bot.send_message(chat_id, resp_txt, parse_mode="HTML", reply_markup=markup)
            return

        # Link Checker State
        if state == "awaiting_link_check":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, "⏳ <b>লিংকটি স্ক্যান ও পরীক্ষা করা হচ্ছে...</b>", parse_mode="HTML")
            rep = analyze_link_safety(text)

            flags_txt = "\n".join([f"• {f}" for f in rep["flags"]])
            redirect_txt = "None (Direct)"
            if rep["redirect_chain"]:
                redirect_txt = f"{rep['redirect_count']} Hops:\n" + "\n".join([f"→ <code>{html.escape(u)}</code>" for u in rep["redirect_chain"][:4]])

            out_msg = (
                "🛡️ <b>𝐋𝐈𝐍𝐊 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐀𝐍𝐀𝐋𝐘𝐒𝐈𝐒 𝐑𝐄𝐏𝐎𝐑𝐓</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎯 <b>Status:</b> <b>{rep['status_code']}</b>\n"
                f"🛡️ <b>Safety Level:</b> <b>{rep['safety_level']}</b>\n"
                f"⏱️ <b>Response Time:</b> {rep['response_time_ms']} ms\n"
                f"🌐 <b>Target IP:</b> <code>{rep['ip']}</code>\n"
                f"🖥️ <b>Server:</b> <code>{rep['server']}</code>\n\n"
                f"🔗 <b>Destination URL:</b>\n<code>{html.escape(rep['final_url'])}</code>\n\n"
                f"🔄 <b>Redirect Chain:</b>\n{redirect_txt}\n\n"
                f"⚠️ <b>Security Checks:</b>\n{flags_txt}\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            bot.edit_message_text(out_msg, chat_id, wait_m.message_id, parse_mode="HTML", disable_web_page_preview=True)
            return

        # Specific Downloader States
        if state == "awaiting_tiktok_url":
            clear_state(user.id)
            threading.Thread(target=download_and_send_tiktok, args=(chat_id, text), daemon=True).start()
            return

        elif state == "awaiting_insta_url":
            clear_state(user.id)
            threading.Thread(target=download_and_send_instagram, args=(chat_id, text), daemon=True).start()
            return

        elif state == "awaiting_pin_url":
            clear_state(user.id)
            threading.Thread(target=download_and_send_pinterest, args=(chat_id, text), daemon=True).start()
            return

        elif state == "awaiting_video_url":
            clear_state(user.id)
            threading.Thread(target=download_and_send_universal_video, args=(chat_id, text), daemon=True).start()
            return

        elif state == "awaiting_yt_thumb":
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
            info = resolve_phone_info(text)

            wa_link = f"https://wa.me/{info['clean_digits']}"
            tg_link = f"tg://resolve?phone={info['clean_digits']}"

            info_txt = (
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📞 <b>𝐏𝐇𝐎𝐍𝐄 𝐍𝐔𝐌𝐁𝐄𝐑 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"👤 <b>Owner / Name   :</b> <code>{html.escape(info['owner_name'])}</code>\n"
                f"🔹 <b>Intl. Format   :</b> <code>{html.escape(info['intl_format'])}</code>\n"
                f"🔹 <b>National Format:</b> <code>{html.escape(info['nat_format'])}</code>\n"
                f"🌍 <b>Country        :</b> <code>{html.escape(info['country'])}</code>\n"
                f"📡 <b>Carrier / SIM  :</b> <code>{html.escape(info['carrier'])}</code>\n"
                f"📱 <b>Line Type      :</b> <code>{html.escape(info['type'])}</code>\n"
                f"⏰ <b>Timezone       :</b> <code>{html.escape(info['timezone'])}</code>\n"
                f"✅ <b>Is Valid       :</b> <code>{'Yes' if info['valid'] else 'No'}</code>\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🕵️‍♂️ <b>𝐃𝐈𝐑𝐄𝐂𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐈𝐍𝐆:</b>\n"
                f"💬 <a href='{wa_link}'>Direct WhatsApp Chat</a>\n"
                f"✈️ <a href='{tg_link}'>Direct Telegram Contact</a>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "✅ <i>Search Completed Successfully!</i>"
            )
            bot.edit_message_text(info_txt, chat_id, wait_m.message_id, parse_mode="HTML", disable_web_page_preview=True)
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
        # 11. AUTOMATIC URL DETECTOR (ALL PLATFORMS)
        # ==========================================
        url_match = re.search(r'https?://[^\s<>"]+', text)
        if url_match:
            found_url = url_match.group(0).rstrip('.,;!?')
            domain = urllib.parse.urlparse(found_url).netloc.lower()

            clear_state(user.id)
            if any(k in domain for k in ["tiktok.com"]):
                threading.Thread(target=download_and_send_tiktok, args=(chat_id, found_url), daemon=True).start()
                return
            elif any(k in domain for k in ["instagram.com", "instagr.am"]):
                threading.Thread(target=download_and_send_instagram, args=(chat_id, found_url), daemon=True).start()
                return
            elif any(k in domain for k in ["pinterest.com", "pin.it"]):
                threading.Thread(target=download_and_send_pinterest, args=(chat_id, found_url), daemon=True).start()
                return
            elif any(k in domain for k in ["youtube.com", "youtu.be", "facebook.com", "fb.watch", "fb.com"]):
                threading.Thread(target=download_and_send_universal_video, args=(chat_id, found_url), daemon=True).start()
                return
            else:
                threading.Thread(target=download_and_send_universal_video, args=(chat_id, found_url), daemon=True).start()
                return

        bot.reply_to(
            message,
            "⚠️ দয়া করে নিচের মেনু থেকে যেকোনো একটি টুল সিলেক্ট করুন অথবা ভিডিও ডাউনলোড করতে সরাসরি <b>Video URL</b> পাঠান 👇",
            parse_mode="HTML",
            reply_markup=get_main_reply_keyboard(user.id)
        )

    @bot.my_chat_member_handler()
    def handle_my_chat_member_event(update):
        try:
            chat = update.chat
            if chat.type in ["channel", "supergroup"]:
                set_setting("required_channel_2_id", str(chat.id))
                print(f"[*] Auto-detected VIP Channel ID: {chat.id} ({chat.title})", flush=True)
        except Exception as e:
            print(f"[!] Error in my_chat_member: {e}", flush=True)


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
