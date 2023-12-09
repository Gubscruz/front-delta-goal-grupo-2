import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from api_utils import *
from unidecode import unidecode
from utils import *
import plotly.graph_objects as go
import pandas as pd

#Configura a página
st.set_page_config(page_title='Dashboard Cruzamentos')

#Controla o state session
if 'jogo' in st.session_state:
    jogo_id_set = st.session_state['jogo']
    set_selected_option(jogo_id_set)

id_jogo = get_selected_option()[0]
st.session_state['jogo']=id_jogo

#carregue a imagem de logo
img_logo = get_image_base64('./static/Delta_Goal_Branco-removebg-preview.png')

#Carrega as cores
base_colors_dict= carregar_cores('./static/constants.yaml')

# Define o estilo da barra lateral
css = f"""
    <style>
        [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .st-emotion-cache-pkbazv {{
            color: rgba(255, 255, 255, 1);
        }}

        .st-emotion-cache-pkbazv:hover {{
            color: rgba(255, 255, 255, 1);
        }}

        .st-emotion-cache-17lntkn {{
            color: rgba(255, 255, 255, 0.6);
        }}

        .st-emotion-cache-17lntkn:hover {{
            color: rgba(255, 255, 255, 1);
        }}

        .st-emotion-cache-1oe5cao{{
            margin-top: 100px;
        }}
        .st-emotion-cache-lrlib::before {{
            content: url('data:image/png;base64,{img_logo}');
            margin-top: 0;
            margin-left: 2.2rem;
            width: 100px;  /* Defina a largura desejada */
            height: 100px; /* Defina a altura desejada */
            background-size: contain; /* Ajusta o tamanho da ima
            }}

        @font-face {{
            font-family: 'Hagrid';
            src: ('static\fonts\Hagrid-Italic-trial.ttf') ;* Substitua pelo caminho real da fonte */
            font-weight: normal;
            font-style: normal;
        }}

        body {{
            font-family: 'Hagrid', sans-serif;  /* Use a fonte personalizada no corpo do documento */
        }} 
    </style> 
    """
st.markdown(css,unsafe_allow_html=True)


st.markdown(f'<div style=" font-weight: bold ;height: 50px;width: 100%;display: flex;align-items: flex-end;justify-content: center ;font-size:35px; border-radius:10px">'
            f'Cruzamentos'
            f'</div>'
            , unsafe_allow_html=True)

st.divider()

# Pega os nomes dos times do jogo analisado
achou, nomes_1s = get_nomes_times(id_jogo)
if not(achou): 
    st.error(nomes_1s)
else:
    nome_time1 = nomes_1s['nomes_times'][0]
    nome_time2 = nomes_1s['nomes_times'][1]
    id_time1 = nomes_1s['id_times'][0]
    id_time2 = nomes_1s['id_times'][1]

# Usa as funções da api para pegar os dados
achou, data_desfecho_cruzamento = get_cruzamento_desfechos_time(id_jogo)
if not achou:
    st.error(data_desfecho_cruzamento)
achou, lista_cruzamentos_por_jogador = get_cruzamentos_por_jogador(id_jogo)
if not(achou): 
    st.error(lista_cruzamentos_por_jogador)
achou, lista_cruzamentos = exibir_lista_de_cruzamentos(id_jogo)
if not(achou): 
    st.error(exibir_lista_de_cruzamentos)
achou, data_top_5_jogadores = get_top_5_jogadores(id_jogo)
if not(achou): 
    st.error(data_top_5_jogadores)
achou, filtros_cruzamentos = get_filtros_cruzamentos(id_jogo)
if not(achou):
    st.error(filtros_cruzamentos)




#titulos
col1_titulo,col2_titulo = st.columns([1,1])

with col1_titulo:
    st.markdown(f'<h1 style="font-size:25px; font-weight:True; color:black"><img src="{lista_cruzamentos["cruzamentos"][nome_time1][0]}" style="margin-right:10px;width:50px; margin-bottom:5px"></img>{nome_time1}</h1>',unsafe_allow_html=True)

