# tests/test_bookings.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import hash_password
import tempfile
import sqlite3
import json

@pytest.fixture
def client():
    # Import here to avoid issues
    from app import app
    from config import Config
    
    db_fd, db_path = tempfile.mkstemp()
    
    # Update BOTH app config AND Config class
    app.config['DATABASE_PATH'] = db_path
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    Config.DATABASE_PATH = db_path  # Important: Update the Config class too!
    
    # Create database and tables
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create all tables
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            host_id INTEGER NOT NULL,
            price_per_night REAL NOT NULL,
            max_guests INTEGER NOT NULL,
            amenities TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (host_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            guests INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'confirmed',
            contact_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (listing_id) REFERENCES listings (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert test data
    cursor.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Test User', 'test@example.com', hash_password('password123'))
    )
    user_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO listings (title, description, city, address, host_id, price_per_night, max_guests, amenities)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('Test Listing', 'Test description', 'Mumbai', '123 Test St, Mumbai', user_id, 5000.0, 4, '[]'))
    
    conn.commit()
    conn.close()
    
    with app.test_client() as client:
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)

def test_create_booking_success(client):
    # Login first
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"Login response: {login_response.status_code}, {login_response.get_json()}")
    
    response = client.post('/bookings', json={
        'listing_id': 1,
        'check_in': '2025-01-15',
        'check_out': '2025-01-18',
        'guests': 2
    })
    if response.status_code != 201:
        print(f"Booking error: {response.get_json()}")
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] == True
    assert 'booking_id' in data
    assert data['breakdown']['nights'] == 3

def test_create_booking_unauthorized(client):
    response = client.post('/bookings', json={
        'listing_id': 1,
        'check_in': '2025-01-15',
        'check_out': '2025-01-18',
        'guests': 2
    })
    assert response.status_code == 401

def test_create_booking_conflict(client):
    # Login
    client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # First booking
    client.post('/bookings', json={
        'listing_id': 1,
        'check_in': '2025-01-15',
        'check_out': '2025-01-18',
        'guests': 2
    })
    
    # Overlapping booking
    response = client.post('/bookings', json={
        'listing_id': 1,
        'check_in': '2025-01-16',
        'check_out': '2025-01-19',
        'guests': 2
    })
    assert response.status_code == 409

def test_check_availability(client):
    response = client.get('/api/availability/1?check_in=2025-02-01&check_out=2025-02-05')
    assert response.status_code == 200
    data = response.get_json()
    assert 'available' in data

def test_calculate_price(client):
    # Login
    client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/bookings', json={
        'listing_id': 1,
        'check_in': '2025-01-15',
        'check_out': '2025-01-20',
        'guests': 2
    })
    data = response.get_json()
    
    # 5 nights * ₹5000 = ₹25000
    # Service fee: ₹3500 (14%)
    # Taxes: ₹3000 (12%)
    # Total: ₹31500
    assert data['breakdown']['nights'] == 5
    assert data['breakdown']['subtotal'] == 25000.0
    assert data['breakdown']['total'] == 31500.0