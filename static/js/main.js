
// Main JavaScript for Urban Climate Risk Predictor

document.addEventListener('DOMContentLoaded', function() {
    console.log('Urban Climate Risk Predictor - Application Loaded');
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    for (const tooltip of tooltips) {
        new bootstrap.Tooltip(tooltip);
    }
    
    // Function to format numbers with commas
    window.formatNumber = function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };
    
    // Temperature slider value display (predict.html)
    const tempSlider = document.getElementById('temp-slider');
    if (tempSlider) {
        const tempValue = document.getElementById('temp-value');
        const tempInput = document.getElementById('temp-input');
        
        tempSlider.addEventListener('input', function() {
            const value = parseFloat(tempSlider.value).toFixed(1);
            tempValue.textContent = value + '°C';
            tempInput.value = value;
        });
    }
});
