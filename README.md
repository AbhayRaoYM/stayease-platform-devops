# StayEase – Airbnb Clone MVP

A full-stack Airbnb clone with Flask backend, SQLite database, and responsive frontend — integrated with a complete CI/CD pipeline using Docker, Jenkins, GitHub Webhooks, and Prometheus.

# Features

User authentication (signup/login)
Browse and search listings
View listing details with image carousel
Book listings with date selection
User dashboard with booking history
Mock payment flow
Responsive design


# Tech Stack

Frontend: HTML5, CSS3, Vanilla JavaScript (ES6+)
Backend: Flask (Python)
Database: SQLite (PostgreSQL compatible schema)
Authentication: bcrypt password hashing
Containerization: Docker
CI/CD: Jenkins
Image Registry: Docker Hub
Tunnel: ngrok
Monitoring: Prometheus


# Setup Instructions

## Prerequisites

Python 3.8+
pip


## Installation


Clone the repository:


bashgit clone <repository-url>
cd airbnb-clone


Create virtual environment:


bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:


bashpip install -r requirements.txt


Set up environment variables:


bashcp .env.example .env
# Edit .env with your SECRET_KEY


Initialize database:


bashpython seed_data.py


Run the application:


bashflask run


Open browser to http://localhost:5000



🐳 Docker Quick Start

Prefer running via Docker without the full pipeline?

bashdocker build -t stayease .
docker run -p 5000:5000 stayease

App will be live at http://localhost:5000


⚙️ DevOps Pipeline Setup

Follow these steps to get the full CI/CD pipeline running locally.

Prerequisites


Docker
Jenkins
ngrok
A Docker Hub account


1. Set Up Jenkins

Install Jenkins (Ubuntu):

bashsudo apt update && sudo apt install -y openjdk-17-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update && sudo apt install -y jenkins
sudo systemctl start jenkins

Access Jenkins at http://localhost:8080 and complete the setup wizard.

Install required plugins (Manage Jenkins → Plugins):


Git Plugin
Docker Pipeline
GitHub Integration Plugin


Create a Pipeline job:


New Item → Pipeline → OK
Pipeline Definition → Pipeline script from SCM
SCM → Git → paste your repo URL
Script Path → Jenkinsfile
Save


2. Add Docker Hub Credentials


Manage Jenkins → Credentials → Global → Add Credentials
Kind: Username with password
ID: dockerhub-credentials
Enter your Docker Hub username and password → Save


3. Set Up ngrok

bashngrok http 8080

Copy the forwarding URL (e.g. https://abc123.ngrok.io) — you'll need it for the webhook.


⚠️ Free ngrok URLs change every session. Update the webhook URL each time you restart ngrok.



4. Configure GitHub Webhook


GitHub repo → Settings → Webhooks → Add webhook
Payload URL: https://abc123.ngrok.io/github-webhook/
Content type: application/json
Trigger: Just the push event → Save


Every push to the repo will now automatically trigger the Jenkins pipeline.

5. Set Up Prometheus

Create prometheus.yml:

yamlglobal:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'stayease'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'

Run Prometheus:

bashdocker run -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

Access Prometheus at http://localhost:9090

Pipeline Flow

Git Push → GitHub Webhook → ngrok → Jenkins
  └── Checkout code
  └── Build Docker image
  └── Push to Docker Hub
  └── Stop old container
  └── Deploy new container → Prometheus Monitoring


Testing

Run tests with pytest:

bashpytest tests/

Test Accounts


User 1: john@example.com / password123
User 2: jane@example.com / password123
Host: alice@example.com / password123


Mock Payment

Use any test card format:


Card: 4111111111111111
Expiry: Any future date
CVV: Any 3 digits


Project Structure

stayease/
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
├── Dockerfile          # Container build instructions
├── Jenkinsfile         # CI/CD pipeline definition
├── prometheus.yml      # Prometheus scrape config
├── requirements.txt
└── README.md

API Endpoints


GET / - Landing page
GET /listings - List/filter listings
GET /listings/<id> - Listing details
POST /auth/signup - User registration
POST /auth/login - User login
POST /auth/logout - User logout
POST /bookings - Create booking
GET /users/<id>/bookings - User bookings
GET /api/availability/<listing_id> - Check availability