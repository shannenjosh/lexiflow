import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def handler(request):
    try:
        body = request.get_json()
        text = body.get("text", "")

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Summarize the following text:\n\n{text}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"summary": response.text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
