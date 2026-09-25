import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    assert client.get('/health').json()['status']=='ok'

def test_register_login_home():
    email='test@example.com'
    r=client.post('/register',json={'email':email,'password':'password123'})
    assert r.status_code in (200,409)
    assert client.post('/login',json={'email':email,'password':'password123'}).status_code==200
    r=client.post('/generate-home',json={'budget':25000,'room_type':'Living Room','style':'modern','items':[{'category':'lighting','quantity':2}]})
    assert r.status_code==200
    assert r.json()['budget_used']<=r.json()['budget']
