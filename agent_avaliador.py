from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field
from typing import List

from dotenv import load_dotenv
load_dotenv()

class PerguntasAssessment(BaseModel):
    perguntas: List[str] = Field(
        ...,
        description="Lista de perguntas possíveis de serem avaliadas dada a resposta do usuário."
    )

class Nota(BaseModel):
    nota: int = Field(
        ...,
        description="Nota do nível de maturidade da resposta do usuário. Nota >= 0"
    )

class PerguntaResumo(BaseModel):
    pergunta: str = Field(
        ...,
        description="Pergunta que resume várias perguntas do assessment."
    )

def gerador_mensagem_chat(df):
    total_perguntas = df['perguntas'].unique()
    perguntas_utilizadas = total_perguntas[:2]
    instructions = '''
    Você é um especialista em Lean Management e em avaliação de maturidade de processos organizacionais.
    Foi criado um assessment e sua tarefa é avaliar as perguntas desse assessment.
    Você deve observar as perguntas do assessment e construir uma nova pergunta cuja resposta do usuário possa responder várias delas.
    A nova pergunta não precisa ser curta como as perguntas do assessment, mas ela precisa ser inteligente e resumir as perguntas em uma única pergunta.
    **Você deve usar palavras chave contidas nos níveis de maturidade de cada pergunta para induzir a resposta do usuário.**
    Retorne apenas a pergunta como uma string. Nada mais do que isso.
    **Perguntas do Assessment**
    {perguntas_utilizadas}
    **Níveis de Maturidade das perguntas**
    {niveis_maturidade}
    '''
    niveis_maturidade = df.loc[df['perguntas'].isin(perguntas_utilizadas), 'niveis'].unique()
    niveis_maturidade = ', '.join(niveis_maturidade)

    instructions = instructions.format(perguntas_utilizadas=perguntas_utilizadas, niveis_maturidade=niveis_maturidade)

    agent_pergutas = Agent(
        name='avaliador',
        model=OpenAIChat(id = 'gpt-4o-mini'),
        instructions=instructions,
        response_model=PerguntaResumo,
    )

    response = agent_pergutas.run("")
    pergunta_resumo = response.content.pergunta

    print(pergunta_resumo)

    return pergunta_resumo



def perguntas_avaliar(resposta, df):
    instructions = '''
    Você é um especialista em Lean Management e em avaliação de maturidade de processos organizacionais.
    Foi criado um assessment e sua tarefa é analisar as respostas do usuário para as perguntas desse assessment.
    Você receberá uma resposta do usuário e terá que identificar para quais das perguntas do formulário é possível avaliar a resposta.
    Apenas identifique as perguntas que podem ser avaliadas dentre as que serão passadas para você.
    Não quero que você avalie as perguntas que foram identificadas, apenas identifique-as e retorne uma lista com as perguntas que podem ser avaliadas.
    Se a resposta do usuário não for clara o suficiente para identificar as perguntas, retorne uma lista vazia.
    **Resposta do usuário**
    {resposta}
    **Perguntas possíveis**
    {total_perguntas}
    '''

    instructions = instructions.format(resposta=resposta, total_perguntas=df['perguntas'].unique())

    agent_pergutas = Agent(
        name='avaliador',
        model=OpenAIChat(id = 'gpt-4o-mini'),
        instructions=instructions,
        response_model=PerguntasAssessment,
    )

    response = agent_pergutas.run("")
    perguntas_para_analise = response.content.perguntas

    return perguntas_para_analise


def nota(perguntas_para_analise, prompt, df):
    if perguntas_para_analise == []:
        return {}
    elif perguntas_para_analise == None:
        return {}
    else:
        dict_perguntas_para_analise = {}
        for pergunta in perguntas_para_analise:
            dict_perguntas_para_analise[pergunta] = 0

        for pergunta in perguntas_para_analise:
            instructions = '''
            Você é um especialista em Lean Management e em avaliação de maturidade de processos organizacionais.
            Foi criado um assessment e sua tarefa a analisar as respostas do usuário para as perguntas desse assessment.
            Você receberá uma resposta do usuário para uma certa pergunta e você terá que avaliá-la.
            Para cada pergunta, foram definidos níveis de maturidade.
            Quero que você analise a resposta, a pergunta e os níveis de maturidade e me diga qual dos níveis melhor descreve a resposta do usuário.
            O output deve ser um número inteiro correspondente ao nível de maturidade.
            Se a resposta do usuário não for clara o suficiente para identificar o nível de maturidade, retorne 0.

            **Resposta do usuário**
            {resposta}
            **Pergunta**
            {pergunta}
            **Níveis de maturidade**
            {niveis}
            '''

            niveis = df.loc[df['perguntas'] == pergunta]['niveis'].to_list()

            instructions = instructions.format(resposta=prompt, pergunta=pergunta, niveis=niveis)
            # print(instructions)

            agent_avaliador = Agent(
                name='avaliador',
                model=OpenAIChat(id = 'gpt-4o-mini'),
                instructions=instructions,
                response_model=Nota,
            )
            nota = agent_avaliador.run("")
            nota = nota.content.nota
            dict_perguntas_para_analise[pergunta] = nota

        return dict_perguntas_para_analise


