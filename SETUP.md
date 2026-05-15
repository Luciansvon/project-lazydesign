# 🚀 Panduan Setup Bot Asisten Keuangan & Pribadi

Bot Telegram dengan analisis keuangan AI-powered dan manajemen produktivitas.

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- Akun Telegram
- API Key dari OpenRouter (atau alternatif lain)

---

## 🔧 Langkah Setup Step-by-Step

### **Step 1: Clone/Download Project**

Jika menggunakan Git:
```bash
git clone <repository-url>
cd finance-assistant-bot
```

Atau download manual dan extract ke folder.

---

### **Step 2: Buat Virtual Environment (Recommended)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

---

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

Dependencies yang akan terinstall:
- `python-telegram-bot` - Framework bot Telegram
- `sqlalchemy` - Database ORM
- `pydantic` - Validasi konfigurasi
- `python-dotenv` - Load environment variables
- `requests` - HTTP client untuk API calls
- `pandas` - Analisis data (opsional untuk fitur lanjutan)

---

### **Step 4: Dapatkan Telegram Bot Token**

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot`
3. Ikuti instruksi:
   - Beri nama bot (contoh: `Finance Assistant Bot`)
   - Beri username (harus berakhiran `bot`, contoh: `myfinance_bot`)
4. BotFather akan memberikan **TOKEN** (seperti: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **Simpan token ini!**

---

### **Step 5: Dapatkan OpenRouter API Key**

OpenRouter memberikan akses ke berbagai model AI (Claude, GPT-4, Gemini, dll) dengan satu API key.

1. Kunjungi **https://openrouter.ai/**
2. Klik **Sign Up** atau **Login** (bisa pakai Google/GitHub)
3. Setelah login, buka **https://openrouter.ai/keys**
4. Klik **Create Key**
5. Beri nama key (contoh: `Finance Bot`)
6. **Copy API key** yang ditampilkan (hanya muncul sekali!)

**Alternatif:**
- **Ollama (Gratis, lokal):** Download dari https://ollama.ai, lalu jalankan `ollama run llama2`
- **Direct OpenAI:** Beli credit di https://platform.openai.com

---

### **Step 6: Konfigurasi Environment Variables**

1. Copy file contoh:
   ```bash
   cp .env.example .env
   ```

2. Edit file `.env` dengan text editor:
   ```bash
   # Isi dengan nilai Anda
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   
   # Pilih model AI (opsional, default: claude-3-haiku)
   OPENROUTER_MODEL=anthropic/claude-3-haiku
   ```

3. **Rekomendasi Model OpenRouter:**
   - `anthropic/claude-3-haiku` - Cepat & murah (recommended)
   - `anthropic/claude-3-sonnet` - Lebih pintar, harga medium
   - `google/gemini-pro` - Alternatif bagus
   - `meta-llama/llama-3-70b-instruct` - Open source, berkualitas tinggi

---

### **Step 7: Jalankan Bot**

```bash
python main.py
```

Jika berhasil, Anda akan melihat:
```
✅ Bot siap dijalankan!
Tekan Ctrl+C untuk berhenti.
```

---

### **Step 8: Test Bot di Telegram**

1. Buka Telegram
2. Cari username bot Anda (contoh: `@myfinance_bot`)
3. Klik **Start** atau ketik `/start`
4. Bot akan merespons dengan menu utama

---

## 📱 Cara Menggunakan Bot

### **Perintah Dasar:**

```
/start - Mulai bot
/help - Lihat semua perintah
```

### **Keuangan:**
```
/add_income 5000000 Gaji "Gaji bulan Januari"
/add_expense 50000 Makanan "Makan siang"
/summary - Ringkasan keuangan 30 hari
/health - Skor kesehatan keuangan
/ai_analysis - Analisis mendalam dengan AI ✨
```

### **Task Management:**
```
/add_task Bayar listrik --due 2024-01-25 --priority high
/my_tasks - Lihat task pending
/complete_task 1 - Tandai task #1 selesai
/productivity - Skor produktivitas
/ai_productivity - Analisis produktivitas dengan AI ✨
```

### **Chat AI:**
```
/ask Bagaimana cara menabung lebih efektif?
/ask Tips mengatur gaji 5 juta per bulan
/ask Cara mengurangi pengeluaran makanan?
```

---

## 🔍 Troubleshooting

### **Error: "TELEGRAM_BOT_TOKEN tidak ditemukan"**
- Pastikan file `.env` ada di folder yang sama dengan `main.py`
- Cek apakah TOKEN sudah diisi dengan benar
- Restart bot setelah edit `.env`

### **Error: "OPENROUTER_API_KEY tidak ditemukan"**
- Fitur AI tetap berjalan dengan fallback analysis (tanpa AI)
- Untuk enable, isi `OPENROUTER_API_KEY` di `.env`

### **Bot tidak merespons**
- Cek koneksi internet
- Pastikan token bot benar
- Lihat log error di terminal

### **Import Error**
```bash
pip install -r requirements.txt --upgrade
```

---

## 💰 Biaya OpenRouter

OpenRouter menggunakan sistem pay-as-you-go:

- **Claude 3 Haiku:** ~$0.25 per 1M tokens (sangat murah!)
- **Gemini Pro:** ~$0.125 per 1M tokens
- **Llama 3 70B:** ~$0.65 per 1M tokens

**Estimasi biaya bulanan:**
- Penggunaan normal: $1-5/bulan
- Heavy usage: $10-20/bulan

Deposit awal minimal: **$5**

---

## 🛡️ Keamanan

- Jangan share `.env` file ke publik
- Jangan commit `.env` ke Git (sudah ada di `.gitignore`)
- Rotate API key secara berkala
- Backup database secara rutin (`finance_assistant.db`)

---

## 📚 Referensi

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Telegram Bot](https://docs.python-telegram-bot.org/)
- [Komunitas Reddit r/personalfinance](https://reddit.com/r/personalfinance)
- [GitHub Awesome Finance](https://github.com/topics/personal-finance)

---

## 🎯 Next Steps

Setelah bot berjalan:

1. **Customize** model AI sesuai budget
2. **Invite** bot ke grup keluarga untuk tracking bersama
3. **Setup** reminder harian/mingguan
4. **Explore** fitur advanced seperti budget alerts
5. **Contribute** ke project jika ada ide fitur baru!

---

## 📞 Support

Jika ada masalah:
1. Cek file `docs/USAGE.md` untuk panduan lengkap
2. Baca log error di terminal
3. Buka issue di GitHub repository

**Selamat menggunakan! 🎉**