with col2_titulo:
    st.markdown(f'<h1 style="font-size:25px; font-weight:True; color:black; margin-left:50px">{nome_time2}<img src="{lista_cruzamentos["cruzamentos"][nome_time2][0]}" style="margin-left:10px;width:50px;"></img></h1>',unsafe_allow_html=True)

# ---------------------------------GRAFICO DE ZONAS FREQUENTES---------------------------------

# Grafico zonas frequentes
achou,frequencia_zonas_por_time = get_frequencia_zonas_cruzamentos(id_jogo)
if not(achou):
    st.error(frequencia_zonas_por_time)

zonas_time1 = {
            'D2.2' : (137, 120),
            'D2.1' : (273, 120),
            'D1.2' : (413, 120),
            'D3' : (210, 290),
            'D1.1' : (413, 360),
            'E3' : (210, 730),
            'E1.1' : (413, 660),
            'E2.2' : (137, 900),
            'E2.1' : (273, 900),
            'E1.2' : (413, 900),
        }

zonas_time2 = {
            'D2.2' : (1695, 900),
            'D2.1' : (1560, 900),
            'D1.2' : (1423, 900),
            'D3' : (1630, 730),
            'D1.1' : (1420, 660),
            'E3' : (1630, 290),
            'E1.1' : (1420, 360),
            'E2.2' : (1705, 120),
            'E2.1' : (1567, 120),
            'E1.2' : (1430, 120),
        }

template_quadro = Image.open('./static/quadro_cruzamentos.png')
quadro_cruzamentos = template_quadro.resize((1920, 1080))
draw = ImageDraw.Draw(quadro_cruzamentos)
font = ImageFont.truetype('static/fonts/Asap-Regular.ttf', 50)

contador = 1
for time in frequencia_zonas_por_time['frequencia_zona']:
    if contador == 1:
        for zona in frequencia_zonas_por_time['frequencia_zona'][time]:
            draw.text(zonas_time1[zona], frequencia_zonas_por_time['frequencia_zona'][time][zona], (255, 255, 255), font=font)
    else:
        for zona in frequencia_zonas_por_time['frequencia_zona'][time]:
            draw.text(zonas_time2[zona], frequencia_zonas_por_time['frequencia_zona'][time][zona], (255, 255, 255), font=font)
    contador += 1
        
st.image(quadro_cruzamentos)

# ---------------------------------GRAFICOS DE CADA TIME---------------------------------

col_time1, col_3, col_time2 = st.columns([4,1,4])

# Lista top 5 jogadores 
with col_time1:
    top5 = ''
    st.write(f'**Top 5 jogadores {nome_time1}:**')
    for jogador in data_top_5_jogadores['top5'][nome_time1]:
        top5 += (
            f'<div style="display: flex; align-items: center; margin-left: 10px;">'
            f'    <img src="{lista_cruzamentos["cruzamentos"][nome_time1][0]}" style="margin-right: 10px;width:20px;"></img>'
            f'    <div style="flex-grow: 1;">{jogador["numero"]} - {jogador["nome"]}</div>'
            f'    <div style="margin-left: auto;">{jogador["cruzamentos"]} cruzamentos</div>'
            f'</div>'
            f'<br>'
        )

    st.markdown(
        f'{top5}',
        unsafe_allow_html=True,
    )
            

with col_time2:
    top5 = ''
    st.write(f'**Top 5 jogadores {nome_time2}:**')
    for jogador in data_top_5_jogadores['top5'][nome_time2]:
        top5 += (
            f'<div style="display: flex; align-items: center; margin-left: 10px;">'
            f'    <img src="{lista_cruzamentos["cruzamentos"][nome_time2][0]}" style="margin-right: 10px;width:20px;"></img>'
            f'    <div style="flex-grow: 1;">{jogador["numero"]} - {jogador["nome"]}</div>'
            f'    <div style="margin-left: auto;">{jogador["cruzamentos"]} cruzamentos</div>'
            f'</div>'
            f'<br>'
        )

    st.markdown(
        f'{top5}',
        unsafe_allow_html=True,
    )

