import os
import random

from groq import Groq

def call_groq(prompt):

    models = [
        "openai/gpt-oss-20b",
        "moonshotai/kimi-k2-instruct-0905",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "qwen/qwen3-32b",
        "openai/gpt-oss-safeguard-20b"
    ]

    try:
        selected_model = random.choice(models)
        print(f"mdel choisis : ", selected_model)
        print('groq est appelé...')
        client = Groq(api_key=os.environ.get("GROQ_API"))
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=selected_model,
            temperature=1,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")

