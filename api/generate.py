"""
Vercel Serverless Function: Text Generation
Endpoint: POST /api/generate
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add _models directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '_models'))

from generator import TextGenerator

# Global model instance (cached between requests)
generator = None

def get_generator():
    """Initialize or return cached generator model"""
    global generator
    if generator is None:
        print("🔄 Initializing Text Generator model...")
        generator = TextGenerator()
        print("✅ Text Generator ready!")
    return generator


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
        """Handle POST requests for text generation"""
        # Set response headers with CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                response = {"error": "Empty request body"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract and validate parameters
            prompt = data.get('prompt', '').strip()
            tone = data.get('tone', 'formal')
            max_length = int(data.get('maxLength', 500))
            temperature = float(data.get('temperature', 0.7))
            
            if not prompt:
                response = {"error": "No prompt provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            if len(prompt) < 10:
                response = {"error": "Prompt must be at least 10 characters"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Validate parameters
            if tone not in ['formal', 'casual', 'creative', 'technical']:
                tone = 'formal'
            
            max_length = max(100, min(max_length, 1000))
            temperature = max(0.1, min(temperature, 1.0))
            
            # Run generation
            print(f"📊 Generating from prompt: '{prompt[:50]}...' (tone: {tone}, length: {max_length})")
            gen = get_generator()
            result = gen.generate(prompt, tone, max_length, temperature)
            
            # Return result
            self.wfile.write(json.dumps(result).encode())
            print(f"✅ Generation complete: {result['wordCount']} words")
            
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON format"}
            self.wfile.write(json.dumps(error_response).encode())
            print("❌ JSON decode error")
        except Exception as e:
            error_response = {"error": f"Internal error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            print(f"❌ Error: {str(e)}")