import streamlit as st
import os
import glob
import pandas as pd
from agents.agent_avaliador import gerador_mensagem_chat, perguntas_avaliar, nota

from dotenv import load_dotenv
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Chat de Avaliação", page_icon="💬", layout="wide")

# Título da aplicação
st.title("Chat de Avaliação")

# Inicialização das variáveis de sessão
if "selected_assessment" not in st.session_state:
    st.session_state.selected_assessment = None

if "df_assessment" not in st.session_state:
    st.session_state.df_assessment = None
    
if st.session_state.selected_assessment is None:
    st.subheader("Escolha o assessment que deseja responder")

# Criação do menu lateral
with st.sidebar:
    st.title("Assessments Disponíveis")
    
    # Caminho para a pasta de assessments
    assessments_path = os.path.join(os.getcwd(), "Assessments")
    
    # Busca por arquivos de assessment
    assessment_files = glob.glob(os.path.join(assessments_path, "*.xlsx"))
    
    # Lista os arquivos disponíveis
    if assessment_files:
        for file_path in assessment_files:
            file_name = os.path.basename(file_path)
            file_name_limpo = file_name.replace("assessment_", "").replace(".xlsx", "")
            if st.button(file_name_limpo):
                # Carrega o assessment selecionado e armazena na sessão
                st.session_state.selected_assessment = file_name
                st.session_state.df_assessment = pd.read_excel(file_path)
                st.session_state.df_assessment['nota'] = 0
                st.rerun()  # Recarrega a página para mostrar o chat

if st.session_state.selected_assessment and st.session_state.df_assessment is not None:
    if 0 in st.session_state.df_assessment['nota'].unique():
        # Inicialização do histórico de mensagens na sessão
        if "messages" not in st.session_state:
            # Inicializa com a mensagem de boas-vindas do assistente
            st.markdown("## Perguntas e níveis do assessment escolhido:")
            df = st.session_state.df_assessment
            perguntas = df['perguntas'].unique()
            for p in perguntas:
                niveis = df.loc[df['perguntas'] == p]
                st.markdown(f'#### {p}')
                st.dataframe(niveis[['niveis']])

            if st.button("Iniciar Assessment"):
                st.session_state.assessment_iniciado = True
                st.session_state.messages = [
                    {"role": "assistant",
                    "content": gerador_mensagem_chat(st.session_state.df_assessment.loc[st.session_state.df_assessment['nota'] == 0])}
                ]
                st.rerun()
        if "assessment_iniciado" in st.session_state:
            # Exibição do histórico de mensagens
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Input do usuário
            if prompt := st.chat_input("Digite sua mensagem aqui..."):
                # Adiciona a mensagem do usuário ao histórico
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Exibe a mensagem do usuário
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    st.markdown(f'Processando resposta...')

                # chamar função de quais perguntas avaliar
                perguntas_para_analise = perguntas_avaliar(prompt, st.session_state.df_assessment)
                with st.chat_message("assistant"):
                    st.markdown(f'Com base na sua resposta, vou avaliar as seguintes perguntas do assessment:\n{perguntas_para_analise}')

                #chamar função de avaliar nota
                dict_notas = nota(perguntas_para_analise, prompt, st.session_state.df_assessment)
                # Update notes only when the new note is higher than the existing one
                st.session_state.df_assessment["nota"] = st.session_state.df_assessment.apply(
                    lambda row: max(dict_notas.get(row["perguntas"], 0), row["nota"]),
                    axis=1
                )
                with st.chat_message("assistant"):
                    st.markdown(f'As notas para os seguintes níveis de maturidade foram avaliadas:\n{dict_notas}')

                with st.chat_message("assistant"):
                    st.markdown(f'Próxima pergunta...')

                #chamar função pra gerar pergunta resumida só das que não foram avaliadas
                perguntas_nao_avaliadas = st.session_state.df_assessment.loc[st.session_state.df_assessment['nota'] == 0]

                # Verifica se ainda existem perguntas não avaliadas
                if not perguntas_nao_avaliadas.empty:
                    pergunta_resumo = gerador_mensagem_chat(perguntas_nao_avaliadas)
                    st.session_state.messages.append({"role": "assistant", "content": pergunta_resumo})
                    with st.chat_message("assistant"):
                        st.markdown(pergunta_resumo)
                else:
                    # Se todas as perguntas foram avaliadas, recarrega a página para mostrar o resultado final
                    st.rerun()
    else:
        st.markdown('Fim do assessment. Resultado final:')
        st.write(st.session_state.df_assessment[['perguntas', 'nota']].drop_duplicates().reset_index(drop=True))
        import io
        buffer = io.BytesIO()
        st.session_state.df_assessment[['perguntas', 'nota']].drop_duplicates().to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="Baixar resultado em Excel",
            data=buffer,
            file_name="resultado_assessment.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )