import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from api_utils import *
from unidecode import unidecode
import pandas as pd
import plotly.graph_objects as go
from utils import *


#carrega configurações de página
st.set_page_config(page_title='Dashboard Quebra de Linha')

#Controle de state session
if 'jogo' in st.session_state:
    jogo_id_set = st.session_state['jogo']
    set_selected_option(jogo_id_set)

id_jogo= get_selected_option()[0]
st.session_state['jogo']=id_jogo

#Carregando imagens
img_logo = get_image_base64('./static/Delta_Goal_Branco-removebg-preview.png')

#Carregando cores
base_colors_dict = carregar_cores('./static/constants.yaml')

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

        
        .st-emotion-cache-ue6h4q{{ 
        font-size: 14px;
        color: rgb(49, 51, 63);
        display: flex;
        visibility: visible;
        margin-bottom: 0;
        height: auto;
        min-height: 0.67rem;
        vertical-align: middle;
        flex-direction: row;
        -webkit-box-align: center;
        align-items: center;
        }}

        
    </style>
    """


st.markdown(css,unsafe_allow_html=True)


    
st.markdown(f'<div style=" font-weight: bold ;height: 50px;width: 100%;display: flex;align-items: flex-end;justify-content: center ;font-size:35px; border-radius:10px">'
            f'Quebras de Linha de Defesa'
            f'</div>'
            , unsafe_allow_html=True)
st.divider()

# Pega os nomes dos times do jogo analisado
achou, nomes_id_times = get_nomes_times(id_jogo)
if not(achou): 
    st.error(nomes_id_times)
else:
    nome_time1 = nomes_id_times['nomes_times'][0]
    nome_time2 = nomes_id_times['nomes_times'][1]
    id_time1 = nomes_id_times['id_times'][0]
    id_time2 = nomes_id_times['id_times'][1]



# Usa as funções da api para pegar os dados
achou, data_desfecho_quebra_linha_por_time = get_desfechos_quebra_linha_por_time(id_jogo)
if not(achou): 
    st.error(data_desfecho_quebra_linha_por_time)
achou, data_jogadores_mais_envolvidos = get_jogadores_mais_envolvidos_quebra_linha(id_jogo)
if not(achou): 
    st.error(data_jogadores_mais_envolvidos)
achou, data_desfecho_quebra_linha_zonas = get_zonas_frequentes_quebra_linha(id_jogo)
if not(achou): 
    st.error(data_desfecho_quebra_linha_zonas)
achou, lista_rupturas = exibir_lista_de_rupturas(id_jogo)
if not(achou): 
    st.error(lista_rupturas)
achou, filtros_quebra = get_filtros_quebra(id_jogo)
if not(achou):
    st.error(filtros_quebra)


#titulos
col1_titulo,col2_titulo = st.columns([1,1])

with col1_titulo:
    st.markdown(f'<h1 style="font-size:25px; font-weight:True; color:black"><img src="{lista_rupturas["quebra_linha"][nome_time1][0]}" style="margin-right:10px;width:50px;"></img>{nome_time1}</h1>',unsafe_allow_html=True)

with col2_titulo:
    st.markdown(f'<h1 style="font-size:25px; font-weight:True; color:black; margin-left:50px">{nome_time2}<img src="{lista_rupturas["quebra_linha"][nome_time2][0]}" style="margin-left:10px;width:50px;"></img></h1>',unsafe_allow_html=True)


# Grafico zonas frequentes
image = Image.open('static/campo_quebra.jpeg')

total = data_desfecho_quebra_linha_zonas['rupturas']['Total']
zona1a = (data_desfecho_quebra_linha_zonas['rupturas']['Zona 1 - A'] / total) * 100
zona1b = (data_desfecho_quebra_linha_zonas['rupturas']['Zona 1 - B'] / total) * 100
zona2 = (data_desfecho_quebra_linha_zonas['rupturas']['Zona 2'] / total) * 100
zona3a = (data_desfecho_quebra_linha_zonas['rupturas']['Zona 3 - A'] / total) * 100
zona3b = (data_desfecho_quebra_linha_zonas['rupturas']['Zona 3 - B'] / total) * 100

draw = ImageDraw.Draw(image)
width, height = image.size

x1 = width // 3
x2 = (width // 3) * 2

y1 = height // 4
y2 = height

font_size = 85

font = ImageFont.truetype('static/fonts/Asap-Regular.ttf', 50)

draw.text((x1/3 + 30, y1), f"{zona1a:.1f}%", fill="white", font=font)
draw.text((x1 - 200, y1), f"{zona1b:.1f}%", fill="white", font=font)
draw.text(((x2 - (x1/3) - 40), y1), f"{zona2:.1f}%", fill="white", font=font)
draw.text(((x2 + (x1/7)) - 90, y1), f"{zona3a:.1f}%", fill="white", font=font)
draw.text(((x2 + (x1/2)) - 60, y1), f"{zona3b:.1f}%", fill="white", font=font)


st.image(image, use_column_width=True)


# --------------------------------- GRAFICOS DE CADA TIME---------------------------------------

# Cria as colunas para cada time
col_time1, col_3, col_time2 = st.columns([4,1,4])
# Grafico de desfechos
with col_time1:
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black ">Desfechos {nome_time1}: </h1>',unsafe_allow_html=True)

    labels = data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time1].keys()

    total = 0
    for valor in data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time1].values():
        total += valor

    porcentagens = []
    for valor in data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time1].values():
        porcentagem = valor / total
        porcentagens.append(porcentagem)

    sizes = porcentagens

    
    #pegando as cores
    base_colors =[]

    for label in labels:
        for label_color in base_colors_dict.keys():
            label_color_ = label_color.replace('_cor','')
            label_color_ = label_color_.replace('_',' ')
            if unidecode(label) == label_color_:
                base_colors.append(base_colors_dict[label_color])

    


    
    df_time_1_pie = pd.DataFrame(zip(labels,sizes), columns=['Desfechos', 'Porcentagem'])

    # Exibindo o gráfico
    labels = df_time_1_pie.Desfechos.values
    values = df_time_1_pie.Porcentagem.values

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig.update_traces(hoverinfo='label', marker=dict(colors=base_colors))

    
    fig.update_layout(width=250, legend=dict(orientation="h", y=0, x=0),margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig)

    # Grafico de jogadores mais envolvidos
    names = [item['nome'] for item in data_jogadores_mais_envolvidos['top5'][nome_time1]]
    values = [item['rupturas'] for item in data_jogadores_mais_envolvidos['top5'][nome_time1]]

    
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black ">Top 5 Jogadores {nome_time1}: </h1>',unsafe_allow_html=True)

    

    fig2 = go.Figure(data=[go.Bar(x=names, y=values)])
    # Customize aspect
    fig2.update_traces(marker_color=base_colors_dict['Passe_nao_concluido_cor'], width=0.5)
    fig2.update_layout(height=300,margin=dict(l=0, r=0, b=0, t=0))
    
    st.plotly_chart(fig2,use_container_width=True)


#------------------------SEGUNDO TIME------------------------


# Grafico de desfechos
with col_time2:
    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black ">Desfechos {nome_time2}: </h1>',unsafe_allow_html=True)
    labels = data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time2].keys()

    total = 0
    for valor in data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time2].values():
        total += valor

    porcentagens = []
    for valor in data_desfecho_quebra_linha_por_time['desfechos_por_time'][nome_time2].values():
        porcentagem = valor / total
        porcentagens.append(porcentagem)

    sizes = porcentagens
    #pegando as cores
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

    # Grafico de jogadores mais envolvidos
    names = [item['nome'] for item in data_jogadores_mais_envolvidos['top5'][nome_time2]]
    values = [item['rupturas'] for item in data_jogadores_mais_envolvidos['top5'][nome_time2]]

    st.markdown(f'<h1 style="font-size:16px; font-weight:True; color:black ">Top 5 Jogadores {nome_time2}: </h1>',unsafe_allow_html=True)

    

    fig4 = go.Figure(data=[go.Bar(x=names, y=values)])
    # Customize aspect
    fig4.update_traces(marker_color=base_colors_dict['Passe_nao_concluido_cor'], width=0.5)
    fig4.update_layout(height=300,margin=dict(l=0, r=0, b=0, t=0), yaxis = dict(tickmode = 'linear',tick0 = 0,dtick = 1))
    st.plotly_chart(fig4,use_container_width=True)



# ------------------------LISTA DE RUPTURAS------------------------

st.write("#### Rupturas do Jogo:")


#Filtros
col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)

times_filtro = ['Todos',nome_time1,nome_time2]
times_filtro = tuple(times_filtro)
filtro_time = col_filtro1.selectbox('Time:', times_filtro, key='time')

jogadores_filtro = ['Todos']
for jogador in filtros_quebra['jogadores']:
    jogadores_filtro.append(jogador)
jogadores_filtro = tuple(jogadores_filtro)
filtro_jogador = col_filtro2.selectbox('Jogador:', jogadores_filtro, key='jogador')

zona_filtro = ['Todos']
for zona in filtros_quebra['zonas']:
    zona_filtro.append(zona)
zona_filtro = tuple(zona_filtro)
filtro_zona = col_filtro3.selectbox('Zona:', zona_filtro, key='zona')

desfecho_filtro = ['Todos']
for desfecho in filtros_quebra['desfechos']:
    desfecho_filtro.append(desfecho)
desfecho_filtro = tuple(desfecho_filtro)
filtro_desfecho = col_filtro4.selectbox('Desfecho:', desfecho_filtro, key='desfecho')

filtro_aplicado = False
if filtro_time != 'Todos':
    if filtro_time == nome_time1:
        lista_rupturas['quebra_linha'][nome_time2][1] = []
    else:
        lista_rupturas['quebra_linha'][nome_time1][1] = []
if filtro_jogador != 'Todos':
    for time in lista_rupturas['quebra_linha']:
        rupturas = []
        for ruptura in lista_rupturas['quebra_linha'][time][1]:
            if ruptura['nome_jogador_ruptura'] == filtro_jogador:
                rupturas.append(ruptura)
        lista_rupturas['quebra_linha'][time][1] = rupturas
if filtro_zona != 'Todos':
    for time in lista_rupturas['quebra_linha']:
        rupturas = []
        for ruptura in lista_rupturas['quebra_linha'][time][1]:
            if ruptura['zona_defesa'] == filtro_zona:
                rupturas.append(ruptura)
        lista_rupturas['quebra_linha'][time][1] = rupturas
if filtro_desfecho != 'Todos':
    for time in lista_rupturas['quebra_linha']:
        rupturas = []
        for ruptura in lista_rupturas['quebra_linha'][time][1]:
            if ruptura['desfecho'] == filtro_desfecho:
                rupturas.append(ruptura)
        lista_rupturas['quebra_linha'][time][1] = rupturas

if lista_rupturas['quebra_linha'][nome_time1][1] == [] and lista_rupturas['quebra_linha'][nome_time2][1] == []:
    st.error('Não foram encontradas rupturas com os filtros selecionados')


for time_ in lista_rupturas['quebra_linha']:
    if time_ == nome_time1:
        outro_time = nome_time2
        id_time = id_time1
    else: 
        id_time = id_time2
        outro_time = nome_time1
    #chamada fantasma para carregar o video
    exibir_video_ruptura(jogo_id= id_jogo, quebra_id=0, time_id =id_time)
    #Cria listas de rupturas
    for i in range(len(lista_rupturas['quebra_linha'][time_][1])):
        if time_ == nome_time2:
            num = i + len(lista_rupturas['quebra_linha'][nome_time1][1])
        else: 
            num = i
        with st.container():
            exp,desfecho,zona = st.columns([8,2.5,1])
            #Faz um expander para cada ruptura
            with exp: 
                with st.expander(f"Quebra de Linha {num + 1} - {lista_rupturas['quebra_linha'][time_][1][i]['inicio_ruptura']} "):
                    st.write("#### Video da Ruptura:")

                    #Botão para exibir o video
                    ver_video = st.button('Ver Video',key=f'{id_jogo} {num + 1} {id_time}')
                    if ver_video:
                        achou,link_video = exibir_video_ruptura(jogo_id= id_jogo, quebra_id=i, time_id =id_time)
                        if not(achou):
                            st.error(link_video)
                        st.video(link_video)
                    
                    #Divide o expander em duas partes
                    col_dados_rup_1,col_dados_rup_2= st.columns([1,1])
                    with col_dados_rup_1:

                        st.markdown(f'<h6 style="font-size:20px; padding-bottom:0px">Posse de bola</h6>',unsafe_allow_html=True)
                        st.markdown(
                                        f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:10px">'
                                        f'<img src="{lista_rupturas["quebra_linha"][time_][0]}" style="margin-right:5px;width:20px;"></img>'
                                        f"{lista_rupturas['quebra_linha'][time_][1][i]['nome_jogador_posse_bola']} {lista_rupturas['quebra_linha'][time_][1][i]['numero_jogador_posse_bola']}"
                                        '</div>',
                                        unsafe_allow_html=True,
                                    )
                        st.markdown(f'<h6 style="font-size:20px; padding-bottom:0px">Jogador em ruptura</h6>',unsafe_allow_html=True)
                        st.write(f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:10px">'
                                f'<img src="{lista_rupturas["quebra_linha"][time_][0]}" style="margin-right:5px;width:20px;"></img>'
                            f"{lista_rupturas['quebra_linha'][time_][1][i]['nome_jogador_ruptura']}   {lista_rupturas['quebra_linha'][time_][1][i]['numero_jogador_ruptura']}"
                            '</div>',
                                        unsafe_allow_html=True,
                                )

                    jogadores_adv = ''
                    for i_ in range(len(lista_rupturas['quebra_linha'][time_][1][i]["nomes_jogadores_defesa"])):
                            jogadores_adv += f'<div style=" display: flex; align-items:center; justify-content:left; margin-left:10px">'
                            jogadores_adv += f'<img src="{lista_rupturas["quebra_linha"][outro_time][0]}" style="margin-right:5px;width:20px;"></img>'
                            jogadores_adv += f"{lista_rupturas['quebra_linha'][time_][1][i]['nomes_jogadores_defesa'][i_]} {lista_rupturas['quebra_linha'][time_][1][i]['numeros_jogadores_defesa'][i_]}"
                            jogadores_adv += '</div> <br>'

                    with col_dados_rup_2:
                        st.markdown(f'<h6 style="font-size:20px; padding-bottom:0px">Jogadores na linha defensiva</h6>',unsafe_allow_html=True)
                        st.markdown(
                                        f'{jogadores_adv}',
                                        unsafe_allow_html=True,
                                    )
                        
                with desfecho:
                    for label_color in base_colors_dict.keys():
                                label_color_ = label_color.replace('_cor','')
                                label_color_ = label_color_.replace('_',' ')
                                if unidecode(lista_rupturas["quebra_linha"][time_][1][i]["desfecho"]) == label_color_:
                                    cor_desfecho =base_colors_dict[label_color]

                    st.write(f'<div style="background-color:{cor_desfecho}; padding: 10px 0px; margin:3px 0px; border-radius: 20px; display: flex; align-items: center; justify-content:center; font-size:small; color:white; padding-left: 7px; padding-right:2px">'
                        f"{lista_rupturas['quebra_linha'][time_][1][i]['desfecho']}"
                        '</div>',
                                    unsafe_allow_html=True,
                                )
                with zona:
                    st.markdown(
                        f'<div style="background-color:#DFE0E9; padding: 12px 0px; border-radius: 20px;margin:3px 0px;  display: flex; align-items: center; justify-content: center; font-size:10px">'
                        f'{lista_rupturas["quebra_linha"][time_][1][i]["zona_defesa"]}'
                        '</div>',
                        unsafe_allow_html=True,
                    )

