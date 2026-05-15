"""
Modul analisis keuangan
"""
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database import Transaction, Budget
from typing import Dict, List, Optional

class FinanceAnalyzer:
    """Kelas untuk analisis data keuangan"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_transactions_df(self, user_id: str, days: int = 30) -> pd.DataFrame:
        """Ambil transaksi user sebagai DataFrame"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.date >= cutoff_date
        ).all()
        
        if not transactions:
            return pd.DataFrame()
        
        df = pd.DataFrame([{
            'id': t.id,
            'amount': t.amount,
            'category': t.category,
            'type': t.transaction_type,
            'description': t.description,
            'date': t.date
        } for t in transactions])
        
        return df
    
    def get_summary(self, user_id: str, days: int = 30) -> Dict:
        """Dapatkan ringkasan keuangan"""
        df = self.get_transactions_df(user_id, days)
        
        if df.empty:
            return {
                'total_income': 0,
                'total_expense': 0,
                'net_balance': 0,
                'transaction_count': 0,
                'categories': {}
            }
        
        income = df[df['type'] == 'income']['amount'].sum()
        expense = df[df['type'] == 'expense']['amount'].sum()
        
        # Group by category
        expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
        income_by_category = df[df['type'] == 'income'].groupby('category')['amount'].sum().to_dict()
        
        return {
            'total_income': income,
            'total_expense': expense,
            'net_balance': income - expense,
            'transaction_count': len(df),
            'expense_categories': expense_by_category,
            'income_categories': income_by_category,
            'period_days': days
        }
    
    def get_category_breakdown(self, user_id: str, days: int = 30) -> Dict:
        """Breakdown pengeluaran per kategori"""
        df = self.get_transactions_df(user_id, days)
        
        if df.empty:
            return {}
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty:
            return {}
        
        breakdown = expenses.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
        breakdown.columns = ['total', 'count', 'average']
        breakdown['percentage'] = (breakdown['total'] / breakdown['total'].sum() * 100).round(2)
        
        return breakdown.to_dict('index')
    
    def get_daily_spending(self, user_id: str, days: int = 30) -> Dict:
        """Pengeluaran harian"""
        df = self.get_transactions_df(user_id, days)
        
        if df.empty:
            return {}
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty:
            return {}
        
        expenses['date_only'] = expenses['date'].dt.date
        daily = expenses.groupby('date_only')['amount'].sum()
        
        return daily.to_dict()
    
    def predict_monthly_spending(self, user_id: str) -> Optional[float]:
        """Prediksi pengeluaran bulan ini berdasarkan tren"""
        # Ambil data 3 bulan terakhir
        df = self.get_transactions_df(user_id, days=90)
        
        if df.empty:
            return None
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty:
            return None
        
        # Group by month
        expenses['month'] = expenses['date'].dt.to_period('M')
        monthly = expenses.groupby('month')['amount'].sum()
        
        if len(monthly) < 2:
            # Tidak cukup data untuk prediksi
            current_month_expenses = expenses[expenses['month'] == expenses['month'].max()]['amount'].sum()
            return current_month_expenses * 1.1  # Estimasi sederhana
        
        # Simple moving average prediction
        avg_monthly = monthly.mean()
        trend = monthly.diff().mean()
        
        prediction = avg_monthly + trend
        return max(0, prediction)
    
    def get_budget_status(self, user_id: str) -> List[Dict]:
        """Status budget per kategori"""
        budgets = self.db.query(Budget).filter(
            Budget.user_id == user_id
        ).all()
        
        status_list = []
        
        for budget in budgets:
            # Hitung pengeluaran bulan ini untuk kategori ini
            current_month_start = datetime.utcnow().replace(day=1)
            
            expenses = self.db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.category == budget.category,
                Transaction.transaction_type == 'expense',
                Transaction.date >= current_month_start
            ).all()
            
            spent = sum(t.amount for t in expenses)
            percentage = (spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0
            
            status_list.append({
                'category': budget.category,
                'limit': budget.limit_amount,
                'spent': spent,
                'remaining': budget.limit_amount - spent,
                'percentage': round(percentage, 2),
                'status': 'warning' if percentage > 80 else ('danger' if percentage > 100 else 'good')
            })
        
        return status_list
    
    def get_financial_health_score(self, user_id: str) -> Dict:
        """Hitung skor kesehatan keuangan (0-100)"""
        summary = self.get_summary(user_id, days=30)
        
        if summary['total_income'] == 0:
            return {'score': 0, 'factors': []}
        
        factors = []
        score = 0
        
        # Factor 1: Savings rate (40 points)
        savings_rate = (summary['total_income'] - summary['total_expense']) / summary['total_income']
        if savings_rate >= 0.2:
            score += 40
            factors.append("✅ Tabungan baik (>20%)")
        elif savings_rate >= 0.1:
            score += 25
            factors.append("⚠️ Tabungan cukup (10-20%)")
        else:
            score += 10
            factors.append("❌ Tabungan rendah (<10%)")
        
        # Factor 2: Expense consistency (30 points)
        daily = self.get_daily_spending(user_id)
        if daily:
            values = list(daily.values())
            avg = sum(values) / len(values)
            variance = sum((x - avg) ** 2 for x in values) / len(values)
            cv = (variance ** 0.5) / avg if avg > 0 else 0
            
            if cv < 0.5:
                score += 30
                factors.append("✅ Pengeluaran stabil")
            elif cv < 1.0:
                score += 20
                factors.append("⚠️ Pengeluaran cukup fluktuatif")
            else:
                score += 10
                factors.append("❌ Pengeluaran sangat fluktuatif")
        
        # Factor 3: Category diversity (30 points)
        categories = summary.get('expense_categories', {})
        if len(categories) >= 5:
            score += 30
            factors.append("✅ Diversifikasi kategori baik")
        elif len(categories) >= 3:
            score += 20
            factors.append("⚠️ Kategori cukup beragam")
        else:
            score += 10
            factors.append("❌ Kategori terbatas")
        
        return {
            'score': min(100, score),
            'factors': factors,
            'savings_rate': round(savings_rate * 100, 2)
        }
