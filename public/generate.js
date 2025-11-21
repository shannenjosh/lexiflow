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