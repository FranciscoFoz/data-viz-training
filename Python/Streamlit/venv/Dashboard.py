import streamlit as st 
import requests
import pandas as pd
import plotly.express as px


# FUNÇÕES
def formata_numero(valor, prefixo = ''):
    for unidade in ['','mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'




st.title('DASHBOARD DE VENDAS :shopping_trolley:')


# IMPORTAÇÃO DOS DADOS
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# TABELAS
receita_estados = dados.groupby('Local da compra')[['Preço']].sum().reset_index()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra','lat','lon']].merge(receita_estados, left_on='Local da compra', right_on='Local da compra').sort_values('Preço', ascending=False)

#GRÁFICOS

fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat':False,'lon':False},
                                  title = 'Receita por estado')


# CARDS
coluna1, coluna2 = st.columns(2)
with coluna1:  
    st.metric('Receita',formata_numero(dados['Preço'].sum(),'R$'))
    st.plotly_chart(fig_mapa_receita)
with coluna2:
    st.metric('Quantidade de vendas',formata_numero(dados.shape[0]))



st.dataframe(dados)


