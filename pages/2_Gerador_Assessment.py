import streamlit as st
import os
from agents.agent_gerador_assessment import gerar_perguntas, gerar_niveis_maturidade

# Interface Streamlit simplificada para demonstração
st.set_page_config(page_title="Gerador de Assessment Lean", page_icon="📊", layout="wide")

# Inicializar variáveis de sessão para navegação
if 'current_page' not in st.session_state:
    st.session_state.current_page = "assessment"


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
            st.session_state.niveis = gerar_niveis_maturidade(area=area, perguntas=st.session_state.perguntas)
        
        # Exibir níveis se foram gerados
        if st.session_state.niveis is not None:
            st.subheader("Níveis de Maturidade")
            st.write(st.session_state.niveis)

            # Botão para gerar Excel
            if st.button("Gerar Excel"):
                try:
                    # Caminho para salvar o arquivo
                    save_path = os.path.join("Assessments", f"assessment_{area}.xlsx")
                    
                    # Salvar o DataFrame em um arquivo Excel
                    st.session_state.niveis.to_excel(save_path, index=False)
                    
                    st.success(f"Arquivo salvo com sucesso em: {save_path}")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao salvar o arquivo: {e}")
        
        

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ usando Streamlit")