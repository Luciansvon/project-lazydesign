"""
Financial & Personal Assistant Bot - Main Entry Point
Bot Telegram untuk analisis keuangan dan asisten pribadi
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.orm import Session

from src.config import settings
from src.database import init_db, SessionLocal, Transaction, Budget
from src.finance_analyzer import FinanceAnalyzer
from src.assistant import PersonalAssistant

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_db_session() -> Session:
    """Get database session"""
    return SessionLocal()

# ========== COMMAND HANDLERS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /start - Welcome message"""
    user_id = str(update.effective_user.id)
    
    welcome_message = f"""
👋 Halo {update.effective_user.first_name}! 

Saya adalah asisten keuangan dan pribadi Anda. Saya bisa membantu Anda:

📊 *Analisis Keuangan:*
- Catat pemasukan & pengeluaran
- Lihat ringkasan keuangan
- Analisis kategori spending
- Prediksi keuangan

🤖 *Asisten Pribadi:*
- Kelola task & to-do list
- Buat catatan harian
- Pengingat deadline
- Analisis produktivitas

*Ketik /help* untuk melihat semua perintah yang tersedia!
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Laporan Keuangan", callback_data="finance_report")],
        [InlineKeyboardButton("✅ Task List", callback_data="task_list")],
        [InlineKeyboardButton("📝 Catatan", callback_data="notes_list")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /help - Show all available commands"""
    help_text = """
📚 *DAFTAR PERINTAH*

*💰 KEUANGAN:*
/add_income - Tambah pemasukan
/add_expense - Tambah pengeluaran
/summary - Ringkasan keuangan
/categories - Breakdown kategori
/budget - Set budget
/budget_status - Status budget
/health - Skor kesehatan keuangan

*✅ TASK MANAGEMENT:*
/add_task - Tambah task baru
/my_tasks - Lihat task
/complete_task - Selesaikan task
/delete_task - Hapus task
/task_summary - Ringkasan task

*📝 CATATAN:*
/add_note - Tambah catatan
/my_notes - Lihat catatan
/delete_note - Hapus catatan

*📊 LAPORAN:*
/daily_report - Laporan harian
/weekly_report - Laporan mingguan
/productivity - Skor produktivitas

*⚙️ LAINNYA:*
/start - Mulai bot
/help - Bantuan ini
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ========== FINANCE COMMANDS ==========

async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /add_income - Add income transaction"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "❌ Format: /add_income <jumlah> <kategori> [deskripsi]\n"
                "Contoh: /add_income 5000000 Gaji \"Gaji bulan Januari\""
            )
            return
        
        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else ""
        
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            category=category,
            transaction_type="income",
            description=description
        )
        
        db.add(transaction)
        db.commit()
        
        await update.message.reply_text(
            f"✅ Pemasukan berhasil dicatat!\n\n"
            f"💰 Jumlah: Rp {amount:,.0f}\n"
            f"📁 Kategori: {category}\n"
            f"📝 Deskripsi: {description or '-'}"
        )
    finally:
        db.close()

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /add_expense - Add expense transaction"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "❌ Format: /add_expense <jumlah> <kategori> [deskripsi]\n"
                "Contoh: /add_expense 50000 Makanan \"Makan siang\""
            )
            return
        
        amount = float(context.args[0])
        category = context.args[1]
        description = " ".join(context.args[2:]) if len(context.args) > 2 else ""
        
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            category=category,
            transaction_type="expense",
            description=description
        )
        
        db.add(transaction)
        db.commit()
        
        analyzer = FinanceAnalyzer(db)
        summary = analyzer.get_summary(user_id, days=30)
        remaining = summary['total_income'] - summary['total_expense']
        
        await update.message.reply_text(
            f"✅ Pengeluaran berhasil dicatat!\n\n"
            f"💸 Jumlah: Rp {amount:,.0f}\n"
            f"📁 Kategori: {category}\n"
            f"📝 Deskripsi: {description or '-'}\n\n"
            f"📊 *Saldo bulan ini:* Rp {remaining:,.0f}"
        , parse_mode='Markdown')
    finally:
        db.close()

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /summary - Show financial summary"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        analyzer = FinanceAnalyzer(db)
        summary_data = analyzer.get_summary(user_id, days=30)
        
        report = f"""
📊 *RINGKASAN KEUANGAN (30 hari)*

💰 Pemasukan: Rp {summary_data['total_income']:,.0f}
💸 Pengeluaran: Rp {summary_data['total_expense']:,.0f}
━━━━━━━━━━━━━━━━
💵 *Saldo: Rp {summary_data['net_balance']:,.0f}*

📈 Total Transaksi: {summary_data['transaction_count']}
        """
        
        # Top categories
        if summary_data.get('expense_categories'):
            top_expenses = sorted(
                summary_data['expense_categories'].items(), 
                key=lambda x: x[1], reverse=True
            )[:3]
            
            report += "\n*Top Pengeluaran:*\n"
            for cat, amount in top_expenses:
                report += f"• {cat}: Rp {amount:,.0f}\n"
        
        await update.message.reply_text(report, parse_mode='Markdown')
    finally:
        db.close()

async def health_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /health - Show financial health score"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        analyzer = FinanceAnalyzer(db)
        health = analyzer.get_financial_health_score(user_id)
        
        score = health['score']
        
        if score >= 80:
            emoji = "🟢"
            text = "Sangat Baik!"
        elif score >= 60:
            emoji = "🟡"
            text = "Cukup Baik"
        elif score >= 40:
            emoji = "🟠"
            text = "Perlu Perbaikan"
        else:
            emoji = "🔴"
            text = "Perlu Perhatian Serius"
        
        report = f"""
{emoji} *SKOR KESEHATAN KEUANGAN: {score}/100*
{text}

