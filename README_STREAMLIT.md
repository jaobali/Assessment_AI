# Gerador de Assessment de Maturidade Lean - Interface Streamlit

Esta aplicação fornece uma interface gráfica para o gerador de assessment de maturidade Lean, permitindo que o usuário defina a área e a quantidade de perguntas para o assessment.

## Funcionalidades

- Geração de perguntas para assessment de maturidade Lean
- Criação de 5 níveis de maturidade para cada pergunta
- Visualização dos resultados em formato de tabela
- Exportação dos resultados para Excel
- Interface amigável com Streamlit

## Requisitos

Certifique-se de ter todas as dependências instaladas:

```bash
pip install -r requirements.txt
```

## Como executar

Para iniciar a aplicação Streamlit, execute o seguinte comando no terminal:

```bash
streamlit run streamlit_app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

## Como usar

1. Na barra lateral, defina a área para a qual deseja gerar o assessment (ex: Marketing, Vendas, Produção, etc.)
2. Ajuste a quantidade de perguntas desejada usando o controle deslizante
3. Clique no botão "Gerar Assessment"
4. Aguarde o processamento (pode levar alguns minutos dependendo da quantidade de perguntas)
5. Visualize as perguntas geradas e o resultado final em formato de tabela
6. Baixe o arquivo Excel com os resultados usando o botão "Baixar Excel"

## Estrutura do projeto

- `streamlit_app.py`: Contém o código da interface Streamlit
- `requirements.txt`: Lista de dependências necessárias
- `assessment_[AREA].xlsx`: Arquivo Excel gerado com os resultados do assessment

## Observações

- O processo de geração pode levar alguns minutos, especialmente para assessments com muitas perguntas
- A aplicação utiliza a biblioteca Agno para interagir com modelos de linguagem
- É necessário ter um arquivo `.env` com as credenciais de API apropriadas