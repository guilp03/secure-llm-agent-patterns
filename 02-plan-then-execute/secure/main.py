"""
Plan-Then-Execute — Versão SEGURA

Fase 1 (Planning): LLM vê apenas o prompt do usuário → gera plano imutável.
Fase 2 (Execution): código executa o plano; dados externos preenchem args,
                    nunca escolhem ações nem alteram destinatários.
"""
import json
import sys
import os
import copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from tools import calendar_tool, email_tool

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI()
MODEL = "gpt-4.1"
console = Console()

PLANNING_PROMPT = """Crie um plano de execução como lista de tool calls para atender o pedido do usuário.

Ferramentas disponíveis:
- calendar.read — lê os eventos de hoje. Sem argumentos.
- email.send — envia e-mail. Args: to (string), subject (string).

Retorne APENAS um JSON:
{"plan": [{"step": 1, "tool": "calendar.read", "args": {}}, {"step": 2, "tool": "email.send", "args": {"to": "...", "subject": "..."}}]}"""


def run(user_prompt: str) -> None:
    # FASE 1 — Planning: LLM não vê nenhum dado externo.
    # O destinatário é extraído do prompt do usuário e travado no plano.
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PLANNING_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw_plan = response.choices[0].message.content
    plan = json.loads(raw_plan).get("plan", [])

    # Plano imutável — salvo antes de qualquer dado externo ser lido
    immutable_plan = copy.deepcopy(plan)

    console.print(Panel(
        Syntax(raw_plan, "json", theme="monokai"),
        title="[blue]Fase 1 — Plano (gerado sem dados externos)[/blue]",
        border_style="blue"
    ))

    table = Table(show_header=True, header_style="bold cyan", border_style="blue")
    table.add_column("Step", width=6)
    table.add_column("Tool")
    table.add_column("Args")
    for step in immutable_plan:
        table.add_row(str(step["step"]), step["tool"], json.dumps(step.get("args", {})))
    console.print(table)

    # FASE 2 — Execution: execução mecânica do plano travado.
    # Dados do calendário (incluindo a injeção) chegam apenas aqui,
    # como conteúdo do body — nunca como instrução para o LLM.
    console.print(f"\n[blue]Fase 2 — Execução[/blue]")

    calendar_data = None
    for step in immutable_plan:
        tool = step["tool"]
        args = copy.deepcopy(step.get("args", {}))

        if tool == "calendar.read":
            calendar_data = calendar_tool.read_today()
            console.print(f"  [dim]▶ calendar.read → {len(calendar_data)} chars lidos[/dim]")

        elif tool == "email.send":
            body = calendar_data or "(sem dados)"
            email_tool.send(to=args["to"], subject=args["subject"], body=body)


if __name__ == "__main__":
    console.print("\n[bold green]Assistente de Agenda — Modo Seguro (Plan-Then-Execute)[/bold green]")
    console.print("Digite sua solicitação (ou 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ("sair", "exit", "quit"):
            break
        if not user_input:
            continue
        run(user_input)
        console.print()
