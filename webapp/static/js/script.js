// Custom JavaScript for House Price Prediction Web App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Initialize animated elements
    animateOnScroll();
    
    // Custom range sliders with bubbles
    setupRangeSliders();
    
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Update URL hash without jumping
                history.pushState(null, null, targetId);
            }
        });
    });
    
    // Highlight active nav item based on scroll position
    function setActiveNavItem() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.clientHeight;
            const sectionId = section.getAttribute('id');
            
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    // Setup range sliders with bubbles
    function setupRangeSliders() {
        document.querySelectorAll('input[type="range"]').forEach(slider => {
            // Create wrapper if not already wrapped
            if (!slider.parentElement.classList.contains('custom-range-wrapper')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'custom-range-wrapper';
                slider.parentNode.insertBefore(wrapper, slider);
                wrapper.appendChild(slider);
                
                // Create bubble
                const bubble = document.createElement('div');
                bubble.className = 'range-value-bubble';
                bubble.innerHTML = slider.value;
                wrapper.appendChild(bubble);
                
                // Position bubble on load
                const newPosition = (slider.value - slider.min) / (slider.max - slider.min);
                const newLeft = newPosition * (slider.offsetWidth - 15) + 7;
                bubble.style.left = `${newLeft}px`;
                
                // Update bubble on input
                slider.addEventListener('input', function() {
                    bubble.innerHTML = this.value;
                    const position = (this.value - this.min) / (this.max - this.min);
                    const leftPosition = position * (this.offsetWidth - 15) + 7;
                    bubble.style.left = `${leftPosition}px`;
                });
            }
        });
    }
    
    // Animate elements when they come into view
    function animateOnScroll() {
        const elements = document.querySelectorAll('.card, .col-md-6, h2, .btn-lg');
        
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        elements.forEach(element => {
            observer.observe(element);
        });
    }
    
    window.addEventListener('scroll', setActiveNavItem);
});

// Form validation functions
function validateNumberInput(input, min, max) {
    const value = parseFloat(input.value);
    if (isNaN(value) || value < min || value > max) {
        input.classList.add('is-invalid');
        return false;
    } else {
        input.classList.remove('is-invalid');
        return true;
    }
}

// Apply number validation to all number inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
    const min = parseFloat(input.getAttribute('min') || -Infinity);
    const max = parseFloat(input.getAttribute('max') || Infinity);
    
    input.addEventListener('change', function() {
        validateNumberInput(this, min, max);
    });
});

// Make the prediction result more interactive with animation and sound
function showPredictionResult(price) {
    const resultElement = document.getElementById('prediction-result');
    const priceElement = document.getElementById('price-value');
    
    // Make sure the element is visible
    resultElement.classList.remove('d-none');
    
    // Scroll to result
    resultElement.scrollIntoView({ behavior: 'smooth' });
    
    // Animate the price counting up
    const finalPrice = parseFloat(price.replace(/[^0-9.-]+/g, ''));
    const duration = 1500; // 1.5 seconds
    const frameRate = 60;
    const frameDuration = 1000 / frameRate;
    const frames = duration / frameDuration;
    const increment = finalPrice / frames;
    
    let currentPrice = 0;
    const counter = setInterval(() => {
        currentPrice += increment;
        if (currentPrice > finalPrice) {
            currentPrice = finalPrice;
            clearInterval(counter);
        }
        priceElement.textContent = '$' + currentPrice.toLocaleString('en-US', { maximumFractionDigits: 2 });
    }, frameDuration);
    
    // Play a success sound (only if the user has interacted with the page)
    try {
        const audio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3');
        audio.volume = 0.3;
        audio.play().catch(e => console.log('Audio could not be played', e));
    } catch (e) {
        console.log('Audio playback error', e);
    }
    
    // Add a confetti effect
    addConfetti();
}

// Simple confetti effect
function addConfetti() {
    const confettiCount = 100;
    const container = document.body;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.zIndex = '9999';
        confetti.style.width = Math.random() * 10 + 5 + 'px';
        confetti.style.height = Math.random() * 10 + 5 + 'px';
        confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
        confetti.style.borderRadius = '50%';
        confetti.style.opacity = Math.random();
        confetti.style.left = Math.random() * window.innerWidth + 'px';
        confetti.style.top = -20 + 'px';
        
        container.appendChild(confetti);
        
        // Animate the confetti
        const animation = confetti.animate([
            { transform: `translateY(0) rotate(0deg)`, opacity: 1 },
            { transform: `translateY(${window.innerHeight}px) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: Math.random() * 3000 + 2000,
            easing: 'cubic-bezier(0, .9, .57, 1)',
            delay: Math.random() * 2000
        });
        
        animation.onfinish = () => confetti.remove();
    }
}