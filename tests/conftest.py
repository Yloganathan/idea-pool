import pytest
import json
from idea_pool import create_app
from idea_pool.db_api import execute

@pytest.fixture(scope='module')
def client():
    app = create_app('config.TestConfig')
    with app.app_context():
        yield app.test_client()

        execute("delete from users where name like '%test%'")
        execute("delete from ideas where content like '%test%'")
        execute("delete from revoked_tokens")


test_current_user = 'testuser1@gmail.com'
test_current_password = 'abcxyz'

@pytest.fixture(scope='module')
def current_user(client):
    execute('INSERT INTO users (email,name,password,avatar_url, created_at) VALUES (?,?,?,?,?)',
                (test_current_user, 'testexistingname', 'abcxyz'.encode('utf-8'), 'avatar_url', 342454632))
    login_req = client.post('/access-tokens', json= {
                "email": test_current_user,
                "password": test_current_password
                })
    result =  json.loads(login_req.data)
    result['email'] = test_current_user
    result['password'] = test_current_password
    return result
