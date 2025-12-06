# routes/bookings.py
from flask import Blueprint, request, jsonify, session, render_template
from models import get_db
from datetime import datetime
import json

bookings_bp = Blueprint('bookings', __name__)

def calculate_nights(check_in, check_out):
    date_in = datetime.strptime(check_in, '%Y-%m-%d')
    date_out = datetime.strptime(check_out, '%Y-%m-%d')
    return (date_out - date_in).days

@bookings_bp.route('/bookings', methods=['POST'])
def create_booking():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json() if request.is_json else request.form
    
    # Get and validate data
    try:
        listing_id = int(data.get('listing_id')) if data.get('listing_id') else None
        guests = int(data.get('guests')) if data.get('guests') else None
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid listing_id or guests value'}), 400
    
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    contact_info = data.get('contact_info', '')
    
    # Validation
    if not all([listing_id, check_in, check_out, guests]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        if check_in_date >= check_out_date:
            return jsonify({'error': 'Check-out must be after check-in'}), 400
        
        if check_in_date < datetime.now():
            return jsonify({'error': 'Check-in cannot be in the past'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get listing
    cursor.execute('SELECT * FROM listings WHERE id = ?', (listing_id,))
    listing = cursor.fetchone()
    
    if not listing:
        conn.close()
        return jsonify({'error': 'Listing not found'}), 404
    
    if guests > listing['max_guests']:
        conn.close()
        return jsonify({'error': f'Maximum {listing["max_guests"]} guests allowed'}), 400
    
    # Check availability
    cursor.execute('''
        SELECT COUNT(*) as count FROM bookings
        WHERE listing_id = ? AND status = 'confirmed'
        AND (
            (check_in <= ? AND check_out > ?) OR
            (check_in < ? AND check_out >= ?) OR
            (check_in >= ? AND check_out <= ?)
        )
    ''', (listing_id, check_in, check_in, check_out, check_out, check_in, check_out))
    
    conflict = cursor.fetchone()
    if conflict['count'] > 0:
        conn.close()
        return jsonify({'error': 'Listing not available for selected dates'}), 409
    
    # Calculate total price
    nights = calculate_nights(check_in, check_out)
    subtotal = nights * listing['price_per_night']
    service_fee = subtotal * 0.14  # 14% service fee
    taxes = subtotal * 0.12  # 12% taxes
    total_price = subtotal + service_fee + taxes
    
    # Create booking
    cursor.execute('''
        INSERT INTO bookings (listing_id, user_id, check_in, check_out, guests, total_price, contact_info)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (listing_id, session['user_id'], check_in, check_out, guests, total_price, contact_info))
    
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'booking_id': booking_id,
        'total_price': round(total_price, 2),
        'breakdown': {
            'nights': nights,
            'price_per_night': listing['price_per_night'],
            'subtotal': round(subtotal, 2),
            'service_fee': round(service_fee, 2),
            'taxes': round(taxes, 2),
            'total': round(total_price, 2)
        }
    }), 201

@bookings_bp.route('/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT b.*, l.title, l.city, l.address,
               (SELECT image_path FROM listing_images WHERE listing_id = l.id ORDER BY display_order LIMIT 1) as image
        FROM bookings b
        JOIN listings l ON b.listing_id = l.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    ''', (user_id,))
    
    bookings = cursor.fetchall()
    conn.close()
    
    result = []
    for booking in bookings:
        result.append({
            'id': booking['id'],
            'listing_id': booking['listing_id'],
            'listing_title': booking['title'],
            'city': booking['city'],
            'address': booking['address'],
            'image': booking['image'] or '/static/images/placeholder.jpg',
            'check_in': booking['check_in'],
            'check_out': booking['check_out'],
            'guests': booking['guests'],
            'total_price': booking['total_price'],
            'status': booking['status'],
            'created_at': booking['created_at']
        })
    
    return jsonify(result), 200

@bookings_bp.route('/booking/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT b.*, l.title, l.city, l.address, l.price_per_night,
               (SELECT image_path FROM listing_images WHERE listing_id = l.id ORDER BY display_order LIMIT 1) as image
        FROM bookings b
        JOIN listings l ON b.listing_id = l.id
        WHERE b.id = ? AND b.user_id = ?
    ''', (booking_id, session['user_id']))
    
    booking = cursor.fetchone()
    conn.close()
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    nights = calculate_nights(booking['check_in'], booking['check_out'])
    subtotal = nights * booking['price_per_night']
    
    result = {
        'id': booking['id'],
        'listing_title': booking['title'],
        'city': booking['city'],
        'address': booking['address'],
        'image': booking['image'] or '/static/images/placeholder.jpg',
        'check_in': booking['check_in'],
        'check_out': booking['check_out'],
        'guests': booking['guests'],
        'total_price': booking['total_price'],
        'status': booking['status'],
        'created_at': booking['created_at'],
        'breakdown': {
            'nights': nights,
            'price_per_night': booking['price_per_night'],
            'subtotal': round(subtotal, 2)
        }
    }
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result), 200
    return render_template('booking_confirmation.html', booking=result)

@bookings_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if booking exists and belongs to user
    cursor.execute('''
        SELECT * FROM bookings 
        WHERE id = ? AND user_id = ?
    ''', (booking_id, session['user_id']))
    
    booking = cursor.fetchone()
    
    if not booking:
        conn.close()
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking['status'] == 'cancelled':
        conn.close()
        return jsonify({'error': 'Booking is already cancelled'}), 400
    
    # Check if booking is in the future
    from datetime import datetime
    check_in_date = datetime.strptime(booking['check_in'], '%Y-%m-%d')
    if check_in_date < datetime.now():
        conn.close()
        return jsonify({'error': 'Cannot cancel past bookings'}), 400
    
    # Cancel the booking
    cursor.execute('''
        UPDATE bookings 
        SET status = 'cancelled' 
        WHERE id = ?
    ''', (booking_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Booking cancelled successfully'
    }), 200