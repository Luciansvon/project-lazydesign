# 🤖 Finance & Personal Assistant Bot

Bot Telegram cerdas untuk analisis keuangan dan manajemen produktivitas dengan AI-powered insights via OpenRouter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![AI](https://img.shields.io/badge/AI-OpenRouter-green.svg)

---

## ✨ Fitur Utama

### 💰 Analisis Keuangan
- 📊 Tracking pemasukan & pengeluaran
- 📈 Ringkasan otomatis (harian, mingguan, bulanan)
- 🎯 Skor kesehatan keuangan (0-100)
- 🤖 **AI Analysis** - Insight mendalam dari Claude/GPT-4
- 🔮 Prediksi spending berdasarkan tren

### ✅ Task & Produktivitas
- 📝 Manajemen to-do list
- ⏰ Deadline tracking dengan reminder
- 🎯 Prioritas task (low/medium/high)
- 📊 Skor produktivitas
- 🤖 **AI Productivity Analysis** - Tips personal

### 🤖 AI Assistant
- 💬 Chat bebas tentang keuangan & produktivitas
- 🧠 Context-aware (mengingat kondisi keuangan Anda)
- 🌐 Multi-model support (Claude, GPT-4, Gemini, Llama)

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env dengan Telegram token & OpenRouter API key

# 3. Run bot
python main.py
```

📖 **Panduan lengkap:** Lihat [SETUP.md](SETUP.md) atau [QUICK_START.md](QUICK_START.md)

---

## 🎯 Command List

### Keuangan
```
/add_income <jumlah> <kategori> [deskripsi]
/add_expense <jumlah> <kategori> [deskripsi]
/summary - Ringkasan 30 hari
/health - Skor kesehatan keuangan
/ai_analysis - Analisis AI mendalam ✨
```

### Task
```
/add_task <judul> [--due YYYY-MM-DD] [--priority low|medium|high]
/my_tasks - Task pending
/complete_task <id> - Tandai selesai
/productivity - Skor produktivitas
/ai_productivity - Analisis AI ✨
```

### Chat AI
```
/ask <pertanyaan> - Tanya apapun
```

---

## 🔧 Konfigurasi AI

Bot menggunakan **OpenRouter** untuk akses multi-model AI:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_MODEL=anthropic/claude-3-haiku  # Default
```

### Model Tersedia:
- `anthropic/claude-3-haiku` ⭐ (Recommended - cepat & murah)
- `anthropic/claude-3-sonnet` (Balanced)
- `openai/gpt-4-turbo` (Premium)
- `google/gemini-pro` (Alternatif)
- `meta-llama/llama-3-70b-instruct` (Open source)

**Tanpa API key?** Bot tetap berfungsi dengan analisis basic!

---

## 💰 Biaya

OpenRouter pay-as-you-go:
- Claude 3 Haiku: ~$0.25 per 1M tokens
- Estimasi: $1-5/bulan (normal usage)
- Deposit awal: $5

🔗 Dapatkan API key: https://openrouter.ai/keys

---

## 📁 Struktur Project

```
finance-assistant-bot/
├── main.py                 # Entry point
├── src/
│   ├── config.py          # Konfigurasi
│   ├── database.py        # Models & DB
│   ├── finance_analyzer.py # Analisis keuangan
│   ├── assistant.py       # Task management
│   └── ai_service.py      # OpenRouter integration ✨
├── requirements.txt
├── .env.example
├── SETUP.md               # Panduan lengkap
├── QUICK_START.md         # Quick guide
└── README.md
```

---

## 🛡️ Keamanan

- ✅ `.env` tidak di-commit (ada di `.gitignore`)
- ✅ Database SQLite lokal
- ✅ Tidak ada data yang dikirim ke server eksternal kecuali ke OpenRouter API
- ✅ API key terenkripsi di environment variables

---

## 📚 Referensi

Inspirasi dari komunitas:
- r/personalfinance - Reddit
- GitHub: Expense Tracker Bot
- GitHub: Gemini Finance Bot
- OpenRouter examples

---

## 🤝 Contributing

Pull request welcome! Ide fitur:
- [ ] Budget alerts via notification
- [ ] Export data ke CSV/Excel
- [ ] Multi-user support
- [ ] Web dashboard
- [ ] Receipt scanning (OCR)

---

## 📞 Support

- 📖 Dokumentasi: `SETUP.md`, `docs/USAGE.md`
- 🐛 Bug report: GitHub Issues
- 💬 Diskusi: Telegram group (coming soon)

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects!

---

**Made with ❤️ for better financial management**
