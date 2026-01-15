// Simple authentication system for demo purposes
// In production, use a proper backend authentication system

// Demo user credentials (you can add more users here)
const DEMO_USERS = {
    'demo': 'demo2024',
    'client': 'client2024',
    'admin': 'admin2024'
};

// Check if user is already logged in
function checkAuth() {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    const username = sessionStorage.getItem('username');
    
    if (isLoggedIn === 'true' && username) {
        return true;
    }
    return false;
}

// Login form handler
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            
            // Validate credentials
            if (DEMO_USERS[username] && DEMO_USERS[username] === password) {
                // Successful login
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('username', username);
                sessionStorage.setItem('loginTime', new Date().toISOString());
                
                // Redirect to main page
                window.location.href = 'index.html';
            } else {
                // Failed login
                errorMessage.textContent = 'Invalid username or password. Please try again.';
                errorMessage.classList.add('show');
                
                // Clear password field
                document.getElementById('password').value = '';
                
                // Hide error after 5 seconds
                setTimeout(() => {
                    errorMessage.classList.remove('show');
                }, 5000);
            }
        });
    }
});

// Logout function
function logout() {
    sessionStorage.removeItem('isLoggedIn');
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('loginTime');
    window.location.href = 'login.html';
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { checkAuth, logout };
}

// Made with Bob
