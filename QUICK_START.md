# 🚀 Quick Start Guide - Finance & Personal Assistant Bot

## ⚡ Setup dalam 5 Menit

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Dapatkan Telegram Bot Token
- Buka **@BotFather** di Telegram
- Ketik `/newbot`
- Copy token yang diberikan

### 3️⃣ Dapatkan OpenRouter API Key
- Kunjungi **https://openrouter.ai/**
- Sign up / Login
- Buka **https://openrouter.ai/keys**
- Create Key dan copy API key

### 4️⃣ Konfigurasi .env
```bash
cp .env.example .env
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 5️⃣ Run Bot
```bash
python main.py
```

---

## 📱 Test Bot

1. Buka Telegram
2. Cari username bot Anda
3. Klik **Start**
4. Coba perintah:
   - `/help` - Lihat semua fitur
   - `/add_income 5000000 Gaji "Gaji Januari"`
   - `/add_expense 50000 Makanan "Makan siang"`
   - `/summary` - Lihat ringkasan
   - `/ai_analysis` - Analisis dengan AI!

---

## 🎯 Fitur Utama

### 💰 Keuangan
- Catat pemasukan/pengeluaran
- Ringkasan otomatis
- Skor kesehatan keuangan
- **AI Analysis** untuk insight mendalam

### ✅ Task Management
- Buat task dengan deadline & prioritas
- Tracking produktivitas
- **AI Productivity Analysis**

### 🤖 Chat AI
- `/ask` - Tanya apapun tentang keuangan
- Tips personal berdasarkan data Anda

---

## 🔧 Model AI Tersedia

Via OpenRouter (recommended):
- `anthropic/claude-3-haiku` - Cepat & murah ⭐
- `anthropic/claude-3-sonnet` - Balanced
- `google/gemini-pro` - Alternatif bagus
- `meta-llama/llama-3-70b-instruct` - Open source

Edit di `.env`:
```env
OPENROUTER_MODEL=anthropic/claude-3-haiku
```

---

## 💰 Estimasi Biaya

OpenRouter pay-as-you-go:
- Claude 3 Haiku: ~$0.25/1M tokens
- Normal usage: $1-5/bulan
- Deposit awal: $5

**Tanpa AI?** Bot tetap berfungsi dengan analisis basic!

---

## ❓ Troubleshooting

**Bot tidak start?**
```bash
# Cek .env file ada
ls -la .env

# Cek dependencies
pip install -r requirements.txt --upgrade

# Jalankan dengan verbose
python main.py
```

**AI tidak bekerja?**
- Pastikan `OPENROUTER_API_KEY` terisi
- Bot tetap jalan dengan fallback mode (tanpa AI)

---

## 📚 Dokumentasi Lengkap

- `SETUP.md` - Panduan setup detail
- `docs/USAGE.md` - Cara pakai semua fitur
- `.env.example` - Template konfigurasi

---

**Happy tracking! 🎉**
