
# tests/test_auth.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
import sqlite3

@pytest.fixture
def client():
    # Import here to avoid circular imports
    from app import app
    from config import Config
    
    db_fd, db_path = tempfile.mkstemp()
    
    # Update BOTH app config AND Config class
    app.config['DATABASE_PATH'] = db_path
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    Config.DATABASE_PATH = db_path  # Important: Update the Config class too!
    
    # Initialize database with the test path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

def test_signup_success(client):
    response = client.post('/auth/signup', json={
        'name': 'New Test User',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    if response.status_code != 201:
        print(f"Error response: {response.get_json()}")
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] == True
    assert 'user' in data

def test_signup_duplicate_email(client):
    client.post('/auth/signup', json={
        'name': 'User One',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/signup', json={
        'name': 'User Two',
        'email': 'test@example.com',
        'password': 'password456'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_signup_invalid_email(client):
    response = client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'invalid-email',
        'password': 'password123'
    })
    assert response.status_code == 400

def test_signup_short_password(client):
    response = client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123'
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True

def test_login_wrong_password(client):
    client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_logout(client):
    client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/logout')
    assert response.status_code == 200
