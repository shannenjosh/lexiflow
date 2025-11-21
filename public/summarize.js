const response = await fetch('/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: text,
        ratio: parseFloat(lengthRatio.value),
        format: formatType.value
    })
});