// static/js/app.js - Main app functionality
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupUserMenu();
});

async function checkAuthStatus() {
    try {
        const response = await fetch('/auth/me');
        if (response.ok) {
            const user = await response.json();
            showAuthenticatedUI(user);
        } else {
            showGuestUI();
        }
    } catch (error) {
        showGuestUI();
    }
}

function showAuthenticatedUI(user) {
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');
    if (authLinks) authLinks.classList.add('hidden');
    if (userLinks) userLinks.classList.remove('hidden');
}

function showGuestUI() {
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');
    if (authLinks) authLinks.classList.remove('hidden');
    if (userLinks) userLinks.classList.add('hidden');
}

function setupUserMenu() {
    const menuBtn = document.getElementById('userMenuBtn');
    const dropdown = document.getElementById('userDropdown');
    
    if (menuBtn && dropdown) {
        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('hidden');
        });
        
        document.addEventListener('click', () => {
            dropdown.classList.add('hidden');
        });
    }
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await logout();
        });
    }
}

async function logout() {
    try {
        await fetch('/auth/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
    }
}