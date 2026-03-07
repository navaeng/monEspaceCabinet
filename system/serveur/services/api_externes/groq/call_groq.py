import os
from groq import Groq

def call_groq(prompt):
    try:
        print('groq est appelé...')
        client = Groq(api_key=os.environ.get("GROQ_API"))
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
            temperature=0,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")

