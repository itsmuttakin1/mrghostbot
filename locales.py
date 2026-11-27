# -*- coding: utf-8 -*-
"""
Trilingual localization module for Mr Ghost Bot.
Supports:
  - 'bn': Bangla (বাংলা)
  - 'en': English
  - 'id': Indonesian (Bahasa Indonesia)
"""

SUPPORTED_LANGS = ("bn", "en", "id")

LANG_CHOICE_BUTTONS = {
    "🇧🇩 বাংলা": "bn",
    "🇧🇩 বাংলা (Bangla)": "bn",
    "🇬🇧 English": "en",
    "🇮🇩 Indonesia": "id",
    "🇮🇩 Bahasa Indonesia": "id",
}

BUTTONS = {
    "btn_file_sharing": {
        "bn": "📂 ফাইল শেয়ারিং বট",
        "en": "📂 File Sharing Bot",
        "id": "📂 Berbagi File",
    },
    "btn_fb_dl": {
        "bn": "📹 ফেসবুক ডাউনলোড",
        "en": "📹 Facebook Download",
        "id": "📹 Unduh Facebook",
    },
    "btn_tiktok_dl": {
        "bn": "🎵 টিকটক ডাউনলোড",
        "en": "🎵 TikTok Download",
        "id": "🎵 Unduh TikTok",
    },
    "btn_insta_dl": {
        "bn": "📸 ইনস্টাগ্রাম ডাউনলোড",
        "en": "📸 Instagram Download",
        "id": "📸 Unduh Instagram",
    },
    "btn_thumb_dl": {
        "bn": "🖼️ থাম্বনেইল ডাউনলোডার",
        "en": "🖼️ Thumbnail Downloader",
        "id": "🖼️ Pengunduh Thumbnail",
    },
    "btn_img_link": {
        "bn": "🖼️ ছবি থেকে লিংক",
        "en": "🖼️ Image to Link",
        "id": "🖼️ Gambar ke Link",
    },
    "btn_live_tv": {
        "bn": "📺 লাইভ টিভি",
        "en": "📺 Live TV",
        "id": "📺 TV Langsung",
    },
    "btn_num_info": {
        "bn": "📞 নাম্বার ইনফো",
        "en": "📞 Number to Info",
        "id": "📞 Info Nomor",
    },
    "btn_qr": {
        "bn": "🔳 কিউআর মেকার",
        "en": "🔳 Qr Maker",
        "id": "🔳 Pembuat QR",
    },
    "btn_enc_dec": {
        "bn": "🔐 এনকোড ও ডিকোড",
        "en": "🔐 Encode & Decode",
        "id": "🔐 Enkode & Dekode",
    },
    "btn_link_check": {
        "bn": "🛡️ লিংক চেকার",
        "en": "🛡️ Link Checker",
        "id": "🛡️ Pemeriksa Link",
    },
    "btn_yt_extract": {
        "bn": "📝 ওয়াইটি টাইটেল/ট্যাগ",
        "en": "📝 Yt Title Tags Extract",
        "id": "📝 Ekstrak Judul/Tag YT",
    },
    "btn_tik_title": {
        "bn": "📝 টিকটক টাইটেল",
        "en": "📝 TikTok Title Extract",
        "id": "📝 Ekstrak Judul TikTok",
    },
    "btn_ip_track": {
        "bn": "🌍 আইপি ট্র্যাকার",
        "en": "🌍 IP Tracker",
        "id": "🌍 Pelacak IP",
    },
    "btn_wa_open": {
        "bn": "💫 হোয়াটসঅ্যাপ ওপেনার",
        "en": "💫 Whatsapp Opener",
        "id": "💫 Pembuka WhatsApp",
    },
    "btn_card_hub": {
        "bn": "🪪 ভিসা / মাস্টার কার্ড",
        "en": "🪪 Visa / Master Card Maker",
        "id": "🪪 Pembuat Kartu Visa/Master",
    },
    "btn_nid": {
        "bn": "🆔 বিডি এনআইডি টুলস",
        "en": "🆔 BD NID Tools",
        "id": "🆔 Alat NID BD",
    },
    "btn_aadhaar": {
        "bn": "🪪 আধার টুলস",
        "en": "🪪 Aadhaar Tools",
        "id": "🪪 Alat Aadhaar",
    },
    "btn_sms_bomb": {
        "bn": "⚠️ এসএমএস বোম্বার",
        "en": "⚠️ SMS BOMBER",
        "id": "⚠️ SMS BOMBER",
    },
    "btn_stats": {
        "bn": "📊 পরিসংখ্যান",
        "en": "📊 Stats",
        "id": "📊 Statistik",
    },
    "btn_help": {
        "bn": "ℹ️ সাহায্য",
        "en": "ℹ️ Help",
        "id": "ℹ️ Bantuan",
    },
    "btn_lang": {
        "bn": "🌐 ভাষা / Language",
        "en": "🌐 Language",
        "id": "🌐 Bahasa / Language",
    },
    "btn_upload_file": {
        "bn": "📤 ফাইল আপলোড",
        "en": "📤 Upload File",
        "id": "📤 Unggah File",
    },
    "btn_home": {
        "bn": "🏠 হোম",
        "en": "🏠 Home",
        "id": "🏠 Beranda",
    },
    "btn_get_card": {
        "bn": "💳 কার্ড নিন ({cost} কয়েন)",
        "en": "💳 Get Card ({cost} Coins)",
        "id": "💳 Ambil Kartu ({cost} Koin)",
    },
    "btn_cc_gen": {
        "bn": "💳 সিসি জেনারেটর",
        "en": "💳 CC Generator",
        "id": "💳 Generator CC",
    },
    "btn_daily_bonus": {
        "bn": "🎁 ডেইলি বোনাস",
        "en": "🎁 Daily Bonus",
        "id": "🎁 Bonus Harian",
    },
    "btn_my_balance": {
        "bn": "💰 আমার ব্যালেন্স",
        "en": "💰 My Balance",
        "id": "💰 Saldo Saya",
    },
}

# Build reverse lookup from any language's label (plus legacy aliases) to action key
_REVERSE_BUTTON_MAP = {}
for _key, _langs in BUTTONS.items():
    if _key == "btn_get_card":
        continue
    for _lbl in _langs.values():
        _REVERSE_BUTTON_MAP[_lbl] = _key

_LEGACY_ALIASES = {
    "🏠 Main Menu": "btn_home",
    "🔙 Back to Main Menu": "btn_home",
    "🔙 মেইন মেনু": "btn_home",
    "💳 Get Free Card": "btn_get_card",
}
_REVERSE_BUTTON_MAP.update(_LEGACY_ALIASES)


def btn(lang: str, key: str, **kwargs) -> str:
    lang = lang if lang in SUPPORTED_LANGS else "bn"
    text = BUTTONS[key].get(lang, BUTTONS[key]["en"])
    return text.format(**kwargs) if kwargs else text


def resolve_button_action(text: str):
    if not text:
        return None
    if text in _REVERSE_BUTTON_MAP:
        return _REVERSE_BUTTON_MAP[text]
    if text.startswith(("💳 Get Card", "💳 কার্ড নিন", "💳 Ambil Kartu")):
        return "btn_get_card"
    return None


