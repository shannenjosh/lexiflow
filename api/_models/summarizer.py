"""
Vercel Serverless Function for Text Summarization
Endpoint: /api/summarize
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add _models directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '_models'))

from summarizer import TextSummarizer

# Global variable to cache the model
summarizer = None

def get_summarizer():
    """Get or initialize the summarizer model (singleton pattern)"""
    global summarizer
    if summarizer is None:
        print("Initializing Text Summarizer...")
        summarizer = TextSummarizer()
        print("Text Summarizer ready!")
    return summarizer


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read and parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract parameters from request
            text = data.get('text', '').strip()
            ratio = float(data.get('ratio', 0.5))
            format_type = data.get('format', 'paragraph')
            
            # Validate input
            if not text:
                response = {"error": "No text provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            if len(text) < 100:
                response = {"error": "Text must be at least 100 characters"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get summarizer and run summarization
            print(f"Summarizing text: {len(text)} characters with ratio {ratio}")
            summ = get_summarizer()
            result = summ.summarize(text, ratio, format_type)
            
            # Return result as JSON
            self.wfile.write(json.dumps(result).encode())
            print("Summarization complete!")
            
        except Exception as e:
            # Handle errors gracefully
            print(f"Error in summarize function: {str(e)}")
            error_response = {
                "error": f"Internal server error: {str(e)}"
            }
            self.wfile.write(json.dumps(error_response).encode())