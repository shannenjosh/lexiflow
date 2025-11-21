<<<<<<< HEAD
import google.generativeai as genai
=======
"""
Vercel Serverless Function: Text Summarization
Endpoint: POST /api/summarize
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
        """Handle POST requests for text summarization"""
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
            text = data.get('text', '').strip()
            ratio = float(data.get('ratio', 0.5))
            format_type = data.get('format', 'paragraph')
            
            if not text:
                response = {"error": "No text provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            if len(text) < 50:
                response = {"error": "Text must be at least 50 characters"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Build prompt based on format and ratio
            length_desc = "brief" if ratio <= 0.25 else "medium-length" if ratio <= 0.5 else "detailed"
            format_instruction = "as bullet points" if format_type == 'bullets' else "as a paragraph"
            
            prompt = f"""Summarize the following text in a {length_desc} summary {format_instruction}. 
Keep the summary to approximately {int(ratio * 100)}% of the original length.

Text to summarize:
{text}

Summary:"""
            
            # Generate summary using Gemini
            print(f"Summarizing text: {len(text)} characters with ratio {ratio}")
            model = genai.GenerativeModel("gemini-pro")
            gemini_response = model.generate_content(prompt)
            
            summary = gemini_response.text.strip()
            
            # Calculate statistics
            original_words = len(text.split())
            summary_words = len(summary.split())
            compression = round((1 - summary_words / original_words) * 100, 1) if original_words > 0 else 0
            
            # Return result
            result = {
                "summary": summary,
                "originalWords": original_words,
                "summaryWords": summary_words,
                "compressionRatio": f"{compression}%"
            }
            
            self.wfile.write(json.dumps(result).encode())
            print(f"✅ Summarization complete: {summary_words} words")
            
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON format"}
            self.wfile.write(json.dumps(error_response).encode())
            print("❌ JSON decode error")
        except Exception as e:
            error_response = {"error": f"Internal error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            print(f"❌ Error: {str(e)}")
>>>>>>> ee328d5 (Initial commit)
