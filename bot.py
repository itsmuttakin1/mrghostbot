import os
import sys
import re
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
from locales import (
    SUPPORTED_LANGS,
    LANG_CHOICE_BUTTONS,
    btn,
    resolve_button_action,
    t,
)

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

# Auto-load YouTube Cookies from environment variable (for Railway / Cloud Hosting)
env_cookies = os.getenv("YOUTUBE_COOKIES", "").strip()
if env_cookies and (not os.path.exists("cookies.txt") or os.path.getsize("cookies.txt") == 0):
    try:
        with open("cookies.txt", "w", encoding="utf-8") as cf:
            cf.write(env_cookies)
        print("[*] Successfully loaded cookies from YOUTUBE_COOKIES environment variable!", flush=True)
    except Exception as e:
        print(f"[!] Error writing env cookies: {e}", flush=True)

if not BOT_TOKEN:
    print("❌ CRITICAL ERROR: BOT_TOKEN is missing in Environment Variables!", flush=True)

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None
if bot:
    telebot.apihelper.CUSTOM_REQUEST_TIMEOUT = 120

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
                Facebook, TikTok, Instagram সহ যেকোনো সোশ্যাল ভিডিও সহজে ডাউনলোড করুন
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

def is_youtube_or_pinterest(url):
    if not url:
        return False
    low = url.lower()
    return any(k in low for k in ["youtube.com", "youtu.be", "pinterest.com", "pin.it"])

def resolve_url(url):
    if not url:
        return url
    clean_u = url.strip()
    if any(k in clean_u.lower() for k in ["youtube.com", "youtu.be"]):
        return clean_u
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        res = requests.head(clean_u, allow_redirects=True, timeout=8, headers=headers)
        return res.url
    except Exception:
        return clean_u

FFMPEG_DIR = os.path.abspath("ffmpeg_bin") if os.path.exists("ffmpeg_bin") else None
HAS_FFMPEG = bool(FFMPEG_DIR or shutil.which("ffmpeg"))

def get_ydl_options(output_path):
    fmt = 'best[height<=720]/bestvideo[height<=720]+bestaudio/b[ext=mp4]/best' if HAS_FFMPEG else 'b[ext=mp4]/best[ext=mp4]/best'
    opts = {
        'format': fmt,
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'no_check_certificates': True,
        'source_address': '0.0.0.0',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    if FFMPEG_DIR:
        opts['ffmpeg_location'] = FFMPEG_DIR
    proxy = os.getenv("PROXY") or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
    if proxy:
        opts['proxy'] = proxy
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
    if is_youtube_or_pinterest(raw_url):
        return jsonify({'success': False, 'error': 'YouTube ও Pinterest ডাউনলোডার রিমুভ করা হয়েছে। TikTok, Facebook বা Instagram লিংক দিন।'}), 400

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
                language TEXT DEFAULT 'bn',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("PRAGMA table_info(users)")
        cols = [c[1] for c in cursor.fetchall()]
        if "coins" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN coins INTEGER DEFAULT 0")
        if "last_daily_bonus" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN last_daily_bonus TEXT DEFAULT NULL")
        if "language" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'bn'")

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

USER_LANG_CACHE = {}

def get_user_lang(user_id):
    if not user_id:
        return "bn"
    if user_id in USER_LANG_CACHE:
        return USER_LANG_CACHE[user_id]
    try:
        with db_mutex:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
        lang = row[0] if (row and row[0] in SUPPORTED_LANGS) else "bn"
    except Exception:
        lang = "bn"
    USER_LANG_CACHE[user_id] = lang
    return lang

def set_user_lang(user_id, lang):
    if lang not in SUPPORTED_LANGS:
        lang = "bn"
    USER_LANG_CACHE[user_id] = lang
    with db_mutex:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, language) VALUES (?, 'N/A', 'User', ?)", (user_id, lang))
        cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
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

def send_join_prompt(chat_id, callback_action="verify_home", user_id=None):
    # Safety: Never send join prompt to groups, supergroups, or channels
    try:
        if int(chat_id) < 0:
            return
    except Exception:
        pass
    lang = get_user_lang(user_id or chat_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t(lang, "join_btn_1", channel=REQUIRED_CHANNEL), url=CHANNEL_URL),
        types.InlineKeyboardButton(t(lang, "join_btn_2"), url=REQUIRED_CHANNEL_2_URL),
        types.InlineKeyboardButton(t(lang, "join_btn_verify"), callback_data=callback_action)
    )
    text = t(lang, "join_prompt", channel=REQUIRED_CHANNEL, ch2_url=REQUIRED_CHANNEL_2_URL)
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)

def verify_user_access(message, action_tag="verify_home"):
    # Strictly ignore all groups, supergroups, and channels
    if not message or not message.chat or message.chat.type != "private":
        return False
    user = message.from_user
    register_user(user)
    lang = get_user_lang(user.id)

    if is_banned(user.id):
        bot.send_message(
            message.chat.id,
            t(lang, "banned_full"),
            parse_mode="HTML"
        )
        return False

    if is_maintenance() and user.id not in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            t(lang, "maintenance"),
            parse_mode="HTML"
        )
        return False

    if not check_channel_joined(user.id):
        send_join_prompt(message.chat.id, action_tag, user_id=user.id)
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
# 4. BULLETPROOF MESSAGE SENDER & KEYBOARDS
# ==========================================
def safe_send_message(chat_id, text, parse_mode="HTML", reply_markup=None, disable_web_page_preview=None, **kwargs):
    """
    Bulletproof message sender:
    1. Tries sending with requested parse_mode and reply_markup.
    2. If it fails with HTML parse error (or any other API error), falls back to plain text with markup.
    3. If reply_markup causes any failure, falls back without reply_markup.
    """
    if not bot:
        return None
    opts = {}
    if disable_web_page_preview is not None:
        opts['disable_web_page_preview'] = disable_web_page_preview
    opts.update(kwargs)

    # Attempt 1: Standard send with requested parse_mode
    try:
        return bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup, **opts)
    except Exception as e1:
        print(f"[!] safe_send_message primary (HTML) failed: {e1}", flush=True)

    # Attempt 2: Plain text with reply_markup (stripping tags and decoding entities)
    plain_text = re.sub(r'<[^>]+>', '', str(text)).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    try:
        return bot.send_message(chat_id, plain_text, parse_mode=None, reply_markup=reply_markup, **opts)
    except Exception as e2:
        print(f"[!] safe_send_message plain fallback failed: {e2}", flush=True)

    # Attempt 3: Plain text without reply_markup (in case reply_markup caused Telegram rejection)
    try:
        return bot.send_message(chat_id, plain_text, parse_mode=None, **opts)
    except Exception as e3:
        print(f"[!] safe_send_message stripped fallback failed: {e3}", flush=True)
        return None

