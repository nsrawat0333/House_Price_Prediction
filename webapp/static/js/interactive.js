// Additional interactive elements

document.addEventListener('DOMContentLoaded', function() {
    // Scroll progress indicator
    window.addEventListener('scroll', function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.querySelector('.scroll-progress-bar').style.width = scrolled + '%';
        
        // Show/hide back to top button
        const backToTopButton = document.getElementById('back-to-top');
        if (winScroll > 300) {
            backToTopButton.style.display = 'flex';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Back to top button functionality
    document.getElementById('back-to-top').addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Add hover effects for cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 123, 255, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // Add custom tooltip initialization
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        const tooltipSpan = document.createElement('span');
        tooltipSpan.className = 'tooltiptext';
        tooltipSpan.textContent = tooltipText;
        element.classList.add('custom-tooltip');
        element.appendChild(tooltipSpan);
    });
    
    // Feature hover effect
    document.querySelectorAll('.feature-icon').forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2) rotate(5deg)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0)';
        });
    });
});

// Add a typing animation effect to important headings
function initTypingAnimation() {
    const typingElements = document.querySelectorAll('.typing-animation');
    
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        
        let i = 0;
        const interval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(interval);
            }
        }, 100);
    });
}

// Add image comparison slider for before/after visualizations
function setupImageComparison() {
    const slider = document.querySelector('.img-comp-slider');
    if (!slider) return;
    
    const container = slider.parentElement;
    const imgBefore = container.querySelector('.img-comp-before');
    const imgAfter = container.querySelector('.img-comp-after');
    
    let isDown = false;
    
    slider.addEventListener('mousedown', () => {
        isDown = true;
    });
    
    window.addEventListener('mouseup', () => {
        isDown = false;
    });
    
    container.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percent = (x / rect.width) * 100;
        
        slider.style.left = percent + '%';
        imgBefore.style.width = percent + '%';
    });
}