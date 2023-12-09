import streamlit as st
from api_utils import *
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from streamlit_extras.switch_page_button import switch_page 
from utils import *


#Configurando a página
st.set_page_config(initial_sidebar_state="expanded")

#Carregando imagens
img_logo = get_image_base64('static/copia_logo_color_delta.png')

#Carregando cores
cores = carrega_cores_nome('static/constants.yaml')


#Criando CSS
css = f"""
    <style>
    .logo {{
            position: fixed;
            top: 70px;
            left: 35px;
            }}
    
    [data-testid="stAppViewContainer"]{{
    background-image: linear-gradient(145deg, #FCEA10, #E6007E, #009FE3);
    color:white
    }}
    .st-emotion-cache-uf99v8 {{
        overflow: auto;
        position: fixed;
        width:100%
        top: 30px;
        text-align: center;
        height:700px;
        }}
    
    [data-testid="stExpander"]{{
       background-color:white;
       color:black;
       border-radius:15px;
       heigth:100px;
       width:735px;
       
    }}


    [data-testid="stSidebar"]{{
        visibility: hidden;
    }}
    
    

    [data-testid="baseButton-secondary"]{{
        background-color:white;
        color:black
        }}
    [data-testid="baseButton-secondary"]:hover{{
        background-color:gray;
        color:black;
        border:black
        }}

    </style>
    <img class=logo src="data:image/png;base64,{img_logo}"></img>
    <div class ="bemvindo">
    <h1 style="color:white; font-size:60px">Bem Vindo</h1>
    <h3 style="color:white; font-size:30px">Aqui você pode ver todos os jogos do seu time. Selecione o jogo que deseja analisar para mais informações</h3>
    </div>
    """



st.markdown(css,unsafe_allow_html=True)


#Carrega times
achou,lista_jogos_dados = get_todos_jogos()
if not(achou): 
    st.error(lista_jogos_dados)

with st.container():
    #Carrega os jogos existentes
    for jogo in lista_jogos_dados['jogos']:
        #Carrega os nomes dos times
        achou, nomes_id_times = get_nomes_times(jogo['_id'])
        if not(achou):  
            st.error(nomes_id_times)
        else:
            nome_time1 = nomes_id_times['nomes_times'][0]
            nome_time2 = nomes_id_times['nomes_times'][1]
            id_time1 = nomes_id_times['id_times'][0]
            id_time2 = nomes_id_times['id_times'][1]

        #Carrega os eventos chaves
        achou, data_eventos_chaves = get_eventos_chaves(jogo['_id'])
        if not achou:
            st.error(data_eventos_chaves)

        #Criar linha do tempo
        dates = []
        labels = []

        #Pegar informações dos eventos chaves
        for cruzamento in data_eventos_chaves['eventos'][f'{nome_time1}-cruzamento']:
            dates.append(cruzamento['instante_cruzamento'])
            labels.append(f'{nome_time1}\n Cruzamento\n {cruzamento["desfecho"]}')

        for quebra in data_eventos_chaves['eventos'][f'{nome_time1}-quebra']:
            dates.append(quebra['instante_ruptura'])
            labels.append(f'{nome_time1}\n Quebra de Linha\n {quebra["desfecho"]}')

        for cruzamento in data_eventos_chaves['eventos'][f'{nome_time2}-cruzamento']:
            dates.append(cruzamento['instante_cruzamento'])
            labels.append(f'{nome_time2}\n Cruzamento\n {cruzamento["desfecho"]}')

        for quebra in data_eventos_chaves['eventos'][f'{nome_time2}-quebra']:
            dates.append(quebra['instante_ruptura'])
            labels.append(f'{nome_time2}\n Quebra de Linha\n {quebra["desfecho"]}') 

        #expander de cada jogo 
        with st.expander(f'{jogo["times"][0]} e {jogo["times"][1]}'):
            #Carrega linha do tempo
            datetime_dates = [datetime.strptime(d, '%H:%M:%S') for d in dates]

            min_date = datetime.strptime('00:00:00', '%H:%M:%S')
            max_date = datetime.strptime('01:40:00', '%H:%M:%S')


            labels = ['{0:%H:%M:%S}\n{1}'.format(d, l) for l, d in zip(labels, datetime_dates)]

            fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
            ax.set_ylim(-2, 1.75)
            ax.set_xlim(min_date, max_date)
            ax.axhline(0, xmin=0.01, xmax=0.95, c=cores['preto'], zorder=1)


            ax.scatter(datetime_dates, np.zeros(len(dates)), s=120, c=cores['azul'], zorder=2)
            ax.scatter(datetime_dates, np.zeros(len(dates)), s=30, c=cores['rosa'], zorder=3)


            label_offsets = np.zeros(len(datetime_dates))
            label_offsets[::2] = 0.35
            label_offsets[1::2] = -1.5
            label_offsets[2::3] = 1.4
            label_offsets[3::4] = -2.8
            label_offsets[4::5] = 2.1


            for i, (l, d) in enumerate(zip(labels, datetime_dates)):
                ax.text(d, label_offsets[i], l, ha='center', fontfamily='serif', color=cores['preto'], fontsize=12)

            stems = np.zeros(len(datetime_dates))
            stems[::2] = 0.3
            stems[1::2] = -0.35
            stems[2::3] = 1.35
            stems[3::4] = -1.7
            stems[4::5] = 2


            markerline, stemline, baseline = ax.stem(datetime_dates, stems, basefmt=' ')
            plt.setp(markerline, marker=',', color=cores['preto'])
            plt.setp(stemline, color=cores['rosa'])


            for spine in ["left", "top", "right", "bottom"]:
                ax.spines[spine].set_visible(False)

            ax.set_xticks([])
            ax.set_yticks([])

            # Exibir o gráfico no Streamlit
            st.pyplot(fig)


            #Cria botões para entrar em cada dashboard
            col1,col2 = st.columns(2)
            with col1:
                if st.button('Dashboard Cruzamentos', key=f'{jogo["_id"]} Dashboard_Cruzamentos'):
                    jogo_id = jogo['_id']
                    caminho = 'Dashboard_Cruzamentos'
                    st.session_state['jogo'] = jogo_id
                    switch_page(caminho)

            with col2:
                if st.button('Dashboard Quebra de Linha', key=f'{jogo["_id"]} Dashboard_Quebra_de_Linha'):
                    jogo_id = jogo['_id']
                    caminho = 'Dashboard_Quebra_de_Linha'
                    st.session_state['jogo'] = jogo_id
                    switch_page(caminho)
