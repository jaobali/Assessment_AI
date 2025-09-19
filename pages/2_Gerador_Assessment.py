import streamlit as st
from agent_gerador_assessment import gerar_perguntas, gerar_niveis_maturidade
from app_chat_avaliacao import chat_with_ai

# Interface Streamlit simplificada para demonstração
st.set_page_config(page_title="Gerador de Assessment Lean", page_icon="📊", layout="wide")

# Inicializar variáveis de sessão para navegação
if 'current_page' not in st.session_state:
    st.session_state.current_page = "assessment"

# Sidebar para navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Ir para:", ["Gerador de Assessment", "Chat com IA"],
    index=0 if st.session_state.current_page == "assessment" else 1,
    key="navigation"
)

# Atualizar página atual com base na seleção
if page == "Gerador de Assessment":
    st.session_state.current_page = "assessment"
else:
    st.session_state.current_page = "chat"

# Sidebar para configurações (apenas na página de assessment)
st.sidebar.markdown("---")

# Inicializar variáveis de sessão
if 'perguntas_geradas' not in st.session_state:
    st.session_state.perguntas_geradas = False
    st.session_state.perguntas = None
    st.session_state.niveis = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Conteúdo da página de Assessment
if st.session_state.current_page == "assessment":
    st.title("Gerador de Assessment de Maturidade Lean")
    st.markdown("""Esta aplicação demonstra a interface para gerar um assessment de maturidade Lean para uma área específica, 
                criando perguntas e níveis de maturidade para cada pergunta.""")
    
    # Sidebar para configurações
    st.sidebar.header("Configurações do Assessment")
    
    # Input para área
    area = st.sidebar.text_input("Área", "Marketing")
    
    # Input para quantidade de perguntas
    qtd_perguntas = st.sidebar.slider("Quantidade de perguntas", 3, 15, 8)

    # Botão para gerar assessment
    if st.sidebar.button("Gerar Assessment"):
        st.session_state.perguntas = gerar_perguntas(area=area, qtd_perguntas=qtd_perguntas)
        st.session_state.perguntas_geradas = True
        st.session_state.niveis = None

    # Exibir perguntas se foram geradas
    if st.session_state.perguntas_geradas:
        st.subheader("Perguntas Geradas")
        st.write(st.session_state.perguntas)
        
        # Botão para gerar níveis de maturidade
        if st.button("Gerar Níveis de Maturidade"):
            st.session_state.niveis = gerar_niveis_maturidade(area=area, qtd_perguntas=qtd_perguntas, perguntas=st.session_state.perguntas)
        
        # Exibir níveis se foram gerados
        if st.session_state.niveis is not None:
            st.subheader("Níveis de Maturidade")
            st.write(st.session_state.niveis)


# Página de Chat
elif st.session_state.current_page == "chat":
    st.title("Chat com IA")
    st.markdown("""Converse com nossa IA para tirar dúvidas sobre o assessment de maturidade Lean ou sobre metodologias Lean em geral.""")
    
    # Exibir mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input para nova mensagem
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Mostrar indicador de carregamento enquanto processa a resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                # Chamar a função de chat com IA para obter uma resposta
                response = chat_with_ai(st.session_state.messages)
        
        # Adicionar resposta da IA ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Exibir resposta da IA
        with st.chat_message("assistant"):
            st.markdown(response)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ usando Streamlit")