"""
AI Service - Integrasi dengan OpenRouter untuk analisis cerdas
OpenRouter memberikan akses ke berbagai model AI (Claude, GPT-4, Llama, dll)
Referensi: https://github.com/OpenRouter/openrouter-examples
"""
import requests
import json
from typing import Dict, List, Optional
from src.config import settings

class AIService:
    """Layanan AI menggunakan OpenRouter API"""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.model = settings.openrouter_model
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            print("⚠️  OPENROUTER_API_KEY tidak ditemukan. Fitur AI akan dinonaktifkan.")
            print("   Dapatkan API key di: https://openrouter.ai/keys")
    
    def _make_request(self, messages: List[Dict], **kwargs) -> Optional[str]:
        """Kirim request ke OpenRouter API"""
        if not self.enabled:
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Required by OpenRouter
            "X-Title": "Finance Assistant Bot"  # Optional
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling OpenRouter API: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"❌ Error parsing API response: {e}")
            return None
    
    def analyze_finances(self, transactions: List[Dict], summary: Dict) -> str:
        """
        Analisis keuangan mendalam menggunakan AI
        Memberikan insight, tips, dan rekomendasi berdasarkan data transaksi
        """
        if not self.enabled:
            return self._fallback_finance_analysis(summary)
        
        # Format transaksi untuk AI
        transaction_text = ""
        for tx in transactions[-20:]:  # Last 20 transactions
            emoji = "💰" if tx['type'] == 'income' else "💸"
            transaction_text += f"- {emoji} Rp {tx['amount']:,.0f} ({tx['category']}): {tx.get('description', '')}\n"
        
        prompt = f"""
Anda adalah asisten keuangan pribadi yang ahli. Analisis kondisi keuangan berikut:

**RINGKASAN (30 hari terakhir):**
- Total Pemasukan: Rp {summary.get('total_income', 0):,.0f}
- Total Pengeluaran: Rp {summary.get('total_expense', 0):,.0f}
- Saldo: Rp {summary.get('net_balance', 0):,.0f}
- Total Transaksi: {summary.get('transaction_count', 0)}

**TOP KATEGORI PENGELUARAN:**
"""
        for cat, amount in summary.get('expense_categories', {}).items():
            prompt += f"- {cat}: Rp {amount:,.0f}\n"
        
        prompt += f"\n**TRANSAKSI TERAKHIR:**\n{transaction_text}"
        
        prompt += """
Berikan analisis dalam format berikut (gunakan bahasa Indonesia yang santai dan mudah dipahami):

1. 📊 **Kondisi Keuangan**: (Analisis singkat kondisi saat ini)
2. ⚠️ **Area Perhatian**: (Kategori yang perlu dikurangi jika ada)
3. 💡 **Tips Penghematan**: (2-3 tips spesifik berdasarkan pola spending)
4. 🎯 **Rekomendasi**: (Saran actionable untuk perbaikan keuangan)

Maksimal 300 kata. Gunakan emoji secukupnya.
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages, max_tokens=500, temperature=0.7)
        
        return response if response else self._fallback_finance_analysis(summary)
    
    def _fallback_finance_analysis(self, summary: Dict) -> str:
        """Fallback analysis tanpa AI"""
        net = summary.get('net_balance', 0)
        income = summary.get('total_income', 0)
        expense = summary.get('total_expense', 0)
        
        if income > 0:
            savings_rate = ((income - expense) / income) * 100
        else:
            savings_rate = 0
        
        analysis = f"""📊 **Analisis Keuangan Sederhana**

💰 Pemasukan: Rp {income:,.0f}
💸 Pengeluaran: Rp {expense:,.0f}
💵 Saldo: Rp {net:,.0f}
📈 Savings Rate: {savings_rate:.1f}%

"""
        if savings_rate >= 30:
            analysis += "✅ Bagus! Anda menabung lebih dari 30% dari pemasukan."
        elif savings_rate >= 10:
            analysis += "⚠️ Cukup baik, tapi bisa ditingkatkan lagi."
        else:
            analysis += "⚠️ Perlu diperhatikan! Coba kurangi pengeluaran tidak penting."
        
        return analysis
    
    def analyze_productivity(self, tasks: List[Dict], productivity_data: Dict) -> str:
        """
        Analisis produktivitas dan berikan tips
        """
        if not self.enabled:
            return self._fallback_productivity_analysis(productivity_data)
        
        task_list = ""
        for task in tasks[:10]:
            status = "✅" if task.get('completed') else "⏳"
            priority = task.get('priority', 'medium')
            task_list += f"- {status} [{priority}] {task['title']}\n"
        
        prompt = f"""
