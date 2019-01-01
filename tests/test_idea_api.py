import json
import pytest

def test_create_idea(client, current_user):
    r = client.post('/ideas',  headers={'x-access-token': current_user['jwt']}, 
                json= {
                    "content": "tuser1111nt",
                    "impact": 3,
                    "ease": 5,
                    "confidence": 6
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['id'] is not None
    assert data['content'] == "tuser1111nt"

invalid_idea = [
    ({}, 400),
    ({"content": "somecontent", "impact":9}, 400),
    ({"impact": "nonumber", "confidence":10}, 400),
    ({"content": "test", "impact":4, "ease": 5 }, 400)
]

@pytest.mark.parametrize('data, status_code', invalid_idea)
def test_create_idea_400(client, current_user, data, status_code):
    r = client.post('/users', headers={'x-access-token': current_user['jwt']}, json=data)
    assert r.status_code == status_code

def test_create_idea_401(client):
    r = client.post('/ideas',
                json= {
                    "content": "tuser1111nt",
                    "impact": 3,
                    "ease": 5,
                    "confidence": 6
                })
    assert r.status_code == 401

def test_update_idea(client, current_user):
    r = client.post('/ideas',  headers={'x-access-token': current_user['jwt']}, 
                json= {
                    "content": "tuser1111nt",
                    "impact": 3,
                    "ease": 5,
                    "confidence": 6
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    id = data['id']
    r = client.put(f'/ideas/{id}',  headers={'x-access-token': current_user['jwt']}, 
                json= {
                    "content": "changed_value",
                    "impact": 8,
                    "ease": 5,
                    "confidence": 6
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['id'] == id
    assert data['content'] == 'changed_value'
    assert data['impact'] == 8


def test_update_idea_400(client, current_user):
    r = client.put(f'/ideas/somerandomid',  headers={'x-access-token': current_user['jwt']}, 
                json= {
                    "content": "changed_value",
                    "impact": 8,
                    "ease": 5,
                    "confidence": 6
                })
    assert r.status_code == 400
  

def test_update_idea_401(client, current_user):
    r = client.put(f'/ideas/somerandomid', 
                json= {
                    "content": "changed_value",
                    "impact": 8,
                    "ease": 5,
                    "confidence": 6
                })
    assert r.status_code == 401

def test_delete_idea(client, current_user):
    r = client.post('/ideas',  headers={'x-access-token': current_user['jwt']}, 
                json= {
                    "content": "tobedeleted",
                    "impact": 3,
                    "ease": 5,
                    "confidence": 6
                })
    data = json.loads(r.data)
    assert r.status_code == 200
    id = data['id']
    r = client.delete(f'/ideas/{id}',  headers={'x-access-token': current_user['jwt']})
    assert r.status_code == 204

def test_delete_idea_400(client, current_user):
    r = client.delete(f'/ideas/somerandomid',  headers={'x-access-token': current_user['jwt']})
    assert r.status_code == 400

def test_delete_idea_401(client, current_user):
    r = client.delete(f'/ideas/somerandomid')
    assert r.status_code == 401