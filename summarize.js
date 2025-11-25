// Summarize functionality
document.addEventListener('DOMContentLoaded', () => {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const summaryText = document.getElementById('summaryText');
    const charCount = document.getElementById('charCount');
    const lengthRatio = document.getElementById('lengthRatio');
    const formatType = document.getElementById('formatType');
    const loading = document.getElementById('loading');
    const errorMsg = document.getElementById('errorMsg');
    const results = document.getElementById('results');
    const copyBtn = document.getElementById('copyBtn');
    
    // Character counter
    summaryText.addEventListener('input', () => {
        const count = summaryText.value.length;
        charCount.textContent = count;
    });
    
    // Summarize button click
    summarizeBtn.addEventListener('click', handleSummarize);
    
    // Enter key to submit (Ctrl+Enter)
    summaryText.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleSummarize();
        }
    });
    
    // Copy button
    copyBtn.addEventListener('click', () => {
        const summaryResult = document.getElementById('summaryResult');
        const text = summaryResult.textContent;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = 'Copy Summary';
            }, 2000);
        });
    });
    
    async function handleSummarize() {
        const text = summaryText.value.trim();
        
        // Validation
        if (!text) {
            showError('Please enter some text to summarize');
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
        summarizeBtn.disabled = true;
        summarizeBtn.textContent = 'Summarizing...';
        
        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    ratio: parseFloat(lengthRatio.value),
                    format: formatType.value
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
                throw new Error(data.error || 'Failed to summarize text');
            }
            
            // Display results
            displayResults(data, text);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'Failed to summarize text. Please try again.');
        } finally {
            loading.style.display = 'none';
            summarizeBtn.disabled = false;
            summarizeBtn.textContent = 'Generate Summary';
        }
    }
    
    function displayResults(data, originalText) {
        // Update summary text
        const summaryResult = document.getElementById('summaryResult');
        summaryResult.textContent = data.summary || 'No summary generated';
        
        // Update statistics
        document.getElementById('originalWords').textContent = data.originalWords || originalText.split(/\s+/).length;
        document.getElementById('summaryWords').textContent = data.summaryWords || 0;
        document.getElementById('compressionRatio').textContent = data.compressionRatio || '--';
        
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