# Grafico desfechos
with col_time1:

    # Grafico de jogadores mais envolvidos time 1
    names = [item for item in lista_cruzamentos_por_jogador['cruzamentos_jogador'][nome_time1].keys()]
    values = [item for item in lista_cruzamentos_por_jogador['cruzamentos_jogador'][nome_time1].values()]
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black">Cruzamentos por jogador {nome_time1}: </h1>',unsafe_allow_html=True)


    fig2 = go.Figure(data=[go.Bar(x=values, y=names, orientation='h')])
    fig2.update_traces(marker_color=base_colors_dict['Passe_nao_concluido_cor'])
    fig2.update_layout(height=300,margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig2,use_container_width=True)

    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black">Desfechos {nome_time1}: </h1>',unsafe_allow_html=True)

    labels = data_desfecho_cruzamento['desfechos_por_time'][nome_time1].keys()

    total = 0
    for valor in data_desfecho_cruzamento['desfechos_por_time'][nome_time1].values():
        total += valor

    porcentagens = []
    for valor in data_desfecho_cruzamento['desfechos_por_time'][nome_time1].values():
        porcentagem = valor / total
        porcentagens.append(porcentagem)

    sizes = porcentagens
    base_colors =[]

    for label in labels:
        for label_color in base_colors_dict.keys():
            label_color_ = label_color.replace('_cor','')
            label_color_ = label_color_.replace('_',' ')
            if unidecode(label) == label_color_:
                base_colors.append(base_colors_dict[label_color])


    df_time_1_pie = pd.DataFrame(zip(labels,sizes), columns=['Desfechos', 'Porcentagem'])

    
    labels = df_time_1_pie.Desfechos.values
    values = df_time_1_pie.Porcentagem.values

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig.update_traces(hoverinfo='label', marker=dict(colors=base_colors))

    
    fig.update_layout(width=250, legend=dict(orientation="h", y=0, x=0),margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig)

with col_time2:
    # Grafico de jogadores mais envolvidos time 2

    names = [item for item in lista_cruzamentos_por_jogador['cruzamentos_jogador'][nome_time2].keys()]
    values = [item for item in lista_cruzamentos_por_jogador['cruzamentos_jogador'][nome_time2].values()]
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black">Cruzamentos por jogador {nome_time1}: </h1>',unsafe_allow_html=True)


    fig4 = go.Figure(data=[go.Bar(x=values, y=names, orientation='h')])
    fig4.update_traces(marker_color=base_colors_dict['Passe_nao_concluido_cor'])
    fig4.update_layout(height=300,margin=dict(l=0, r=0, b=0, t=0), yaxis = dict(tickmode = 'linear',tick0 = 0,dtick = 1))
    st.plotly_chart(fig4,use_container_width=True)
    
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black">Desfechos {nome_time2}: </h1>',unsafe_allow_html=True)
    labels = data_desfecho_cruzamento['desfechos_por_time'][nome_time2].keys()

    total = 0
    for valor in data_desfecho_cruzamento['desfechos_por_time'][nome_time2].values():
        total += valor

    porcentagens = []
    for valor in data_desfecho_cruzamento['desfechos_por_time'][nome_time2].values():
        porcentagem = valor / total
        porcentagens.append(porcentagem)

    sizes = porcentagens
    base_colors =[]

    for label in labels:
        for label_color in base_colors_dict.keys():
            label_color_ = label_color.replace('_cor','')
            label_color_ = label_color_.replace('_',' ')
            if unidecode(label) == label_color_:
                base_colors.append(base_colors_dict[label_color])

    df_time_2_pie = pd.DataFrame(zip(labels,sizes), columns=['Desfechos', 'Porcentagem'])
    
    labels = df_time_2_pie.Desfechos.values
    values = df_time_2_pie.Porcentagem.values

    fig3 = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig3.update_traces(hoverinfo='label', marker=dict(colors=base_colors))
    fig3.update_layout(width=250, legend=dict(orientation="h", y=0, x=0),margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig3)


st.write("#### Cruzamentos do Jogo:")

#Filtros
col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)

