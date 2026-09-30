import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import HomeRequest, JewelryRequest, PartyRequest
from app.services.recommendations import home, jewelry, make_search_url, party
from unittest.mock import patch
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

def test_planner_recommendations_use_search_links():
    with patch('app.services.recommendations.gemini.generate', return_value=None):
        home_result = home(HomeRequest(budget=5000, room_type='Living Room', style='modern', items=[{'category':'lighting'}]))
        party_result = party(PartyRequest(budget=20000, guests=30, event_type='Birthday', city='Pune'))
        jewelry_result = jewelry(JewelryRequest(budget=5000, occasion='Wedding', style='elegant'))

    assert 'amazon.in/s?k=Minimalist+LED+Ceiling+Light' in home_result.recommendations[0].url
    party_rec = next(item for item in party_result.recommendations if item.platform == 'Swiggy')
    assert party_rec.url == 'https://www.swiggy.com/search?query=Party+Food+Package'
    jewelry_rec = next(item for item in jewelry_result.recommendations if item.platform == 'Amazon')
    assert jewelry_rec.url == 'https://www.amazon.in/s?k=Elegant+Stud+Earrings'
    assert make_search_url('Zomato', 'Vegetarian Catering Package') == 'https://www.zomato.com/search?query=Vegetarian+Catering+Package'
    assert make_search_url('OYO', 'Budget Event Venue') == 'https://www.oyorooms.com/search?location=Budget+Event+Venue'
