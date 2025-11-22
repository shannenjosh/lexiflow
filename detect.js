// Detect functionality
document.addEventListener('DOMContentLoaded', () => {
    const detectBtn = document.getElementById('detectBtn');
    const detectText = document.getElementById('detectText');
    const charCount = document.getElementById('charCount');
    const fileUpload = document.getElementById('fileUpload');
    const loading = document.getElementById('loading');
    const errorMsg = document.getElementById('errorMsg');
    const results = document.getElementById('results');
    const copyBtn = document.getElementById('copyBtn');
    
    // Character counter
    detectText.addEventListener('input', () => {
        const count = detectText.value.length;
        charCount.textContent = count;
    });
    
    // File upload
    fileUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                detectText.value = event.target.result;
                charCount.textContent = detectText.value.length;
            };
            reader.readAsText(file);
        }
    });
    
    // Detect button click
    detectBtn.addEventListener('click', handleDetect);
    
    // Enter key to submit (Ctrl+Enter)
    detectText.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleDetect();
        }
    });
    
    // Copy button
    copyBtn.addEventListener('click', () => {
        const analysisDetails = document.getElementById('analysisDetails');
        const verdict = document.getElementById('verdict').textContent;
        const confidence = document.getElementById('confidenceValue').textContent;
        const text = `Verdict: ${verdict}\nConfidence: ${confidence}\n\nAnalysis:\n${analysisDetails.textContent}`;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = 'Copy Results';
            }, 2000);
        });
    });
    
    async function handleDetect() {
        const text = detectText.value.trim();
        
        // Validation
        if (!text) {
            showError('Please enter some text to analyze');
            return;
        }
        
        if (text.length < 50) {
            showError('Text must be at least 50 characters');
            return;
        }
        
        // Clear previous errors
        errorMsg.textContent = '';
        errorMsg.style.display = 'none';
        
        // Show loading
        loading.style.display = 'flex';
        results.style.display = 'none';
        detectBtn.disabled = true;
        detectBtn.textContent = 'Analyzing...';
        
        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                const text = await response.text();
                console.error('Non-JSON response:', text);
                throw new Error(`Server returned: ${text.substring(0, 100)}`);
            }
            
            const data = await response.json();
            
            if (!response.ok || data.error) {
                throw new Error(data.error || 'Failed to analyze text');
            }
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'Failed to analyze text. Please try again.');
        } finally {
            loading.style.display = 'none';
            detectBtn.disabled = false;
            detectBtn.textContent = 'Analyze Text';
        }
    }
    
    function displayResults(data) {
        // Update verdict
        const verdictEl = document.getElementById('verdict');
        verdictEl.textContent = data.isAI ? 'AI Generated' : 'Human Written';
        verdictEl.style.color = data.isAI ? '#e74c3c' : '#27ae60';
        
        // Update confidence
        document.getElementById('confidenceValue').textContent = data.confidence || 'Unknown';
        
        // Update confidence bar
        const confidenceFill = document.getElementById('confidenceFill');
        const aiProb = data.aiProbability || 50;
        confidenceFill.style.width = `${aiProb}%`;
        confidenceFill.textContent = `${aiProb}%`;
        confidenceFill.style.backgroundColor = aiProb > 70 ? '#e74c3c' : aiProb > 50 ? '#f39c12' : '#27ae60';
        
        // Update analysis details
        const analysisDetails = document.getElementById('analysisDetails');
        let detailsHTML = '';
        
        if (data.indicators && data.indicators.length > 0) {
            detailsHTML += '<strong>Key Indicators:</strong><ul>';
            data.indicators.forEach(indicator => {
                detailsHTML += `<li>${indicator}</li>`;
            });
            detailsHTML += '</ul>';
        }
        
        if (data.styleAnalysis) {
            detailsHTML += `<strong>Style Analysis:</strong><p>${data.styleAnalysis}</p>`;
        }
        
        analysisDetails.innerHTML = detailsHTML || '<p>No detailed analysis available</p>';
        
        // Show results
        results.style.display = 'block';
    }
    
    function showError(message) {
        errorMsg.textContent = '❌ ' + message;
        errorMsg.style.display = 'block';
        setTimeout(() => {
            errorMsg.style.display = 'none';
        }, 5000);
    }
});
