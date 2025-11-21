"""
Vercel Serverless Function: Text Summarization
Endpoint: POST /api/summarize
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
        
        # Parse request body
        try:
            body = request.get_json()
        except:
            # Fallback: try to parse body directly
            if hasattr(request, 'body'):
                body = json.loads(request.body) if isinstance(request.body, str) else json.loads(request.body.decode('utf-8'))
            else:
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
        text = body.get('text', '').strip()
        ratio = float(body.get('ratio', 0.5))
        format_type = body.get('format', 'paragraph')
        
        if not text:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "No text provided"})
            }
        
        if len(text) < 50:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Text must be at least 50 characters"})
            }
        
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
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }
        
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid JSON format"})
        }
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": f"Internal error: {str(e)}"})
        }
