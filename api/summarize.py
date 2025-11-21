from http.server import BaseHTTPRequestHandler
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '_models'))
from summarizer import TextSummarizer

summarizer = None

def get_summarizer():
    global summarizer
    if summarizer is None:
        print("Loading Summarizer...")
        summarizer = TextSummarizer()
    return summarizer

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '').strip()
            ratio = float(data.get('ratio', 0.5))
            format_type = data.get('format', 'paragraph')
            
            if not text:
                response = {"error": "No text provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            summ = get_summarizer()
            result = summ.summarize(text, ratio, format_type)
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            print(f"Error: {e}")
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()