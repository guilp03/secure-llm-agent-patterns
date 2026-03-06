"""
Padrão Action-Selector — Versão VULNERÁVEL
O LLM atua como assistente geral com acesso irrestrito ao sistema.
Ele pode seguir instruções do usuário, vazar dados e sair do escopo.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from rich.console import Console
from rich.panel import Panel
from shared.llm_client import client, MODEL
from shared.mock_data import ORDERS, BOOKS, CATEGORIES, SHIPPING_BY_REGION

console = Console()

# O system prompt é vago e não impõe restrições ao comportamento do LLM
SYSTEM_PROMPT = f"""Você é um assistente de atendimento da Livraria Page Turner.
Você pode ajudar com status de pedidos, disponibilidade de livros, categorias e cálculo de frete.
Responda de forma útil e amigável.

Dados do sistema disponíveis:
Pedidos: {ORDERS}
Livros: {BOOKS}
Categorias: {CATEGORIES}
Tabela de frete: {SHIPPING_BY_REGION}"""


def process_input(user_input: str) -> None:
    """Envia o input diretamente ao LLM com contexto completo do sistema."""
    console.print(Panel(user_input, title="[bold]Input do Usuário[/bold]", border_style="blue"))

    # LLM recebe todo o contexto do sistema + input do usuário sem filtros
    result = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,  # mais criativo — segue instruções com mais facilidade
    )

    response = result.choices[0].message.content

    # Resultado formatado pelo próprio LLM — sem validação
    console.print(Panel(response, title="[bold]Resposta do Assistente[/bold]", border_style="green"))


if __name__ == "__main__":
    console.print("\n[bold cyan]Livraria Page Turner — Atendimento (Vulnerável)[/bold cyan]")
    console.print("Digite sua solicitação (ou 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ("sair", "exit", "quit"):
            break
        if not user_input:
            continue
        process_input(user_input)
        console.print()
