import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Instância única do cliente OpenAI (reutilizada em todos os módulos)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelo utilizado em toda a série
MODEL = "gpt-4.1-mini"
