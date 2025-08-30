import os
import requests
import json
from datetime import datetime

class RunwayMLGenerator:
    def __init__(self):
        self.api_key = os.environ['RUNWAYML_API_KEY']
        self.base_url = "https://api.runwayml.com/v1"
    
    def generate_video(self, prompt, duration=5):
        """使用RunwayML Gen4 Turbo生成视频"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gen4-turbo",
            "prompt": prompt,
            "duration": duration,
            "resolution": "1280x720"
        }
        
        response = requests.post(
            f"{self.base_url}/video/generate",
            headers=headers,
            json=payload
        )
        
        return response.json()
