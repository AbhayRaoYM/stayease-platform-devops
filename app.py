from flask import Flask, render_template, session,request
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from config import Config
from models import init_db
import time
import os

app = Flask(__name__)
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total App Requests',
    ['method','endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency'
)
app.config.from_object(Config)

# Initialize database
init_db()

# Register blueprints
from routes.auth import auth_bp
from routes.listings import listings_bp
from routes.bookings import bookings_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(listings_bp)
app.register_blueprint(bookings_bp)

@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path
    ).inc()

    REQUEST_LATENCY.observe(
        time.time() - request.start_time
    )

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {
        'Content-Type': CONTENT_TYPE_LATEST
    }



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)