Anda adalah coach produktivitas profesional. Analisis data berikut:

**STATISTIK TASK:**
- Total Task: {productivity_data.get('total', 0)}
- Selesai: {productivity_data.get('completed', 0)}
- Pending: {productivity_data.get('pending', 0)}
- Overdue: {productivity_data.get('overdue', 0)}
- Completion Rate: {productivity_data.get('completion_rate', 0)}%

**TASK TERAKHIR:**
{task_list if task_list else "Belum ada task"}

Berikan analisis dalam format (bahasa Indonesia santai):

1. 📊 **Status Produktivitas**: (Analisis singkat)
2. 🎯 **Fokus Utama**: (Apa yang harus diprioritaskan)
3. 💡 **Tips Produktivitas**: (2-3 tips spesifik)
4. ⚡ **Action Item**: (1 hal konkret yang bisa dilakukan hari ini)

Maksimal 250 kata.
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages, max_tokens=400, temperature=0.7)
        
        return response if response else self._fallback_productivity_analysis(productivity_data)
    
    def _fallback_productivity_analysis(self, data: Dict) -> str:
        """Fallback productivity analysis tanpa AI"""
        score = data.get('score', 0)
        
        if score >= 80:
            emoji = "🟢"
            msg = "Produktivitas luar biasa!"
        elif score >= 60:
            emoji = "🟡"
            msg = "Produktivitas cukup baik."
        else:
            emoji = "🟠"
            msg = "Perlu peningkatan produktivitas."
        
        return f"""{emoji} **Analisis Produktivitas**

Skor: {score}/100
{msg}

📊 Task Selesai: {data.get('completed', 0)}/{data.get('total', 0)}
⏰ Overdue: {data.get('overdue', 0)}

💡 Tips: Fokus selesaikan task yang overdue terlebih dahulu!
"""
    
    def chat(self, user_message: str, context: str = "") -> str:
        """
        Chat umum dengan AI assistant
        Bisa digunakan untuk tanya jawab tentang keuangan, task, atau topik lain
        """
        if not self.enabled:
            return "⚠️ Fitur chat AI memerlukan OPENROUTER_API_KEY. Silakan konfigurasi di file .env"
        
        system_prompt = """
Anda adalah asisten pribadi yang membantu pengguna dalam manajemen keuangan dan produktivitas.
- Bersikap ramah, profesional, dan mudah dipahami
- Berikan saran yang praktis dan actionable
- Jika ditanya tentang keuangan, berikan tips pengelolaan uang yang bijak
- Jika ditanya tentang produktivitas, bantu prioritaskan task
- Gunakan bahasa Indonesia yang santai tapi tetap profesional
"""
        
        if context:
            system_prompt += f"\n\nKonteks pengguna:\n{context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self._make_request(messages, max_tokens=600, temperature=0.7)
        return response if response else "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    
    def get_spending_prediction(self, transactions: List[Dict], category: str) -> str:
        """
        Prediksi spending untuk kategori tertentu berdasarkan tren historis
        """
        if not self.enabled:
            return "⚠️ Fitur prediksi memerlukan OPENROUTER_API_KEY"
        
        # Hitung average spending per kategori
        category_transactions = [t for t in transactions if t['category'] == category and t['type'] == 'expense']
        
        if len(category_transactions) < 2:
            return f"📊 Data untuk kategori '{category}' masih kurang untuk prediksi akurat. Terus catat pengeluaran Anda!"
        
        total = sum(t['amount'] for t in category_transactions)
        avg = total / len(category_transactions)
        
        prompt = f"""
Berdasarkan data pengeluaran kategori "{category}":
- Jumlah transaksi: {len(category_transactions)}
- Total pengeluaran: Rp {total:,.0f}
- Rata-rata per transaksi: Rp {avg:,.0f}

Berikan prediksi dan saran dalam format:
1. 🔮 **Prediksi Bulan Depan**: (Estimasi pengeluaran)
2. 📈 **Tren**: (Apakah meningkat/menurun/stabil)
3. 💡 **Saran**: (Tips mengontrol pengeluaran di kategori ini)

Maksimal 150 kata.
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(messages, max_tokens=300, temperature=0.6)
        
        prediction = response if response else f"""
📊 **Prediksi Sederhana - {category}**

Rata-rata pengeluaran: Rp {avg:,.0f} per transaksi

💡 Saran: Pantau terus pengeluaran di kategori ini dan buat budget bulanan.
"""
        
        return prediction


# Singleton instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get singleton AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
