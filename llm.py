import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

class OpenAI_GPT4:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API d'OpenAI n'est pas définie dans les variables d'environnement.")
        self.client = OpenAI(api_key=self.api_key)

    def query(self, messages, model="gpt-3.5-turbo", max_tokens=150, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature 
            )
            return response.choices[0].message
        except Exception as e:
            return str(e)

if __name__ == "__main__":  
    gpt4 = OpenAI_GPT4()
    reponse = gpt4.query("Quelle est la météo aujourd'hui?")
    print(reponse)
