# seed_data.py
import json
from models import init_db, get_db, hash_password

def seed_database():
    print("Initializing database...")
    init_db()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM reviews')
    cursor.execute('DELETE FROM bookings')
    cursor.execute('DELETE FROM listing_images')
    cursor.execute('DELETE FROM listings')
    cursor.execute('DELETE FROM users')
    
    print("Creating users...")
    users = [
        ('John Doe', 'john@example.com', 'password123'),
        ('Jane Smith', 'jane@example.com', 'password123'),
        ('Alice Johnson', 'alice@example.com', 'password123'),
    ]
    
    user_ids = []
    for name, email, password in users:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, hash_password(password))
        )
        user_ids.append(cursor.lastrowid)
    
    print("Creating listings...")
    listings = [
        {
            'title': 'Luxury Apartment in South Mumbai',
            'description': 'Stunning 3-bedroom apartment with sea view in the heart of South Mumbai. Walking distance to Gateway of India, Colaba Causeway, and Marine Drive. Features modern amenities, fully equipped kitchen, and breathtaking Arabian Sea views.',
            'city': 'Mumbai',
            'address': 'Nariman Point, Mumbai, Maharashtra',
            'host_id': user_ids[2],
            'price_per_night': 8500.0,
            'max_guests': 6,
            'amenities': json.dumps(['WiFi', 'Kitchen', 'Washer', 'Air conditioning', 'Sea view', 'Balcony'])
        },
        {
            'title': 'Heritage Haveli in Old Delhi',
            'description': 'Experience royal living in this beautifully restored 200-year-old haveli. Traditional Mughal architecture with modern comforts. Located in the historic lanes of Chandni Chowk, close to Red Fort and Jama Masjid.',
            'city': 'Delhi',
            'address': 'Chandni Chowk, Old Delhi, Delhi',
            'host_id': user_ids[2],
            'price_per_night': 6500.0,
            'max_guests': 8,
            'amenities': json.dumps(['WiFi', 'Traditional decor', 'Courtyard', 'Air conditioning', 'Heritage property'])
        },
        {
            'title': 'Beachfront Villa in Goa',
            'description': 'Wake up to the sound of waves in this stunning beachfront villa. Private beach access, infinity pool, and spacious deck. Perfect for a tropical getaway in North Goa.',
            'city': 'Goa',
            'address': 'Candolim Beach, North Goa, Goa',
            'host_id': user_ids[2],
            'price_per_night': 12000.0,
            'max_guests': 8,
            'amenities': json.dumps(['WiFi', 'Beach access', 'Swimming pool', 'BBQ area', 'Ocean view', 'Garden'])
        },
        {
            'title': 'Tech Hub Apartment in Koramangala',
            'description': 'Modern 2-bedroom apartment in the heart of Bangalore\'s startup district. Perfect for digital nomads and tech professionals. Close to cafes, coworking spaces, and restaurants.',
            'city': 'Bengaluru',
            'address': 'Koramangala 5th Block, Bengaluru, Karnataka',
            'host_id': user_ids[0],
            'price_per_night': 4500.0,
            'max_guests': 4,
            'amenities': json.dumps(['WiFi', 'Workspace', 'Kitchen', 'Air conditioning', 'Parking'])
        },
        {
            'title': 'Lakeside Cottage in Udaipur',
            'description': 'Romantic lakeside cottage with stunning views of Lake Pichola and City Palace. Traditional Rajasthani architecture with modern amenities. Perfect for couples and honeymooners.',
            'city': 'Udaipur',
            'address': 'Lake Pichola Road, Udaipur, Rajasthan',
            'host_id': user_ids[1],
            'price_per_night': 7500.0,
            'max_guests': 2,
            'amenities': json.dumps(['WiFi', 'Lake view', 'Balcony', 'Air conditioning', 'Traditional decor'])
        },
        {
            'title': 'Houseboat in Backwaters',
            'description': 'Experience Kerala\'s famous backwaters in this traditional houseboat. Includes all meals, private chef, and guided tours. Float through scenic canals surrounded by coconut groves.',
            'city': 'Alleppey',
            'address': 'Vembanad Lake, Alleppey, Kerala',
            'host_id': user_ids[2],
            'price_per_night': 15000.0,
            'max_guests': 4,
            'amenities': json.dumps(['WiFi', 'Meals included', 'Private chef', 'AC bedrooms', 'Boat deck'])
        },
        {
            'title': 'Colonial Bungalow in Darjeeling',
            'description': 'Charming British-era bungalow with panoramic views of Kanchenjunga. Surrounded by tea gardens, featuring a fireplace and beautiful garden. Perfect for a mountain retreat.',
            'city': 'Darjeeling',
            'address': 'Observatory Hill Road, Darjeeling, West Bengal',
            'host_id': user_ids[1],
            'price_per_night': 5500.0,
            'max_guests': 6,
            'amenities': json.dumps(['WiFi', 'Fireplace', 'Garden', 'Mountain view', 'Tea estate access'])
        },
        {
            'title': 'Modern Loft in IT Corridor',
            'description': 'Sleek and modern loft apartment in Hyderabad\'s HITEC City. Close to major IT companies, shopping malls, and restaurants. Perfect for business travelers and tech professionals.',
            'city': 'Hyderabad',
            'address': 'HITEC City, Hyderabad, Telangana',
            'host_id': user_ids[0],
            'price_per_night': 4000.0,
            'max_guests': 3,
            'amenities': json.dumps(['WiFi', 'Workspace', 'Gym access', 'Air conditioning', 'Parking'])
        },
        {
            'title': 'Riverside Cottage in Rishikesh',
            'description': 'Peaceful cottage on the banks of the holy Ganges. Perfect for yoga retreats and spiritual seekers. Walking distance to ashrams, yoga centers, and adventure sports.',
            'city': 'Rishikesh',
            'address': 'Tapovan, Rishikesh, Uttarakhand',
            'host_id': user_ids[1],
            'price_per_night': 3500.0,
            'max_guests': 4,
            'amenities': json.dumps(['WiFi', 'River view', 'Garden', 'Yoga space', 'Meditation area'])
        },
        {
            'title': 'French Quarter Studio',
            'description': 'Charming studio apartment in the French colonial quarter of Pondicherry. Colorful streets, cafes, and beaches nearby. Perfect blend of French and Tamil culture.',
            'city': 'Pondicherry',
            'address': 'White Town, Pondicherry, Puducherry',
            'host_id': user_ids[0],
            'price_per_night': 3000.0,
            'max_guests': 2,
            'amenities': json.dumps(['WiFi', 'Kitchen', 'Balcony', 'Air conditioning', 'Heritage building'])
        },
        {
            'title': 'Palace View Apartment in Jaipur',
            'description': 'Spacious apartment with stunning views of Hawa Mahal and City Palace. Located in the heart of Pink City, close to bazaars, forts, and restaurants.',
            'city': 'Jaipur',
            'address': 'Near Hawa Mahal, Jaipur, Rajasthan',
            'host_id': user_ids[2],
            'price_per_night': 5000.0,
            'max_guests': 5,
            'amenities': json.dumps(['WiFi', 'Palace view', 'Terrace', 'Air conditioning', 'Traditional decor'])
        },
        {
            'title': 'IT Park Modern Flat',
            'description': 'Contemporary 2-bedroom apartment near Pune IT parks. Ideal for professionals and families. Close to Phoenix Mall, restaurants, and entertainment zones.',
            'city': 'Pune',
            'address': 'Hinjewadi IT Park, Pune, Maharashtra',
            'host_id': user_ids[1],
            'price_per_night': 3800.0,
            'max_guests': 4,
            'amenities': json.dumps(['WiFi', 'Kitchen', 'Gym', 'Parking', 'Air conditioning'])
        },
        {
            'title': 'Himalayan Mountain Lodge',
            'description': 'Cozy mountain lodge with spectacular valley views in Manali. Perfect for adventure seekers and nature lovers. Close to skiing, trekking, and hot springs.',
            'city': 'Manali',
            'address': 'Old Manali, Himachal Pradesh',
            'host_id': user_ids[2],
            'price_per_night': 4500.0,
            'max_guests': 6,
            'amenities': json.dumps(['WiFi', 'Fireplace', 'Mountain view', 'Balcony', 'Parking'])
        },
        {
            'title': 'Beach Shack in Varkala',
            'description': 'Rustic beach shack with direct access to the famous Varkala cliff beach. Watch stunning sunsets, practice yoga, and enjoy fresh seafood. Perfect for beach lovers.',
            'city': 'Varkala',
            'address': 'North Cliff, Varkala, Kerala',
            'host_id': user_ids[0],
            'price_per_night': 2800.0,
            'max_guests': 3,
            'amenities': json.dumps(['WiFi', 'Beach access', 'Sea view', 'Hammock', 'Outdoor shower'])
        },
        {
            'title': 'Garden Villa in Coorg',
            'description': 'Beautiful villa surrounded by coffee plantations in the Scotland of India. Private garden, bonfire area, and stunning views. Perfect for family getaways.',
            'city': 'Coorg',
            'address': 'Madikeri, Coorg, Karnataka',
            'host_id': user_ids[1],
            'price_per_night': 6000.0,
            'max_guests': 7,
            'amenities': json.dumps(['WiFi', 'Garden', 'Bonfire area', 'Coffee plantation', 'Mountain view'])
        },
    ]
    
    listing_ids = []
    for listing in listings:
        cursor.execute('''
            INSERT INTO listings (title, description, city, address, host_id, price_per_night, max_guests, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            listing['title'],
            listing['description'],
            listing['city'],
            listing['address'],
            listing['host_id'],
            listing['price_per_night'],
            listing['max_guests'],
            listing['amenities']
        ))
        listing_ids.append(cursor.lastrowid)
    
    print("Adding listing images...")
    images = [
        # Mumbai Apartment
        (listing_ids[0], 'https://images.unsplash.com/photo-1567767292278-a4f21aa2d36e?w=800', 0),
        (listing_ids[0], 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800', 1),
        # Delhi Haveli
        (listing_ids[1], 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800', 0),
        (listing_ids[1], 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800', 1),
        # Goa Beach Villa
        (listing_ids[2], 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800', 0),
        (listing_ids[2], 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800', 1),
        # Bangalore Apartment
        (listing_ids[3], 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800', 0),
        (listing_ids[3], 'https://images.unsplash.com/photo-1502672260066-6bc35f0a63b9?w=800', 1),
        # Udaipur Cottage
        (listing_ids[4], 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800', 0),
        (listing_ids[4], 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800', 1),
        # Alleppey Houseboat
        (listing_ids[5], 'https://images.unsplash.com/photo-1605519171242-e91aca6da8ea?w=800', 0),
        (listing_ids[5], 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800', 1),
        # Darjeeling Bungalow
        (listing_ids[6], 'https://images.unsplash.com/photo-1542718610-a1d656d1884c?w=800', 0),
        (listing_ids[6], 'https://images.unsplash.com/photo-1586375300773-8384e3e4916f?w=800', 1),
        # Hyderabad Loft
        (listing_ids[7], 'https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=800', 0),
        (listing_ids[7], 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800', 1),
        # Rishikesh Cottage
        (listing_ids[8], 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800', 0),
        (listing_ids[8], 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800', 1),
        # Pondicherry Studio
        (listing_ids[9], 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800', 0),
        (listing_ids[9], 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800', 1),
        # Jaipur Apartment
        (listing_ids[10], 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800', 0),
        (listing_ids[10], 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800', 1),
        # Pune Flat
        (listing_ids[11], 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800', 0),
        (listing_ids[11], 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800', 1),
        # Manali Lodge
        (listing_ids[12], 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800', 0),
        (listing_ids[12], 'https://images.unsplash.com/photo-1542718610-a1d656d1884c?w=800', 1),
        # Varkala Beach Shack
        (listing_ids[13], 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800', 0),
        (listing_ids[13], 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800', 1),
        # Coorg Villa
        (listing_ids[14], 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800', 0),
        (listing_ids[14], 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800', 1),
    ]
    
    for listing_id, image_path, order in images:
        cursor.execute(
            'INSERT INTO listing_images (listing_id, image_path, display_order) VALUES (?, ?, ?)',
            (listing_id, image_path, order)
        )
    
    print("Creating sample bookings...")
    bookings = [
        (listing_ids[0], user_ids[0], '2024-12-15', '2024-12-18', 2, 25500.0),
        (listing_ids[2], user_ids[1], '2024-12-20', '2024-12-25', 4, 60000.0),
        (listing_ids[5], user_ids[0], '2025-01-10', '2025-01-12', 2, 30000.0),
    ]
    
    for listing_id, user_id, check_in, check_out, guests, total in bookings:
        cursor.execute('''
            INSERT INTO bookings (listing_id, user_id, check_in, check_out, guests, total_price, status)
            VALUES (?, ?, ?, ?, ?, ?, 'confirmed')
        ''', (listing_id, user_id, check_in, check_out, guests, total))
    
    print("Adding reviews...")
    reviews = [
        (listing_ids[0], user_ids[0], 5, 'Amazing place! Perfect location with stunning sea views. Highly recommended!'),
        (listing_ids[0], user_ids[1], 4, 'Great apartment in South Mumbai, would definitely stay again.'),
        (listing_ids[2], user_ids[1], 5, 'Incredible beachfront villa in Goa. The infinity pool and beach access were perfect!'),
        (listing_ids[3], user_ids[0], 5, 'Perfect location in Koramangala. Great for work and close to everything.'),
        (listing_ids[5], user_ids[1], 5, 'The houseboat experience was magical! Amazing food and beautiful backwaters.'),
        (listing_ids[4], user_ids[0], 5, 'Romantic lakeside cottage with breathtaking views of Udaipur. Perfect honeymoon spot!'),
        (listing_ids[6], user_ids[1], 4, 'Beautiful colonial bungalow with amazing tea garden views. Very peaceful.'),
        (listing_ids[10], user_ids[0], 5, 'Wonderful stay in Pink City! Could see Hawa Mahal from the terrace.'),
    ]
    
    for listing_id, user_id, rating, comment in reviews:
        cursor.execute(
            'INSERT INTO reviews (listing_id, user_id, rating, comment) VALUES (?, ?, ?, ?)',
            (listing_id, user_id, rating, comment)
        )
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database seeded successfully!")
    print("\nTest accounts:")
    print("  john@example.com / password123")
    print("  jane@example.com / password123")
    print("  alice@example.com / password123 (host)")

if __name__ == '__main__':
    seed_database()