*Faktor Penilaian:*
"""
        for factor in health['factors']:
            report += f"{factor}\n"
        
        report += f"\n💰 Savings Rate: {health.get('savings_rate', 0)}%"
        
        await update.message.reply_text(report, parse_mode='Markdown')
    finally:
        db.close()

# ========== TASK COMMANDS ==========

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /add_task - Add new task"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        assistant = PersonalAssistant(db)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Format: /add_task <judul task> [--due YYYY-MM-DD] [--priority low|medium|high]\n"
                "Contoh: /add_task Bayar listrik --due 2024-01-25 --priority high"
            )
            return
        
        # Parse arguments
        title_parts = []
        due_date = None
        priority = "medium"
        
        i = 0
        while i < len(context.args):
            arg = context.args[i]
            if arg == "--due" and i + 1 < len(context.args):
                from datetime import datetime
                due_date = datetime.strptime(context.args[i + 1], "%Y-%m-%d")
                i += 2
            elif arg == "--priority" and i + 1 < len(context.args):
                priority = context.args[i + 1]
                i += 2
            else:
                title_parts.append(arg)
                i += 1
        
        title = " ".join(title_parts)
        
        task = assistant.create_task(
            user_id=user_id,
            title=title,
            due_date=due_date,
            priority=priority
        )
        
        due_str = due_date.strftime("%Y-%m-%d") if due_date else "Tidak ada deadline"
        
        await update.message.reply_text(
            f"✅ Task berhasil ditambahkan!\n\n"
            f"📋 Judul: {title}\n"
            f"📅 Deadline: {due_str}\n"
            f"🎯 Prioritas: {priority}\n"
            f"ID: #{task.id}"
        )
    finally:
        db.close()

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /my_tasks - Show user's tasks"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        assistant = PersonalAssistant(db)
        
        tasks = assistant.get_tasks(user_id, completed=False)
        
        if not tasks:
            await update.message.reply_text("✅ Tidak ada task pending. Bagus!")
            return
        
        report = "📋 *TASK ANDA:*\n\n"
        
        for i, task in enumerate(tasks[:10], 1):
            due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No deadline"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
            
            report += f"{i}. {priority_emoji} {task.title}\n"
            report += f"   📅 {due_str}\n\n"
        
        if len(tasks) > 10:
            report += f"...dan {len(tasks) - 10} task lainnya\n"
        
        await update.message.reply_text(report, parse_mode='Markdown')
    finally:
        db.close()

async def complete_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /complete_task - Mark task as complete"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        assistant = PersonalAssistant(db)
        
        if not context.args:
            await update.message.reply_text("❌ Format: /complete_task <task_id>")
            return
        
        task_id = int(context.args[0])
        task = assistant.complete_task(user_id, task_id)
        
        if task:
            await update.message.reply_text(f"✅ Task '{task.title}' selesai! 🎉")
        else:
            await update.message.reply_text("❌ Task tidak ditemukan.")
    finally:
        db.close()

async def productivity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /productivity - Show productivity score"""
    db = get_db_session()
    try:
        user_id = str(update.effective_user.id)
        assistant = PersonalAssistant(db)
        
        prod = assistant.get_productivity_score(user_id)
        
        score = prod['score']
        
        if score >= 80:
            emoji = "🟢"
        elif score >= 60:
            emoji = "🟡"
        else:
            emoji = "🟠"
        
        report = f"""
{emoji} *SKOR PRODUKTIVITAS: {score}/100*

📊 *Statistik:*
• Total Task: {prod['total']}
• Selesai: {prod['completed']}
• Pending: {prod['pending']}
• Overdue: {prod['overdue']}
• Completion Rate: {prod['completion_rate']}%

*Faktor:*
"""
        for factor in prod['factors']:
            report += f"{factor}\n"
        
        await update.message.reply_text(report, parse_mode='Markdown')
    finally:
        db.close()

# ========== CALLBACK QUERY HANDLER ==========

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "finance_report":
        await summary(update, context)
    elif data == "task_list":
        await my_tasks(update, context)
    elif data == "notes_list":
        await query.edit_message_text("📝 Fitur catatan akan segera hadir!")

# ========== MAIN ==========

def main():
    """Main function to run the bot"""
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Check if bot token is configured
    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found! Please set it in .env file")
        print("\n❌ ERROR: TELEGRAM_BOT_TOKEN tidak ditemukan!")
        print("Silakan copy .env.example ke .env dan isi token bot Anda.\n")
        print("Cara mendapatkan token:")
        print("1. Buka Telegram, cari @BotFather")
        print("2. Ketik /newbot dan ikuti instruksi")
        print("3. Copy token yang diberikan")
        print("4. Paste ke file .env\n")
        return
    
    # Create application
    app = Application.builder().token(settings.telegram_bot_token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Finance commands
    app.add_handler(CommandHandler("add_income", add_income))
    app.add_handler(CommandHandler("add_expense", add_expense))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("health", health_score))
    
    # Task commands
    app.add_handler(CommandHandler("add_task", add_task))
    app.add_handler(CommandHandler("my_tasks", my_tasks))
    app.add_handler(CommandHandler("complete_task", complete_task_cmd))
    app.add_handler(CommandHandler("productivity", productivity))
    
    # Callback handler
    app.add_handler(MessageHandler(filters.Regex("^/(.*)"), help_command))
    
    # Start bot
    logger.info("Bot starting...")
    print("\n✅ Bot siap dijalankan!")
    print("Tekan Ctrl+C untuk berhenti.\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
