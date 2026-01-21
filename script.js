// ============================================
// Minimal JavaScript for Static Site
// ============================================

// This file contains minimal JavaScript functionality
// The site works perfectly without JavaScript enabled

// Wait for the page to fully load before running any scripts
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for anchor links (if any are added in the future)
    // This is a nice-to-have enhancement, not required
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only prevent default if it's an anchor link (not empty hash)
            if (href !== '#') {
                const target = document.querySelector(href);
                
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Note: No other JavaScript is needed for this simple static site
    // All functionality is handled by HTML and CSS
    
});
