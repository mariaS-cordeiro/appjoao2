import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64

# Nome do app
st.set_page_config(page_title="AcessaNotas", layout="centered")
st.title("📝 AcessaNotas – Anotações Acessíveis")

st.markdown("### Preencha as informações da anotação:")

# Campos do formulário
nome_disciplina = st.text_input("📚 Nome da disciplina", key="disciplina", placeholder="Ex: Comunicação Acessível")
tematica = st.text_input("🎯 Temática da disciplina", key="tematica", placeholder="Ex: anotar")
data = st.date_input("📅 Data", key="data", value=datetime.today())

# Upload de imagem
st.markdown("### 📷 Envie uma foto")
foto = st.file_uploader("Upload da imagem", type=["jpg", "jpeg", "png"], key="foto")

# Área de anotação com fonte grande
st.markdown("### 🗒️ Anotações")
anotacoes = st.text_area("Digite aqui suas anotações:", height=400, key="anotacoes",
                         placeholder="Escreva com tranquilidade...", help="Espaço acessível para escrever",
                         label_visibility="collapsed")

# Gravação de áudio
st.markdown("### 🎤 Grave um áudio")
audio = st.file_uploader("Gravação de áudio", type=["mp3", "wav", "m4a"], key="audio")

# Criar pasta para arquivos
os.makedirs("anotacoes_salvas", exist_ok=True)

# Botão de salvar
if st.button("💾 Salvar Anotação"):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Salvar foto
    foto_path = ""
    if foto:
        foto_path = f"anotacoes_salvas/foto_{timestamp}.jpg"
        with open(foto_path, "wb") as f:
            f.write(foto.read())

    # Salvar áudio
    audio_path = ""
    if audio:
        audio_path = f"anotacoes_salvas/audio_{timestamp}.{audio.type.split('/')[-1]}"
        with open(audio_path, "wb") as f:
            f.write(audio.read())

    # Carregar base existente ou criar nova
    csv_path = "anotacoes_salvas/registros.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=["Data", "Nome da disciplina", "Temática", "Anotações", "Imagem", "Áudio"])

    # Adicionar nova linha
    nova_linha = {
        "Data": data.strftime("%d/%m/%Y"),
        "Nome da disciplina": nome_disciplina,
        "Temática": tematica,
        "Anotações": anotacoes,
        "Imagem": foto_path,
        "Áudio": audio_path
    }

    df = df._append(nova_linha, ignore_index=True)
    df.to_csv(csv_path, index=False)

    st.success("✅ Anotação salva com sucesso!")

# Mostrar tabela com registros
st.markdown("## 📋 Anotações salvas")
if os.path.exists("anotacoes_salvas/registros.csv"):
    df = pd.read_csv("anotacoes_salvas/registros.csv")

    def gerar_link_download(arquivo):
        if pd.isna(arquivo) or not os.path.exists(arquivo):
            return ""
        nome_arquivo = os.path.basename(arquivo)
        with open(arquivo, "rb") as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            mime = "image/jpeg" if "jpg" in nome_arquivo else "audio/mpeg"
            href = f'<a href="data:{mime};base64,{b64}" download="{nome_arquivo}">🔗 Baixar</a>'
            return href

    df["Imagem"] = df["Imagem"].apply(gerar_link_download)
    df["Áudio"] = df["Áudio"].apply(gerar_link_download)

    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("Nenhuma anotação salva ainda.")
