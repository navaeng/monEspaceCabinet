import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def call_groq(prompt):
    client = Groq(
        api_key=os.environ.get("GROQ_API"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-120b",
    )

    return chat_completion.choices[0].message.content
