# LLM Injection Patterns

Serie educacional sobre segurança em agentes LLM, baseada no paper:
**"Design Patterns for Securing LLM Agents against Prompt Injections"**

## O que é esta série

Cada exemplo mostra um padrão de segurança com duas versões:
- **vulnerable/** — implementação ingênua, suscetível a injeção de prompt
- **secure/** — implementação com o padrão de segurança aplicado

## Padrões disponíveis

| # | Padrão | Descrição |
|---|--------|-----------|
| 01 | [Action-Selector](./01-action-selector/README.md) | LLM como classificador de intenção, sem acesso a dados ou ferramentas |

## Configuração do ambiente

```bash
pip install -r requirements.txt
cp .env.example .env
# Edite o .env e adicione sua OPENAI_API_KEY
```

## Créditos

Baseado no paper: *Design Patterns for Securing LLM Agents against Prompt Injections*
