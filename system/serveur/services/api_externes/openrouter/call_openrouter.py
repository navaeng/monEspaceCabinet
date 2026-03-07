import os
from openai import OpenAI

def call_openrouter(prompt):
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTER_API"))
        completion = client.chat.completions.create(
            model="nousresearch/hermes-3-llama-3.1-405b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")