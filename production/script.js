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
    
    // Header shrink on scroll
    const header = document.querySelector('.header');
    if (header) {
        let lastScroll = 0;
        const scrollThreshold = 50;
        
        function handleScroll() {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            
            if (currentScroll > scrollThreshold) {
                if (!header.classList.contains('header-compact')) {
                    header.classList.add('header-compact');
                }
            } else {
                if (header.classList.contains('header-compact')) {
                    header.classList.remove('header-compact');
                }
            }
            
            lastScroll = currentScroll;
        }
        
        // Throttle scroll events for performance
        let ticking = false;
        window.addEventListener('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(function() {
                    handleScroll();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }
    
    // Mobile hamburger menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    
    if (menuToggle && nav) {
        menuToggle.addEventListener('click', function() {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            nav.classList.toggle('menu-open');
            
            // Prevent body scroll when menu is open
            if (!isExpanded) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
        
        // Close menu when clicking on a nav link
        const navLinks = nav.querySelectorAll('.nav-link');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                menuToggle.setAttribute('aria-expanded', 'false');
                nav.classList.remove('menu-open');
                document.body.style.overflow = '';
            });
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && nav.classList.contains('menu-open')) {
                menuToggle.setAttribute('aria-expanded', 'false');
                nav.classList.remove('menu-open');
                document.body.style.overflow = '';
            }
        });
    }
    
});
