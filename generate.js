// Generate functionality
document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const regenerateBtn = document.getElementById('regenerateBtn');
    const promptText = document.getElementById('promptText');
    const toneSelect = document.getElementById('toneSelect');
    const lengthSelect = document.getElementById('lengthSelect');
    const tempSlider = document.getElementById('tempSlider');
    const tempValue = document.getElementById('tempValue');
    const loading = document.getElementById('loading');
    const errorMsg = document.getElementById('errorMsg');
    const results = document.getElementById('results');
    const copyBtn = document.getElementById('copyBtn');
    
    // Update temperature display
    tempSlider.addEventListener('input', () => {
        tempValue.textContent = tempSlider.value;
    });
    
    // Generate button click
    generateBtn.addEventListener('click', handleGenerate);
    
    // Regenerate button click
    regenerateBtn.addEventListener('click', handleGenerate);
    
    // Enter key to submit (Ctrl+Enter)
    promptText.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleGenerate();
        }
    });
    
    // Copy button
    copyBtn.addEventListener('click', () => {
        const generatedText = document.getElementById('generatedText');
        const text = generatedText.textContent;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = 'Copy Text';
            }, 2000);
        });
    });
    
    async function handleGenerate() {
        const prompt = promptText.value.trim();
        
        // Validation
        if (!prompt) {
            showError('Please enter a prompt');
            return;
        }
        
        if (prompt.length < 10) {
            showError('Prompt must be at least 10 characters');
            return;
        }
        
        // Clear previous errors
        errorMsg.textContent = '';
        errorMsg.style.display = 'none';
        
        // Show loading
        loading.style.display = 'flex';
        results.style.display = 'none';
        generateBtn.disabled = true;
        regenerateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: prompt,
                    tone: toneSelect.value,
                    maxLength: parseInt(lengthSelect.value),
                    temperature: parseFloat(tempSlider.value)
                })
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
                throw new Error(data.error || 'Failed to generate text');
            }
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'Failed to generate text. Please try again.');
        } finally {
            loading.style.display = 'none';
            generateBtn.disabled = false;
            regenerateBtn.disabled = false;
            generateBtn.textContent = 'Generate Text';
        }
    }
    
    function displayResults(data) {
        // Update generated text
        const generatedText = document.getElementById('generatedText');
        generatedText.textContent = data.generatedText || 'No text generated';
        
        // Update statistics
        document.getElementById('wordCount').textContent = data.wordCount || 0;
        document.getElementById('tokensUsed').textContent = data.tokensUsed || 'N/A';
        
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