def _kb_btn(text, style=None, use_style=False):
    return types.KeyboardButton(text)

def get_main_reply_keyboard(user_id=None, use_style=False):
    lang = get_user_lang(user_id) if user_id else "bn"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, row_width=2)

    # Row 1: File Sharing
    markup.row(
        types.KeyboardButton(btn(lang, "btn_file_sharing"))
    )
    # Row 2: Facebook | TikTok
    markup.row(
        types.KeyboardButton(btn(lang, "btn_fb_dl")),
        types.KeyboardButton(btn(lang, "btn_tiktok_dl"))
    )
    # Row 3: Instagram | Thumbnail
    markup.row(
        types.KeyboardButton(btn(lang, "btn_insta_dl")),
        types.KeyboardButton(btn(lang, "btn_thumb_dl"))
    )
    # Row 4: Image to Link | Live TV
    markup.row(
        types.KeyboardButton(btn(lang, "btn_img_link")),
        types.KeyboardButton(btn(lang, "btn_live_tv"))
    )
    # Row 5: Number to Info | QR Maker
    markup.row(
        types.KeyboardButton(btn(lang, "btn_num_info")),
        types.KeyboardButton(btn(lang, "btn_qr"))
    )
    # Row 6: Encode & Decode | Link Checker
    markup.row(
        types.KeyboardButton(btn(lang, "btn_enc_dec")),
        types.KeyboardButton(btn(lang, "btn_link_check"))
    )
    # Row 7: Title/Tags Extract | TikTok Title Extract
    markup.row(
        types.KeyboardButton(btn(lang, "btn_yt_extract")),
        types.KeyboardButton(btn(lang, "btn_tik_title"))
    )
    # Row 8: IP Tracker | WhatsApp
    markup.row(
        types.KeyboardButton(btn(lang, "btn_ip_track")),
        types.KeyboardButton(btn(lang, "btn_wa_open"))
    )
    # Row 9: Card Maker | NID Tools
    markup.row(
        types.KeyboardButton(btn(lang, "btn_card_hub")),
        types.KeyboardButton(btn(lang, "btn_nid"))
    )
    # Row 10: Aadhaar Tools | SMS Bomber
    markup.row(
        types.KeyboardButton(btn(lang, "btn_aadhaar")),
        types.KeyboardButton(btn(lang, "btn_sms_bomb"))
    )
    # Row 11: Stats | Help
    markup.row(
        types.KeyboardButton(btn(lang, "btn_stats")),
        types.KeyboardButton(btn(lang, "btn_help"))
    )
    # Row 12: Language Selector
    markup.row(
        types.KeyboardButton(btn(lang, "btn_lang"))
    )
    return markup

def get_language_keyboard(user_id=None, use_style=False):
    lang = get_user_lang(user_id) if user_id else "bn"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, row_width=2)
    markup.row(
        types.KeyboardButton("🇧🇩 বাংলা"),
        types.KeyboardButton("🇬🇧 English")
    )
    markup.row(
        types.KeyboardButton("🇮🇩 Indonesia"),
        types.KeyboardButton(btn(lang, "btn_home"))
    )
    return markup

def get_file_sharing_keyboard(user_id=None, use_style=False):
    lang = get_user_lang(user_id) if user_id else "bn"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, row_width=2)
    markup.row(
        types.KeyboardButton(btn(lang, "btn_upload_file")),
        types.KeyboardButton(btn(lang, "btn_stats"))
    )
    markup.row(types.KeyboardButton(btn(lang, "btn_home")))
    return markup

def get_visa_menu_keyboard(user_id=None, use_style=False):
    lang = get_user_lang(user_id) if user_id else "bn"
    cost = get_card_cost()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, row_width=2)
    markup.row(
        types.KeyboardButton(btn(lang, "btn_get_card", cost=cost)),
        types.KeyboardButton(btn(lang, "btn_cc_gen"))
    )
    markup.row(
        types.KeyboardButton(btn(lang, "btn_daily_bonus")),
        types.KeyboardButton(btn(lang, "btn_my_balance"))
    )
    markup.row(types.KeyboardButton(btn(lang, "btn_home")))
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
        types.KeyboardButton("🔗 Mod Share Link", style="primary"),
        types.KeyboardButton(protect_btn, style="success" if protect else "danger")
    )
    markup.row(
        types.KeyboardButton(maint_btn, style="danger" if maint else "success"),
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

def send_shared_file_by_code(chat_id, file_code, user_id=None):
    lang = get_user_lang(user_id or chat_id)
    row = get_shared_file(file_code)
    if not row:
        bot.send_message(
            chat_id,
            t(lang, "fs_not_found"),
            parse_mode="HTML"
        )
        return

    file_id, file_type, file_name, caption = row
    status_m = bot.send_message(chat_id, t(lang, "fs_sending"), parse_mode="HTML")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t(lang, "btn_join_main_ch"), url=CHANNEL_URL))

    sent_msg = None
    try:
        if file_type == "video":
            sent_msg = bot.send_video(chat_id, file_id, caption=caption or "", reply_markup=markup)
        elif file_type == "photo":
            sent_msg = bot.send_photo(chat_id, file_id, caption=caption or "", reply_markup=markup)
        else:
            sent_msg = bot.send_document(chat_id, file_id, caption=caption or file_name or "", reply_markup=markup)

        try:
            bot.delete_message(chat_id, status_m.message_id)
        except Exception:
            pass

        if sent_msg:
            notice_text = t(lang, "fs_notice_5min")
            notice_msg = bot.send_message(chat_id, notice_text, parse_mode="HTML")

            # Auto-delete messages from inbox after 5 minutes (300 seconds)
            def auto_delete_inbox_messages(target_cid, target_mids, msg_lang, delay=300):
                time.sleep(delay)
                for mid in target_mids:
                    try:
                        bot.delete_message(target_cid, mid)
                    except Exception:
                        pass
                try:
                    bot.send_message(
                        target_cid,
                        t(msg_lang, "fs_deleted_5min"),
                        parse_mode="HTML"
                    )
                except Exception:
                    pass

            threading.Thread(
                target=auto_delete_inbox_messages,
                args=(chat_id, [sent_msg.message_id, notice_msg.message_id], lang, 300),
                daemon=True
            ).start()

    except Exception as e:
        bot.send_message(chat_id, t(lang, "fs_send_error", err=html.escape(str(e)[:100])), parse_mode="HTML")

