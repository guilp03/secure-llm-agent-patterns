"""
Ferramenta simulada: leitura de calendário.
Em produção, isso consultaria uma API de calendário real.
"""
import json
import os

# Caminho absoluto para garantir que funciona independente do diretório de execução
_CALENDAR_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "calendar.json")


def read_today() -> str:
    """
    Lê todos os eventos do calendário de hoje.
    Retorna uma string formatada — INCLUINDO as descriptions,
    que podem conter conteúdo malicioso (injeção de prompt).
    """
    with open(_CALENDAR_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    lines = ["Agenda de hoje:"]
    for event in events:
        lines.append(f"\n[{event['time']}] {event['title']}")
        lines.append(f"  Descrição: {event['description']}")

    return "\n".join(lines)
