import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(messages: list, language: str = "Čeština") -> str:
    if language == "Čeština":
        system_prompt = "Uživatelé se na tebe obrací pro konzultaci svých otázek a problémů. Odpovídáš česky a v případě žádosti o hlubší zamýšlení se do detailů rozepíšeš"
    else:
        system_prompt = "Users are chatting with you to consult their questions and problems. You reply in English and if user requires a deeper thought of the idea, you will be more specific"

    # Vytvoření konverzace pro API
    full_conversation = [{"role": "system", "content": system_prompt}] + messages

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_conversation,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Chyba při volání OpenAI API:\n\n{e}"