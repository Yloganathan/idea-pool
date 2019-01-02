import json
import pytest

def test_user_signup(client):
    r = client.post('/users', json= {
                "email": "user2@gmail.com",
                "name":"testuser2",
                "password": "AAb1cdftr"
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['jwt'] is not None
    assert data['refresh_token'] is not None

invalid_signup = [
    ({}, 400),
    ({"email": "some", "password":"pass"}, 400),
    ({"user": "test", "password":"pass"}, 400),
    ({"user": "test", "email":"some"}, 400),
    ({"user": "test", "email":"some@domain.com", "password":"password"}, 400),
    ({"user": "test", "email":"some@domain.com", "password": "1Ac3d"}, 400),
    ({"user": "test", "email":"some@domain.com", "password": "1dffdc3d"}, 400),
    ({"user": "test", "email":"some@domain.com", "password": "AA122AAAA"}, 400),
    ({"user": "test", "email":"some@domain,com", "password": "AAb1cdftr"}, 400),
]

@pytest.mark.parametrize('data, status_code', invalid_signup)
def test_user_signup_400(client, data, status_code):
    r = client.post('/users', json=data)
    assert r.status_code == status_code

def test_user_login(client, current_user):
    r = client.post('/access-tokens', json= {
                "email": current_user['email'],
                "password": current_user['password']
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['jwt'] is not None
    assert data['refresh_token'] is not None

def test_user_login400(client):
    r = client.post('/access-tokens', json= {
                "email": "nonexistantuser@mail.com",
                "password": "abcxyz"
                })
    assert r.status_code == 400


def test_current_user_no_auth(client):
    r = client.get('/me')
    assert r.status_code == 401

def test_current_user(client, current_user):
    r = client.get('/me', headers={'x-access-token': current_user['jwt']}
                           )
    assert r.status_code ==  200
    data = json.loads(r.data)
    assert data['email'] == "testuser1@gmail.com"
    assert data['avatar_url'] is not None
    assert data['name'] is not None
    
    
def test_refresh_token_no_auth(client):
    r = client.post('/access-tokens/refresh')
    assert r.status_code == 401

def test_refresh_token(client, current_user):
    r = client.post('/access-tokens/refresh', headers={'x-access-token': current_user['refresh_token']})
    assert r.status_code ==  200
    data = json.loads(r.data)
    assert data['jwt'] is not None

def test_refresh_token_body(client, current_user):
    r = client.post('/access-tokens/refresh', json={'refresh_token': current_user['refresh_token']})
    assert r.status_code ==  200
    data = json.loads(r.data)
    assert data['jwt'] is not None

def test_user_logout(client):
    r = client.delete('/access-tokens')
    assert r.status_code == 401


def test_user_logout(client, current_user):
    r = client.delete('/access-tokens', headers={'x-access-token': current_user['jwt']}
                           )
    assert r.status_code == 204
    r = client.get('/me', headers={'x-access-token': current_user['jwt']}
                           )
    assert r.status_code == 401
    data = json.loads(r.data)
    assert data['msg'] ==  'Token has been revoked'

