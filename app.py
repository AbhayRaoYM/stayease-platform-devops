from flask import Flask, render_template, session
from prometheus_flask_exporter import PrometheusMetrics
from config import Config
from models import init_db
import os

app = Flask(__name__)
metrics=PrometheusMetrics(app)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)