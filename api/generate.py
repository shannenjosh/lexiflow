<<<<<<< HEAD
import google.generativeai as genai
=======
"""
Vercel Serverless Function: Text Generation
Endpoint: POST /api/generate
Uses Google Gemini API
"""

from http.server import BaseHTTPRequestHandler
>>>>>>> ee328d5 (Initial commit)
import json
import os
import google.generativeai as genai

<<<<<<< HEAD
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def handler(request):
    try:
        body = request.get_json()
        prompt = body.get("prompt", "")

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"text": response.text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
=======
# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

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
            
            # Build prompt with tone and length instructions
            tone_instructions = {
                'formal': 'Use a formal, professional tone with proper grammar and structure.',
                'casual': 'Use a casual, conversational tone that is friendly and approachable.',
                'creative': 'Use a creative, engaging tone with vivid descriptions and storytelling elements.',
                'technical': 'Use a technical, precise tone with clear explanations and terminology.'
            }
            
            full_prompt = f"""{tone_instructions.get(tone, tone_instructions['formal'])}

Generate approximately {max_length} words of text based on the following prompt:

{prompt}

Make sure the response is well-structured, coherent, and directly addresses the prompt."""
            
            # Generate text using Gemini
            print(f"📊 Generating from prompt: '{prompt[:50]}...' (tone: {tone}, length: {max_length})")
            model = genai.GenerativeModel("gemini-pro")
            
            # Configure generation settings
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": int(max_length * 1.5),  # Rough estimate: 1.5 tokens per word
            }
            
            gemini_response = model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            generated_text = gemini_response.text.strip()
            word_count = len(generated_text.split())
            
            # Return result
            result = {
                "generatedText": generated_text,
                "wordCount": word_count,
                "tokensUsed": "N/A"  # Gemini doesn't provide exact token count in this format
            }
            
            self.wfile.write(json.dumps(result).encode())
            print(f"✅ Generation complete: {word_count} words")
            
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON format"}
            self.wfile.write(json.dumps(error_response).encode())
            print("❌ JSON decode error")
        except Exception as e:
            error_response = {"error": f"Internal error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            print(f"❌ Error: {str(e)}")
>>>>>>> ee328d5 (Initial commit)
