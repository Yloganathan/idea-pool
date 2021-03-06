import time
from idea_pool.db_api import query, execute

class Idea:
    def __init__(self, id, content, impact, ease, confidence, email=None):
        self.id = id
        self.content = content
        self.impact = impact
        self.ease = ease
        self.confidence = confidence
        self.average_score = sum([impact,ease,confidence])/3
        self.created_at = int(time.time())
        self.email = email

    @staticmethod
    def get_by_user(email):
        return query('select id, content, impact, ease, confidence, average_score, created_at from ideas where email = ? ORDER BY average_score DESC', [email])
    
    @staticmethod
    def get_by_id(id):
        return query('select id, content, impact, ease, confidence, average_score, created_at from ideas where id = ?', [id], one=True)

    @staticmethod
    def create(idea):   
        execute('INSERT INTO ideas (id, content, impact, ease, confidence, average_score, created_at, email) VALUES (?,?,?,?,?,?,?,?)',
                                (idea.id, idea.content, idea.impact, idea.ease, idea.confidence, idea.average_score, idea.created_at, idea.email))
        return Idea.get_by_id(idea.id)
    
    @staticmethod
    def update(idea):
        execute('UPDATE ideas set content = ?, impact = ?, ease = ?, confidence=?, average_score=? where id = ?',(idea.content, idea.impact, idea.ease, idea.confidence, idea.average_score, idea.id))
        return Idea.get_by_id(idea.id)
    
    @staticmethod
    def delete(id):
        execute('delete from ideas where id = ?',[id])
