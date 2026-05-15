# Panduan Penggunaan Bot

## Cara Menjalankan Bot

### 1. Instalasi Dependencies
pip install -r requirements.txt

### 2. Konfigurasi
cp .env.example .env

Edit file .env dan isi TELEGRAM_BOT_TOKEN dari @BotFather

### 3. Jalankan Bot
python main.py

## Perintah Keuangan
- /add_income <jumlah> <kategori> - Catat pemasukan
- /add_expense <jumlah> <kategori> - Catat pengeluaran  
- /summary - Ringkasan keuangan
- /health - Skor kesehatan keuangan

## Perintah Task
- /add_task <judul> --due YYYY-MM-DD - Tambah task
- /my_tasks - Lihat task
- /complete_task <id> - Selesaikan task
- /productivity - Skor produktivitas
