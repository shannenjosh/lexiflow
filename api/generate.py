"""
Vercel Serverless Function: Text Generation
Endpoint: POST /api/generate
Uses Google Gemini API
"""

import json
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Handle CORS preflight
        if request.method == 'OPTIONS':
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({})
            }
        
        # Parse request body - Vercel Python format
        body = {}
        if hasattr(request, 'body'):
            if isinstance(request.body, bytes):
                body = json.loads(request.body.decode('utf-8'))
            elif isinstance(request.body, str):
                body = json.loads(request.body)
        elif hasattr(request, 'get_json'):
            try:
                body = request.get_json()
            except:
                body = {}
        
        if not body:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Empty request body"})
            }
        
        # Extract and validate parameters
        prompt = body.get('prompt', '').strip()
        tone = body.get('tone', 'formal')
        max_length = int(body.get('maxLength', 500))
        temperature = float(body.get('temperature', 0.7))
        
        if not prompt:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "No prompt provided"})
            }
        
        if len(prompt) < 10:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Prompt must be at least 10 characters"})
            }
        
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
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }
        
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": f"Invalid JSON format: {str(e)}"})
        }
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": f"Internal error: {str(e)}"})
        }
