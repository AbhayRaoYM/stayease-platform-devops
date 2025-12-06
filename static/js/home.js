// static/js/home.js - Homepage functionality
document.addEventListener('DOMContentLoaded', () => {
    loadListings();
    setupSearchForm();
});

async function loadListings(params = {}) {
    const spinner = document.getElementById('loadingSpinner');
    const grid = document.getElementById('listingsGrid');
    
    spinner.classList.remove('hidden');
    
    try {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`/listings?${queryString}`, {
            headers: { 'Accept': 'application/json' }
        });
        const listings = await response.json();
        
        displayListings(listings);
    } catch (error) {
        grid.innerHTML = '<p>Error loading listings. Please try again.</p>';
    } finally {
        spinner.classList.add('hidden');
    }
}

function displayListings(listings) {
    const grid = document.getElementById('listingsGrid');
    
    if (listings.length === 0) {
        grid.innerHTML = '<p>No listings found. Try adjusting your search.</p>';
        return;
    }
    
    grid.innerHTML = listings.map(listing => `
        <a href="/listings/${listing.id}" class="listing-card">
            <img src="${listing.image}" alt="${listing.title}" class="listing-image">
            <div class="listing-info">
                <h3>${listing.title}</h3>
                <p class="listing-location">${listing.city}</p>
                ${listing.avg_rating ? `
                    <p class="listing-rating">⭐ ${listing.avg_rating} (${listing.review_count})</p>
                ` : ''}
                <p class="listing-price">₹${listing.price_per_night} / night</p>
            </div>
        </a>
    `).join('');
}

function setupSearchForm() {
    const form = document.getElementById('searchForm');
    if (!form) return;
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const params = {};
        
        for (let [key, value] of formData.entries()) {
            if (value) params[key] = value;
        }
        
        loadListings(params);
    });
}