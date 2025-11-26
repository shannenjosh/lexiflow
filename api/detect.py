from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            import google.generativeai as genai
            
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                self.wfile.write(json.dumps({"error": "API key not configured"}).encode())
                return
            
            genai.configure(api_key=api_key)
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '').strip()
            
            if len(text) < 50:
                self.wfile.write(json.dumps({"error": "Text must be at least 50 characters"}).encode())
                return
            
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""Analyze if this text is AI-generated or human-written. Respond with JSON only:

Text: "{text}"

{{"isAI": true, "confidence": 85.5, "reasoning": "brief explanation"}}"""
            
            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean JSON
            if '```' in result_text:
                result_text = result_text.split('```')[1].replace('json', '').strip()
            
            result = json.loads(result_text)
            result['perplexity'] = 0
            result['burstiness'] = 0
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "isAI": False,
                "confidence": 50,
                "perplexity": 0,
                "burstiness": 0
            }
            self.wfile.write(json.dumps(error_result).encode())