TEXTS = {
    # --- Access, Ban, Maintenance, Force Join ---
    "banned_short": {
        "bn": "🚫 তুমি এই বট থেকে ব্যান করা আছো!",
        "en": "🚫 You are banned from using this bot!",
        "id": "🚫 Anda diblokir dari menggunakan bot ini!",
    },
    "banned_full": {
        "bn": "🚫 <b>Access Denied!</b>\n\nতুমি এই বট থেকে ব্যান করা আছো! Unban করতে এডমিনের সাথে যোগাযোগ করো।",
        "en": "🚫 <b>Access Denied!</b>\n\nYou have been banned from this bot! Contact an admin to unban.",
        "id": "🚫 <b>Akses Ditolak!</b>\n\nAnda diblokir dari bot ini! Hubungi admin untuk membuka blokir.",
    },
    "maintenance": {
        "bn": "🚧 <b>Bot Under Maintenance!</b>\n\n🔧 সিস্টেম আপগ্রেড চলছে...\n⏳ অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।",
        "en": "🚧 <b>Bot Under Maintenance!</b>\n\n🔧 System upgrade is in progress...\n⏳ Please try again later.",
        "id": "🚧 <b>Bot Sedang Pemeliharaan!</b>\n\n🔧 Peningkatan sistem sedang berlangsung...\n⏳ Silakan coba lagi nanti.",
    },
    "join_btn_1": {
        "bn": "📢 ১. মেইন চ্যানেলে জয়েন করুন ({channel})",
        "en": "📢 1. Join Main Channel ({channel})",
        "id": "📢 1. Gabung Saluran Utama ({channel})",
    },
    "join_btn_2": {
        "bn": "📢 ২. VIP চ্যানেল ২-তে জয়েন করুন",
        "en": "📢 2. Join VIP Channel 2",
        "id": "📢 2. Gabung Saluran VIP 2",
    },
    "join_btn_verify": {
        "bn": "✅ উভয় চ্যানেলে জয়েন করেছি / ভেরিফাই",
        "en": "✅ Joined Both / Verify Now",
        "id": "✅ Sudah Gabung Keduanya / Verifikasi",
    },
    "join_prompt": {
        "bn": (
            "⛔ <b>Access Denied! | প্রবেশাধিকার সংরক্ষিত</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ বটের যেকোনো টুলস ও ফিচার ব্যবহার করতে হলে আপনাকে <b>উভয় চ্যানেলে</b> অবশ্যই জয়েন থাকতে হবে:\n\n"
            "👉 <b>চ্যানেল ১:</b> {channel}\n"
            "👉 <b>চ্যানেল ২:</b> <a href='{ch2_url}'>VIP Private Channel</a>\n\n"
            "উভয় চ্যানেলে জয়েন করার পর নিচের বাটনে ক্লিক করুন।"
        ),
        "en": (
            "⛔ <b>Access Denied!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ To use any tools and features of this bot, you must join <b>both channels</b>:\n\n"
            "👉 <b>Channel 1:</b> {channel}\n"
            "👉 <b>Channel 2:</b> <a href='{ch2_url}'>VIP Private Channel</a>\n\n"
            "After joining both channels, click the verify button below."
        ),
        "id": (
            "⛔ <b>Akses Ditolak!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ Untuk menggunakan alat dan fitur bot ini, Anda wajib bergabung di <b>kedua saluran</b>:\n\n"
            "👉 <b>Saluran 1:</b> {channel}\n"
            "👉 <b>Saluran 2:</b> <a href='{ch2_url}'>Saluran VIP Privat</a>\n\n"
            "Setelah bergabung di keduanya, klik tombol verifikasi di bawah."
        ),
    },
    "verify_not_joined_alert": {
        "bn": "❌ আপনি এখনো উভয় চ্যানেলে জয়েন করেননি! আগে দুটি চ্যানেলেই জয়েন করে আবার চেষ্টা করুন।",
        "en": "❌ You haven't joined both channels yet! Please join both channels first and try again.",
        "id": "❌ Anda belum bergabung di kedua saluran! Silakan gabung keduanya terlebih dahulu lalu coba lagi.",
    },
    "verify_need_join_short": {
        "bn": "⚠️ আগে উভয় চ্যানেলে জয়েন করুন!",
        "en": "⚠️ Please join both channels first!",
        "id": "⚠️ Silakan gabung kedua saluran terlebih dahulu!",
    },
    "verify_success_alert": {
        "bn": "✅ উভয় চ্যানেলে জয়েন ভেরিফিকেশন সফল হয়েছে!",
        "en": "✅ Channel verification successful!",
        "id": "✅ Verifikasi saluran berhasil!",
    },
    "verify_success_msg": {
        "bn": "✅ <b>ভেরিফিকেশন সফল হয়েছে!</b>\nনিচের মেনু থেকে যেকোনো টুলস ব্যবহার করুন 👇",
        "en": "✅ <b>Verification Successful!</b>\nSelect any tool from the menu below 👇",
        "id": "✅ <b>Verifikasi Berhasil!</b>\nPilih alat apa saja dari menu di bawah 👇",
    },

    # --- Welcome & Help & Language ---
    "welcome": {
        "bn": (
            "👋 <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 𝐔𝐓𝐈𝐋𝐈𝐓𝐘 𝐁𝐎𝐓!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "🌐 আমাদের বটটি একটি <b>100% Free Public Utility & Video Downloader Bot</b>।\n"
            "কোনো লিমিট বা চার্জ ছাড়াই সকল টুলস এবং ডাউনলোডার আনলিমিটেড ব্যবহার করুন!\n\n"
            "⚡ <b>অটো ভিডিও ডাউনলোডার:</b>\n"
            "সরাসরি চ্যাটে <b>TikTok, Facebook বা Instagram</b> লিংক পাঠালেই বট অটোমেটিক ভিডিও ও টাইটেলসহ ডাউনলোড করে দেবে!\n\n"
            "✨ <b>জনপ্রিয় ফিচারসমূহ:</b>\n"
            "• 🎬 Auto Video Downloader (TikTok, Facebook, Instagram)\n"
            "• 🌐 ৩টি ভাষা সাপোর্ট (বাংলা, English, Indonesia)\n"
            "• 🖼️ Image to Direct Link (ImgBB Hosting)\n"
            "• 📺 Live TV Streaming Hub\n"
            "• 🔐 Encode & Decode Suite (Base64, URL, Hex, Binary)\n"
            "• 🛡️ Real-time Link & Phishing Checker\n"
            "• 📞 Phone Number to Information Lookup\n\n"
            "⚠️ <b>জরুরী নোটিশ:</b> বটটি সম্পূর্ণ বৈধ ও গঠনমূলক কাজে ব্যবহার করুন।\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
        "en": (
            "👋 <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 𝐔𝐓𝐈𝐋𝐈𝐓𝐘 𝐁𝐎𝐓!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "🌐 This bot is a <b>100% Free Public Utility & Video Downloader Bot</b>.\n"
            "Use all tools and downloaders unlimited with zero limits or charges!\n\n"
            "⚡ <b>Auto Video Downloader:</b>\n"
            "Simply send any <b>TikTok, Facebook, or Instagram</b> link directly in chat and the bot will automatically download the video with its title!\n\n"
            "✨ <b>Popular Features:</b>\n"
            "• 🎬 Auto Video Downloader (TikTok, Facebook, Instagram)\n"
            "• 🌐 3 Languages Supported (Bangla, English, Indonesia)\n"
            "• 🖼️ Image to Direct Link (ImgBB Hosting)\n"
            "• 📺 Live TV Streaming Hub\n"
            "• 🔐 Encode & Decode Suite (Base64, URL, Hex, Binary)\n"
            "• 🛡️ Real-time Link & Phishing Checker\n"
            "• 📞 Phone Number to Information Lookup\n\n"
            "⚠️ <b>Notice:</b> Please use this bot strictly for legal and constructive purposes.\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
        "id": (
            "👋 <b>𝐒𝐄𝐋𝐀𝐌𝐀𝐓 𝐃𝐀𝐓𝐀𝐍𝐆 𝐃𝐈 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 𝐔𝐓𝐈𝐋𝐈𝐓𝐘 𝐁𝐎𝐓!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "🌐 Bot ini adalah <b>Bot Utilitas & Pengunduh Video 100% Gratis</b>.\n"
            "Gunakan semua alat dan pengunduh tanpa batas dan tanpa biaya!\n\n"
            "⚡ <b>Pengunduh Video Otomatis:</b>\n"
            "Cukup kirim tautan <b>TikTok, Facebook, atau Instagram</b> langsung di chat dan bot akan otomatis mengunduh video beserta judulnya!\n\n"
            "✨ <b>Fitur Populer:</b>\n"
            "• 🎬 Pengunduh Video Otomatis (TikTok, Facebook, Instagram)\n"
            "• 🌐 Mendukung 3 Bahasa (Bangla, English, Indonesia)\n"
            "• 🖼️ Gambar ke Tautan Langsung (Hosting ImgBB)\n"
            "• 📺 Hub Streaming TV Langsung\n"
            "• 🔐 Suite Enkode & Dekode (Base64, URL, Hex, Biner)\n"
            "• 🛡️ Pemeriksa Keamanan & Phishing Tautan\n"
            "• 📞 Pencarian Informasi Nomor Telepon\n\n"
            "⚠️ <b>Pemberitahuan:</b> Gunakan bot ini hanya untuk tujuan yang legal dan bermanfaat.\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
    },
    "help_text": {
        "bn": (
            "🛡️ <b>𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 — 𝐂𝐲𝐛𝐞𝐫 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 & 𝐔𝐭𝐢𝐥𝐢𝐭𝐲 𝐒𝐮𝐢𝐭𝐞</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "<b>ফ্রি টুলসসমূহ:</b>\n"
            "• 📥 অটো ভিডিও ডাউনলোডার (TikTok, Facebook, Instagram — টাইটেলসহ)\n"
            "• 🌐 ভাষা পরিবর্তন (বাংলা / English / Indonesia)\n"
            "• 🖼️ Image to Link (ImgBB Direct Hosting)\n"
            "• 📺 Live TV Streaming Player\n"
            "• 📂 File Sharing & Cloud Link Generator\n"
            "• 🖼️ YouTube Thumbnail ও Title/Tags Extractor\n"
            "• 🎵 TikTok Video ও Title Extractor (No Watermark)\n"
            "• 📞 Phone Number Info ও IP Location Tracker\n"
            "• 💫 Direct WhatsApp Chat Opener\n"
            "• 🔳 QR Code Generator ও CC/BIN Generator\n"
            "• 🔐 Encode/Decode ও Link Security Checker\n"
            "• 🆔 BD NID ও Aadhaar Resources\n\n"
            "<b>বট কমান্ড:</b>\n"
            "/start - বট চালু বা রিস্টার্ট করুন\n"
            "/lang - ভাষা পরিবর্তন করুন\n"
            "/help - এই সাহায্য মেনু দেখুন\n"
            "/ad - এডমিন প্যানেল (শুধুমাত্র এডমিন)\n\n"
            "<b>চ্যানেল শর্ত:</b>\n"
            "আমাদের অফিসিয়াল চ্যানেলে (@mrghost_121) যুক্ত থাকতে হবে।"
        ),
        "en": (
            "🛡️ <b>𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 — 𝐂𝐲𝐛𝐞𝐫 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 & 𝐔𝐭𝐢𝐥𝐢𝐭𝐲 𝐒𝐮𝐢𝐭𝐞</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "<b>Available Free Tools:</b>\n"
            "• 📥 Auto Video Downloader (TikTok, Facebook, Instagram — with Title)\n"
            "• 🌐 Language Switcher (Bangla / English / Indonesia)\n"
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
            "/lang - Change bot language\n"
            "/help - View this help menu\n"
            "/ad - Admin Control Panel (Admins Only)\n\n"
            "<b>Channel Requirement:</b>\n"
            "You must stay joined to our official channel (@mrghost_121)."
        ),
        "id": (
            "🛡️ <b>𝐌𝐑 𝐆𝐇𝐎𝐒𝐓 — 𝐂𝐲𝐛𝐞𝐫 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 & 𝐔𝐭𝐢𝐥𝐢𝐭𝐲 𝐒𝐮𝐢𝐭𝐞</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "<b>Alat Gratis yang Tersedia:</b>\n"
            "• 📥 Pengunduh Video Otomatis (TikTok, Facebook, Instagram — dengan Judul)\n"
            "• 🌐 Pengubah Bahasa (Bangla / English / Indonesia)\n"
            "• 🖼️ Gambar ke Link (Hosting Langsung ImgBB)\n"
            "• 📺 Pemutar Streaming TV Langsung\n"
            "• 📂 Berbagi File & Pembuat Tautan Cloud\n"
            "• 🖼️ Pengunduh Thumbnail & Ekstraktor Judul/Tag YouTube\n"
            "• 🎵 Pengunduh Video & Judul TikTok (Tanpa Watermark)\n"
            "• 📞 Info Nomor Telepon & Pelacak Lokasi IP\n"
            "• 💫 Pembuka Chat WhatsApp Langsung\n"
            "• 🔳 Pembuat Kode QR & Generator CC/BIN\n"
            "• 🔐 Enkode/Dekode & Pemeriksa Keamanan Tautan\n"
            "• 🆔 Alat BD NID & Aadhaar\n\n"
            "<b>Perintah Bot:</b>\n"
            "/start - Mulai atau mulai ulang bot\n"
            "/lang - Ubah bahasa bot\n"
            "/help - Lihat menu bantuan ini\n"
            "/ad - Panel Kontrol Admin (Khusus Admin)\n\n"
            "<b>Syarat Saluran:</b>\n"
            "Anda harus bergabung dengan saluran resmi kami (@mrghost_121)."
        ),
    },
    "help_btn_channel": {
        "bn": "📢 চ্যানেলে জয়েন করুন",
        "en": "📢 Join Channel",
        "id": "📢 Gabung Saluran",
    },
    "help_btn_support": {
        "bn": "💬 সাপোর্ট যোগাযোগ",
        "en": "💬 Contact Support",
        "id": "💬 Hubungi Dukungan",
    },
    "lang_prompt": {
        "bn": (
            "🌐 <b>ভাষা নির্বাচন করুন / Select Language / Pilih Bahasa</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "নিচের কিবোর্ড থেকে আপনার পছন্দের ভাষা সিলেক্ট করুন। পুরো বটটি সেই ভাষায় পরিবর্তন হয়ে যাবে 👇"
        ),
        "en": (
            "🌐 <b>Select Language / ভাষা নির্বাচন করুন / Pilih Bahasa</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "Choose your preferred language from the keyboard below. The entire bot will switch to that language 👇"
        ),
        "id": (
            "🌐 <b>Pilih Bahasa / Select Language / ভাষা নির্বাচন করুন</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "Pilih bahasa pilihan Anda dari keyboard di bawah. Seluruh bot akan berubah ke bahasa tersebut 👇"
        ),
    },
    "lang_changed": {
        "bn": "✅ <b>ভাষা পরিবর্তন সম্পন্ন!</b>\nএখন থেকে সম্পূর্ণ বটটি <b>বাংলা</b> ভাষায় চলবে।",
        "en": "✅ <b>Language Updated!</b>\nThe entire bot is now set to <b>English</b>.",
        "id": "✅ <b>Bahasa Diperbarui!</b>\nSeluruh bot sekarang menggunakan <b>Bahasa Indonesia</b>.",
    },

    # --- File Sharing ---
    "fs_panel": {
        "bn": (
            "📂 <b>𝐅𝐈𝐋𝐄 𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐒𝐘𝐒𝐓𝐄𝐌 — 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ এখানে আপনি যেকোনো Document, Photo বা Video আপলোড করে শেয়ার লিংক বানাতে পারবেন (১০০% ফ্রি)।\n\n"
            "👇 নিচের বাটন থেকে নির্বাচন করুন অথবা সরাসরি ফাইল পাঠান:"
        ),
        "en": (
            "📂 <b>𝐅𝐈𝐋𝐄 𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐒𝐘𝐒𝐓𝐄𝐌 — 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Upload any Document, Photo, or Video here to generate a shareable link (100% Free).\n\n"
            "👇 Select an option below or send a file directly:"
        ),
        "id": (
            "📂 <b>𝐒𝐈𝐒𝐓𝐄𝐌 𝐁𝐄𝐑𝐁𝐀𝐆𝐈 𝐅𝐈𝐋𝐄 — 𝐌𝐑 𝐆𝐇𝐎𝐒𝐓</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Unggah Dokumen, Foto, atau Video apa saja di sini untuk membuat tautan berbagi (100% Gratis).\n\n"
            "👇 Pilih opsi di bawah atau kirim file langsung:"
        ),
    },
    "fs_ask_upload": {
        "bn": "📤 <b>যেকোনো ফাইল পাঠান:</b>\n\nআপনি Document, Video বা Photo পাঠাতে পারেন। বট স্বয়ংক্রিয়ভাবে একটি ইউনিক শেয়ার লিংক বানিয়ে দেবে।",
        "en": "📤 <b>Send Any File:</b>\n\nYou can send a Document, Video, or Photo. The bot will automatically generate a unique share link.",
        "id": "📤 <b>Kirim File Apa Saja:</b>\n\nAnda dapat mengirim Dokumen, Video, atau Foto. Bot akan otomatis membuat tautan berbagi unik.",
    },
    "fs_uploaded": {
        "bn": (
            "✅ <b>ফাইল সফলভাবে আপলোড হয়েছে!</b>\n\n"
            "📁 <b>নাম:</b> <code>{fname}</code>\n"
            "📂 <b>File Code:</b> <code>{code}</code>\n\n"
            "🔗 <b>শেয়ার লিংক:</b>\n{link}\n\n"
            "<i>এই লিংকে ক্লিক করলে চ্যানেলে জয়েন ভেরিফাই করে যে কেউ ফাইলটি পেয়ে যাবে।</i>"
        ),
        "en": (
            "✅ <b>File Uploaded Successfully!</b>\n\n"
            "📁 <b>Name:</b> <code>{fname}</code>\n"
            "📂 <b>File Code:</b> <code>{code}</code>\n\n"
            "🔗 <b>Share Link:</b>\n{link}\n\n"
            "<i>Anyone clicking this link can access the file after verifying channel membership.</i>"
        ),
        "id": (
            "✅ <b>File Berhasil Diunggah!</b>\n\n"
            "📁 <b>Nama:</b> <code>{fname}</code>\n"
            "📂 <b>Kode File:</b> <code>{code}</code>\n\n"
            "🔗 <b>Tautan Berbagi:</b>\n{link}\n\n"
            "<i>Siapa pun yang mengklik tautan ini akan menerima file setelah memverifikasi keanggotaan saluran.</i>"
        ),
    },
    "fs_btn_upload_more": {
        "bn": "📤 আরও আপলোড করুন",
        "en": "📤 Upload More",
        "id": "📤 Unggah Lagi",
    },
    "fs_btn_main_menu": {
        "bn": "🏠 মেইন মেনু",
        "en": "🏠 Main Menu",
        "id": "🏠 Menu Utama",
    },
    "fs_not_found": {
        "bn": "❌ <b>ফাইল পাওয়া যায়নি!</b>\nফাইলটি মুছে ফেলা হয়েছে অথবা লিংকটি মেয়াদোত্তীর্ণ।",
        "en": "❌ <b>File Not Found!</b>\nThe file has been deleted or the link has expired.",
        "id": "❌ <b>File Tidak Ditemukan!</b>\nFile telah dihapus atau tautan sudah kedaluwarsa.",
    },
    "fs_sending": {
        "bn": "⏳ <b>আপনার ফাইল পাঠানো হচ্ছে...</b>",
        "en": "⏳ <b>Sending your file...</b>",
        "id": "⏳ <b>Mengirim file Anda...</b>",
    },
    "fs_notice_5min": {
        "bn": (
            "⚠️ <b>জরুরী নোটিশ:</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "কপিরাইট ও নিরাপত্তার স্বার্থে এই ফাইলটি <b>৫ মিনিট (5 mins)</b> পর আপনার ইনবক্স থেকে স্বয়ংক্রিয়ভাবে মুছে যাবে।\n\n"
            "📌 <i>প্রয়োজনে ফাইলটি এখনই আপনার 'Saved Messages'-এ ফরোয়ার্ড করে রাখুন অথবা ফোনে সেভ করুন।</i>\n"
            "🔄 <i>(লিংকটি পার্মানেন্ট থাকবে; পরবর্তীতে যেকোনো সময় লিংকে ক্লিক করলেই আবার ফাইলটি পাবেন।)</i>"
        ),
        "en": (
            "⚠️ <b>Important Notice:</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "For copyright & security reasons, this file will be automatically deleted from your inbox after <b>5 minutes</b>.\n\n"
            "📌 <i>Forward this file to your 'Saved Messages' or save it to your device now if needed.</i>\n"
            "🔄 <i>(The share link remains permanent; you can click the link again anytime to receive the file again.)</i>"
        ),
        "id": (
            "⚠️ <b>Pemberitahuan Penting:</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "Demi hak cipta & keamanan, file ini akan otomatis terhapus dari kotak masuk Anda setelah <b>5 menit</b>.\n\n"
            "📌 <i>Teruskan file ini ke 'Saved Messages' atau simpan ke perangkat Anda sekarang jika perlu.</i>\n"
            "🔄 <i>(Tautan berbagi bersifat permanen; klik tautan lagi kapan saja untuk mendapatkan file kembali.)</i>"
        ),
    },
    "fs_deleted_5min": {
        "bn": "⏳ <b>সময় সমাপ্ত!</b>\n৫ মিনিট পূর্ণ হওয়ায় পূর্বের ফাইলটি ইনবক্স থেকে মুছে দেওয়া হয়েছে। পুনরায় ফাইলটি পেতে মূল শেয়ার লিংকে ক্লিক করুন।",
        "en": "⏳ <b>Time's Up!</b>\n5 minutes have passed, so the file has been removed from your inbox. Click the original share link to get it again.",
        "id": "⏳ <b>Waktu Habis!</b>\nSetelah 5 menit, file sebelumnya telah dihapus dari kotak masuk. Klik tautan berbagi asli untuk mendapatkannya kembali.",
    },
    "fs_send_error": {
        "bn": "❌ ফাইল পাঠাতে সমস্যা হয়েছে: {err}",
        "en": "❌ Failed to send file: {err}",
        "id": "❌ Gagal mengirim file: {err}",
    },

    # --- Stats ---
    "stats_msg": {
        "bn": (
            "📊 <b>𝐔𝐒𝐄𝐑 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>ব্যবহারকারীর তথ্য:</b>\n"
            "• নাম: <b>{name}</b>\n"
            "• আইডি: <code>{uid}</code>\n"
            "• ইউজারনেম: @{uname}\n\n"
            "📈 <b>অ্যাক্টিভিটি ও স্ট্যাটাস:</b>\n"
            "• সাবস্ক্রিপশন: <b>Free Lifetime Access ⚡</b>\n"
            "• আপনার আপলোডকৃত ফাইল: <b>{uploads}</b> টি\n"
            "• আপনার কয়েন ব্যালেন্স: <b>{coins} Coins 💰</b>\n"
            "• ক্লাউড স্টোরেজ: <b>Unlimited Storage</b>\n\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
        "en": (
            "📊 <b>𝐔𝐒𝐄𝐑 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>User Info:</b>\n"
            "• Name: <b>{name}</b>\n"
            "• ID: <code>{uid}</code>\n"
            "• Username: @{uname}\n\n"
            "📈 <b>Activity & Status:</b>\n"
            "• Subscription: <b>Free Lifetime Access ⚡</b>\n"
            "• Your Uploaded Files: <b>{uploads}</b>\n"
            "• Your Coin Balance: <b>{coins} Coins 💰</b>\n"
            "• Cloud Storage: <b>Unlimited Storage</b>\n\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
        "id": (
            "📊 <b>𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐊 𝐀𝐊𝐔𝐍 𝐏𝐄𝐍𝐆𝐆𝐔𝐍𝐀</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>Info Pengguna:</b>\n"
            "• Nama: <b>{name}</b>\n"
            "• ID: <code>{uid}</code>\n"
            "• Username: @{uname}\n\n"
            "📈 <b>Aktivitas & Status:</b>\n"
            "• Langganan: <b>Akses Gratis Seumur Hidup ⚡</b>\n"
            "• File Diunggah: <b>{uploads}</b>\n"
            "• Saldo Koin Anda: <b>{coins} Koin 💰</b>\n"
            "• Penyimpanan Cloud: <b>Tanpa Batas</b>\n\n"
            "👨‍💻 <b>Powered by Mr Ghost</b> (@mrghost_121)"
        ),
    },
    "btn_join_main_ch": {
        "bn": "📢 মেইন চ্যানেলে জয়েন করুন",
        "en": "📢 Join Main Channel",
        "id": "📢 Gabung Saluran Utama",
    },
    "btn_join_vip_ch": {
        "bn": "📢 VIP চ্যানেল ২ জয়েন করুন",
        "en": "📢 Join VIP Channel 2",
        "id": "📢 Gabung Saluran VIP 2",
    },
    "btn_upload_new_file": {
        "bn": "📤 নতুন ফাইল আপলোড করুন",
        "en": "📤 Upload New File",
        "id": "📤 Unggah File Baru",
    },

    # --- Video Downloaders (TikTok, FB, Insta) ---
    "ask_fb_url": {
        "bn": "📹 <b>Facebook Video & Reels Downloader</b>\n\nআপনার ফেসবুক ভিডিও বা রিলস (Reels) লিংকটি পাঠান 👇",
        "en": "📹 <b>Facebook Video & Reels Downloader</b>\n\nSend your Facebook video or Reels link below 👇",
        "id": "📹 <b>Pengunduh Video & Reels Facebook</b>\n\nKirim tautan video atau Reels Facebook Anda di bawah 👇",
    },
    "ask_tiktok_url": {
        "bn": "🎵 <b>TikTok Video Downloader (No Watermark)</b>\n\nসরাসরি চ্যাটে আপনার কাঙ্ক্ষিত TikTok ভিডিওর লিংক পাঠান 👇",
        "en": "🎵 <b>TikTok Video Downloader (No Watermark)</b>\n\nSend your TikTok video link directly in chat 👇",
        "id": "🎵 <b>Pengunduh Video TikTok (Tanpa Watermark)</b>\n\nKirim tautan video TikTok langsung di chat 👇",
    },
    "ask_insta_url": {
        "bn": "📸 <b>Instagram Video & Reels Downloader</b>\n\nআপনার ইনস্টাগ্রাম রিলস, ভিডিও বা পোস্টের লিংক পাঠান 👇",
        "en": "📸 <b>Instagram Video & Reels Downloader</b>\n\nSend your Instagram Reels, video, or post link below 👇",
        "id": "📸 <b>Pengunduh Video & Reels Instagram</b>\n\nKirim tautan Reels, video, atau postingan Instagram di bawah 👇",
    },
    "dl_processing_tiktok": {
        "bn": "⏳ <b>TikTok ভিডিও সংগ্রহ ও প্রসেস করা হচ্ছে...</b>",
        "en": "⏳ <b>Fetching and processing TikTok video...</b>",
        "id": "⏳ <b>Mengambil dan memproses video TikTok...</b>",
    },
    "dl_processing_insta": {
        "bn": "⏳ <b>Instagram রিলস/পোস্ট সংগ্রহ ও প্রসেস করা হচ্ছে...</b>",
        "en": "⏳ <b>Fetching and processing Instagram Reels/video...</b>",
        "id": "⏳ <b>Mengambil dan memproses Reels/video Instagram...</b>",
    },
    "dl_processing_video": {
        "bn": "⏳ <b>ভিডিও সংগ্রহ ও প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...</b>",
        "en": "⏳ <b>Fetching and processing video, please wait...</b>",
        "id": "⏳ <b>Mengambil dan memproses video, harap tunggu...</b>",
    },
    "dl_caption_tiktok": {
        "bn": (
            "🎵 <b>𝐓𝐈𝐊𝐓𝐎𝐊 𝐕𝐈𝐃𝐄𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>টাইটেল (Title):</b>\n<code>{title}</code>\n\n"
            "👤 <b>নির্মাতা (Author):</b> <code>{author}</code>\n"
        ),
        "en": (
            "🎵 <b>𝐓𝐈𝐊𝐓𝐎𝐊 𝐕𝐈𝐃𝐄𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>Title:</b>\n<code>{title}</code>\n\n"
            "👤 <b>Author:</b> <code>{author}</code>\n"
        ),
        "id": (
            "🎵 <b>𝐕𝐈𝐃𝐄𝐎 𝐓𝐈𝐊𝐓𝐎𝐊 𝐃𝐈𝐔𝐍𝐃𝐔𝐇</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>Judul:</b>\n<code>{title}</code>\n\n"
            "👤 <b>Pembuat:</b> <code>{author}</code>\n"
        ),
    },
    "dl_caption_music_line": {
        "bn": "🎶 <b>মিউজিক:</b> <code>{music}</code>\n\n",
        "en": "🎶 <b>Music:</b> <code>{music}</code>\n\n",
        "id": "🎶 <b>Musik:</b> <code>{music}</code>\n\n",
    },
    "dl_caption_tiktok_footer": {
        "bn": "⚡ <i>ওয়াটারমার্ক ছাড়া HD কোয়ালিটি</i>\n👨‍💻 Powered by <a href=\"https://t.me/mrghost_121\">Mr Ghost</a>",
        "en": "⚡ <i>Downloaded without Watermark in HD</i>\n👨‍💻 Powered by <a href=\"https://t.me/mrghost_121\">Mr Ghost</a>",
        "id": "⚡ <i>Diunduh tanpa Watermark dalam HD</i>\n👨‍💻 Powered by <a href=\"https://t.me/mrghost_121\">Mr Ghost</a>",
    },
    "dl_caption_insta": {
        "bn": (
            "📸 <b>𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>ভিডিও টাইটেল (Title):</b>\n<code>{title}</code>\n\n"
            "✅ <i>HD Quality Video / Photo</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "en": (
            "📸 <b>𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐃</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>Video Title:</b>\n<code>{title}</code>\n\n"
            "✅ <i>HD Quality Video / Photo</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "id": (
            "📸 <b>𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 𝐃𝐈𝐔𝐍𝐃𝐔𝐇</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎬 <b>Judul Video:</b>\n<code>{title}</code>\n\n"
            "✅ <i>Video / Foto Kualitas HD</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
    },
    "dl_caption_universal": {
        "bn": (
            "✅ <b>ভিডিও ডাউনলোড সফল হয়েছে!</b>\n\n"
            "🎬 <b>ভিডিও টাইটেল (ক্লিক করলে কপি হবে):</b>\n"
            "<code>{title}</code>\n\n"
            '⚡ Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "en": (
            "✅ <b>Video Downloaded Successfully!</b>\n\n"
            "🎬 <b>Video Title (Tap to Copy):</b>\n"
            "<code>{title}</code>\n\n"
            '⚡ Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "id": (
            "✅ <b>Video Berhasil Diunduh!</b>\n\n"
            "🎬 <b>Judul Video (Ketuk untuk Salin):</b>\n"
            "<code>{title}</code>\n\n"
            '⚡ Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
    },
    "dl_too_large": {
        "bn": "❌ <b>ভিডিও সাইজ ৫০MB-এর বেশি!</b>\nটেলিগ্রাম বটের সীমাবদ্ধতার কারণে ৫০MB-এর বেশি ফাইল সরাসরি পাঠানো সম্ভব নয়।",
        "en": "❌ <b>Video size exceeds 50MB!</b>\nDue to Telegram bot limits, files larger than 50MB cannot be sent directly.",
        "id": "❌ <b>Ukuran video melebihi 50MB!</b>\nKarena batasan bot Telegram, file di atas 50MB tidak dapat dikirim langsung.",
    },
    "dl_failed": {
        "bn": "⚠️ <b>ভিডিওটি ডাউনলোড করা সম্ভব হয়নি।</b>\n\nঅনুগ্রহ করে লিংকটি সঠিক ও পাবলিক কিনা যাচাই করুন অথবা অন্য একটি ভিডিও লিংক দিয়ে চেষ্টা করুন।",
        "en": "⚠️ <b>Could not download the video.</b>\n\nPlease make sure the link is valid and public, or try another video link.",
        "id": "⚠️ <b>Video gagal diunduh.</b>\n\nPastikan tautan valid dan bersifat publik, atau coba tautan video lainnya.",
    },
    "dl_unsupported_removed": {
        "bn": "⚠️ <b>YouTube ও Pinterest ভিডিও ডাউনলোডার রিমুভ করা হয়েছে।</b>\nদয়া করে শুধুমাত্র <b>TikTok, Facebook বা Instagram</b> লিংক পাঠান!",
        "en": "⚠️ <b>YouTube & Pinterest video downloaders have been removed.</b>\nPlease send only <b>TikTok, Facebook, or Instagram</b> links!",
        "id": "⚠️ <b>Pengunduh video YouTube & Pinterest telah dihapus.</b>\nSilakan kirim hanya tautan <b>TikTok, Facebook, atau Instagram</b>!",
    },

    # --- Thumbnail Downloader & YT/TikTok Extractors ---
    "ask_yt_thumb": {
        "bn": "🖼️ <b>YouTube Thumbnail Downloader</b>\n\nদয়া করে আপনার কাঙ্ক্ষিত ইউটিউব ভিডিওর লিংকটি এখানে পাঠান:\n<i>উদাহরণ: https://youtu.be/xxxxxx</i>",
        "en": "🖼️ <b>YouTube Thumbnail Downloader</b>\n\nPlease send the YouTube video link below:\n<i>Example: https://youtu.be/xxxxxx</i>",
        "id": "🖼️ <b>Pengunduh Thumbnail YouTube</b>\n\nSilakan kirim tautan video YouTube di bawah:\n<i>Contoh: https://youtu.be/xxxxxx</i>",
    },
    "yt_thumb_caption": {
        "bn": "🎯 <b>আপনার ইউটিউব ভিডিওর থাম্বনেইল!</b>\n🔥 <i>Quality: Ultra HD (Max Resolution)</i>",
        "en": "🎯 <b>Your YouTube Video Thumbnail!</b>\n🔥 <i>Quality: Ultra HD (Max Resolution)</i>",
        "id": "🎯 <b>Thumbnail Video YouTube Anda!</b>\n🔥 <i>Kualitas: Ultra HD (Resolusi Maksimal)</i>",
    },
    "yt_thumb_invalid": {
        "bn": "❌ এটি সঠিক ইউটিউব লিংক নয়! দয়া করে সঠিক লিংক পাঠান।",
        "en": "❌ This is not a valid YouTube link! Please send a valid link.",
        "id": "❌ Ini bukan tautan YouTube yang valid! Silakan kirim tautan yang benar.",
    },
    "ask_yt_extract": {
        "bn": "🎥 <b>YouTube Data Extractor</b>\n\nযে ভিডিওর Title, Description ও Tags চান, তার লিংকটি পাঠান 👇",
        "en": "🎥 <b>YouTube Data Extractor</b>\n\nSend the video link to extract its Title, Description & Tags 👇",
        "id": "🎥 <b>Ekstraktor Data YouTube</b>\n\nKirim tautan video untuk mengambil Judul, Deskripsi & Tag 👇",
    },
    "yt_extracting": {
        "bn": "⏳ <b>ইউটিউব থেকে ডাটা সংগ্রহ করা হচ্ছে...</b>",
        "en": "⏳ <b>Extracting Data from YouTube...</b>",
        "id": "⏳ <b>Mengambil data dari YouTube...</b>",
    },
    "yt_extract_result": {
        "bn": (
            "🎯 <b>YouTube ডাটা সফলভাবে পাওয়া গেছে!</b>\n\n"
            "📌 <b>Title:</b>\n<code>{title}</code>\n\n"
            "📝 <b>Description:</b>\n<pre>{desc}</pre>\n\n"
            "🏷️ <b>Tags / Keywords:</b>\n<code>{tags}</code>"
        ),
        "en": (
            "🎯 <b>YouTube Data Extracted Successfully!</b>\n\n"
            "📌 <b>Title:</b>\n<code>{title}</code>\n\n"
            "📝 <b>Description:</b>\n<pre>{desc}</pre>\n\n"
            "🏷️ <b>Tags / Keywords:</b>\n<code>{tags}</code>"
        ),
        "id": (
            "🎯 <b>Data YouTube Berhasil Diekstrak!</b>\n\n"
            "📌 <b>Judul:</b>\n<code>{title}</code>\n\n"
            "📝 <b>Deskripsi:</b>\n<pre>{desc}</pre>\n\n"
            "🏷️ <b>Tag / Kata Kunci:</b>\n<code>{tags}</code>"
        ),
    },
    "yt_extract_failed": {
        "bn": "❌ এই লিংক থেকে ডাটা বের করা যায়নি! সঠিক ইউটিউব লিংক দিন।",
        "en": "❌ Could not extract data from this link! Please provide a valid YouTube link.",
        "id": "❌ Tidak dapat mengekstrak data dari tautan ini! Berikan tautan YouTube yang valid.",
    },
    "ask_tik_title": {
        "bn": "🎵 <b>TikTok Title Extractor</b>\n\nটিকটক ভিডিওর টাইটেল বা ক্যাপশন এক্সট্রাক্ট করতে লিংক পাঠান 👇",
        "en": "🎵 <b>TikTok Title Extractor</b>\n\nSend a TikTok video link to extract its title/caption 👇",
        "id": "🎵 <b>Ekstraktor Judul TikTok</b>\n\nKirim tautan video TikTok untuk mengekstrak judul/caption 👇",
    },
    "tik_title_loading": {
        "bn": "⏳ <b>TikTok টাইটেল সংগ্রহ করা হচ্ছে...</b>",
        "en": "⏳ <b>Extracting TikTok Title...</b>",
        "id": "⏳ <b>Mengekstrak Judul TikTok...</b>",
    },
    "tik_title_success": {
        "bn": "🎵 <b>TikTok ভিডিও টাইটেল পাওয়া গেছে!</b>\n\n📝 <b>Title:</b>\n<code>{title}</code>",
        "en": "🎵 <b>TikTok Video Title Extracted Successfully!</b>\n\n📝 <b>Title:</b>\n<code>{title}</code>",
        "id": "🎵 <b>Judul Video TikTok Berhasil Diekstrak!</b>\n\n📝 <b>Judul:</b>\n<code>{title}</code>",
    },
    "tik_title_fail": {
        "bn": "❌ TikTok ভিডিওর ডাটা পাওয়া যায়নি!",
        "en": "❌ Failed to fetch TikTok video data!",
        "id": "❌ Gagal mengambil data video TikTok!",
    },
    "server_no_resp": {
        "bn": "❌ সার্ভার রেসপন্স করছে না, কিছুক্ষণ পর চেষ্টা করুন।",
        "en": "❌ Server is not responding, please try again later.",
        "id": "❌ Server tidak merespons, silakan coba lagi nanti.",
    },

    # --- Image to Link ---
    "ask_imgbb": {
        "bn": (
            "🖼️ <b>𝐈𝐌𝐀𝐆𝐄 𝐓𝐎 𝐔𝐑𝐋 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 (𝐈𝐦𝐠𝐁𝐁)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📸 <b>আপনার ছবিটি এখানে পাঠান (Photo হিসেবে):</b>\n\n"
            "⚡ বট সরাসরি ImgBB সার্ভারে আপলোড করে আপনাকে পার্মানেন্ট <b>Direct Image Link</b> বানিয়ে দেবে।\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "en": (
            "🖼️ <b>𝐈𝐌𝐀𝐆𝐄 𝐓𝐎 𝐔𝐑𝐋 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 (𝐈𝐦𝐠𝐁𝐁)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📸 <b>Send your image here (as a Photo):</b>\n\n"
            "⚡ The bot will upload it directly to ImgBB and give you a permanent <b>Direct Image Link</b>.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "id": (
            "🖼️ <b>𝐇𝐎𝐒𝐓𝐈𝐍𝐆 𝐆𝐀𝐌𝐁𝐀𝐑 𝐊𝐄 𝐔𝐑𝐋 (𝐈𝐦𝐠𝐁𝐁)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📸 <b>Kirim gambar Anda di sini (sebagai Foto):</b>\n\n"
            "⚡ Bot akan langsung mengunggah ke ImgBB dan memberikan <b>Tautan Gambar Langsung</b> permanen.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
    },
    "imgbb_uploading": {
        "bn": "⏳ <b>ImgBB সার্ভারে ছবি আপলোড করা হচ্ছে...</b>",
        "en": "⏳ <b>Uploading image to ImgBB server...</b>",
        "id": "⏳ <b>Mengunggah gambar ke server ImgBB...</b>",
    },
    "imgbb_success": {
        "bn": (
            "✅ <b>𝐈𝐌𝐀𝐆𝐄 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔗 <b>Direct Link (ক্লিক করলেই কপি হবে):</b>\n"
            "<code>{direct_url}</code>\n\n"
            "👁️ <b>Viewer URL:</b>\n"
            "<code>{display_url}</code>\n\n"
            "📦 <b>File Size:</b> {size_kb} KB\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ <i>Hosted permanently on ImgBB</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "en": (
            "✅ <b>𝐈𝐌𝐀𝐆𝐄 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔗 <b>Direct Link (Tap to Copy):</b>\n"
            "<code>{direct_url}</code>\n\n"
            "👁️ <b>Viewer URL:</b>\n"
            "<code>{display_url}</code>\n\n"
            "📦 <b>File Size:</b> {size_kb} KB\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ <i>Hosted permanently on ImgBB</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
        "id": (
            "✅ <b>𝐆𝐀𝐌𝐁𝐀𝐑 𝐁𝐄𝐑𝐇𝐀𝐒𝐈𝐋 𝐃𝐈𝐔𝐍𝐆𝐆𝐀𝐇!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔗 <b>Tautan Langsung (Ketuk untuk Salin):</b>\n"
            "<code>{direct_url}</code>\n\n"
            "👁️ <b>URL Penampil:</b>\n"
            "<code>{display_url}</code>\n\n"
            "📦 <b>Ukuran File:</b> {size_kb} KB\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ <i>Dihosting permanen di ImgBB</i>\n"
            '👨‍💻 Powered by <a href="https://t.me/mrghost_121">Mr Ghost</a>'
        ),
    },
    "imgbb_btn_open": {
        "bn": "🌐 ছবিটি খুলুন",
        "en": "🌐 Open Direct Image",
        "id": "🌐 Buka Gambar Langsung",
    },
    "imgbb_fail": {
        "bn": "❌ <b>আপলোড ব্যর্থ হয়েছে:</b> {err}",
        "en": "❌ <b>Upload failed:</b> {err}",
        "id": "❌ <b>Unggahan gagal:</b> {err}",
    },
    "imgbb_err": {
        "bn": "❌ ছবি প্রসেস করতে সমস্যা হয়েছে: {err}",
        "en": "❌ Error processing image: {err}",
        "id": "❌ Terjadi kesalahan memproses gambar: {err}",
    },

    # --- Live TV ---
    "live_tv_msg": {
        "bn": (
            "📺 <b>𝐋𝐈𝐕𝐄 𝐓𝐕 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐔𝐁</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌐 <b>অনলাইন লাইভ টিভি লিংক:</b>\n"
            "👉 https://mboxofficial.vercel.app/\n\n"
            "⚠️ <b>দৃষ্টি আকর্ষণ / জরুরী নোটিশ:</b>\n"
            "এই লিংকটি অনলাইনে সরাসরি যেকোনো ব্রাউজারে ব্যবহার করা যায়, তবে অ্যাপ ছাড়া অনেকগুলো টিভি চ্যানেল কাজ নাও করতে পারে। তাই নিরবচ্ছিন্ন বিনোদনের জন্য তাদের অফিসিয়াল <b>App ব্যবহার করুন</b>।\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "en": (
            "📺 <b>𝐋𝐈𝐕𝐄 𝐓𝐕 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐔𝐁</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌐 <b>Online Live TV Link:</b>\n"
            "👉 https://mboxofficial.vercel.app/\n\n"
            "⚠️ <b>Important Notice:</b>\n"
            "This link works directly in any browser, though some channels may require their official app to stream properly. For uninterrupted entertainment, please use their official <b>App</b>.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "id": (
            "📺 <b>𝐏𝐔𝐒𝐀𝐓 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐓𝐕 𝐋𝐀𝐍𝐆𝐒𝐔𝐍𝐆</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌐 <b>Tautan TV Langsung Online:</b>\n"
            "👉 https://mboxofficial.vercel.app/\n\n"
            "⚠️ <b>Pemberitahuan Penting:</b>\n"
            "Tautan ini dapat dibuka langsung di browser apa saja, namun beberapa saluran mungkin memerlukan aplikasi resmi. Untuk hiburan tanpa gangguan, gunakan <b>Aplikasi resmi</b>.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
    },
    "live_tv_btn_open": {
        "bn": "🌐 লাইভ টিভি খুলুন",
        "en": "🌐 Open Live TV",
        "id": "🌐 Buka TV Langsung",
    },
    "live_tv_btn_ch": {
        "bn": "📢 অফিসিয়াল চ্যানেল",
        "en": "📢 Official Channel",
        "id": "📢 Saluran Resmi",
    },

    # --- Number Info ---
    "ask_num_info": {
        "bn": "📞 <b>Number to Info Feature</b>\n\nযেকোনো নাম্বারের ডিটেইলস জানতে কান্ট্রি কোডসহ নাম্বারটি লিখে পাঠান।\nযেমন: <code>+88017XXXXXXXX</code> বা <code>+14158586273</code>",
        "en": "📞 <b>Number to Info Feature</b>\n\nSend any phone number with country code to inspect details.\nExample: <code>+88017XXXXXXXX</code> or <code>+14158586273</code>",
        "id": "📞 <b>Fitur Info Nomor Telepon</b>\n\nKirim nomor telepon beserta kode negara untuk melihat detailnya.\nContoh: <code>+62812XXXXXXXX</code> atau <code>+14158586273</code>",
    },
    "num_searching": {
        "bn": "⏳ <b>তথ্য খোঁজা হচ্ছে, দয়া করে অপেক্ষা করুন...</b>",
        "en": "⏳ <b>Searching information, please wait...</b>",
        "id": "⏳ <b>Mencari informasi, harap tunggu...</b>",
    },
    "num_result": {
        "bn": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📞 <b>𝐏𝐇𝐎𝐍𝐄 𝐍𝐔𝐌𝐁𝐄𝐑 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>Owner / Name   :</b> <code>{owner}</code>\n"
            "🔹 <b>Intl. Format   :</b> <code>{intl}</code>\n"
            "🔹 <b>National Format:</b> <code>{nat}</code>\n"
            "🌍 <b>Country        :</b> <code>{country}</code>\n"
            "📡 <b>Carrier / SIM  :</b> <code>{carrier}</code>\n"
            "📱 <b>Line Type      :</b> <code>{ltype}</code>\n"
            "⏰ <b>Timezone       :</b> <code>{tz}</code>\n"
            "✅ <b>Is Valid       :</b> <code>{valid}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🕵️‍♂️ <b>সরাসরি মেসেজ করুন:</b>\n"
            "💬 <a href='{wa_link}'>Direct WhatsApp Chat</a>\n"
            "✈️ <a href='{tg_link}'>Direct Telegram Contact</a>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <i>তথ্য খোঁজা সম্পন্ন হয়েছে!</i>"
        ),
        "en": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📞 <b>𝐏𝐇𝐎𝐍𝐄 𝐍𝐔𝐌𝐁𝐄𝐑 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>Owner / Name   :</b> <code>{owner}</code>\n"
            "🔹 <b>Intl. Format   :</b> <code>{intl}</code>\n"
            "🔹 <b>National Format:</b> <code>{nat}</code>\n"
            "🌍 <b>Country        :</b> <code>{country}</code>\n"
            "📡 <b>Carrier / SIM  :</b> <code>{carrier}</code>\n"
            "📱 <b>Line Type      :</b> <code>{ltype}</code>\n"
            "⏰ <b>Timezone       :</b> <code>{tz}</code>\n"
            "✅ <b>Is Valid       :</b> <code>{valid}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🕵️‍♂️ <b>𝐃𝐈𝐑𝐄𝐂𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐈𝐍𝐆:</b>\n"
            "💬 <a href='{wa_link}'>Direct WhatsApp Chat</a>\n"
            "✈️ <a href='{tg_link}'>Direct Telegram Contact</a>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <i>Search Completed Successfully!</i>"
        ),
        "id": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📞 <b>𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐒𝐈 𝐍𝐎𝐌𝐎𝐑 𝐓𝐄𝐋𝐄𝐏𝐎𝐍</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👤 <b>Pemilik / Nama :</b> <code>{owner}</code>\n"
            "🔹 <b>Format Intl.   :</b> <code>{intl}</code>\n"
            "🔹 <b>Format Nasional:</b> <code>{nat}</code>\n"
            "🌍 <b>Negara         :</b> <code>{country}</code>\n"
            "📡 <b>Operator / SIM :</b> <code>{carrier}</code>\n"
            "📱 <b>Tipe Jalur     :</b> <code>{ltype}</code>\n"
            "⏰ <b>Zona Waktu     :</b> <code>{tz}</code>\n"
            "✅ <b>Valid          :</b> <code>{valid}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🕵️‍♂️ <b>𝐏𝐄𝐒𝐀𝐍 𝐋𝐀𝐍𝐆𝐒𝐔𝐍𝐆:</b>\n"
            "💬 <a href='{wa_link}'>Chat WhatsApp Langsung</a>\n"
            "✈️ <a href='{tg_link}'>Kontak Telegram Langsung</a>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ <i>Pencarian Selesai!</i>"
        ),
    },

    # --- QR Maker ---
    "ask_qr": {
        "bn": "🔳 <b>QR Code Maker</b>\n\nQR Code বানাতে নিচে যেকোনো Text বা Link পাঠান 👇",
        "en": "🔳 <b>QR Code Maker</b>\n\nSend any Text or Link below to generate a QR Code 👇",
        "id": "🔳 <b>Pembuat Kode QR</b>\n\nKirim Teks atau Tautan apa saja di bawah untuk membuat Kode QR 👇",
    },
    "qr_ready": {
        "bn": "✅ <b>QR Code প্রস্তুত!</b>\n\n📌 <b>Data:</b> <code>{data}</code>",
        "en": "✅ <b>QR Code Ready!</b>\n\n📌 <b>Data:</b> <code>{data}</code>",
        "id": "✅ <b>Kode QR Siap!</b>\n\n📌 <b>Data:</b> <code>{data}</code>",
    },

    # --- Encode & Decode ---
    "enc_menu_msg": {
        "bn": (
            "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐒𝐔𝐈𝐓𝐄 (১০০% ইন-বট)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "নিচের যেকোনো অ্যালগরিদম বেছে নিন:\n"
            "• Base64 Encode / Decode\n"
            "• URL Encode / Decode\n"
            "• Hex (Hexadecimal) Encode / Decode\n"
            "• Binary (0101) Encode / Decode\n"
            "• ROT13 Cipher & Text Reverse\n\n"
            "👇 <b>নিচের মেনু থেকে আপনার পছন্দ সিলেক্ট করুন:</b>"
        ),
        "en": (
            "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐒𝐔𝐈𝐓𝐄 (100% In-Bot)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Choose any algorithm below:\n"
            "• Base64 Encode / Decode\n"
            "• URL Encode / Decode\n"
            "• Hex (Hexadecimal) Encode / Decode\n"
            "• Binary (0101) Encode / Decode\n"
            "• ROT13 Cipher & Text Reverse\n\n"
            "👇 <b>Select your operation from the menu below:</b>"
        ),
        "id": (
            "🔐 <b>𝐒𝐔𝐈𝐓𝐄 𝐄𝐍𝐊𝐎𝐃𝐄 & 𝐃𝐄𝐊𝐎𝐃𝐄 (100% Di Bot)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Pilih algoritma di bawah:\n"
            "• Enkode / Dekode Base64\n"
            "• Enkode / Dekode URL\n"
            "• Enkode / Dekode Hex\n"
            "• Enkode / Dekode Biner (0101)\n"
            "• Sandi ROT13 & Balik Teks\n\n"
            "👇 <b>Pilih operasi dari menu di bawah:</b>"
        ),
    },
    "enc_menu_short": {
        "bn": "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐌𝐄𝐍𝐔</b>\nনিচের অপশন থেকে সিলেক্ট করুন 👇",
        "en": "🔐 <b>𝐄𝐍𝐂𝐎𝐃𝐄 & 𝐃𝐄𝐂𝐎𝐃𝐄 𝐌𝐄𝐍𝐔</b>\nSelect an option below 👇",
        "id": "🔐 <b>𝐌𝐄𝐍𝐔 𝐄𝐍𝐊𝐎𝐃𝐄 & 𝐃𝐄𝐊𝐎𝐃𝐄</b>\nPilih opsi di bawah 👇",
    },
    "enc_selected": {
        "bn": "📝 <b>সিলেক্টেড: {title}</b>\n\nযে টেক্সটটিকে কনভার্ট করতে চান তা নিচে লিখে পাঠান 👇",
        "en": "📝 <b>Selected: {title}</b>\n\nType and send the text you want to convert below 👇",
        "id": "📝 <b>Dipilih: {title}</b>\n\nKetik dan kirim teks yang ingin Anda konversi di bawah 👇",
    },
    "enc_result": {
        "bn": (
            "🎯 <b>𝐄𝐍𝐂𝐎𝐃𝐄 / 𝐃𝐄𝐂𝐎𝐃𝐄 𝐑𝐄𝐒𝐔𝐋𝐓:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<pre>{result}</pre>\n\n"
            "👆 <i>ক্লিক করলেই সম্পূর্ণ ফলাফল একসাথে কপি হয়ে যাবে।</i>"
        ),
        "en": (
            "🎯 <b>𝐄𝐍𝐂𝐎𝐃𝐄 / 𝐃𝐄𝐂𝐎𝐃𝐄 𝐑𝐄𝐒𝐔𝐋𝐓:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<pre>{result}</pre>\n\n"
            "👆 <i>Tap the box above to copy the full result.</i>"
        ),
        "id": (
            "🎯 <b>𝐇𝐀𝐒𝐈𝐋 𝐄𝐍𝐊𝐎𝐃𝐄 / 𝐃𝐄𝐊𝐎𝐃𝐄:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<pre>{result}</pre>\n\n"
            "👆 <i>Ketuk kotak di atas untuk menyalin hasil lengkap.</i>"
        ),
    },
    "enc_btn_another": {
        "bn": "🔄 আরেকটি অপারেশন",
        "en": "🔄 Another Operation",
        "id": "🔄 Operasi Lainnya",
    },

    # --- Link Checker ---
    "ask_link_check": {
        "bn": (
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
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "en": (
            "🛡️ <b>𝐋𝐈𝐍𝐊 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 & 𝐑𝐄𝐃𝐈𝐑𝐄𝐂𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔍 <b>Send any URL or link here:</b>\n"
            "The bot will inspect:\n"
            "• Whether the link is live & safe\n"
            "• Final Destination URL (Unshorten Link)\n"
            "• Full Redirect Chain\n"
            "• Server IP & Headers\n"
            "• Phishing or suspicious TLD warnings\n\n"
            "👇 <b>Paste or send the link now:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "id": (
            "🛡️ <b>𝐏𝐄𝐌𝐄𝐑𝐈𝐊𝐒𝐀 𝐊𝐄𝐀𝐌𝐀𝐍𝐀𝐍 & 𝐑𝐄𝐃𝐈𝐑𝐄𝐂𝐓 𝐓𝐀𝐔𝐓𝐀𝐍</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔍 <b>Kirim URL atau tautan apa saja di sini:</b>\n"
            "Bot akan memeriksa:\n"
            "• Apakah tautan aktif & aman\n"
            "• URL Tujuan Akhir (Unshorten Link)\n"
            "• Rantai Pengalihan (Redirect Chain)\n"
            "• Informasi IP & Server\n"
            "• Peringatan phishing atau TLD mencurigakan\n\n"
            "👇 <b>Tempel atau kirim tautan sekarang:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
    },
    "link_scanning": {
        "bn": "⏳ <b>লিংকটি স্ক্যান ও পরীক্ষা করা হচ্ছে...</b>",
        "en": "⏳ <b>Scanning and analyzing the link...</b>",
        "id": "⏳ <b>Memindai dan menganalisis tautan...</b>",
    },
    "link_report": {
        "bn": (
            "🛡️ <b>𝐋𝐈𝐍𝐊 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐀𝐍𝐀𝐋𝐘𝐒𝐈𝐒 𝐑𝐄𝐏𝐎𝐑𝐓</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>Status:</b> <b>{status_code}</b>\n"
            "🛡️ <b>Safety Level:</b> <b>{safety_level}</b>\n"
            "⏱️ <b>Response Time:</b> {resp_ms} ms\n"
            "🌐 <b>Target IP:</b> <code>{ip}</code>\n"
            "🖥️ <b>Server:</b> <code>{server}</code>\n\n"
            "🔗 <b>Destination URL:</b>\n<code>{final_url}</code>\n\n"
            "🔄 <b>Redirect Chain:</b>\n{redirect_txt}\n\n"
            "⚠️ <b>Security Checks:</b>\n{flags_txt}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "en": (
            "🛡️ <b>𝐋𝐈𝐍𝐊 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐀𝐍𝐀𝐋𝐘𝐒𝐈𝐒 𝐑𝐄𝐏𝐎𝐑𝐓</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>Status:</b> <b>{status_code}</b>\n"
            "🛡️ <b>Safety Level:</b> <b>{safety_level}</b>\n"
            "⏱️ <b>Response Time:</b> {resp_ms} ms\n"
            "🌐 <b>Target IP:</b> <code>{ip}</code>\n"
            "🖥️ <b>Server:</b> <code>{server}</code>\n\n"
            "🔗 <b>Destination URL:</b>\n<code>{final_url}</code>\n\n"
            "🔄 <b>Redirect Chain:</b>\n{redirect_txt}\n\n"
            "⚠️ <b>Security Checks:</b>\n{flags_txt}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "id": (
            "🛡️ <b>𝐋𝐀𝐏𝐎𝐑𝐀𝐍 𝐀𝐍𝐀𝐋𝐈𝐒𝐈𝐒 𝐊𝐄𝐀𝐌𝐀𝐍𝐀𝐍 𝐓𝐀𝐔𝐓𝐀𝐍</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 <b>Status:</b> <b>{status_code}</b>\n"
            "🛡️ <b>Tingkat Keamanan:</b> <b>{safety_level}</b>\n"
            "⏱️ <b>Waktu Respons:</b> {resp_ms} ms\n"
            "🌐 <b>IP Target:</b> <code>{ip}</code>\n"
            "🖥️ <b>Server:</b> <code>{server}</code>\n\n"
            "🔗 <b>URL Tujuan:</b>\n<code>{final_url}</code>\n\n"
            "🔄 <b>Rantai Pengalihan:</b>\n{redirect_txt}\n\n"
            "⚠️ <b>Pemeriksaan Keamanan:</b>\n{flags_txt}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
    },

    # --- IP Tracker ---
    "ask_ip": {
        "bn": "🌍 <b>IP Tracker</b>\n\n👉 লোকেশনসহ তথ্য জানতে IP Address পাঠান (যেমন: <code>8.8.8.8</code>)",
        "en": "🌍 <b>IP Tracker</b>\n\n👉 Send an IP Address to get full info with location! (e.g. <code>8.8.8.8</code>)",
        "id": "🌍 <b>Pelacak IP</b>\n\n👉 Kirim Alamat IP untuk info lengkap beserta lokasi! (contoh: <code>8.8.8.8</code>)",
    },
    "ip_invalid": {
        "bn": "❌ দয়া করে একটি সঠিক IP Address পাঠান (যেমন: 8.8.8.8)",
        "en": "❌ Please send a valid IP Address (e.g. 8.8.8.8)",
        "id": "❌ Harap kirim Alamat IP yang valid (contoh: 8.8.8.8)",
    },
    "ip_header": {
        "bn": "🔻 <b>IP তথ্য পাওয়া গেছে:</b>\n\n",
        "en": "🔻 <b>IP Information Extracted:</b>\n\n",
        "id": "🔻 <b>Informasi IP Ditemukan:</b>\n\n",
    },
    "ip_not_found": {
        "bn": "❌ IP তথ্য খুঁজে পাওয়া যায়নি।",
        "en": "❌ Could not find IP information.",
        "id": "❌ Informasi IP tidak ditemukan.",
    },

    # --- WhatsApp Opener ---
    "ask_wa": {
        "bn": (
            "📱 <b>Direct WhatsApp Chat Opener</b>\n\n"
            "🌍 সকল দেশ সাপোর্টেড (Contact save করা লাগবে না)\n\n"
            "<b>উদাহরণ:</b>\n"
            "• 017XXXXXXXX (BD)\n"
            "• +919876543210 (India)\n"
            "• +6281234567890 (Indonesia)\n\n"
            "📥 <b>এখন আপনার WhatsApp নাম্বারটি লিখুন 👇</b>"
        ),
        "en": (
            "📱 <b>Direct WhatsApp Chat Opener</b>\n\n"
            "🌍 All countries supported (No need to save contact)\n\n"
            "<b>Examples:</b>\n"
            "• 017XXXXXXXX (BD)\n"
            "• +919876543210 (India)\n"
            "• 1234567890 (USA)\n\n"
            "📥 <b>Enter the WhatsApp number now 👇</b>"
        ),
        "id": (
            "📱 <b>Pembuka Chat WhatsApp Langsung</b>\n\n"
            "🌍 Mendukung semua negara (Tanpa perlu simpan kontak)\n\n"
            "<b>Contoh:</b>\n"
            "• +6281234567890 (Indonesia)\n"
            "• 017XXXXXXXX (BD)\n"
            "• +14158586273 (USA)\n\n"
            "📥 <b>Masukkan nomor WhatsApp sekarang 👇</b>"
        ),
    },
    "wa_invalid": {
        "bn": "❌ সঠিক নাম্বার নয়! কান্ট্রি কোডসহ একটি সঠিক WhatsApp নাম্বার পাঠান।",
        "en": "❌ Invalid number! Send a valid WhatsApp number with country code.",
        "id": "❌ Nomor tidak valid! Kirim nomor WhatsApp yang benar beserta kode negara.",
    },
    "wa_ready": {
        "bn": "🌍 <b>চ্যাট লিংক তৈরি!</b>\nসরাসরি চ্যাট শুরু করতে নিচের বাটনে ক্লিক করুন 👇",
        "en": "🌍 <b>Ready for all countries!</b>\nClick below to start chat 👇",
        "id": "🌍 <b>Siap untuk semua negara!</b>\nKlik di bawah untuk mulai chat 👇",
    },
    "wa_btn_open": {
        "bn": "💬 WhatsApp চ্যাট খুলুন",
        "en": "💬 Open WhatsApp Chat",
        "id": "💬 Buka Chat WhatsApp",
    },

    # --- Visa / Master Card Hub ---
    "card_hub_msg": {
        "bn": (
            "💳 <b>𝐕𝐈𝐒𝐀 / 𝐌𝐀𝐒𝐓𝐄𝐑 𝐂𝐀𝐑𝐃 𝐇𝐔𝐁</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "⚡ <b>কয়েন সিস্টেম তথ্য:</b>\n"
            "• ১টি প্রিমিয়াম কার্ড নিতে <b>{cost} Coins</b> প্রয়োজন।\n"
            "• আপনার বর্তমান ব্যালেন্স: <b>{coins} Coins 💰</b>\n"
            "• প্রতিদিন ফ্রি <b>{daily_b} Coins</b> পেতে <b>🎁 ডেইলি বোনাস</b> এ ক্লিক করুন!\n\n"
            "👇 <b>নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন:</b>"
        ),
        "en": (
            "💳 <b>𝐕𝐈𝐒𝐀 / 𝐌𝐀𝐒𝐓𝐄𝐑 𝐂𝐀𝐑𝐃 𝐇𝐔𝐁</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "⚡ <b>Coin System Info:</b>\n"
            "• 1 Premium Card costs <b>{cost} Coins</b>.\n"
            "• Your Current Balance: <b>{coins} Coins 💰</b>\n"
            "• Click <b>🎁 Daily Bonus</b> to claim <b>{daily_b} Coins</b> free daily!\n\n"
            "👇 <b>Choose an option from the menu below:</b>"
        ),
        "id": (
            "💳 <b>𝐏𝐔𝐒𝐀𝐓 𝐊𝐀𝐑𝐓𝐔 𝐕𝐈𝐒𝐀 / 𝐌𝐀𝐒𝐓𝐄𝐑</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "⚡ <b>Info Sistem Koin:</b>\n"
            "• 1 Kartu Premium membutuhkan <b>{cost} Koin</b>.\n"
            "• Saldo Anda Saat Ini: <b>{coins} Koin 💰</b>\n"
            "• Klik <b>🎁 Bonus Harian</b> untuk klaim <b>{daily_b} Koin</b> gratis setiap hari!\n\n"
            "👇 <b>Pilih opsi dari menu di bawah:</b>"
        ),
    },
    "ask_cc_bin": {
        "bn": "💳 <b>Credit Card Generator (50 Cards)</b>\n\nআপনার কাঙ্ক্ষিত BIN টি দিন (৬ থেকে ৮ ডিজিট)।\n👇 এখন BIN টি লিখে পাঠান:",
        "en": "💳 <b>Credit Card Generator (50 Cards)</b>\n\nEnter your desired BIN (6 to 8 digits).\n👇 Type and send the BIN now:",
        "id": "💳 <b>Generator Kartu Kredit (50 Kartu)</b>\n\nMasukkan BIN pilihan Anda (6 hingga 8 digit).\n👇 Ketik dan kirim BIN sekarang:",
    },
    "cc_bin_invalid": {
        "bn": "❌ ভুল BIN ফরম্যাট! দয়া করে অন্তত ৬ ডিজিটের সঠিক সংখ্যা পাঠান।",
        "en": "❌ Invalid BIN format! Please send at least 6 valid digits.",
        "id": "❌ Format BIN salah! Harap kirim minimal 6 digit angka yang valid.",
    },
    "cc_bin_result": {
        "bn": (
            "💳 <b>BIN: <code>{bin_str}</code> এর জন্য ৫০টি কার্ড তৈরি হয়েছে:</b>\n\n"
            "<pre>{cards}</pre>\n"
            "👇 ওপরের বক্সে ক্লিক করলেই <b>সবগুলো কার্ড একসাথে কপি</b> হয়ে যাবে।"
        ),
        "en": (
            "💳 <b>Generated 50 Cards for BIN:</b> <code>{bin_str}</code>\n\n"
            "<pre>{cards}</pre>\n"
            "👇 Tap the box above to <b>copy all cards</b> at once."
        ),
        "id": (
            "💳 <b>50 Kartu Dibuat untuk BIN:</b> <code>{bin_str}</code>\n\n"
            "<pre>{cards}</pre>\n"
            "👇 Ketuk kotak di atas untuk <b>menyalin semua kartu</b> sekaligus."
        ),
    },
    "card_low_coins": {
        "bn": (
            "❌ <b>কয়েন অপর্যাপ্ত! | Insufficient Coins</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "💳 ১টি প্রিমিয়াম কার্ড নিতে <b>{cost} Coins</b> প্রয়োজন।\n"
            "💰 আপনার বর্তমান ব্যালেন্স: <b>{coins} Coins</b>\n\n"
            "👉 ফ্রিতে কয়েন পেতে <b>🎁 ডেইলি বোনাস</b> বাটনে চাপ দিন অথবা এডমিনের সাথে যোগাযোগ করুন।"
        ),
        "en": (
            "❌ <b>Insufficient Coins!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "💳 1 Premium Card requires <b>{cost} Coins</b>.\n"
            "💰 Your Current Balance: <b>{coins} Coins</b>\n\n"
            "👉 Tap <b>🎁 Daily Bonus</b> to earn free coins or contact an admin."
        ),
        "id": (
            "❌ <b>Koin Tidak Cukup!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "💳 1 Kartu Premium memerlukan <b>{cost} Koin</b>.\n"
            "💰 Saldo Anda Saat Ini: <b>{coins} Koin</b>\n\n"
            "👉 Ketuk <b>🎁 Bonus Harian</b> untuk koin gratis atau hubungi admin."
        ),
    },
    "card_out_of_stock": {
        "bn": "😢 দুঃখিত! এই মুহূর্তে কোনো কার্ড স্টকে নেই। এডমিনকে জানান।",
        "en": "😢 Sorry! No cards are currently in stock. Please notify an admin.",
        "id": "😢 Maaf! Stok kartu sedang habis saat ini. Silakan hubungi admin.",
    },
    "card_delivered": {
        "bn": (
            "🎁 <b>আপনার প্রিমিয়াম কার্ড:</b>\n"
            "<code>{card}</code>\n\n"
            "📌 <b>Random US ZIP:</b> <code>{zip_code}</code>\n"
            "💰 <b>কাটা হয়েছে:</b> -{cost} Coins\n"
            "💵 <b>অবশিষ্ট ব্যালেন্স:</b> <code>{new_bal}</code> Coins\n\n"
            "<i>(কার্ড ও জিপ কোডের ওপর ক্লিক করলেই কপি হয়ে যাবে)</i>"
        ),
        "en": (
            "🎁 <b>Your Premium Card:</b>\n"
            "<code>{card}</code>\n\n"
            "📌 <b>Random US ZIP:</b> <code>{zip_code}</code>\n"
            "💰 <b>Deducted:</b> -{cost} Coins\n"
            "💵 <b>Remaining Balance:</b> <code>{new_bal}</code> Coins\n\n"
            "<i>(Tap the card or ZIP code to copy)</i>"
        ),
        "id": (
            "🎁 <b>Kartu Premium Anda:</b>\n"
            "<code>{card}</code>\n\n"
            "📌 <b>Kode Pos AS Acak:</b> <code>{zip_code}</code>\n"
            "💰 <b>Dipotong:</b> -{cost} Koin\n"
            "💵 <b>Sisa Saldo:</b> <code>{new_bal}</code> Koin\n\n"
            "<i>(Ketuk kartu atau kode pos untuk menyalin)</i>"
        ),
    },
    "daily_claimed": {
        "bn": (
            "🎉 <b>𝐃𝐀𝐈𝐋𝐘 𝐁𝐎𝐍𝐔𝐒 𝐂𝐋𝐀𝐈𝐌𝐄𝐃!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "✅ আপনি আজকের ডেইলি বোনাস হিসেবে <b>+{bonus} Coins</b> পেয়েছেন!\n"
            "💰 আপনার বর্তমান ব্যালেন্স: <b>{new_bal} Coins</b>\n\n"
            "⏰ পরবর্তী বোনাস ২৪ ঘণ্টা পর আবার সংগ্রহ করতে পারবেন।"
        ),
        "en": (
            "🎉 <b>𝐃𝐀𝐈𝐋𝐘 𝐁𝐎𝐍𝐔𝐒 𝐂𝐋𝐀𝐈𝐌𝐄𝐃!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "✅ You received <b>+{bonus} Coins</b> as today's daily bonus!\n"
            "💰 Your Current Balance: <b>{new_bal} Coins</b>\n\n"
            "⏰ You can claim the next bonus in 24 hours."
        ),
        "id": (
            "🎉 <b>𝐁𝐎𝐍𝐔𝐒 𝐇𝐀𝐑𝐈𝐀𝐍 𝐃𝐈𝐊𝐋𝐀𝐈𝐌!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "✅ Anda menerima <b>+{bonus} Koin</b> sebagai bonus harian hari ini!\n"
            "💰 Saldo Anda Saat Ini: <b>{new_bal} Koin</b>\n\n"
            "⏰ Anda dapat mengklaim bonus berikutnya dalam 24 jam."
        ),
    },
    "daily_cooldown": {
        "bn": (
            "⏳ <b>বোনাস ইতিমধ্যে সংগ্রহ করা হয়েছে!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ আপনি আজকের ডেইলি বোনাস ইতিমধ্যে সংগ্রহ করেছেন।\n"
            "🕒 পরবর্তী বোনাস পাওয়া যাবে: <b>{hours} ঘণ্টা {mins} মিনিট</b> পর।\n\n"
            "💰 আপনার বর্তমান ব্যালেন্স: <b>{new_bal} Coins</b>"
        ),
        "en": (
            "⏳ <b>Bonus Already Claimed!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ You have already claimed today's daily bonus.\n"
            "🕒 Next bonus available in: <b>{hours} hours {mins} minutes</b>.\n\n"
            "💰 Your Current Balance: <b>{new_bal} Coins</b>"
        ),
        "id": (
            "⏳ <b>Bonus Sudah Diklaim!</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "❌ Anda sudah mengklaim bonus harian hari ini.\n"
            "🕒 Bonus berikutnya tersedia dalam: <b>{hours} jam {mins} menit</b>.\n\n"
            "💰 Saldo Anda Saat Ini: <b>{new_bal} Koin</b>"
        ),
    },
    "my_balance": {
        "bn": (
            "💰 <b>𝐘𝐎𝐔𝐑 𝐖𝐀𝐋𝐋𝐄𝐓 𝐁𝐀𝐋𝐀𝐍𝐂𝐄</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "👤 <b>User:</b> {name}\n"
            "🆔 <b>ID:</b> <code>{uid}</code>\n"
            "💎 <b>কয়েন ব্যালেন্স:</b> <b>{coins} Coins</b>\n\n"
            "💳 প্রতি কার্ডের মূল্য: <b>{cost} Coins</b>\n"
            "🎁 দৈনিক ফ্রি বোনাস: <b>{daily_b} Coins</b>\n\n"
            "⚡ <i>(শুধুমাত্র Visa / Master Card কিনতে কয়েন ব্যবহৃত হয়, বাকি সব টুলস ফ্রি!)</i>"
        ),
        "en": (
            "💰 <b>𝐘𝐎𝐔𝐑 𝐖𝐀𝐋𝐋𝐄𝐓 𝐁𝐀𝐋𝐀𝐍𝐂𝐄</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "👤 <b>User:</b> {name}\n"
            "🆔 <b>ID:</b> <code>{uid}</code>\n"
            "💎 <b>Coin Balance:</b> <b>{coins} Coins</b>\n\n"
            "💳 Cost Per Card: <b>{cost} Coins</b>\n"
            "🎁 Daily Free Bonus: <b>{daily_b} Coins</b>\n\n"
            "⚡ <i>(Coins are only used for Visa / Master Cards; all other tools are 100% free!)</i>"
        ),
        "id": (
            "💰 <b>𝐒𝐀𝐋𝐃𝐎 𝐃𝐎𝐌𝐏𝐄𝐓 𝐀𝐍𝐃𝐀</b>\n"
            "✦ ━━━━━━━━━━━━━━━━━━━━ ✦\n\n"
            "👤 <b>Pengguna:</b> {name}\n"
            "🆔 <b>ID:</b> <code>{uid}</code>\n"
            "💎 <b>Saldo Koin:</b> <b>{coins} Koin</b>\n\n"
            "💳 Harga Per Kartu: <b>{cost} Koin</b>\n"
            "🎁 Bonus Harian Gratis: <b>{daily_b} Koin</b>\n\n"
            "⚡ <i>(Koin hanya digunakan untuk membeli Kartu Visa / Master; semua alat lainnya 100% gratis!)</i>"
        ),
    },

    # --- Misc Resource Links & Fallback ---
    "nid_tools": {
        "bn": "🆔 <b>BD NID টুলস রিসোর্স:</b>\n\n👉 https://t.me/mrghostdataserver/15\n👉 https://t.me/mrghostdataserver/16",
        "en": "🆔 <b>BD NID Tools Resources:</b>\n\n👉 https://t.me/mrghostdataserver/15\n👉 https://t.me/mrghostdataserver/16",
        "id": "🆔 <b>Sumber Alat BD NID:</b>\n\n👉 https://t.me/mrghostdataserver/15\n👉 https://t.me/mrghostdataserver/16",
    },
    "aadhaar_tools": {
        "bn": "🪪 <b>Aadhaar টুলস রিসোর্স:</b>\n\n👉 https://t.me/mrghostdataserver/14",
        "en": "🪪 <b>Aadhaar Tools Resource:</b>\n\n👉 https://t.me/mrghostdataserver/14",
        "id": "🪪 <b>Sumber Alat Aadhaar:</b>\n\n👉 https://t.me/mrghostdataserver/14",
    },
    "sms_bomber": {
        "bn": "⚠️ <b>SMS Bomber রিসোর্স:</b>\n\n👉 https://t.me/mrghostdataserver/43",
        "en": "⚠️ <b>SMS Bomber Resource:</b>\n\n👉 https://t.me/mrghostdataserver/43",
        "id": "⚠️ <b>Sumber SMS Bomber:</b>\n\n👉 https://t.me/mrghostdataserver/43",
    },
    "coin_notify": {
        "bn": "🔔 <b>আপনার ওয়ালেট ব্যালেন্স আপডেট হয়েছে!</b>\n\nএডমিন আপনার অ্যাকাউন্টে <b>{diff} Coins</b> আপডেট করেছেন।\n💰 বর্তমান ব্যালেন্স: <b>{new_bal} Coins</b>",
        "en": "🔔 <b>Your Wallet Balance Has Been Updated!</b>\n\nAn admin updated <b>{diff} Coins</b> on your account.\n💰 Current Balance: <b>{new_bal} Coins</b>",
        "id": "🔔 <b>Saldo Dompet Anda Telah Diperbarui!</b>\n\nAdmin memperbarui <b>{diff} Koin</b> di akun Anda.\n💰 Saldo Saat Ini: <b>{new_bal} Koin</b>",
    },
    "fallback_unrecognized": {
        "bn": "⚠️ দয়া করে নিচের মেনু থেকে আপনার কাঙ্ক্ষিত টুলটি সিলেক্ট করুন অথবা <b>TikTok / Facebook / Instagram</b> ভিডিও লিংক পাঠান 👇",
        "en": "⚠️ Please select a tool from the menu below or send a <b>TikTok / Facebook / Instagram</b> video link directly 👇",
        "id": "⚠️ Silakan pilih alat dari menu di bawah atau kirim langsung tautan video <b>TikTok / Facebook / Instagram</b> 👇",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    lang = lang if lang in SUPPORTED_LANGS else "bn"
    entry = TEXTS.get(key)
    if not entry:
        return key
    val = entry.get(lang) or entry.get("en") or entry.get("bn") or ""
    return val.format(**kwargs) if kwargs else val
