"""
Text Generation Model
Uses PyTorch GPT-2 model for creative text generation
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class TextGenerator:
    """Text generator using GPT-2 model"""
    
    def __init__(self):
        """Initialize the text generation model"""
        print("Loading GPT-2 model for text generation...")
        
        # Using GPT-2 base model
        model_name = "gpt2"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Use CPU for serverless
            self.device = torch.device('cpu')
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✅ Generator loaded on {self.device}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def apply_tone(self, prompt, tone):
        """Add tone-specific prefix to prompt"""
        tone_prefixes = {
            'formal': "Write in a formal, professional manner: ",
            'casual': "Write in a casual, conversational style: ",
            'creative': "Write creatively and imaginatively: ",
            'technical': "Write in a technical, precise manner: "
        }
        
        prefix = tone_prefixes.get(tone, "")
        return prefix + prompt
    
    def clean_generated_text(self, text):
        """Clean up generated text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Ensure proper ending
        if text and text[-1] not in '.!?':
            # Find last sentence-ending punctuation
            last_punct = max(
                text.rfind('.'),
                text.rfind('!'),
                text.rfind('?')
            )
            if last_punct > len(text) // 2:  # Only if in latter half
                text = text[:last_punct + 1]
        
        return text.strip()
    
    def generate(self, prompt, tone='formal', max_length=500, temperature=0.7):
        """
        Generate text from prompt
        
        Args:
            prompt: Input prompt
            tone: Writing tone ('formal', 'casual', 'creative', 'technical')
            max_length: Target word count
            temperature: Randomness (0.1-1.0)
        
        Returns:
            dict with generatedText, wordCount, tokensUsed
        """
        try:
            print(f"Generating with tone '{tone}', length {max_length}, temp {temperature}...")
            
            # Apply tone to prompt
            full_prompt = self.apply_tone(prompt, tone)
            
            # Tokenize
            inputs = self.tokenizer(
                full_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Calculate max tokens (roughly 1.3 tokens per word)
            max_tokens = min(int(max_length * 1.3), 1024)
            
            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs['input_ids'],
                    max_length=max_tokens,
                    min_length=50,
                    temperature=temperature,
                    top_k=50,
                    top_p=0.95,
                    do_sample=True,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,  # Avoid repetition
                    repetition_penalty=1.2
                )
            
            # Decode generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt prefix
            if generated_text.startswith(full_prompt):
                generated_text = generated_text[len(full_prompt):].strip()
            
            # Clean up text
            generated_text = self.clean_generated_text(generated_text)
            
            # If text is too short, add note
            if len(generated_text) < 50:
                generated_text += "\n\n[Note: Generation was shorter than expected. Try adjusting parameters or prompt.]"
            
            # Calculate statistics
            word_count = len(generated_text.split())
            tokens_used = outputs.shape[1]
            
            result = {
                "generatedText": generated_text,
                "wordCount": word_count,
                "tokensUsed": tokens_used
            }
            
            print(f"Generated {word_count} words ({tokens_used} tokens)")
            return result
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return {
                "generatedText": f"Error generating text: {str(e)}. Please try again with a different prompt or settings.",
                "wordCount": 0,
                "tokensUsed": 0
            }