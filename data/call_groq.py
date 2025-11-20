import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()
    
def call_groq(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen/qwen3-coder:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    

    response = requests.post(url, headers=headers, json=data)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]