times_filtro = ['Todos',nome_time1,nome_time2]
times_filtro = tuple(times_filtro)
filtro_time = col_filtro1.selectbox('Time:', times_filtro, key='time')

jogadores_filtro = ['Todos']
for jogador in filtros_cruzamentos['jogadores']:
    jogadores_filtro.append(jogador)
jogadores_filtro = tuple(jogadores_filtro)
filtro_jogador = col_filtro2.selectbox('Jogador:', jogadores_filtro, key='jogador')

zona_filtro = ['Todos']
for zona in filtros_cruzamentos['zonas']:
    zona_filtro.append(zona)
zona_filtro = tuple(zona_filtro)
filtro_zona = col_filtro3.selectbox('Zona:', zona_filtro, key='zona')

desfecho_filtro = ['Todos']
for desfecho in filtros_cruzamentos['desfechos']:
    desfecho_filtro.append(desfecho)
desfecho_filtro = tuple(desfecho_filtro)
filtro_desfecho = col_filtro4.selectbox('Desfecho:', desfecho_filtro, key='desfecho')

filtro_aplicado = False
if filtro_time != 'Todos':
    if filtro_time == nome_time1:
        lista_cruzamentos['cruzamentos'][nome_time2][1] = []
    else:
        lista_cruzamentos['cruzamentos'][nome_time1][1] = []
if filtro_jogador != 'Todos':
    for time in lista_cruzamentos['cruzamentos']:
        cruzamentos = []
        for cruzamento in lista_cruzamentos['cruzamentos'][time][1]:
            if filtro_jogador in cruzamento['nome_jogadores_time_cruzando'] or filtro_jogador in cruzamento['nome_jogadores_time_defendendo']:
                cruzamentos.append(cruzamento)
        lista_cruzamentos['cruzamentos'][time][1] = cruzamentos
if filtro_zona != 'Todos':
    for time in lista_cruzamentos['cruzamentos']:
        cruzamentos = []
        for cruzamento in lista_cruzamentos['cruzamentos'][time][1]:
            if cruzamento['zona'] == filtro_zona:
                cruzamentos.append(cruzamento)
        lista_cruzamentos['cruzamentos'][time][1] = cruzamentos
if filtro_desfecho != 'Todos':
    for time in lista_cruzamentos['cruzamentos']:
        cruzamentos = []
        for cruzamento in lista_cruzamentos['cruzamentos'][time][1]:
            if cruzamento['desfecho'] == filtro_desfecho:
                cruzamentos.append(cruzamento)
        lista_cruzamentos['cruzamentos'][time][1] = cruzamentos

if lista_cruzamentos['cruzamentos'][nome_time1][1] == [] and lista_cruzamentos['cruzamentos'][nome_time2][1] == []:
    st.error('Não foram encontradas cruzamentos com os filtros selecionados')




