import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def call_groq(prompt):
    keys = [
        os.environ.get("GROQ_API"),
        os.environ.get("GROQ_API_SECOND"),
        os.environ.get("GROQ_API_THIRD"),
    ]

    for key in keys:
        if not key:
            continue

        try:
            client = Groq(api_key=key)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="openai/gpt-oss-120b",
                temperature=0,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"Error calling Groq API: {e}")
            if key == keys[-1]:
                raise e
            print("switch vers la clé de secours...")
