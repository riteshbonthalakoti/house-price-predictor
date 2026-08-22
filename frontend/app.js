document.addEventListener('DOMContentLoaded', async () => {
    // Defaulting to local dev URL. Will be updated before deployment.
    const API_BASE_URL = 'https://ritesh1918-house-price-api.loca.lt';
    
    let chartInstance = null;

    // Fetch Model Insights
    try {
        const response = await fetch(`${API_BASE_URL}/model-info`);
        if (response.ok) {
            const data = await response.json();
            renderChart(data.coefficients);
        }
    } catch (error) {
        console.error("Failed to load model insights:", error);
    }

    function renderChart(coefficients) {
        const ctx = document.getElementById('coefficientsChart').getContext('2d');
        
        const labels = Object.keys(coefficients).map(k => k.replace('_', ' ').toUpperCase());
        const data = Object.values(coefficients);
        
        const backgroundColors = data.map(val => 
            val > 0 ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)'
        );

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feature Importance (Coefficient)',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                }
            }
        });
    }

    // Handle form submission
    const form = document.getElementById('prediction-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = form.querySelector('.predict-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Predicting...';
        btn.disabled = true;
        
        const payload = {
            size_sqft: parseFloat(document.getElementById('size_sqft').value),
            bedrooms: parseInt(document.getElementById('bedrooms').value),
            bathrooms: parseInt(document.getElementById('bathrooms').value),
            age_years: parseInt(document.getElementById('age_years').value),
            location_score: parseInt(document.getElementById('location_score').value)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                
                // Animate value
                const priceElement = document.getElementById('predicted-price');
                const targetPrice = data.predicted_price_lakhs;
                animateValue(priceElement, 0, targetPrice, 1000);
                
                document.getElementById('confidence-note').textContent = data.model_confidence_note;
            } else {
                const err = await response.json();
                alert(`Error: ${JSON.stringify(err.detail)}`);
            }
        } catch (error) {
            console.error(error);
            alert("Failed to connect to the prediction API.");
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = (progress * (end - start) + start).toFixed(2);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
