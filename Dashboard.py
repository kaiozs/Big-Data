import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.subplots as sp
from plotly.subplots import make_subplots
import numpy as np

#INTERNET
#INTERNET_ADM
#INTERNET_ENSINO
#COMPUTADORES

#---------------------------------------------------------------------------------------------------------
#KAIO
#---------------------------------------------------------------------------------------------------------


# Função para estabelecer a conexão com o banco de dados
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='senha123',
        database='projetopython_db'
    )

# Função para buscar dados do banco de dados
def fetch_data(query):
    connection = get_connection()
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            df = pd.read_sql(query, connection)
            cursor.close()
            return df
    finally:
        connection.close()

# Buscar dados da tabela especificada
table_nacional = "SELECT * FROM projetopython_db.equip_censu_nacional"
df_nacional = fetch_data(table_nacional)
table_nordeste = "SELECT * FROM projetopython_db.equip_censu_nordeste"
df_nordeste = fetch_data(table_nordeste)
table_norte = "SELECT * FROM projetopython_db.equip_censu_norte"
df_norte = fetch_data(table_norte)
table_sudeste = "SELECT * FROM projetopython_db.equip_censu_sudeste"
df_sudeste = fetch_data(table_sudeste)

# INICIO 


# SELECIONAR O TIPO DE ANALISE A SER FEITA
option = st.sidebar.radio(
    "Escolha uma opção:",
    ('ANÁLISE GERAL', 'ANÁLISE PE / PB / RN', 'ANÁLISE SUDESTE X NORDESTE'))


# ANÁLISE GERAL
if option == 'ANÁLISE GERAL':
    st.subheader('ANÁLISE GERAL')

    # INICIO
    ano = st.selectbox("Selecione o Ano", df_nacional['ANO'].unique())

    # FILTRAR O PRIMEIRO GRAFICO DE ACORDO COM O ANO
    df_primeiro_grafico = df_nacional[df_nacional['ANO'] == ano]

    st.write("Regiões")
    st.header("Equipamentos de tecnologia escolar")

    # Agrupar os dados por 'ANO' e 'TIPO_INSTITUICAO'
    df_grouped = df_primeiro_grafico.groupby(['ANO', 'TIPO_INSTITUICAO']).sum().reset_index()

    # Plotar gráfico de barras comparativo usando Plotly
    fig = px.bar(df_grouped, x='TIPO_INSTITUICAO', y=['DESKTOP_ALUNOS', 'TABLET_ALUNOS', 'INTERNET', 'WIFI', 'INTERNET_ADM', 'INTERNET_ENSINO'],
                labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                title=f'Comparativo de Equipamentos de Tecnologia por Tipo de Instituição para o Ano {ano}')
    st.plotly_chart(fig)

    # FILTRAR O PRIMEIRO GRAFICO DE ACORDO COM O ANO
    df_primeiro_grafico = df_nacional[df_nacional['ANO'] == ano]

    st.write("Regiões")
    st.header("Equipamentos de tecnologia escolar")

    # Agrupar os dados por 'ANO' e 'TIPO_INSTITUICAO'
    df_grouped = df_primeiro_grafico.groupby(['ANO', 'TIPO_INSTITUICAO']).sum().reset_index()

    # Plotar gráfico de linha comparativo usando Plotly
    fig = px.line(df_grouped, x='TIPO_INSTITUICAO', y=['DESKTOP_ALUNOS', 'TABLET_ALUNOS', 'INTERNET', 'WIFI', 'INTERNET_ADM', 'INTERNET_ENSINO', 'QUANT_INSTITUICAO'],
                labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                title=f'Comparativo de Equipamentos de Tecnologia por Tipo de Instituição para o Ano {ano}')
    st.plotly_chart(fig)

    # FILTRAR O PRIMEIRO GRAFICO DE ACORDO COM O ANO
    df_primeiro_grafico = df_nacional[df_nacional['ANO'] == ano]

    st.write("Regiões")
    st.header("Equipamentos de tecnologia escolar")

    # Agrupar os dados por 'ANO' e 'TIPO_INSTITUICAO'
    df_grouped = df_primeiro_grafico.groupby(['ANO', 'TIPO_INSTITUICAO']).sum().reset_index()

    # Criar a figura com subplots
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=('Gráfico de Barras', 'Gráfico de Linhas'))

    # Adicionar o primeiro subplot (gráfico de barras)
    fig.add_trace(go.Bar(x=df_grouped['TIPO_INSTITUICAO'],
                        y=df_grouped['DESKTOP_ALUNOS'],
                        name='Desktop Alunos'), 
                row=1, col=1)

    fig.add_trace(go.Bar(x=df_grouped['TIPO_INSTITUICAO'],
                        y=df_grouped['TABLET_ALUNOS'],
                        name='Tablet Alunos'), 
                row=1, col=1)

    fig.add_trace(go.Bar(x=df_grouped['TIPO_INSTITUICAO'],
                        y=df_grouped['INTERNET'],
                        name='Internet'), 
                row=1, col=1)

    fig.add_trace(go.Bar(x=df_grouped['TIPO_INSTITUICAO'],
                        y=df_grouped['WIFI'],
                        name='Wifi'), 
                row=1, col=1)

    # Adicionar o segundo subplot (gráfico de linha)
    fig.add_trace(go.Scatter(x=df_grouped['TIPO_INSTITUICAO'],
                            y=df_grouped['INTERNET_ADM'],
                            mode='lines+markers',
                            name='Internet Administração'), 
                row=1, col=2)

    fig.add_trace(go.Scatter(x=df_grouped['TIPO_INSTITUICAO'],
                            y=df_grouped['INTERNET_ENSINO'],
                            mode='lines+markers',
                            name='Internet Ensino'), 
                row=1, col=2)

    fig.update_layout(title=f'Comparativo de Equipamentos de Tecnologia por Tipo de Instituição para o Ano {ano}',
                    xaxis=dict(title='Tipo de Instituição'),
                    yaxis=dict(title='Quantidade'))

    st.plotly_chart(fig)


