const API_URL = "/api/summarize";

async function summarizeText() {
    const input = document.getElementById("text-input").value;

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
    });

    const data = await response.json();

    if (data.error) {
        document.getElementById("output").innerText = "❌ Failed: " + data.error;
    } else {
        document.getElementById("output").innerText = data.summary;
    }
}
