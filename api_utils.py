import streamlit as st
import requests
from io import BytesIO
# from streamlit_extras.switch_page_button import switch_page

BASE_URL = "https://api-deltagoal-3153c6f80993.herokuapp.com/"

import requests


def get_desfechos_quebra_linha(id_jogo):
    """
    Obtém os desfechos de quebra de linha de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os desfechos de quebra de linha ou uma mensagem de erro.
    """

    url_desfechos_quebra_linha = f'{BASE_URL}jogo/{id_jogo}/quebra/desfechos'
    try:
        response = requests.get(url_desfechos_quebra_linha, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page("Login")
        return False, {"message": str(e)}


def get_desfechos_quebra_linha_por_time(id_jogo):
  
    """

    Obtém os desfechos de quebra de linha de um jogo por time.
    
    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os desfechos de quebra de linha por time ou uma mensagem de erro.
    
    """

    url_desfechos_quebra_linha_por_time = f'{BASE_URL}jogo/{id_jogo}/quebra/desfechos/time'
    try:
        response = requests.get(url_desfechos_quebra_linha_por_time, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}

def get_nomes_times(id_jogo):
   
    """
    Obtém os nomes dos times de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os nomes dos times ou uma mensagem de erro.
    """

    url_nomes_times = f'{BASE_URL}jogo/{id_jogo}/time'
    try:
        response = requests.get(url_nomes_times, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}

    
def get_jogadores_mais_envolvidos_quebra_linha(id_jogo):
    """
    Obtém os jogadores mais envolvidos em quebra de linha de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os jogadores mais envolvidos em quebra de linha ou uma mensagem de erro.

    """
    url_jogadores_quebra_linha_por_time = f'{BASE_URL}/jogo/{id_jogo}/quebra/time/top5'
    try:
        response = requests.get(url_jogadores_quebra_linha_por_time, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}

def get_zonas_frequentes_quebra_linha(id_jogo):
    
    """
    Obtém as zonas mais frequentes de quebra de linha de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com as zonas mais frequentes de quebra de linha ou uma mensagem de erro.
    """

    url_zonas_frequentes_quebra_linha = f'{BASE_URL}jogo/{id_jogo}/quebra/zona'
    try:
        response = requests.get(url_zonas_frequentes_quebra_linha, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}

def exibir_lista_de_rupturas(id_jogo):
    """
    Obtém a lista de rupturas de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com a lista de rupturas ou uma mensagem de erro.
    """
    url_lista_de_rupturas = f'{BASE_URL}/jogo/{id_jogo}/quebra'
    try:
        response = requests.get(url_lista_de_rupturas, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}

def exibir_lista_de_rupturas_filtrado(id_jogo, filtro_time, filtro_jogador, filtro_zona, filtro_desfecho):
    url_lista_de_rupturas = f'{BASE_URL}/jogo/{id_jogo}/quebra/time/{filtro_time}/jogador/{filtro_jogador}/zona/{filtro_zona}/desfecho/{filtro_desfecho}'
    try:
        response = requests.get(url_lista_de_rupturas, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, {"message": str(e)}
    
def exibir_video_ruptura(jogo_id, time_id, quebra_id):
    
    """
    Obtém o vídeo de uma ruptura de um jogo.

    Args:
    jogo_id (int): Identificador do jogo.

    time_id (int): Identificador do time.

    quebra_id (int): Identificador da ruptura.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com o vídeo da ruptura ou uma mensagem de erro.
    """
    url_video_ruptura = f'{BASE_URL}jogo/{jogo_id}/quebra/{quebra_id}/video/time/{time_id}'
    try:
        response = requests.get(url_video_ruptura, verify=False)
        video_bytes = BytesIO(response.content)     
        return True,video_bytes
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    
def get_filtros_quebra(id_jogo):
    url_filtros = f'{BASE_URL}/jogo/{id_jogo}/quebra/filtros'
    try:
        response = requests.get(url_filtros,verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, {"message": str(e)}

#----------------Cruzamentos--------------------------

def exibir_video_cruzamento(jogo_id, time_id, cruzamento_id):
    
    """
    
    Obtém o vídeo de um cruzamento de um jogo.

    Args:
    jogo_id (int): Identificador do jogo.

    time_id (int): Identificador do time.

    cruzamento_id (int): Identificador do cruzamento.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com o vídeo do cruzamento ou uma mensagem de erro.

    """
    url_video_cruzamento = f'{BASE_URL}jogo/{jogo_id}/cruzamento/{cruzamento_id}/video/time/{time_id}'
    try:
        response = requests.get(url_video_cruzamento, verify=False)
        video_bytes = BytesIO(response.content)
        response.raise_for_status()
        return True,  video_bytes
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    
def exibir_lista_de_cruzamentos(id_jogo):
    
    """
    
    Obtém a lista de cruzamentos de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com a lista de cruzamentos ou uma mensagem de erro.
    
    """
    url_lista_de_cruzamentos = f'{BASE_URL}/jogo/{id_jogo}/cruzamento'
    try:
        response = requests.get(url_lista_de_cruzamentos, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}


def get_cruzamento_desfechos_time(id_jogo):
    
    """
    Obtém os desfechos de cruzamento de um jogo por time.
    
    Args:
    id_jogo (int): Identificador do jogo.
    
    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os desfechos de cruzamento por time ou uma mensagem de erro.
    
    """
    url_cruzamento_desfechos_time = f'{BASE_URL}/jogo/{id_jogo}/cruzamento/desfechos/time'
    try:
        response = requests.get(url_cruzamento_desfechos_time, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}


def get_frequencia_zonas_cruzamentos(id_jogo):
    
    """
    
    Obtém as zonas mais frequentes de cruzamento de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com as zonas mais frequentes de cruzamento ou uma mensagem de erro.

    """
    url_frequencia_zonas_cruzamentos = f'{BASE_URL}jogo/{id_jogo}/cruzamento/zona'
    try:
        response = requests.get(url_frequencia_zonas_cruzamentos, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}


def get_top_5_jogadores(id_jogo):
    
    """
    Obtém os 5 jogadores mais envolvidos em cruzamentos de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os 5 jogadores mais envolvidos em cruzamentos ou uma mensagem de erro.

    """

    url_top_5_jogadores = f'{BASE_URL}jogo/{id_jogo}/cruzamento/time/top5'
    try:
        response = requests.get(url_top_5_jogadores, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    
    
def get_cruzamentos_por_jogador(id_jogo):
    
    """
    
    Obtém os cruzamentos de um jogo por jogador.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os cruzamentos por jogador ou uma mensagem de erro.

    """
    url_cruzamento_por_jogador = f'{BASE_URL}jogo/{id_jogo}/cruzamento/time/jogador'
    try:
        response = requests.get(url_cruzamento_por_jogador, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    
def get_filtros_cruzamentos(id_jogo):
    url_filtros = f'{BASE_URL}/jogo/{id_jogo}/cruzamento/filtros'
    try:
        response = requests.get(url_filtros, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, {"message": str(e)}

#----------------Jogos--------------------------

def get_eventos_chaves(id_jogo):
    """
    Obtém os eventos chaves de um jogo.

    Args:
    id_jogo (int): Identificador do jogo.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com os eventos chaves ou uma mensagem de erro.

    """
    url_eventos_chaves = f'{BASE_URL}jogo/{id_jogo}/eventos'
    try:
        response = requests.get(url_eventos_chaves, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    

def get_todos_jogos():
    
    """
    Obtém todos os jogos.

    Returns:
    tuple: Tupla contendo um booleano indicando se a requisição foi bem sucedida e um dicionário com todos os jogos ou uma mensagem de erro.

    """
    url_todos_jogos = f'{BASE_URL}jogo'
    try:
        response = requests.get(url_todos_jogos, verify=False)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        # switch_page('Login')
        return False, {"message": str(e)}
    

