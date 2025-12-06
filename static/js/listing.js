// static/js/listing.js - Listing detail page
document.addEventListener('DOMContentLoaded', () => {
    setupBookingForm();
    setupDateInputs();
});

function changeImage(imageSrc) {
    document.getElementById('mainImage').src = imageSrc;
}

function setupDateInputs() {
    const today = new Date().toISOString().split('T')[0];
    const checkInInput = document.querySelector('input[name="check_in"]');
    const checkOutInput = document.querySelector('input[name="check_out"]');
    
    if (checkInInput) {
        checkInInput.min = today;
        checkInInput.addEventListener('change', () => {
            if (checkOutInput) {
                const checkInDate = new Date(checkInInput.value);
                checkInDate.setDate(checkInDate.getDate() + 1);
                checkOutInput.min = checkInDate.toISOString().split('T')[0];
            }
        });
    }
}

function setupBookingForm() {
    const form = document.getElementById('bookingForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Check if user is logged in
        try {
            const authResponse = await fetch('/auth/me');
            if (!authResponse.ok) {
                // Save booking details and redirect to login
                const formData = new FormData(form);
                const bookingData = Object.fromEntries(formData);
                sessionStorage.setItem('pendingBooking', JSON.stringify(bookingData));
                window.location.href = '/auth/login?redirect=booking';
                return;
            }
        } catch (error) {
            alert('Please log in to make a booking');
            window.location.href = '/auth/login';
            return;
        }
        
        // Proceed with booking
        const formData = new FormData(form);
        const bookingData = Object.fromEntries(formData);
        
        try {
            // Check availability first
            const availResponse = await fetch(
                `/api/availability/${bookingData.listing_id}?check_in=${bookingData.check_in}&check_out=${bookingData.check_out}`
            );
            const availData = await availResponse.json();
            
            if (!availData.available) {
                alert('Sorry, this listing is not available for the selected dates.');
                return;
            }
            
            // Show mock payment
            const confirmed = await showPaymentModal(bookingData);
            if (!confirmed) return;
            
            // Create booking
            const response = await fetch('/bookings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bookingData)
            });
            
            if (response.ok) {
                const result = await response.json();
                window.location.href = `/booking/${result.booking_id}`;
            } else {
                const error = await response.json();
                alert(error.error || 'Booking failed. Please try again.');
            }
        } catch (error) {
            alert('An error occurred. Please try again.');
            console.error(error);
        }
    });
}

function showPaymentModal(bookingData) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5); display: flex; align-items: center;
            justify-content: center; z-index: 1000;
        `;
        
        modal.innerHTML = `
            <div style="background: white; padding: 32px; border-radius: 12px; max-width: 500px; width: 90%;">
                <h2 style="margin-bottom: 24px;">Payment Information</h2>
                <p style="margin-bottom: 16px; color: #666;">This is a mock payment. No real transaction will occur.</p>
                <form id="paymentForm">
                    <div style="margin-bottom: 16px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600;">Card Number</label>
                        <input type="text" placeholder="4111 1111 1111 1111" 
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px;">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600;">Expiry</label>
                            <input type="text" placeholder="MM/YY" 
                                   style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px;">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600;">CVV</label>
                            <input type="text" placeholder="123" 
                                   style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px;">
                        </div>
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button type="submit" style="flex: 1; padding: 12px; background: #FF385C; color: white; 
                                border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                            Confirm Payment
                        </button>
                        <button type="button" id="cancelPayment" style="flex: 1; padding: 12px; background: white; 
                                color: #222; border: 1px solid #ddd; border-radius: 8px; font-weight: 600; cursor: pointer;">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const paymentForm = modal.querySelector('#paymentForm');
        const cancelBtn = modal.querySelector('#cancelPayment');
        
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            document.body.removeChild(modal);
            resolve(true);
        });
        
        cancelBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
            resolve(false);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
                resolve(false);
            }
        });
    });
}
