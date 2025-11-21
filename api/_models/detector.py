"""
Vercel Serverless Function for AI Text Detection
Endpoint: /api/detect
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add _models directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '_models'))

from detector import AIDetector

# Global variable to cache the model (persists between requests)
detector = None

def get_detector():
    """Get or initialize the detector model (singleton pattern)"""
    global detector
    if detector is None:
        print("Initializing AI Detector...")
        detector = AIDetector()
        print("AI Detector ready!")
    return detector


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
            
            # Extract text from request
            text = data.get('text', '').strip()
            
            # Validate input
            if not text:
                response = {"error": "No text provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            if len(text) < 50:
                response = {"error": "Text must be at least 50 characters"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get detector and run prediction
            print(f"Processing text: {len(text)} characters")
            det = get_detector()
            result = det.predict(text)
            
            # Return result as JSON
            self.wfile.write(json.dumps(result).encode())
            print("Detection complete!")
            
        except Exception as e:
            # Handle errors gracefully
            print(f"Error in detect function: {str(e)}")
            error_response = {
                "error": f"Internal server error: {str(e)}"
            }
            self.wfile.write(json.dumps(error_response).encode())