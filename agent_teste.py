from agno.agent import Agent
# from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from agno.tools.file import FileTools

from agno.playground import Playground, serve_playground_app

from agno.storage.sqlite import SqliteStorage

from dotenv import load_dotenv
load_dotenv()

# agent_gerador_assessiment = Agent(
#     name='agent_gerador_assessiment',
#     model=OpenAIChat(id = 'gpt-4o-mini'),
# )

# agent_gerador_arquivos = Agent(
#     name='agent_gerador_arquivos',
#     model=OpenAIChat(id = 'gpt-4o-mini'),
#     tools=[FileTools()]
# )

db = SqliteStorage(table_name='agent_session', db_file='tmp/agent.db')

agent = Agent(
    name='agent_buscador_internet',
    model=OpenAIChat(id = 'gpt-4o-mini'),
    tools=[TavilyTools(), FileTools()],
    storage=db
)

app = Playground(
    agents=[agent]
).get_app()

if __name__ == '__main__':
    serve_playground_app("agent_teste.py:app", reload = True)

# agent.print_response("Faça uma pesquisa profunda para descobrir que dia é hoje.")
