import openai
import os

class ContentGenerator:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']
    
    def generate_viral_content(self, niche="pets"):
        """为美国市场生成病毒式内容"""
        prompt = f"""
        Create viral {niche} content for US YouTube/TikTok audience:
        - Hook within first 3 seconds
        - Emotional engagement
        - US cultural references
        - Call-to-action for engagement
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return response.choices[0].message.content
