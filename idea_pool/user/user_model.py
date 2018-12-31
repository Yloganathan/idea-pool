
import hashlib
import time
from idea_pool.db_api import query, execute

class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
        self.avatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() 
        self.created_at = int(time.time())

    @staticmethod
    def find_by_email(email):
        user = query('select email, name, password, avatar_url from users where email = ?',[email], one=True)
        return user
    
    @staticmethod
    def create(user):
        execute('INSERT INTO users (email,name,password,avatar_url, created_at) VALUES (?,?,?,?,?)',(user.email, user.name, user.password, user.avatar_url, user.created_at))
       
    @staticmethod
    def revoke_token(token):
        execute('INSERT INTO revoked_tokens(jti) VALUES (?)', [token])
    
    @staticmethod
    def get_revoked_token(token):
        return query('select * from revoked_tokens where jti = ?',[token], one=True)
 