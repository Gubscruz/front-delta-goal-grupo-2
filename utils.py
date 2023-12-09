import yaml
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64

def get_selected_option():
    # Obtém o valor do parâmetro da query
    """
    Obtém o valor do parâmetro da query na URL.

    Returns:
    str or None: O valor do parâmetro ou None se não estiver presente.
    """
    params = st.experimental_get_query_params()
    return params.get('selected_option')

def set_selected_option(selected_option):
    """
    Salva o valor do parâmetro da query na URL.

    Args:
    selected_option (str): Valor a ser definido como parâmetro.

    Returns:
    None
    """
    # Salva a seleção como parâmetro de query na URL
    st.experimental_set_query_params(selected_option=selected_option)

def carregar_cores(caminho_arquivo):
    """
    Carrega as cores a partir de um arquivo YAML.

    Args:
    caminho_arquivo (str): Caminho do arquivo YAML.

    Returns:
    dict or None: Dicionário contendo as cores relacionada com os desfechos ou None em caso de erro ou arquivo não encontrado.
    """
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            dados = yaml.safe_load(arquivo)
            return dados.get('cores_marca_colorblind', {})
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None
    
def carrega_cores_nome(caminho_arquivo):
    """
    Carrega as cores por nome a partir de um arquivo YAML.

    Args:
    caminho_arquivo (str): Caminho do arquivo YAML.

    Returns:
    dict or None: Dicionário contendo as cores por nome ou None em caso de erro ou arquivo não encontrado.
    """
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            dados = yaml.safe_load(arquivo)
            return dados.get('cores_marca_nome', {})
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

def get_image_base64(image_path):
    """
    Converte uma imagem em base64.

    Args:
    image_path (str): Caminho da imagem.

    Returns:
    str or None: String base64 da imagem ou None em caso de erro ou arquivo não encontrado.
    """
    with open(image_path,'rb') as f:
        data = f.read()
        return base64.b64encode(data).decode()
    