for time_ in lista_cruzamentos['cruzamentos']:
    if time_ == nome_time1:
        outro_time = nome_time2
        id_time = id_time1
    else: 
        id_time = id_time2
        outro_time = nome_time1
    #chamada fantasma para carregar o video
    exibir_video_ruptura(jogo_id= id_jogo, quebra_id=0, time_id =id_time)

    #cria listas de cruzamentos
    for i in range(len(lista_cruzamentos['cruzamentos'][time_][1])):
        if time_ == nome_time2:
            num = i + len(lista_cruzamentos['cruzamentos'][nome_time1][1])
        else: 
            num = i
        
        with st.container():
            exp,desfecho,zona = st.columns([8,2.5,1])
            with exp: 
                #cria expander para exibir vie
                with st.expander(f"Cruzamento {num + 1} - {lista_cruzamentos['cruzamentos'][time_][1][i]['instante_cruzamento']} "):
                    st.write("#### Video da Ruptura:")

                    #Botão para exibir video
                    ver_video = st.button('Ver video',key=f'{id_jogo} {num + 1} {id_time}')
                    if ver_video:
                        achou,link_video = exibir_video_cruzamento(jogo_id=id_jogo,cruzamento_id=i,time_id =id_time)
                        if not(achou):
                            st.error(link_video)
                        st.video(link_video)
                    
                    #cria colunas para exibir dados
                    col_dados_rup_1,col_dados_rup_2= st.columns([1,1])
                    if len(lista_cruzamentos['cruzamentos'][time_][1][i]["nome_jogadores_time_cruzando"]) > 1:
                        jogadores_cruz = ''
                        for i_ in range(len(lista_cruzamentos['cruzamentos'][time_][1][i]["nome_jogadores_time_cruzando"])):
                                jogadores_cruz += f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:20px">'
                                jogadores_cruz += f'<img src="{lista_cruzamentos["cruzamentos"][time_][0]}" style="margin-right:10px;width:20px;"></img>'
                                jogadores_cruz += f"{lista_cruzamentos['cruzamentos'][time_][1][i]['nome_jogadores_time_cruzando'][i_]} {lista_cruzamentos['cruzamentos'][time_][1][i]['numero_jogadores_time_cruzando'][i_]}"
                                jogadores_cruz += '</div> <br>'
                    else:
                        jogadores_cruz = ''
                        jogadores_cruz += f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:20px">'
                        jogadores_cruz += f'<img src="{lista_cruzamentos["cruzamentos"][time_][0]}" style="margin-right:10px;width:20px;"></img>'
                        jogadores_cruz += f"{lista_cruzamentos['cruzamentos'][time_][1][0]['nome_jogadores_time_cruzando'][0]} {lista_cruzamentos['cruzamentos'][time_][1][i]['numero_jogadores_time_cruzando'][0]}"
                        jogadores_cruz += '</div> <br>'
                    with col_dados_rup_1:

                        st.markdown(f'<h6 style="font-size:20px; padding-bottom:0px">Jogadores Cruzando</h6>',unsafe_allow_html=True)
                        st.markdown(
                                        f'{jogadores_cruz}',
                                        unsafe_allow_html=True,
                                    )

                    jogadores_adv = ''
                    for i_ in range(len(lista_cruzamentos['cruzamentos'][time_][1][i]["nome_jogadores_time_defendendo"])):
                            jogadores_adv += f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:20px">'
                            jogadores_adv += f'<img src="{lista_cruzamentos["cruzamentos"][outro_time][0]}" style="margin-right:10px;width:20px;"></img>'
                            jogadores_adv += f"{lista_cruzamentos['cruzamentos'][time_][1][i]['nome_jogadores_time_defendendo'][i_]} {lista_cruzamentos['cruzamentos'][time_][1][i]['numero_jogadores_time_defendendo'][i_ - 1]}"
                            jogadores_adv += '</div> <br>'

                    with col_dados_rup_2:
                        st.markdown(f'<h6 style="font-size:20px; padding-bottom:0px">Jogadores defendendo</h6>',unsafe_allow_html=True)
                        st.markdown(
                                        f'{jogadores_adv}',
                                        unsafe_allow_html=True,
                                    )
                        
                with desfecho:
                    for label_color in base_colors_dict.keys():
                                label_color_ = label_color.replace('_cor','')
                                label_color_ = label_color_.replace('_',' ')
                                if unidecode(lista_cruzamentos["cruzamentos"][time_][1][i]["desfecho"]) == label_color_:
                                    cor_desfecho =base_colors_dict[label_color]

                    st.write(f'<div style="background-color:{cor_desfecho}; padding: 10px 0px; margin:3px 0px; border-radius: 20px; display: flex; align-items: center; justify-content:center; font-size:small; color:white; padding-left: 7px; padding-right:2px">'
                        f"{lista_cruzamentos['cruzamentos'][time_][1][i]['desfecho']}"
                        '</div>',
                                    unsafe_allow_html=True,
                                )
                with zona:
                    st.markdown(
                        f'<div style="background-color:#DFE0E9; padding: 12px 0px; border-radius: 20px;margin:3px 0px;  display: flex; align-items: center; justify-content: center; font-size:10px">'
                        f'{lista_cruzamentos["cruzamentos"][time_][1][i]["zona"]}'
                        '</div>',
                        unsafe_allow_html=True,
                    )



