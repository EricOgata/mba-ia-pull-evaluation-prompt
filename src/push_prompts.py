"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

"""
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
"""
def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    if not check_env_vars([
        "LANGSMITH_TRACING",
        "LANGSMITH_API_KEY",
        "LANGSMITH_ENDPOINT",
        "USERNAME_LANGSMITH_HUB"
    ]):
        return False

    try:
        systemPromp = prompt_data['system_prompt']
        userPrompt = prompt_data['user_prompt']
        promptTemplate = ChatPromptTemplate.from_messages([
            ('system', systemPromp),
            ('user', userPrompt)
        ])
        promptTags = prompt_data['tags'] if 'tags' in prompt_data.keys() else []
        promptDescription = prompt_data['description'] if 'description' in prompt_data.keys() else ""
        # print(promptTags)
        client = Client()
        url = client.push_prompt(
            prompt_identifier=f"{os.getenv('USERNAME_LANGSMITH_HUB')}/{prompt_name}",
            is_public=True,
            object=promptTemplate,
            description=promptDescription,
            tags=promptTags,
        )
        print(url)
        print(f"Prompt {prompt_name} enviado com sucesso! Ver mais em {url}")
    except:
        print('Erro ao enviar prompt.')

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...


def main():
    print_section_header("Validando prompt otimizado antes do push")
    promptData = load_yaml("./prompts/bug_to_user_story_v2.yml")
    validation_result = validate_prompt_structure(promptData['bug_to_user_story_v2'])
    if not validation_result[0]:
        print("Prompt inválido!!!!")
        for error in validation_result[1]:
            print(f"Erro: {error}")
        return
    print("Prompt válido. Prosseguindo com o push para o LangSmith Hub...")
    print_section_header("Realizando push do prompt otimizado para o LangSmith Hub")

    push_prompt_to_langsmith("bug_to_user_story_v2", promptData['bug_to_user_story_v2'])


if __name__ == "__main__":
    sys.exit(main())
