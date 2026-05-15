"""
Modul asisten pribadi - Task management, notes, reminders
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database import Task, Note
from typing import Dict, List, Optional

class PersonalAssistant:
    """Kelas untuk manajemen tugas dan catatan pribadi"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== TASK MANAGEMENT ==========
    
    def create_task(self, user_id: str, title: str, description: str = "", 
                    due_date: Optional[datetime] = None, priority: str = "medium") -> Task:
        """Buat task baru"""
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_tasks(self, user_id: str, completed: bool = False, 
                  upcoming_days: int = 7) -> List[Task]:
        """Ambil daftar task user"""
        query = self.db.query(Task).filter(
            Task.user_id == user_id,
            Task.completed == completed
        )
        
        if not completed:
            # Untuk task yang belum selesai, urutkan by due date
            cutoff = datetime.utcnow() + timedelta(days=upcoming_days)
            query = query.filter(
                (Task.due_date == None) | (Task.due_date <= cutoff)
            )
        
        return query.order_by(Task.due_date.asc(), Task.priority.desc()).all()
    
    def complete_task(self, user_id: str, task_id: int) -> Optional[Task]:
        """Tandai task sebagai selesai"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if task:
            task.completed = True
            self.db.commit()
            self.db.refresh(task)
        
        return task
    
    def delete_task(self, user_id: str, task_id: int) -> bool:
        """Hapus task"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        
        return False
    
    def get_overdue_tasks(self, user_id: str) -> List[Task]:
        """Dapatkan task yang sudah melewati deadline"""
        return self.db.query(Task).filter(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date != None,
            Task.due_date < datetime.utcnow()
        ).order_by(Task.due_date.asc()).all()
    
    def get_task_summary(self, user_id: str) -> Dict:
        """Ringkasan task user"""
        total = self.db.query(Task).filter(Task.user_id == user_id).count()
        completed = self.db.query(Task).filter(
            Task.user_id == user_id,
            Task.completed == True
        ).count()
        pending = total - completed
        overdue = len(self.get_overdue_tasks(user_id))
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': round(completed / total * 100, 2) if total > 0 else 0
        }
    
    # ========== NOTE MANAGEMENT ==========
    
    def create_note(self, user_id: str, content: str, title: str = "", 
                    tags: List[str] = None) -> Note:
        """Buat catatan baru"""
        note = Note(
            user_id=user_id,
            title=title,
            content=content,
            tags=",".join(tags) if tags else ""
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def get_notes(self, user_id: str, search: str = None, 
                  tag: str = None) -> List[Note]:
        """Ambil daftar catatan"""
        query = self.db.query(Note).filter(Note.user_id == user_id)
        
        if search:
            query = query.filter(
                (Note.title.contains(search)) | (Note.content.contains(search))
            )
        
        if tag:
            query = query.filter(Note.tags.contains(tag))
        
        return query.order_by(Note.created_at.desc()).all()
    
    def update_note(self, user_id: str, note_id: int, content: str = None,
                    title: str = None, tags: List[str] = None) -> Optional[Note]:
        """Update catatan"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()
        
        if note:
            if content:
                note.content = content
            if title:
                note.title = title
            if tags:
                note.tags = ",".join(tags)
            
            self.db.commit()
            self.db.refresh(note)
        
        return note
    
    def delete_note(self, user_id: str, note_id: int) -> bool:
        """Hapus catatan"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()
        
        if note:
            self.db.delete(note)
            self.db.commit()
            return True
        
        return False
    
    # ========== PRODUCTIVITY ANALYSIS ==========
    
    def get_productivity_score(self, user_id: str) -> Dict:
        """Hitung skor produktivitas berdasarkan task completion"""
        summary = self.get_task_summary(user_id)
        
        score = 0
        factors = []
        
        # Completion rate (50 points)
        if summary['completion_rate'] >= 80:
            score += 50
            factors.append("✅ Completion rate sangat baik")
        elif summary['completion_rate'] >= 60:
            score += 35
            factors.append("⚠️ Completion rate cukup baik")
        elif summary['completion_rate'] >= 40:
            score += 20
            factors.append("⚠️ Perlu peningkatan")
        else:
            score += 10
            factors.append("❌ Completion rate rendah")
        
        # No overdue tasks (30 points)
        if summary['overdue'] == 0:
            score += 30
            factors.append("✅ Tidak ada task overdue")
        elif summary['overdue'] <= 2:
            score += 15
            factors.append(f"⚠️ Ada {summary['overdue']} task overdue")
        else:
            score += 5
            factors.append(f"❌ Banyak task overdue ({summary['overdue']})")
        
        # Task volume (20 points)
        if summary['total'] >= 10:
            score += 20
            factors.append("✅ Aktif membuat task")
        elif summary['total'] >= 5:
            score += 10
            factors.append("⚠️ Task cukup banyak")
        else:
            score += 5
            factors.append("💡 Coba buat lebih banyak task")
        
        return {
            'score': min(100, score),
            'factors': factors,
            **summary
        }
    
    def get_daily_reminders(self, user_id: str) -> List[Dict]:
        """Dapatkan reminder untuk hari ini"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        # Task yang jatuh tempo hari ini
        due_today = self.db.query(Task).filter(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date >= today,
            Task.due_date < tomorrow
        ).all()
        
        # Task yang overdue
        overdue = self.get_overdue_tasks(user_id)
        
        reminders = []
        
        for task in overdue:
            days_overdue = (datetime.utcnow() - task.due_date).days
            reminders.append({
                'type': 'overdue',
                'task_id': task.id,
                'title': task.title,
                'message': f"🚨 OVERDUE: '{task.title}' sudah {days_overdue} hari melewati deadline!",
                'priority': 'high'
            })
        
        for task in due_today:
            reminders.append({
                'type': 'due_today',
                'task_id': task.id,
                'title': task.title,
                'message': f"⏰ Deadline hari ini: '{task.title}'",
                'priority': 'medium'
            })
        
        return reminders
