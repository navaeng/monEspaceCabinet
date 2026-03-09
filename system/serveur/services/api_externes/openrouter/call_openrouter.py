import os
from openai import OpenAI

from usecase.dossier_competences.json.json_template import json_template


def call_openrouter(prompt, model, json_mode=True):
    try:
        print("Calling OpenRouter API...")
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTERAPI"))
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} if json_mode else None,
            temperature=0,
            max_tokens=8000
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")