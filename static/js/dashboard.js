
// static/js/dashboard.js - User dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadUserBookings();
});

async function loadUserBookings() {
    const spinner = document.getElementById('loadingSpinner');
    const container = document.getElementById('bookingsContainer');
    
    try {
        const authResponse = await fetch('/auth/me');
        if (!authResponse.ok) {
            window.location.href = '/auth/login';
            return;
        }
        
        const user = await authResponse.json();
        const response = await fetch(`/users/${user.id}/bookings`);
        const bookings = await response.json();
        
        spinner.classList.add('hidden');
        
        if (bookings.length === 0) {
            container.innerHTML = '<p>You have no bookings yet.</p>';
            return;
        }
        
        container.innerHTML = bookings.map(booking => {
            const checkIn = new Date(booking.check_in);
            const today = new Date();
            const isPast = checkIn < today;
            const isCancelled = booking.status === 'cancelled';
            
            return `
                <div class="booking-item">
                    <img src="${booking.image}" alt="${booking.listing_title}">
                    <div>
                        <h3>${booking.listing_title}</h3>
                        <p>${booking.city}</p>
                        <p><strong>Check-in:</strong> ${booking.check_in}</p>
                        <p><strong>Check-out:</strong> ${booking.check_out}</p>
                        <p><strong>Guests:</strong> ${booking.guests}</p>
                        <p><strong>Total:</strong> ₹${booking.total_price.toFixed(2)}</p>
                        <div style="display: flex; gap: 10px; align-items: center; margin-top: 10px;">
                            <span class="booking-status ${isCancelled ? 'cancelled' : ''}">${
                                isCancelled ? 'Cancelled' : (isPast ? 'Completed' : 'Upcoming')
                            }</span>
                            ${!isPast && !isCancelled ? `
                                <button onclick="cancelBooking(${booking.id})" class="btn-cancel">
                                    Cancel Booking
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        spinner.classList.add('hidden');
        container.innerHTML = '<p>Error loading bookings.</p>';
    }
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/bookings/${bookingId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('Booking cancelled successfully!');
            loadUserBookings(); // Reload bookings
        } else {
            alert(result.error || 'Failed to cancel booking');
        }
    } catch (error) {
        alert('An error occurred while cancelling the booking');
        console.error(error);
    }
}