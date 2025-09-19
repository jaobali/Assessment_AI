from agno.agent import Agent
from agno.models.openai import OpenAIChat

from typing import List, Dict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

# Definição dos modelos de resposta para o parser
class PerguntasAssessment(BaseModel):
    perguntas: List[str] = Field(
        ...,
        description="Lista de perguntas para o assessment de maturidade Lean."
    )

class NiveisMaturidade(BaseModel):
    niveis: List[str] = Field(
        ...,
        description="Lista com 5 níveis de maturidade para a pergunta de referência."
    )

# # Criação das Perguntas
# area = 'Marketing'
# qtd_perguntas = 8

def gerar_perguntas(area: str, qtd_perguntas: int) -> List[str]:
    """
    Gera uma lista de perguntas para um assessment de maturidade Lean.

    Args:
        area (str): A área para a qual o assessment será gerado.
        qtd_perguntas (int): A quantidade de perguntas a serem geradas.

    Returns:
        List[str]: Uma lista de perguntas para o assessment.
    """


    instructions = '''
    Você é um especialista em Lean Management e em avaliação de maturidade de processos organizacionais.
    Sua tarefa é criar um assessment de maturidade Lean para a área: {area}.
    Você deve criar uma lista de perguntas que serão usadas no assessment.
    A quantidade de perguntas foi definida pelo usuário como {qtd_perguntas}.
    As perguntas devem ser objetivas e aplicáveis ao contexto da área informada.
    As perguntas irão servir para aviliar a maturidade dos processos da empresa baseadas na metodologia Lean.
    Crie EXATAMENTE {qtd_perguntas} perguntas objetivas, aplicáveis e distintas ao contexto da área informada.
    Você deve estruturar a resposta em uma lista de python em que cada elemento é uma das perguntas criadas.
    Exemplo de estrutura esperada:
    ['Pergunta1', 'Pergunta2',..., 'Pergunta{qtd_perguntas}']
    Não use nenhuma tag ou qualquer coisa que não seja a lista de perguntas.
    Eu preciso que seja só a lista pra que eu possa usar o comando json.loads sem falhas.
    Lembre-se de usar '' em cada pergunta para que elas fiquem como string.
    '''

    instructions = instructions.format(area=area, qtd_perguntas=qtd_perguntas)

    agent_perguntas = Agent(
        name='gerador_assessment',
        model=OpenAIChat(id = 'gpt-4o-mini'),
        instructions=instructions,
        response_model=PerguntasAssessment,
        use_json_mode=True
    )

    response = agent_perguntas.run("")

    perguntas = response.content.perguntas

    print(perguntas)

    return perguntas

# Criação dos níveis de maturidade
def gerar_niveis_maturidade(area: str, perguntas: List[str]) -> Dict[str, List[str]]:
    """
    Gera uma lista de níveis de maturidade para cada pergunta.

    Args:
        area (str): A área para a qual o assessment será gerado.
        perguntas (List[str]): A lista de perguntas para o assessment.

    Returns:
        Dict[str, List[str]]: Um dicionário com as perguntas como chave e a lista de níveis de maturidade como valor.
    """

    instructions2 = '''
    Você é um especialista em Lean Management e em avaliação de maturidade de processos organizacionais.
    Sua tarefa é criar um assessment de maturidade Lean para a área: {area}.
    As pergutas do formulário já foram definidas.
    Sua tarefa será criar 5 níveis de maturidade para a pergunta que você irá receber.
    Os níveis devem ter descrições claras, objetivas e progressivas:
    1 - Inicial: práticas inexistentes ou informais.
    2 - Básico: práticas pontuais, sem consistência.
    3 - Intermediário: práticas mais frequentes, mas ainda parciais ou reativas.
    4 - Avançado: práticas consolidadas, aplicadas de forma consistente e com bons resultados.
    5 - Excelência: práticas plenamente incorporadas, sustentáveis e geradoras de impacto estratégico.
    Você deve estruturar a resposta em formato de lista python em que cada elemento é um dos níveis de maturidade.
    Exemplo de estrutura esperada:
    ['1-Critério do nível 1', '2-Critério do nível 2', ..., '5-Critério do nível 5']
    Não use nenhuma tag ou qualquer coisa que não seja a lista de perguntas.
    Eu preciso que seja só a lista pra que eu possa usar o comando json.loads sem falhas.
    Lembre-se de usar '' em cada critério para que ele fique como string.
    De modo geral, preciso que você estruture o output como uma lista de strings.
    **PERGUNTA DE REFERENCIA**
    {pergunta}
    '''

    dict_niveis = {}

    for pergunta in perguntas:
        instructions = instructions2.format(area=area, pergunta=pergunta)
        # print(instructions)
        # print(50*'=')

        agent = Agent(
            name='gerador_niveis',
            model=OpenAIChat(id = 'gpt-4o-mini'),
            instructions=instructions,
            response_model=NiveisMaturidade,
            use_json_mode=True
            # tools=[FileTools()]
        )

        response = agent.run("")
        niveis = response.content.niveis

        print(niveis)
        print(50*'=')

        dict_niveis[pergunta] = niveis

    # Converter o dicionário dict_niveis para um DataFrame pandas
    print("\nConvertendo dicionário para DataFrame...")
    import pandas as pd

    # Criar listas para armazenar os dados
    perguntas_lista = []
    niveis_lista = []

    # Para cada pergunta no dicionário
    for pergunta, niveis in dict_niveis.items():
        # Para cada nível de maturidade (1 a 5)
        for nivel in niveis:
            # Adicionar a pergunta e o nível às listas
            perguntas_lista.append(pergunta)
            niveis_lista.append(nivel.replace("'",""))

    # Criar o DataFrame
    df = pd.DataFrame({
        'perguntas': perguntas_lista,
        'niveis': niveis_lista
    })

    # Exibir o DataFrame
    # print("\nDataFrame criado com sucesso!")
    # display(df)

    # df.to_excel(f"assessment_{area}.xlsx", index=False)

    return df



