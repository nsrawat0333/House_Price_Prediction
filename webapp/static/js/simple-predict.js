// Simple inline prediction animation
function animatePredictionResult(formattedPrice) {
    const resultElement = document.getElementById('prediction-result');
    const priceElement = document.getElementById('price-value');
    
    if (!resultElement || !priceElement) return;
    
    // Make sure the element is visible
    resultElement.classList.remove('d-none');
    
    // Scroll to result
    resultElement.scrollIntoView({ behavior: 'smooth' });
    
    // Get the numeric value
    let finalPrice = 0;
    try {
        finalPrice = parseFloat(formattedPrice.replace(/[^0-9.-]+/g, ''));
    } catch(e) {
        finalPrice = 0;
    }
    
    // Check if value is valid
    if (isNaN(finalPrice) || finalPrice <= 0) {
        priceElement.textContent = formattedPrice;
        return;
    }
    
    // Animate counting up
    let currentPrice = 0;
    const duration = 1500; // ms
    const interval = 30; // ms
    const steps = duration / interval;
    const increment = finalPrice / steps;
    
    const counter = setInterval(() => {
        currentPrice += increment;
        if (currentPrice >= finalPrice) {
            currentPrice = finalPrice;
            clearInterval(counter);
        }
        priceElement.textContent = '$' + currentPrice.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }, interval);
    
    // Add highlight effect to the card
    resultElement.style.transition = "box-shadow 0.3s";
    resultElement.style.boxShadow = "0 0 20px rgba(94, 114, 228, 0.8)";
    
    setTimeout(() => {
        resultElement.style.boxShadow = "";
    }, 2000);
}

// Add to form submission event
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            
            // Update button
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Predicting...';
            submitBtn.disabled = true;
            
            // Send prediction request
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Reset button
                submitBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Predict House Price';
                submitBtn.disabled = false;
                
                // Show result
                if (data.success) {
                    animatePredictionResult(data.formatted_prediction);
                } else {
                    const resultElement = document.getElementById('prediction-result');
                    resultElement.classList.remove('d-none');
                    document.getElementById('price-value').textContent = 'Error: ' + data.error;
                    resultElement.scrollIntoView({ behavior: 'smooth' });
                }
            })
            .catch(error => {
                // Reset button
                submitBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Predict House Price';
                submitBtn.disabled = false;
                
                // Show error
                const resultElement = document.getElementById('prediction-result');
                resultElement.classList.remove('d-none');
                document.getElementById('price-value').textContent = 'Error: Something went wrong';
                resultElement.scrollIntoView({ behavior: 'smooth' });
                console.error('Error:', error);
            });
        });
    }
});