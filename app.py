import streamlit as st
import pandas as pd
import io
import warnings
import json


warnings.simplefilter("ignore", UserWarning)


st.set_page_config(
    page_title="Geração de Resumo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.subheader("📊 Gerador de resumo - Relatórios Descritivos")

st.sidebar.title("ℹ️ Informações")

uploaded_file = st.file_uploader("📂 Faça upload do arquivo Excel (.xlsx ou .xls)", type=["xlsx", "xls"])

if uploaded_file:

    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names 
    col1, col2 = st.columns(2)
    sheet_name = col1.selectbox("📑 Escolha a aba (sheet) do Excel:", sheet_names)
    header_row = col2.number_input("🔢 Número da linha do cabeçalho (começa em 0):", min_value=0, value=0, step=1)

    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=header_row)

    st.subheader("🔍 Visualização dos primeiros dados:")
    if st.button("Visualizar Dados"):
        st.write(df.head())


    

    # dropar colunas vazias

    colunas_escolhidas = st.multiselect("📊 Selecione as colunas para o resumo descritivo:", df.columns)

    if st.button("📥 Carregar Dados"):


        if all(col in df.columns for col in colunas_escolhidas):

            st.subheader("📜 Descrição dos Processos:")
            descricao_texto = ""
            for index, row in df.iterrows():
                descricao = ""
                for coluna in colunas_escolhidas:
                    descricao += f"{coluna}: {row[coluna]}\n"
                descricao += "-----------------------------\n"
                st.markdown(descricao)
                descricao_texto += descricao + "\n"

            st.sidebar.subheader("⬇️ Baixar Resumo")

            output = io.BytesIO()
            output.write(descricao_texto.encode("utf-8"))
            output.seek(0)

            st.sidebar.download_button(
                label="📥 Baixar Relatório",
                data=output,
                file_name="relatorio_descritivo.txt",
                mime="text/plain"
            )    

        else:
            st.error("⚠️ O arquivo enviado não contém todas as colunas esperadas!")
            st.write(f"Colunas encontradas: {list(df.columns)}")
            st.write(f"Colunas esperadas: {colunas_escolhidas}")