def extract_clean_title(info, fallback="Social Video"):
    if not isinstance(info, dict):
        return fallback
    candidates = [
        info.get("fulltitle"),
        info.get("title"),
        info.get("description"),
    ]
    generic_names = {"facebook", "watch", "instagram", "tiktok", "video", "reel", "reels"}
    for cand in candidates:
        if not cand:
            continue
        clean_c = " ".join(str(cand).strip().splitlines()).strip()
        if not clean_c:
            continue
        if clean_c.lower() in generic_names:
            continue
        return clean_c
    return fallback

def fetch_video_title_fallback(url, fallback="Social Video"):
    # 1. Try quick yt-dlp metadata extraction
    try:
        meta_opts = {
            'quiet': True,
            'no_warnings': True,
            'no_check_certificates': True,
            'skip_download': True,
            'source_address': '0.0.0.0',
        }
        proxy = os.getenv("PROXY") or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
        if proxy:
            meta_opts['proxy'] = proxy
        with yt_dlp.YoutubeDL(meta_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = extract_clean_title(info, fallback="")
            if title:
                return title
    except Exception:
        pass

    # 2. Try OpenGraph / HTML title
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code == 200 and resp.text:
            for pattern in [
                r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
                r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
                r'<title>([^<]+)</title>',
            ]:
                m = re.search(pattern, resp.text, re.IGNORECASE)
                if m:
                    raw_t = html.unescape(m.group(1)).strip()
                    if raw_t and raw_t.lower() not in {"facebook", "instagram", "tiktok", "watch", "log in or sign up to view"}:
                        return raw_t
    except Exception:
        pass
    return fallback

def fallback_cobalt_download(user_id, url, status_msg_id=None, video_title=None):
    lang = get_user_lang(user_id)
    cobalt_instances = [
        ("https://cobalt-api.kwiatekm.pl/", {"url": url, "videoQuality": "720"}),
        ("https://api.cobalt.tools/", {"url": url, "videoQuality": "720"}),
        ("https://api.wuk.sh/", {"url": url, "videoQuality": "720"}),
        ("https://api.cobalt.tools/api/json", {"url": url}),
        ("https://cobalt-api.kwiatekm.pl/api/json", {"url": url})
    ]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    for c_url, payload in cobalt_instances:
        try:
            res = requests.post(c_url, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                media_url = data.get("url")
                if media_url:
                    resolved_title = video_title or data.get("filename") or fetch_video_title_fallback(url, "Social Video")
                    caption = t(lang, "dl_caption_universal", title=html.escape(str(resolved_title)[:200]))
                    try:
                        bot.send_video(user_id, media_url, caption=caption, parse_mode="HTML")
                    except Exception:
                        # Download locally if Telegram cannot fetch CDN URL directly
                        os.makedirs("downloads", exist_ok=True)
                        temp_file = f"downloads/cb_{user_id}_{int(time.time())}.mp4"
                        try:
                            v_res = requests.get(media_url, timeout=30, stream=True)
                            if v_res.status_code == 200:
                                with open(temp_file, "wb") as f:
                                    for chunk in v_res.iter_content(chunk_size=1024*1024):
                                        if chunk:
                                            f.write(chunk)
                                with open(temp_file, "rb") as vf:
                                    bot.send_video(user_id, vf, caption=caption, parse_mode="HTML", supports_streaming=True)
                        finally:
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
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
    lang = get_user_lang(user_id)
    status_msg = bot.send_message(user_id, t(lang, "dl_processing_tiktok"), parse_mode="HTML")
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

            caption = t(
                lang,
                "dl_caption_tiktok",
                title=html.escape(title[:250]),
                author=html.escape(author)
            )
            if music:
                caption += t(lang, "dl_caption_music_line", music=html.escape(music[:80]))
            else:
                caption += "\n"
            caption += t(lang, "dl_caption_tiktok_footer")

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
            caption = t(
                lang,
                "dl_caption_tiktok",
                title=html.escape(title[:220]),
                author="TikTok"
            ) + "\n" + t(lang, "dl_caption_tiktok_footer")
            bot.send_video(
                user_id,
                video_url,
                caption=caption,
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
    lang = get_user_lang(user_id)
    status_msg = bot.send_message(user_id, t(lang, "dl_processing_insta"), parse_mode="HTML")
    url = resolve_url(raw_url)

    # Method 1: Public IG API
    try:
        api_url = f"https://api.vkrdown.com/web/app/instagram.php?url={urllib.parse.quote(url)}"
        r = requests.get(api_url, timeout=15).json()
        data = r.get("data") or {}
        media_url = data.get("download_url") or data.get("url") or (r.get("media") or [{}])[0].get("url")
        if media_url:
            raw_title = data.get("title") or data.get("caption") or r.get("title")
            if not raw_title:
                raw_title = fetch_video_title_fallback(url, "Instagram Video")
            caption = t(lang, "dl_caption_insta", title=html.escape(str(raw_title)[:200]))
            is_video = ".mp4" in media_url or "video" in str(data.get("type", "")).lower()
            try:
                if is_video:
                    bot.send_video(user_id, media_url, caption=caption, parse_mode="HTML")
                else:
                    bot.send_photo(user_id, media_url, caption=caption, parse_mode="HTML")
            except Exception:
                # Download locally if direct URL delivery fails
                os.makedirs("downloads", exist_ok=True)
                ext = "mp4" if is_video else "jpg"
                temp_file = f"downloads/ig_{user_id}_{int(time.time())}.{ext}"
                try:
                    m_res = requests.get(media_url, timeout=30, stream=True)
                    if m_res.status_code == 200:
                        with open(temp_file, "wb") as f:
                            for chunk in m_res.iter_content(chunk_size=1024*1024):
                                if chunk:
                                    f.write(chunk)
                        with open(temp_file, "rb") as mf:
                            if is_video:
                                bot.send_video(user_id, mf, caption=caption, parse_mode="HTML", supports_streaming=True)
                            else:
                                bot.send_photo(user_id, mf, caption=caption, parse_mode="HTML")
                    else:
                        raise RuntimeError("IG media download failed")
                finally:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
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

    # Method 3: Universal Downloader (yt-dlp with title extraction)
    download_and_send_universal_video(user_id, raw_url, status_msg_id=status_msg.message_id)

def download_and_send_universal_video(user_id, raw_url, status_msg_id=None):
    if not bot:
        return
    lang = get_user_lang(user_id)
    if is_youtube_or_pinterest(raw_url):
        if status_msg_id:
            try:
                bot.edit_message_text(t(lang, "dl_unsupported_removed"), user_id, status_msg_id, parse_mode="HTML")
            except Exception:
                bot.send_message(user_id, t(lang, "dl_unsupported_removed"), parse_mode="HTML")
        else:
            bot.send_message(user_id, t(lang, "dl_unsupported_removed"), parse_mode="HTML")
        return

    if status_msg_id:
        msg_id = status_msg_id
    else:
        status_msg = bot.send_message(user_id, t(lang, "dl_processing_video"), parse_mode="HTML")
        msg_id = status_msg.message_id

    u_match = re.search(r'https?://[^\s<>"]+', raw_url)
    clean_raw = u_match.group(0).rstrip('.,;!?') if u_match else raw_url.strip()
    target_url = resolve_url(clean_raw)

    output_dir = f"downloads/{user_id}_{int(time.time() * 1000)}"
    os.makedirs(output_dir, exist_ok=True)
    out_template = f'{output_dir}/%(id)s.%(ext)s'

    video_title = "Social Video"
    downloaded = False

    try:
        # Strategy 1: Primary yt-dlp
        try:
            ydl_opts = get_ydl_options(out_template)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=True)
                if info:
                    video_title = extract_clean_title(info, "Social Video")
            files = [f for f in glob.glob(f"{output_dir}/*") if not f.endswith(('.temp', '.part', '.ytdl'))]
            if files:
                downloaded = True
        except Exception as e1:
            print(f"[!] Strategy 1 error: {e1}", flush=True)

        # Strategy 2: Progressive MP4 fallback (No ffmpeg needed)
        if not downloaded:
            try:
                retry_opts = {
                    'format': 'b[ext=mp4]/best[ext=mp4]/best',
                    'outtmpl': out_template,
                    'quiet': True,
                    'no_warnings': True,
                    'no_check_certificates': True,
                    'source_address': '0.0.0.0',
                }
                if FFMPEG_DIR:
                    retry_opts['ffmpeg_location'] = FFMPEG_DIR
                proxy = os.getenv("PROXY") or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
                if proxy:
                    retry_opts['proxy'] = proxy
                if os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 0:
                    retry_opts['cookiefile'] = "cookies.txt"
                with yt_dlp.YoutubeDL(retry_opts) as ydl_retry:
                    info2 = ydl_retry.extract_info(target_url, download=True)
                    if info2:
                        video_title = extract_clean_title(info2, "Social Video")
                files = [f for f in glob.glob(f"{output_dir}/*") if not f.endswith(('.temp', '.part', '.ytdl'))]
                if files:
                    downloaded = True
            except Exception as e2:
                print(f"[!] Strategy 2 error: {e2}", flush=True)

        # If downloaded successfully, deliver to user
        if downloaded:
            files = [f for f in glob.glob(f"{output_dir}/*") if not f.endswith(('.temp', '.part', '.ytdl'))]
            if files:
                file_path = files[0]
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

                if file_size_mb > 49.5:
                    bot.edit_message_text(
                        t(lang, "dl_too_large"),
                        user_id,
                        msg_id,
                        parse_mode="HTML"
                    )
                    return

                if video_title == "Social Video":
                    video_title = fetch_video_title_fallback(target_url, "Social Video")
                escaped_title = html.escape(video_title[:200])
                caption_text = t(lang, "dl_caption_universal", title=escaped_title)

                sent = False
                try:
                    with open(file_path, 'rb') as vf:
                        bot.send_video(user_id, vf, caption=caption_text, parse_mode="HTML", supports_streaming=True, timeout=120)
                    sent = True
                except Exception as send_vid_err:
                    print(f"[!] send_video failed: {send_vid_err}, retrying with send_document...", flush=True)
                    try:
                        with open(file_path, 'rb') as vf:
                            bot.send_document(user_id, vf, caption=caption_text, parse_mode="HTML", timeout=120)
                        sent = True
                    except Exception as send_doc_err:
                        print(f"[!] send_document failed: {send_doc_err}", flush=True)

                if sent:
                    try:
                        bot.delete_message(user_id, msg_id)
                    except Exception:
                        pass
                    return

        # Strategy 3: Cobalt fallback
        try:
            if fallback_cobalt_download(user_id, target_url, msg_id):
                return
        except Exception:
            pass

        # Strategy 4: TikTok fallback if it's TikTok
        if "tiktok.com" in target_url:
            download_and_send_tiktok(user_id, target_url)
            return

        # If all methods failed
        try:
            bot.edit_message_text(
                t(lang, "dl_failed"),
                user_id,
                msg_id,
                parse_mode="HTML"
            )
        except Exception:
            pass

    finally:
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir, ignore_errors=True)
            except Exception:
                pass

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
# 6. BOT HANDLERS (COMMANDS & TOOLS)
# ==========================================
if bot:
    @bot.message_handler(commands=['start', 'home', 'menu'])
    def handle_start(message):
        if message.chat.type != "private":
            return
        user = message.from_user
        clear_state(user.id)
        is_new = register_user(user)
        lang = get_user_lang(user.id)

        if is_banned(user.id):
            bot.send_message(message.chat.id, t(lang, "banned_short"), parse_mode="HTML")
            return

        parts = message.text.split(maxsplit=1)
        payload = parts[1].strip() if len(parts) > 1 else ""

        if payload in ["mod_apk", "mod", "mod_update"]:
            mod_text = (
                "⚠️ <b>SERVER UPDATE IN PROGRESS | সার্ভার আপডেট চলছে</b>\n"
                "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                "🇬🇧 <b>[ENGLISH]</b>\n"
                "Their server is currently undergoing an update, which is why the Mod APK is temporarily not working. The admin is actively working on remaking the app. To receive the latest update, please stay joined to our official channel and continue using our bot's other features!\n\n"
                "🇧🇩 <b>[বাংলা]</b>\n"
                "তাদের সার্ভার আপডেট হওয়ার কারণে বর্তমানে Mod APK কাজ করছে না। এডমিন বিষয়টি নিয়ে কাজ করছেন এবং অ্যাপটি নতুনভাবে তৈরি করছেন। পরবর্তী আপডেট সবার আগে পেতে আমাদের অফিসিয়াল চ্যানেলে যুক্ত থাকুন এবং আমাদের বটের অন্যান্য ফিচার ব্যবহার করুন!\n\n"
                "🇮🇩 <b>[INDONESIA]</b>\n"
                "Server mereka sedang dalam pembaruan, itulah sebabnya Mod APK saat ini tidak berfungsi. Admin sedang bekerja keras untuk membuat ulang aplikasi tersebut. Untuk mendapatkan pembaruan terbaru, tetap bergabung di channel resmi kami dan silakan gunakan fitur-fitur bot lainnya!\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"📢 <b>Official Channel:</b> {REQUIRED_CHANNEL}"
            )
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("📢 Join Official Channel", url=CHANNEL_URL),
                types.InlineKeyboardButton("🤖 Explore Bot Features", callback_data="verify_home")
            )
            bot.send_message(message.chat.id, mod_text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
            return

        if payload.startswith("file_") or payload.startswith("f_"):
            if not check_channel_joined(user.id):
                send_join_prompt(message.chat.id, f"verify_file|{payload}", user_id=user.id)
                return
            send_shared_file_by_code(message.chat.id, payload, user_id=user.id)
            return

        if is_maintenance() and user.id not in ADMIN_IDS:
            bot.send_message(
                message.chat.id,
                t(lang, "maintenance"),
                parse_mode="HTML"
            )
            return

        if is_new:
            notify_admin_log(user, "MR GHOST BOT STARTED (New User)")

        if not check_channel_joined(user.id):
            send_join_prompt(message.chat.id, "verify_home", user_id=user.id)
            return

        # 1. Send Start Photo First (Protected content based on Admin setting, not forwarded)
        if os.path.exists(START_PHOTO_PATH):
            try:
                protect = is_photo_protection_enabled()
                with open(START_PHOTO_PATH, 'rb') as pf:
                    bot.send_photo(message.chat.id, pf, protect_content=protect)
            except Exception as e:
                print(f"[!] Start photo send error: {e}", flush=True)

        # 2. Send Stylish Welcome Message with Persistent Menu Keyboard
        welcome_text = t(lang, "welcome")
        safe_send_message(
            message.chat.id,
            welcome_text,
            parse_mode="HTML",
            reply_markup=get_main_reply_keyboard(user.id)
        )

    @bot.message_handler(commands=['lang', 'language'])
    def handle_lang_cmd(message):
        if message.chat.type != "private":
            return
        user = message.from_user
        register_user(user)
        if is_banned(user.id):
            bot.send_message(message.chat.id, t(get_user_lang(user.id), "banned_short"), parse_mode="HTML")
            return
        clear_state(user.id)
        lang = get_user_lang(user.id)
        bot.send_message(
            message.chat.id,
            t(lang, "lang_prompt"),
            parse_mode="HTML",
            reply_markup=get_language_keyboard(user.id)
        )

    @bot.message_handler(commands=['help', 'about'])
    def handle_help(message):
        if message.chat.type != "private":
            return
        lang = get_user_lang(message.from_user.id)
        help_text = t(lang, "help_text")
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(t(lang, "help_btn_channel"), url=CHANNEL_URL),
            types.InlineKeyboardButton(t(lang, "help_btn_support"), url="https://t.me/helpghotsteam")
        )
        safe_send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)

    @bot.message_handler(commands=['banlist'])
    def handle_banlist_cmd(message):
        if message.chat.type != "private":
            return
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
        if message.chat.type != "private":
            return
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
        if message.chat.type != "private":
            return
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
        if message.chat.type != "private":
            return
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

    # ==========================================
    # 7. MEDIA UPLOAD HANDLER
    # ==========================================
    @bot.message_handler(content_types=['document', 'video', 'photo'])
    def handle_media_upload(message):
        if message.chat.type != "private":
            return
        user_id = message.from_user.id
        state = get_state(user_id)
        lang = get_user_lang(user_id)

        # Admin uploading cookies.txt
        if user_id in ADMIN_IDS and message.document and (state == "admin_upload_cookie" or message.document.file_name == "cookies.txt"):
            clear_state(user_id)
            try:
                file_info = bot.get_file(message.document.file_id)
                downloaded = bot.download_file(file_info.file_path)
                with open("cookies.txt", "wb") as f:
                    f.write(downloaded)
                bot.reply_to(message, "✅ <b>cookies.txt সফলভাবে আপডেট করা হয়েছে!</b>\nকুকিজ সক্রিয় থাকবে।", parse_mode="HTML")
            except Exception as e:
                bot.reply_to(message, f"❌ কুকিজ ফাইল সেভ করতে ব্যর্থ: {e}")
            return

        # Image to Link State
        if state == "awaiting_imgbb_photo" and message.photo:
            clear_state(user_id)
            wait_m = bot.send_message(message.chat.id, t(lang, "imgbb_uploading"), parse_mode="HTML")
            try:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_bytes = bot.download_file(file_info.file_path)
                res = upload_image_to_imgbb(file_bytes)
                if res.get("success"):
                    direct_url = res["url"]
                    display_url = res["display_url"]
                    size_kb = res["size"]

                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton(t(lang, "imgbb_btn_open"), url=direct_url))

                    out_txt = t(
                        lang,
                        "imgbb_success",
                        direct_url=direct_url,
                        display_url=display_url,
                        size_kb=size_kb
                    )
                    bot.edit_message_text(out_txt, message.chat.id, wait_m.message_id, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=False)
                else:
                    bot.edit_message_text(t(lang, "imgbb_fail", err=html.escape(str(res.get('error')))), message.chat.id, wait_m.message_id, parse_mode="HTML")
            except Exception as e:
                bot.edit_message_text(t(lang, "imgbb_err", err=html.escape(str(e))), message.chat.id, wait_m.message_id, parse_mode="HTML")
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

        msg = t(
            lang,
            "fs_uploaded",
            fname=html.escape(file_name),
            code=unique_code,
            link=share_link
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t(lang, "fs_btn_upload_more"), callback_data="act_upload"))
        markup.add(types.InlineKeyboardButton(t(lang, "fs_btn_main_menu"), callback_data="verify_home"))
        bot.reply_to(message, msg, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)

    # ==========================================
    # 8. CALLBACK QUERY HANDLERS
    # ==========================================
    @bot.callback_query_handler(func=lambda call: True)
    def handle_all_callbacks(call):
        if call.message and call.message.chat.type != "private":
            return
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        data = call.data
        lang = get_user_lang(user_id)

        if data.startswith("verify_"):
            if not check_channel_joined(user_id):
                bot.answer_callback_query(call.id, t(lang, "verify_not_joined_alert"), show_alert=True)
                send_join_prompt(chat_id, "verify_home", user_id=user_id)
                return

            bot.answer_callback_query(call.id, t(lang, "verify_success_alert"))
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except Exception:
                pass

            if data.startswith("verify_file|"):
                file_code = data.split("|", 1)[1]
                send_shared_file_by_code(chat_id, file_code, user_id=user_id)
            else:
                safe_send_message(
                    chat_id,
                    t(lang, "verify_success_msg"),
                    parse_mode="HTML",
                    reply_markup=get_main_reply_keyboard(user_id)
                )
            return

        if not check_channel_joined(user_id):
            bot.answer_callback_query(call.id, t(lang, "verify_need_join_short"), show_alert=True)
            send_join_prompt(chat_id, "verify_home", user_id=user_id)
            return

        if data == "act_upload":
            bot.answer_callback_query(call.id)
            set_state(user_id, "awaiting_file_upload")
            bot.send_message(
                chat_id,
                t(lang, "fs_ask_upload"),
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
                t(lang, "enc_selected", title=title),
                parse_mode="HTML"
            )
            return

        if data == "open_enc_menu":
            bot.answer_callback_query(call.id)
            bot.send_message(
                chat_id,
                t(lang, "enc_menu_short"),
                parse_mode="HTML",
                reply_markup=get_encode_decode_keyboard()
            )
            return

    # ==========================================
    # 9. TEXT MESSAGE & MENU ROUTER
    # ==========================================
    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        if message.chat.type != "private":
            return
        user = message.from_user
        text = message.text.strip()
        chat_id = message.chat.id
        register_user(user)
        lang = get_user_lang(user.id)

        if text in LANG_CHOICE_BUTTONS:
            if is_banned(user.id):
                bot.send_message(chat_id, t(lang, "banned_short"), parse_mode="HTML")
                return
            new_lang = LANG_CHOICE_BUTTONS[text]
            set_user_lang(user.id, new_lang)
            clear_state(user.id)
            if not check_channel_joined(user.id):
                bot.send_message(chat_id, t(new_lang, "lang_changed"), parse_mode="HTML")
                send_join_prompt(chat_id, "verify_home", user_id=user.id)
                return
            bot.send_message(
                chat_id,
                t(new_lang, "lang_changed"),
                parse_mode="HTML",
                reply_markup=get_main_reply_keyboard(user.id)
            )
            return

        if resolve_button_action(text) == "btn_home":
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
            elif text == "🔗 Mod Share Link":
                try:
                    b_info = bot.get_me()
                    b_username = b_info.username
                except Exception:
                    b_username = "mrghost_121_bot"
                mod_link = f"https://t.me/{b_username}?start=mod_apk"
                msg = (
                    "🔗 <b>MOD APK SHARE LINK GENERATED</b>\n"
                    "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
                    "এই লিংকটি যেকোনো ইউজার বা গ্রুপে শেয়ার করতে পারেন। ব্যবহারকারী এই লিংকে ক্লিক করলে ৩টি ভাষায় (Bangla, English, Indonesia) সার্ভার আপডেট ও অ্যাপ মেকিংয়ের নোটিশ দেখতে পাবে:\n\n"
                    f"👉 <b>Shareable Deep Link:</b>\n<code>{mod_link}</code>\n\n"
                    "📌 <i>লিংকটিতে চাপ দিলে স্বয়ংক্রিয়ভাবে কপি হয়ে যাবে।</i>"
                )
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    types.InlineKeyboardButton("🚀 Test Link", url=mod_link),
                    types.InlineKeyboardButton("📤 Share Link", url=f"https://t.me/share/url?url={mod_link}&text=Mod%20APK%20Update%20Notice")
                )
                bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
                return

            if message.forward_from_chat and message.forward_from_chat.type in ["channel", "supergroup"]:
                f_chat = message.forward_from_chat
                set_setting("required_channel_2_id", str(f_chat.id))
                bot.reply_to(message, f"✅ <b>Channel 2 ID স্বয়ংক্রিয়ভাবে ডিটেক্ট ও সেভ হয়েছে!</b>\n\n📢 <b>Title:</b> {html.escape(f_chat.title or '')}\n🆔 <b>Chat ID:</b> <code>{f_chat.id}</code>", parse_mode="HTML")
                clear_state(user.id)
                return

        if not verify_user_access(message, "verify_home"):
            return

        action = resolve_button_action(text)

        if action:
            clear_state(user.id)

            if action == "btn_file_sharing":
                bot.send_message(chat_id, t(lang, "fs_panel"), parse_mode="HTML", reply_markup=get_file_sharing_keyboard(user.id))
                return

            elif action == "btn_upload_file":
                set_state(user.id, "awaiting_file_upload")
                bot.send_message(chat_id, t(lang, "fs_ask_upload"), parse_mode="HTML")
                return

            elif action == "btn_stats":
                _, user_up, _ = get_user_stats(user.id)
                user_coins = get_user_coins(user.id)
                stats_msg = t(
                    lang,
                    "stats_msg",
                    name=html.escape(user.first_name or "User"),
                    uid=user.id,
                    uname=user.username or "N/A",
                    uploads=user_up,
                    coins=user_coins
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(t(lang, "btn_join_main_ch"), url=CHANNEL_URL))
                markup.add(types.InlineKeyboardButton(t(lang, "btn_join_vip_ch"), url=REQUIRED_CHANNEL_2_URL))
                markup.add(types.InlineKeyboardButton(t(lang, "btn_upload_new_file"), callback_data="act_upload"))
                bot.send_message(chat_id, stats_msg, parse_mode="HTML", reply_markup=markup)
                return

            elif action == "btn_help":
                handle_help(message)
                return

            elif action == "btn_lang":
                bot.send_message(chat_id, t(lang, "lang_prompt"), parse_mode="HTML", reply_markup=get_language_keyboard(user.id))
                return

            elif action == "btn_fb_dl":
                notify_admin_log(user, "Facebook Downloader")
                set_state(user.id, "awaiting_video_url")
                bot.send_message(chat_id, t(lang, "ask_fb_url"), parse_mode="HTML")
                return

            elif action == "btn_tiktok_dl":
                notify_admin_log(user, "TikTok Downloader")
                set_state(user.id, "awaiting_tiktok_url")
                bot.send_message(chat_id, t(lang, "ask_tiktok_url"), parse_mode="HTML")
                return

            elif action == "btn_insta_dl":
                notify_admin_log(user, "Instagram Downloader")
                set_state(user.id, "awaiting_insta_url")
                bot.send_message(chat_id, t(lang, "ask_insta_url"), parse_mode="HTML")
                return

            elif action == "btn_thumb_dl":
                notify_admin_log(user, "Thumbnail Downloader")
                set_state(user.id, "awaiting_yt_thumb")
                bot.send_message(chat_id, t(lang, "ask_yt_thumb"), parse_mode="HTML")
                return

            elif action == "btn_img_link":
                notify_admin_log(user, "Image to Link")
                set_state(user.id, "awaiting_imgbb_photo")
                bot.send_message(chat_id, t(lang, "ask_imgbb"), parse_mode="HTML")
                return

            elif action == "btn_live_tv":
                notify_admin_log(user, "Live TV")
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(t(lang, "live_tv_btn_open"), url="https://mboxofficial.vercel.app/"),
                    types.InlineKeyboardButton(t(lang, "live_tv_btn_ch"), url=CHANNEL_URL)
                )
                bot.send_message(chat_id, t(lang, "live_tv_msg"), parse_mode="HTML", reply_markup=markup)
                return

            elif action == "btn_yt_extract":
                notify_admin_log(user, "YT Title/Tags Extractor")
                set_state(user.id, "awaiting_yt_extract")
                bot.send_message(chat_id, t(lang, "ask_yt_extract"), parse_mode="HTML")
                return

            elif action == "btn_tik_title":
                notify_admin_log(user, "TikTok Title Extractor")
                set_state(user.id, "awaiting_tik_title")
                bot.send_message(chat_id, t(lang, "ask_tik_title"), parse_mode="HTML")
                return

            elif action == "btn_num_info":
                notify_admin_log(user, "Number to Info")
                set_state(user.id, "awaiting_num_info")
                bot.send_message(chat_id, t(lang, "ask_num_info"), parse_mode="HTML")
                return

            elif action == "btn_qr":
                notify_admin_log(user, "QR Maker")
                set_state(user.id, "awaiting_qr_text")
                bot.send_message(chat_id, t(lang, "ask_qr"), parse_mode="HTML")
                return

            elif action == "btn_enc_dec":
                notify_admin_log(user, "Encode & Decode Tool")
                bot.send_message(
                    chat_id,
                    t(lang, "enc_menu_msg"),
                    parse_mode="HTML",
                    reply_markup=get_encode_decode_keyboard()
                )
                return

            elif action == "btn_link_check":
                notify_admin_log(user, "Link Checker Tool")
                set_state(user.id, "awaiting_link_check")
                bot.send_message(chat_id, t(lang, "ask_link_check"), parse_mode="HTML")
                return

            elif action == "btn_ip_track":
                notify_admin_log(user, "IP Tracker")
                set_state(user.id, "awaiting_ip")
                bot.send_message(chat_id, t(lang, "ask_ip"), parse_mode="HTML")
                return

            elif action == "btn_wa_open":
                notify_admin_log(user, "WhatsApp Opener")
                set_state(user.id, "awaiting_wa_num")
                bot.send_message(chat_id, t(lang, "ask_wa"), parse_mode="HTML")
                return

            elif action == "btn_card_hub":
                notify_admin_log(user, "Visa / Master Card Hub")
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                daily_b = get_daily_bonus_amount()
                msg = t(lang, "card_hub_msg", cost=cost, coins=user_coins, daily_b=daily_b)
                bot.send_message(
                    chat_id,
                    msg,
                    parse_mode="HTML",
                    reply_markup=get_visa_menu_keyboard(user.id)
                )
                return

            elif action == "btn_cc_gen":
                notify_admin_log(user, "CC Generator")
                set_state(user.id, "awaiting_cc_bin")
                bot.send_message(chat_id, t(lang, "ask_cc_bin"), parse_mode="HTML")
                return

            elif action == "btn_get_card":
                notify_admin_log(user, "Card Purchase")
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                if user_coins < cost:
                    bot.send_message(chat_id, t(lang, "card_low_coins", cost=cost, coins=user_coins), parse_mode="HTML")
                    return

                card = pop_card_db()
                if not card:
                    bot.send_message(chat_id, t(lang, "card_out_of_stock"), parse_mode="HTML")
                else:
                    new_bal = deduct_user_coins(user.id, cost)
                    random_zip = random.randint(10000, 99999)
                    bot.send_message(
                        chat_id,
                        t(lang, "card_delivered", card=html.escape(card), zip_code=random_zip, cost=cost, new_bal=new_bal),
                        parse_mode="HTML"
                    )
                return

            elif action == "btn_daily_bonus":
                notify_admin_log(user, "Daily Bonus Claim")
                claimed, bonus_or_hours, mins, new_bal = claim_daily_bonus(user.id)
                if claimed:
                    bot.send_message(
                        chat_id,
                        t(lang, "daily_claimed", bonus=bonus_or_hours, new_bal=new_bal),
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        t(lang, "daily_cooldown", hours=bonus_or_hours, mins=mins, new_bal=new_bal),
                        parse_mode="HTML"
                    )
                return

            elif action == "btn_my_balance":
                user_coins = get_user_coins(user.id)
                cost = get_card_cost()
                daily_b = get_daily_bonus_amount()
                bot.send_message(
                    chat_id,
                    t(lang, "my_balance", name=html.escape(user.first_name or "User"), uid=user.id, coins=user_coins, cost=cost, daily_b=daily_b),
                    parse_mode="HTML"
                )
                return

            elif action == "btn_nid":
                notify_admin_log(user, "BD NID Tools")
                bot.send_message(chat_id, t(lang, "nid_tools"), parse_mode="HTML")
                return

            elif action == "btn_aadhaar":
                notify_admin_log(user, "Aadhaar Tools")
                bot.send_message(chat_id, t(lang, "aadhaar_tools"), parse_mode="HTML")
                return

            elif action == "btn_sms_bomb":
                notify_admin_log(user, "SMS Bomber")
                bot.send_message(chat_id, t(lang, "sms_bomber"), parse_mode="HTML")
                return

        # ==========================================
        # 10. STATE-BASED INPUT PROCESSING
        # ==========================================
        state = get_state(user.id)

        if state == "admin_upload_cookie" and user.id in ADMIN_IDS:
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
                    t_lang = get_user_lang(target_uid)
                    bot.send_message(
                        target_uid,
                        t(t_lang, "coin_notify", diff=diff_text, new_bal=new_b),
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
            markup.add(types.InlineKeyboardButton(t(lang, "enc_btn_another"), callback_data="open_enc_menu"))

            resp_txt = t(lang, "enc_result", result=html.escape(result))
            bot.send_message(chat_id, resp_txt, parse_mode="HTML", reply_markup=markup)
            return

        # Link Checker State
        if state == "awaiting_link_check":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, t(lang, "link_scanning"), parse_mode="HTML")
            rep = analyze_link_safety(text)

            flags_txt = "\n".join([f"• {f}" for f in rep["flags"]])
            redirect_txt = "None (Direct)"
            if rep["redirect_chain"]:
                redirect_txt = f"{rep['redirect_count']} Hops:\n" + "\n".join([f"→ <code>{html.escape(u)}</code>" for u in rep["redirect_chain"][:4]])

            out_msg = t(
                lang,
                "link_report",
                status_code=rep["status_code"],
                safety_level=rep["safety_level"],
                resp_ms=rep["response_time_ms"],
                ip=rep["ip"],
                server=rep["server"],
                final_url=html.escape(rep["final_url"]),
                redirect_txt=redirect_txt,
                flags_txt=flags_txt
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
                    caption=t(lang, "yt_thumb_caption"),
                    parse_mode="HTML"
                )
            else:
                bot.send_message(chat_id, t(lang, "yt_thumb_invalid"), parse_mode="HTML")
            return

        elif state == "awaiting_yt_extract":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, t(lang, "yt_extracting"), parse_mode="HTML")
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

                res_text = t(lang, "yt_extract_result", title=html.escape(title), desc=html.escape(desc), tags=html.escape(tags))
                bot.edit_message_text(res_text, chat_id, wait_m.message_id, parse_mode="HTML")
            except Exception:
                try:
                    r = requests.get("https://yt-vid.hazex.workers.dev/?url=" + urllib.parse.quote(text), timeout=10).json()
                    title = r.get("title") or "No Title Found"
                    desc = (r.get("description") or "No Description")[:2000]
                    tags_raw = r.get("tags")
                    tags = ", ".join(tags_raw) if isinstance(tags_raw, list) else (tags_raw or "No Tags Found")
                    res_text = t(lang, "yt_extract_result", title=html.escape(title), desc=html.escape(desc), tags=html.escape(str(tags)))
                    bot.edit_message_text(res_text, chat_id, wait_m.message_id, parse_mode="HTML")
                except Exception:
                    bot.edit_message_text(t(lang, "yt_extract_failed"), chat_id, wait_m.message_id, parse_mode="HTML")
            return

        elif state == "awaiting_tik_title":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, t(lang, "tik_title_loading"), parse_mode="HTML")
            try:
                r = requests.get("https://www.tikwm.com/api/?url=" + urllib.parse.quote(text), timeout=12).json()
                if r.get("data"):
                    title = r["data"].get("title") or "No Title Found!"
                    bot.edit_message_text(
                        t(lang, "tik_title_success", title=html.escape(title)),
                        chat_id,
                        wait_m.message_id,
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text(t(lang, "tik_title_fail"), chat_id, wait_m.message_id, parse_mode="HTML")
            except Exception:
                bot.edit_message_text(t(lang, "server_no_resp"), chat_id, wait_m.message_id, parse_mode="HTML")
            return

        elif state == "awaiting_num_info":
            clear_state(user.id)
            wait_m = bot.send_message(chat_id, t(lang, "num_searching"), parse_mode="HTML")
            info = resolve_phone_info(text)

            wa_link = f"https://wa.me/{info['clean_digits']}"
            tg_link = f"tg://resolve?phone={info['clean_digits']}"

            info_txt = t(
                lang,
                "num_result",
                owner=html.escape(info['owner_name']),
                intl=html.escape(info['intl_format']),
                nat=html.escape(info['nat_format']),
                country=html.escape(info['country']),
                carrier=html.escape(info['carrier']),
                ltype=html.escape(info['type']),
                tz=html.escape(info['timezone']),
                valid='Yes' if info['valid'] else 'No',
                wa_link=wa_link,
                tg_link=tg_link
            )
            bot.edit_message_text(info_txt, chat_id, wait_m.message_id, parse_mode="HTML", disable_web_page_preview=True)
            return

        elif state == "awaiting_qr_text":
            clear_state(user.id)
            qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + urllib.parse.quote(text)
            bot.send_photo(
                chat_id,
                qr_url,
                caption=t(lang, "qr_ready", data=html.escape(text)),
                parse_mode="HTML"
            )
            return

        elif state == "awaiting_ip":
            clear_state(user.id)
            if "." not in text:
                bot.send_message(chat_id, t(lang, "ip_invalid"), parse_mode="HTML")
                return
            try:
                r = requests.get(f"http://ip-api.com/json/{urllib.parse.quote(text)}", timeout=10).json()
                if r.get("status") == "fail":
                    bot.send_message(chat_id, f"❌ <b>Error:</b> {html.escape(r.get('message', 'Invalid IP'))}", parse_mode="HTML")
                    return
                txt = t(lang, "ip_header")
                for k, v in r.items():
                    txt += f"<b>{html.escape(str(k))}</b> : <code>{html.escape(str(v))}</code>\n"
                bot.send_message(chat_id, txt, parse_mode="HTML")
                if r.get("lat") and r.get("lon"):
                    bot.send_location(chat_id, r["lat"], r["lon"])
            except Exception:
                bot.send_message(chat_id, t(lang, "ip_not_found"), parse_mode="HTML")
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
                bot.send_message(chat_id, t(lang, "wa_invalid"), parse_mode="HTML")
                return

            link = f"https://wa.me/{number}"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(t(lang, "wa_btn_open"), url=link))
            bot.send_message(chat_id, t(lang, "wa_ready"), parse_mode="HTML", reply_markup=markup)
            return

        elif state == "awaiting_cc_bin":
            clear_state(user.id)
            bin_str = re.sub(r'[^0-9]', '', text)
            if len(bin_str) < 6:
                bot.send_message(chat_id, t(lang, "cc_bin_invalid"), parse_mode="HTML")
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
            resp = t(lang, "cc_bin_result", bin_str=bin_str, cards=cards_block)
            bot.send_message(chat_id, resp, parse_mode="HTML")
            return

        # ==========================================
        # 11. AUTO VIDEO DOWNLOADER (TIKTOK / FB / INSTA - PRIVATE CHAT ONLY)
        # ==========================================
        url_match = re.search(r'https?://[^\s<>"]+', text)
        if url_match:
            found_url = url_match.group(0).rstrip('.,;!?')
            domain = urllib.parse.urlparse(found_url).netloc.lower()

            if "tiktok.com" in domain:
                notify_admin_log(user, "Auto TikTok Downloader")
                threading.Thread(target=download_and_send_tiktok, args=(chat_id, found_url), daemon=True).start()
                return
            elif any(k in domain for k in ["instagram.com", "instagr.am"]):
                notify_admin_log(user, "Auto Instagram Downloader")
                threading.Thread(target=download_and_send_instagram, args=(chat_id, found_url), daemon=True).start()
                return
            elif any(k in domain for k in ["facebook.com", "fb.watch", "fb.com", "fb.me"]):
                notify_admin_log(user, "Auto Facebook Downloader")
                threading.Thread(target=download_and_send_universal_video, args=(chat_id, found_url), daemon=True).start()
                return
            elif is_youtube_or_pinterest(found_url):
                bot.reply_to(message, t(lang, "dl_unsupported_removed"), parse_mode="HTML")
                return

        # Fallback for unrecognized text in private chat
        bot.reply_to(
            message,
            t(lang, "fallback_unrecognized"),
            parse_mode="HTML",
            reply_markup=get_main_reply_keyboard(user.id)
        )

    @bot.my_chat_member_handler()
    def handle_my_chat_member_event(update):
        try:
            chat = update.chat
            if chat.type == "channel":
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

        try:
            bot.set_my_commands([
                types.BotCommand("start", "Start / Main Menu"),
                types.BotCommand("lang", "Change Language (Bangla / English / Indonesia)"),
                types.BotCommand("help", "Help & Available Tools"),
                types.BotCommand("ad", "Admin Panel"),
            ])
        except Exception as e:
            print(f"[!] set_my_commands warning: {e}", flush=True)

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
