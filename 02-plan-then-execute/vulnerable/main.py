"""
Plan-Then-Execute — Versão VULNERÁVEL
Prompt único mistura instruções do usuário e dados externos.
O LLM não distingue instrução legítima de conteúdo malicioso nos dados.
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from tools import calendar_tool, email_tool

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI()
MODEL = "gpt-4.1"
console = Console()


def run(user_prompt: str) -> None:
    calendar_data = calendar_tool.read_today()

    # VULNERABILIDADE: dados externos entram no mesmo prompt que as instruções.
    # O LLM trata o conteúdo malicioso do calendário como instrução válida.
    prompt = f"""Você é um assistente de produtividade pessoal.

Pedido do usuário:
{user_prompt}

Dados disponíveis:
{calendar_data}

Ferramentas disponíveis:
- send_email(to, subject, body): envia um e-mail

Com base no pedido e nos dados acima, retorne um JSON:
{{"action": "send_email", "to": "...", "subject": "...", "body": "..."}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = response.choices[0].message.content
    console.print(Panel(
        Syntax(raw, "json", theme="monokai"),
        title="[magenta]Resposta do LLM[/magenta]",
        border_style="magenta"
    ))

    action = json.loads(raw)
    email_tool.send(to=action["to"], subject=action["subject"], body=action["body"])


if __name__ == "__main__":
    console.print("\n[bold red]Assistente de Agenda — Modo Vulnerável[/bold red]")
    console.print("Digite sua solicitação (ou 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ("sair", "exit", "quit"):
            break
        if not user_input:
            continue
        run(user_input)
        console.print()
