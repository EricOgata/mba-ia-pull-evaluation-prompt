"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="module")
def promptData():
    """Carrega dados de prompt"""
    data = load_prompts(PROMPT_PATH)
    return data["bug_to_user_story_v2"]

class TestPrompts:
    def test_prompt_has_system_prompt(self, promptData):
    #   """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in promptData, "O campo \"system_prompt\" não existe no prompt."
        assert promptData['system_prompt'].strip() != "", "O campo \"\" não pode ser nulo."

    def test_prompt_has_role_definition(self, promptData):
    #   """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        lowerCasePrompt = promptData['system_prompt'].lower()
        targets = ["você é um", "você é uma", "you are a", "you're a"]
        assert any(needle in lowerCasePrompt for needle in targets), "O prompt deve definir uma persona"

    def test_prompt_mentions_format(self, promptData):
    #   """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        lowerCasePrompt = promptData['system_prompt'].lower()
        targets = ["user story", "critérios de aceitação", "detalhes técnicos", "observações"]
        assert all(needle in lowerCasePrompt for needle in targets), "O prompt deve definir o formato esperado da resposta"
    #   pass

    def test_prompt_has_few_shot_examples(self, promptData):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        lowerCasePrompt = promptData['system_prompt'].lower()
        assert lowerCasePrompt.count("exemplo") >= 3, "O prompt deve conter, no mínimo, 3 exemplos de entrada/saída"
        assert "relato de bug:" in lowerCasePrompt and "resposta:" in lowerCasePrompt, "Exemplos devem listar entrada (relato de bug) e saída (resposta)"

    def test_prompt_no_todos(self, promptData):
    #   """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        promptStringified = " ".join(str(value) for value in promptData.values())
        assert "[TODO]" not in promptStringified, "Prompt contém \"[TODO]\" perdido"

    def test_minimum_techniques(self, promptData):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = promptData.get('techniques_applied', [])
        assert len(techniques) >= 2, "Mínimo de 2 técnicas devem ser usadas."

    def test_prompt_structure(self, promptData):
        isValid, errors = validate_prompt_structure(promptData)
        assert isValid, f"Prompt inválido: {errors}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])