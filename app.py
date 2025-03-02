import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Carregar a chave da API do arquivo .env (caso esteja rodando localmente)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Se estiver rodando no Streamlit Cloud, use st.secrets
if not api_key:
    api_key = st.secrets["OPENAI_API_KEY"]

openai.api_key = api_key  # Configurar a chave da API

def gerar_imagem(descricao):
    """Gera uma imagem usando DALL·E da OpenAI com base na descrição fornecida."""
    try:
        response = openai.Image.create(
            prompt=descricao,
            n=1,
            size="1024x1024"
        )

        image_url = response["data"][0]["url"]

        # Baixar a imagem e carregar no Pillow
        response = requests.get(image_url)
        imagem = Image.open(BytesIO(response.content))
        return imagem
    except Exception as e:
        st.error(f"Erro ao gerar a imagem: {e}")
        return None

# Interface Streamlit
st.title("ZemAI - Gerador de Imagens de Móveis Planejados")

descricao = st.text_area("Descreva o móvel planejado que você deseja:", "")
if st.button("Gerar Imagem"):
    if descricao:
        imagem_gerada = gerar_imagem(descricao)
        if imagem_gerada:
            st.image(imagem_gerada, caption="Imagem gerada pelo ZemAI")
    else:
        st.warning("Por favor, insira uma descrição do móvel.")
