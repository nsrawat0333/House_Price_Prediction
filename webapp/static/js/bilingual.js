// Bilingual support script for House Price Prediction web app

document.addEventListener('DOMContentLoaded', function() {
    // Get the language toggle button
    const langToggleBtn = document.getElementById('language-toggle');
    
    // Check for language preference in local storage
    let currentLang = localStorage.getItem('preferredLanguage') || 'en';
    
    // Apply the language settings on load
    setLanguageDisplay(currentLang);
    
    // Add click event to the language toggle button
    if (langToggleBtn) {
        langToggleBtn.addEventListener('click', function() {
            // Toggle the language
            currentLang = currentLang === 'en' ? 'hi' : 'en';
            
            // Save preference
            localStorage.setItem('preferredLanguage', currentLang);
            
            // Apply the language settings
            setLanguageDisplay(currentLang);
            
            // Show feedback
            showLanguageChangeFeedback(currentLang);
        });
    }
    
    // Function to set language display
    function setLanguageDisplay(lang) {
        // Get all English and Hindi elements
        const enElements = document.querySelectorAll('.en');
        const hiElements = document.querySelectorAll('.hi');
        
        if (lang === 'en') {
            // Show English, hide Hindi
            enElements.forEach(el => {
                el.style.display = 'block';
                el.style.fontWeight = '500';
            });
            
            hiElements.forEach(el => {
                el.style.display = 'none';
            });
        } else {
            // Show Hindi, show smaller English
            enElements.forEach(el => {
                el.style.display = 'block';
                el.style.fontWeight = 'normal';
                el.style.fontSize = '0.8em';
                el.style.opacity = '0.7';
            });
            
            hiElements.forEach(el => {
                el.style.display = 'block';
                el.style.fontWeight = '500';
                el.style.fontSize = '1em';
            });
        }
        
        // Update button icon
        updateLanguageButtonIcon(lang);
    }
    
    // Function to update the language button icon
    function updateLanguageButtonIcon(lang) {
        const langToggleBtn = document.getElementById('language-toggle');
        if (!langToggleBtn) return;
        
        if (lang === 'en') {
            langToggleBtn.innerHTML = '<i class="fas fa-language"></i>';
            langToggleBtn.title = 'Switch to Hindi / हिंदी में बदलें';
        } else {
            langToggleBtn.innerHTML = 'अ';
            langToggleBtn.title = 'Switch to English / अंग्रेजी में बदलें';
        }
    }
    
    // Function to show language change feedback
    function showLanguageChangeFeedback(lang) {
        const feedbackDiv = document.createElement('div');
        feedbackDiv.style.position = 'fixed';
        feedbackDiv.style.top = '100px';
        feedbackDiv.style.right = '20px';
        feedbackDiv.style.padding = '10px 15px';
        feedbackDiv.style.backgroundColor = '#5e72e4';
        feedbackDiv.style.color = 'white';
        feedbackDiv.style.borderRadius = '4px';
        feedbackDiv.style.zIndex = '10000';
        feedbackDiv.style.boxShadow = '0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08)';
        feedbackDiv.style.opacity = '0';
        feedbackDiv.style.transition = 'opacity 0.3s ease-in-out';
        
        const message = lang === 'en' 
            ? 'Language changed to English' 
            : 'भाषा हिंदी में बदल गई';
            
        feedbackDiv.textContent = message;
        document.body.appendChild(feedbackDiv);
        
        // Fade in
        setTimeout(() => {
            feedbackDiv.style.opacity = '1';
        }, 10);
        
        // Fade out and remove
        setTimeout(() => {
            feedbackDiv.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(feedbackDiv);
            }, 300);
        }, 2000);
    }
});