elif option == 'ANÁLISE PE / PB / RN':
    st.subheader('ANÁLISE PE / PB / RN')
    
    # INICIO
    ano = st.selectbox("Selecione o Ano", df_nacional['ANO'].unique())

    # Buscar dados da tabela especificada
    query = "SELECT * FROM projetopython_db.equip_censu_nordeste WHERE ESTADO IN ('Pernambuco', 'Paraíba', 'Rio Grande do Norte')"
    df_nordeste = fetch_data(query)

    # Filtrar os dados de acordo com o ano selecionado
    df_filtrado = df_nordeste[df_nordeste['ANO'] == ano]

    st.write("Estados")
    st.header("Equipamentos de tecnologia escolar")

    # Agrupar os dados por 'ESTADO' e 'ANO'
    df_grouped = df_filtrado.groupby(['ESTADO']).sum().reset_index()

    # Gráfico de Barras
    fig_barras = px.bar(df_grouped, x='ESTADO', y=['DESKTOP_ALUNOS', 'TABLET_ALUNOS', 'WIFI'],
                        labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                        title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}')
    st.plotly_chart(fig_barras)

    # Gráfico de Linhas
    fig_linhas = px.line(df_grouped, x='ESTADO', y=['DESKTOP_ALUNOS', 'TABLET_ALUNOS', 'WIFI'],
                        labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                        title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}')
    st.plotly_chart(fig_linhas)

    # Criar a figura com subplots
    fig_subplots = sp.make_subplots(rows=1, cols=2, subplot_titles=('Gráfico de Barras', 'Gráfico de Linhas'))

    # Adicionar o primeiro subplot (gráfico de barras)
    fig_subplots.add_trace(go.Bar(x=df_grouped['ESTADO'], y=df_grouped['DESKTOP_ALUNOS'], name='Desktop Alunos'), row=1, col=1)
    fig_subplots.add_trace(go.Bar(x=df_grouped['ESTADO'], y=df_grouped['TABLET_ALUNOS'], name='Tablet Alunos'), row=1, col=1)
    fig_subplots.add_trace(go.Bar(x=df_grouped['ESTADO'], y=df_grouped['WIFI'], name='Wifi'), row=1, col=1)

    # Adicionar o segundo subplot (gráfico de linhas)
    fig_subplots.add_trace(go.Scatter(x=df_grouped['ESTADO'], y=df_grouped['DESKTOP_ALUNOS'], mode='lines+markers', name='Desktop Alunos'), row=1, col=2)
    fig_subplots.add_trace(go.Scatter(x=df_grouped['ESTADO'], y=df_grouped['TABLET_ALUNOS'], mode='lines+markers', name='Tablet Alunos'), row=1, col=2)
    fig_subplots.add_trace(go.Scatter(x=df_grouped['ESTADO'], y=df_grouped['WIFI'], mode='lines+markers', name='Wifi'), row=1, col=2)

    fig_subplots.update_layout(title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}',
                            xaxis=dict(title='Estado'),
                            yaxis=dict(title='Quantidade'))

    st.plotly_chart(fig_subplots)

    # ANALISE DE INTERNET

    # Buscar dados da tabela especificada
    query = "SELECT * FROM projetopython_db.equip_censu_nordeste WHERE ESTADO IN ('Pernambuco', 'Paraíba', 'Rio Grande do Norte')"
    df_nordeste = fetch_data(query)

    # Filtrar os dados de acordo com o ano selecionado
    df_filtrado = df_nordeste[df_nordeste['ANO'] == ano]

    st.write("Estados")
    st.header("Equipamentos de tecnologia escolar")

    # Agrupar os dados por 'ESTADO' e 'ANO'
    df_grouped = df_filtrado.groupby(['ESTADO']).sum().reset_index()

    # Selecionar apenas as colunas de interesse ('INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO')
    df_grouped = df_grouped[['ESTADO', 'INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']]

    # Gráfico de Barras
    fig_barras = px.bar(df_grouped, x='ESTADO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'],
                        labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                        title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}')
    st.plotly_chart(fig_barras)

    # Gráfico de Linhas
    fig_linhas = px.line(df_grouped, x='ESTADO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'],
                        labels={'value': 'Quantidade', 'variable': 'Equipamentos'},
                        title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}')
    st.plotly_chart(fig_linhas)

    # Criar a figura com subplots
    fig_subplots = make_subplots(rows=1, cols=2, subplot_titles=('Gráfico de Barras', 'Gráfico de Linhas'))

    # Adicionar o primeiro subplot (gráfico de barras)
    for col in ['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']:
        fig_subplots.add_trace(go.Bar(x=df_grouped['ESTADO'], y=df_grouped[col], name=col), row=1, col=1)

    # Adicionar o segundo subplot (gráfico de linhas)
    for col in ['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']:
        fig_subplots.add_trace(go.Scatter(x=df_grouped['ESTADO'], y=df_grouped[col], mode='lines+markers', name=col), row=1, col=2)

    fig_subplots.update_layout(title=f'Quantidade de Equipamentos de Tecnologia por Estado para o Ano {ano}',
                            xaxis=dict(title='Estado'),
                            yaxis=dict(title='Quantidade'))

    st.plotly_chart(fig_subplots)


