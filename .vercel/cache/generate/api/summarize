from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # import Gemini
            import google.generativeai as genai

            # get API key
            api_key = os.getenv("AIzaSyAZuEShA5Go2EIAQN2_4V8lf8t6waJPEKs")
            if not api_key:
                self.wfile.write(json.dumps({
                    "error": "GEMINI_API_KEY missing"
                }).encode())
                return

            genai.configure(api_key=api_key)

            # read request body
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            text = data.get("text", "").strip()

            if not text:
                self.wfile.write(json.dumps({
                    "error": "No text provided"
                }).encode())
                return

            # summarize
            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(f"Summarize this: {text}")

            summary = response.text.strip()

            self.wfile.write(json.dumps({
                "summary": summary
            }).encode())

        except Exception as e:
            self.wfile.write(json.dumps({
                "error": str(e),
                "type": type(e).__name__
            }).encode())
