import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
    
def call_groq(prompt, temperature=0):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,

            }
        ],                
        temperature=temperature,
        model="openai/gpt-oss-120b", 
    )
    
    return chat_completion.choices[0].message.content