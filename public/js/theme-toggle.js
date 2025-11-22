// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    const html = document.documentElement;
    
    // Get saved theme from localStorage or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme
    if (savedTheme === 'dark') {
        html.setAttribute('data-theme', 'dark');
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
    }
    
    // Theme toggle functionality
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-theme');
            
            if (currentTheme === 'dark') {
                // Switch to light mode
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            } else {
                // Switch to dark mode
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            }
        });
    }
    
    // Optional: System preference detection
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Apply system preference only if no saved preference
    if (!localStorage.getItem('theme') && prefersDark.matches) {
        html.setAttribute('data-theme', 'dark');
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
    }
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        // Only apply if user hasn't explicitly set a preference
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                html.setAttribute('data-theme', 'dark');
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            } else {
                html.setAttribute('data-theme', 'light');
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            }
        }
    });
});