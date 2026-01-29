import asyncio
import os
import random

from browser_use import Agent, Browser
from langchain_groq import ChatGroq
from pydantic import SecretStr

keys = [
    os.environ.get("GROQ_API"),
    os.environ.get("GROQ_API_SECOND"),
    os.environ.get("GROQ_API_THIRD"),
]


class GroqWrapper:
    """Wrapper pour rendre ChatGroq compatible avec browser_use"""

    def __init__(self, api_key, model="llama-3.1-70b-versatile"):
        self.llm = ChatGroq(model=model, api_key=SecretStr(api_key))
        self.provider = "groq"
        self.model = model  # Attribut requis par browser_use

    def __getattr__(self, name):
        # Délègue tous les autres attributs/méthodes à ChatGroq
        return getattr(self.llm, name)


async def run_ia_prospection(li_email, li_pass, job_title):
    api_key = random.choice([k for k in keys if k])
    llm = GroqWrapper(api_key)

    browser = Browser()

    task = (
        f"1. Va sur https://www.linkedin.com/login\n"
        f"2. Connecte-toi avec l'email '{li_email}' et le mot de passe '{li_pass}'.\n"
        f"3. Une fois connecté, recherche des '{job_title}' dans les filtres 'Personnes'.\n"
        f"4. Clique sur 'Se connecter' pour les 2 premiers profils.\n"
        f"5. Si une popup s'ouvre, clique sur 'Envoyer sans note'."
    )

    agent = Agent(task=task, llm=llm, browser=browser)

    try:
        result = await agent.run()
        return result
    finally:
        await browser.close()


if __name__ == "__main__":
    EMAIL = "kouicicontact@yahoo.com"
    PASS = ""  # Mettez votre mot de passe
    JOB = "Développeur Python"

    asyncio.run(run_ia_prospection(EMAIL, PASS, JOB))