elif option == 'ANÁLISE SUDESTE X NORDESTE':
    st.subheader('ANÁLISE SUDESTE X NORDESTE')
    
    ano = st.selectbox("Selecione o Ano", df_nordeste['ANO'].unique())

    # Filtrar dados de acordo com o ano selecionado
    df_nordeste_ano = df_nordeste[df_nordeste['ANO'] == ano]
    df_sudeste_ano = df_sudeste[df_sudeste['ANO'] == ano]

    #Agrupar os dados por 'TIPO_INSTITUICAO' e somar as colunas de interesse
    df_nordeste_grouped = df_nordeste_ano.groupby('TIPO_INSTITUICAO')[['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']].sum().reset_index()
    df_sudeste_grouped = df_sudeste_ano.groupby('TIPO_INSTITUICAO')[['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']].sum().reset_index()

    # Adicionar coluna para identificar a região
    df_nordeste_grouped['REGIAO'] = 'Nordeste'
    df_sudeste_grouped['REGIAO'] = 'Sudeste'

    # Concatenar os dados das duas regiões
    df_comparacao = pd.concat([df_nordeste_grouped, df_sudeste_grouped])

    # Plotar gráfico de barras comparativo usando Plotly
    fig = px.bar(df_comparacao, x='TIPO_INSTITUICAO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'], 
                color='REGIAO', barmode='group',
                labels={'value': 'Quantidade', 'variable': 'Tipo de Internet'},
                title=f'Comparativo de Quantidade de Internet por Tipo de Instituição para o Ano {ano}')
    st.plotly_chart(fig)

    # Gráfico de linhas para ver a tendência entre as regiões
    fig = px.line(df_comparacao, x='TIPO_INSTITUICAO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'], 
                color='REGIAO', markers=True,
                labels={'value': 'Quantidade', 'variable': 'Tipo de Internet'},
                title=f'Tendência de Quantidade de Internet por Tipo de Instituição para o Ano {ano}')
    st.plotly_chart(fig)

    # Filtrar dados de acordo com o ano selecionado
    df_nordeste_ano = df_nordeste[df_nordeste['ANO'] == ano]
    df_sudeste_ano = df_sudeste[df_sudeste['ANO'] == ano]

    # Agrupar os dados por 'TIPO_INSTITUICAO' e somar as colunas de interesse
    df_nordeste_grouped = df_nordeste_ano.groupby('TIPO_INSTITUICAO')[['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']].sum().reset_index()
    df_sudeste_grouped = df_sudeste_ano.groupby('TIPO_INSTITUICAO')[['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO']].sum().reset_index()

    # Plotar gráficos separados para cada região
    st.subheader('NORDESTE')
    fig_nordeste = px.bar(df_nordeste_grouped, x='TIPO_INSTITUICAO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'], 
                        barmode='group',
                        labels={'value': 'Quantidade', 'variable': 'Tipo de Internet'},
                        title=f'Quantidade de Internet por Tipo de Instituição no Nordeste para o Ano {ano}')
    st.plotly_chart(fig_nordeste)

    st.subheader('SUDESTE')
    fig_sudeste = px.bar(df_sudeste_grouped, x='TIPO_INSTITUICAO', y=['INTERNET', 'INTERNET_ADM', 'INTERNET_ENSINO'], 
                        barmode='group',
                        labels={'value': 'Quantidade', 'variable': 'Tipo de Internet'},
                        title=f'Quantidade de Internet por Tipo de Instituição no Sudeste para o Ano {ano}')
    st.plotly_chart(fig_sudeste)