# Airbnb Clone MVP

A full-stack Airbnb clone with Flask backend, SQLite database, and responsive frontend.

## Features
- User authentication (signup/login)
- Browse and search listings
- View listing details with image carousel
- Book listings with date selection
- User dashboard with booking history
- Mock payment flow
- Responsive design

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Backend**: Flask (Python)
- **Database**: SQLite (PostgreSQL compatible schema)
- **Authentication**: bcrypt password hashing

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd airbnb-clone
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your SECRET_KEY
```

5. Initialize database:
```bash
python seed_data.py
```

6. Run the application:
```bash
flask run
```

7. Open browser to `http://localhost:5000`

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Test Accounts

- **User 1**: john@example.com / password123
- **User 2**: jane@example.com / password123
- **Host**: alice@example.com / password123

## Mock Payment

Use any test card format:
- Card: 4111111111111111
- Expiry: Any future date
- CVV: Any 3 digits

## Project Structure

```
airbnb-clone/
├── app.py              # Flask application entry point
├── config.py           # Configuration settings
├── models.py           # Database models
├── routes/             # API routes
│   ├── auth.py
│   ├── listings.py
│   └── bookings.py
├── static/             # Frontend files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # HTML templates
├── tests/              # Unit tests
├── seed_data.py        # Database seeding
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Landing page
- `GET /listings` - List/filter listings
- `GET /listings/<id>` - Listing details
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /bookings` - Create booking
- `GET /users/<id>/bookings` - User bookings
- `GET /api/availability/<listing_id>` - Check availability

## License

MIT