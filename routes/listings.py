# routes/listings.py
from flask import Blueprint, request, jsonify, render_template
from models import get_db
from datetime import datetime
import json

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/listings', methods=['GET'])
def get_listings():
    # Get query parameters
    location = request.args.get('location', '').strip()
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    guests = request.args.get('guests', type=int)
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query
    query = '''
        SELECT l.*, 
               (SELECT image_path FROM listing_images WHERE listing_id = l.id ORDER BY display_order LIMIT 1) as image,
               (SELECT AVG(rating) FROM reviews WHERE listing_id = l.id) as avg_rating,
               (SELECT COUNT(*) FROM reviews WHERE listing_id = l.id) as review_count
        FROM listings l
        WHERE 1=1
    '''
    params = []
    
    if location:
        query += ' AND (LOWER(l.city) LIKE ? OR LOWER(l.address) LIKE ? OR LOWER(l.title) LIKE ?)'
        search_term = f'%{location.lower()}%'
        params.extend([search_term, search_term, search_term])
    
    if guests:
        query += ' AND l.max_guests >= ?'
        params.append(guests)
    
    if price_min is not None:
        query += ' AND l.price_per_night >= ?'
        params.append(price_min)
    
    if price_max is not None:
        query += ' AND l.price_per_night <= ?'
        params.append(price_max)
    
    # Check availability if dates provided
    if check_in and check_out:
        query += '''
            AND l.id NOT IN (
                SELECT listing_id FROM bookings
                WHERE status = 'confirmed'
                AND (
                    (check_in <= ? AND check_out > ?) OR
                    (check_in < ? AND check_out >= ?) OR
                    (check_in >= ? AND check_out <= ?)
                )
            )
        '''
        params.extend([check_in, check_in, check_out, check_out, check_in, check_out])
    
    query += ' ORDER BY l.created_at DESC'
    
    cursor.execute(query, params)
    listings = cursor.fetchall()
    conn.close()
    
    result = []
    for listing in listings:
        result.append({
            'id': listing['id'],
            'title': listing['title'],
            'city': listing['city'],
            'price_per_night': listing['price_per_night'],
            'max_guests': listing['max_guests'],
            'image': listing['image'] or '/static/images/placeholder.jpg',
            'avg_rating': round(listing['avg_rating'], 1) if listing['avg_rating'] else None,
            'review_count': listing['review_count']
        })
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result), 200
    return render_template('listings.html', listings=result)

@listings_bp.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_details(listing_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Get listing
    cursor.execute('SELECT * FROM listings WHERE id = ?', (listing_id,))
    listing = cursor.fetchone()
    
    if not listing:
        conn.close()
        return jsonify({'error': 'Listing not found'}), 404
    
    # Get images
    cursor.execute(
        'SELECT image_path FROM listing_images WHERE listing_id = ? ORDER BY display_order',
        (listing_id,)
    )
    images = [row['image_path'] for row in cursor.fetchall()]
    
    # Get reviews
    cursor.execute('''
        SELECT r.*, u.name as user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.listing_id = ?
        ORDER BY r.created_at DESC
    ''', (listing_id,))
    reviews = cursor.fetchall()
    
    # Get host info
    cursor.execute('SELECT id, name FROM users WHERE id = ?', (listing['host_id'],))
    host = cursor.fetchone()
    
    conn.close()
    
    result = {
        'id': listing['id'],
        'title': listing['title'],
        'description': listing['description'],
        'city': listing['city'],
        'address': listing['address'],
        'price_per_night': listing['price_per_night'],
        'max_guests': listing['max_guests'],
        'amenities': json.loads(listing['amenities']) if listing['amenities'] else [],
        'images': images if images else ['/static/images/placeholder.jpg'],
        'host': {'id': host['id'], 'name': host['name']} if host else None,
        'reviews': [
            {
                'id': r['id'],
                'user_name': r['user_name'],
                'rating': r['rating'],
                'comment': r['comment'],
                'created_at': r['created_at']
            }
            for r in reviews
        ],
        'avg_rating': sum(r['rating'] for r in reviews) / len(reviews) if reviews else None,
        'review_count': len(reviews)
    }
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result), 200
    return render_template('listing_detail.html', listing=result)

@listings_bp.route('/api/availability/<int:listing_id>', methods=['GET'])
def check_availability(listing_id):
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    
    if not check_in or not check_out:
        return jsonify({'error': 'check_in and check_out required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check for conflicts
    cursor.execute('''
        SELECT COUNT(*) as count FROM bookings
        WHERE listing_id = ? AND status = 'confirmed'
        AND (
            (check_in <= ? AND check_out > ?) OR
            (check_in < ? AND check_out >= ?) OR
            (check_in >= ? AND check_out <= ?)
        )
    ''', (listing_id, check_in, check_in, check_out, check_out, check_in, check_out))
    
    result = cursor.fetchone()
    conn.close()
    
    available = result['count'] == 0
    return jsonify({'available': available}), 200

